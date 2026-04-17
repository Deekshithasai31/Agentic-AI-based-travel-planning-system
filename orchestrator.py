"""
Orchestrator — the brain of the agentic system.
Implements a TRUE ReAct loop: THINK → ACT → OBSERVE → REPLAN
Uses OpenAI GPT to reason and decide, Python agents to execute.
"""

import json
import copy
from datetime import datetime
from openai import OpenAI

from agents import route_agent, transport_agent, hotel_agent, budget_agent, places_agent
from validator import validate_final_plan, is_plan_complete


# Valid actions GPT is allowed to choose
VALID_ACTIONS = [
    "call_route_agent",
    "call_transport_agent",
    "call_hotel_agent",
    "call_budget_agent",
    "call_places_agent",
    "finalize_plan",
]

MAX_ITERATIONS = 8

SYSTEM_PROMPT = """
You are an AI Travel Orchestrator for India trips.
You work in a ReAct loop: THINK → ACT → OBSERVE → REPLAN

Your job is ONLY to reason and decide which agent to call next.
Do NOT perform any calculations — all math is done by Python agents.

Available actions:
- call_route_agent       → calculate distance + duration between cities
- call_transport_agent   → get transport options (bus/train/flight) with costs
- call_hotel_agent       → find hotels at destination within budget
- call_budget_agent      → allocate budget across transport/hotel/food/activities
- call_places_agent      → get real tourist places at destination via Foursquare
- finalize_plan          → ONLY when all agents done AND budget fits

Recommended order:
1. call_route_agent first (need distance for everything else)
2. call_budget_agent (get budget allocations)
3. call_transport_agent (compare options vs budget)
4. call_hotel_agent (find stay within remaining budget)
5. call_places_agent (get tourist spots)
6. finalize_plan (only if total cost fits budget)

Decision trade-off rules:
- If travel time > 30% of total trip days → prefer faster transport
- If transport cost > 40% of budget → switch to cheaper mode
- If hotel budget_stretch is true → consider if cheaper transport frees budget
- Always validate total before finalizing

Replan rules:
- If total exceeds budget → do NOT finalize, try different transport or hotel tier
- If hotel stretch → explain why and whether to accept or retry
- Be explicit about WHY you are making each decision

Always respond in this EXACT JSON format (nothing else, no markdown):
{
  "think": "your detailed reasoning here",
  "act": "one of the valid action names",
  "observe": "what you learned from the last agent result",
  "replan": "what you are changing and why, or null if no change"
}
"""


def build_state_message(state, source, destination, budget, days):
    """Build a structured message describing current state for GPT."""
    return f"""
Current trip planning state:
- Source: {source}
- Destination: {destination}
- Total Budget: ₹{budget}
- Days: {days}
- Iteration: {state['iteration']}

Agent results so far:
Route:     {json.dumps(state['route'])     if state['route']     else 'NOT YET CALLED'}
Transport: {json.dumps(state['transport']) if state['transport'] else 'NOT YET CALLED'}
Hotel:     {json.dumps(state['hotel'])     if state['hotel']     else 'NOT YET CALLED'}
Budget:    {json.dumps(state['budget'])    if state['budget']    else 'NOT YET CALLED'}
Places:    {json.dumps(state['places'])    if state['places']    else 'NOT YET CALLED'}

Selected transport: {json.dumps(state['selected_transport']) if state['selected_transport'] else 'NONE'}
Selected hotel:     {json.dumps(state['selected_hotel'])     if state['selected_hotel']     else 'NONE'}
Current total cost: ₹{state['current_total']}

What should you do next? Remember to respond ONLY in the required JSON format.
"""


def parse_gpt_response(content):
    """Safely parse GPT JSON response. Returns dict or None."""
    try:
        clean = content.strip()
        if clean.startswith("```"):
            lines = clean.split("\n")
            clean = "\n".join(lines[1:-1])
        return json.loads(clean)
    except Exception:
        return None


def call_gpt(client, messages, logs, iteration):
    """
    Call OpenAI GPT with full conversation history.
    Handles JSON parsing errors with a repair prompt.
    Returns parsed dict or None.
    """
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            temperature=0.3,
        )
        raw = response.choices[0].message.content
        parsed = parse_gpt_response(raw)

        if parsed is None:
            logs.append({
                "iteration": iteration,
                "step": "OBSERVE",
                "content": "Invalid JSON response from GPT, sending repair prompt",
            })
            repair_msg = {
                "role": "user",
                "content": (
                    f"Your last response was not valid JSON.\n"
                    f"You returned: {raw[:300]}\n"
                    f"Please return ONLY valid JSON in this exact format:\n"
                    '{"think": "...", "act": "...", "observe": "...", "replan": "..."}'
                )
            }
            messages.append({"role": "assistant", "content": raw})
            messages.append(repair_msg)

            retry = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages,
                temperature=0.1,
            )
            raw2 = retry.choices[0].message.content
            parsed = parse_gpt_response(raw2)

            if parsed is None:
                logs.append({
                    "iteration": iteration,
                    "step": "OBSERVE",
                    "content": "Repair failed — skipping this iteration",
                })
                return None, raw2

            return parsed, raw2

        return parsed, raw

    except Exception as e:
        logs.append({
            "iteration": iteration,
            "step": "OBSERVE",
            "content": f"GPT call failed: {str(e)}",
        })
        return None, ""


def compute_current_total(state, days):
    """Compute total cost from current state."""
    t_cost = state["selected_transport"]["cost"] if state["selected_transport"] else 0
    h_cost = (state["selected_hotel"]["price_per_night"] * days
              if state["selected_hotel"] else 0)
    f_cost = state["budget"].get("food_budget", 0) if state["budget"] else 0
    a_cost = state["budget"].get("activities_budget", 0) if state["budget"] else 0
    return t_cost + h_cost + f_cost + a_cost


def run_agent_loop(source, destination, budget, days, openai_api_key, foursquare_api_key):
    """
    Main ReAct loop. Returns (final_plan, logs).
    Now uses foursquare_api_key instead of otm_api_key.
    """
    client = OpenAI(api_key=openai_api_key)

    logs = []
    state = {
        "route":              {},
        "transport":          {},
        "hotel":              {},
        "budget":             {},
        "places":             [],
        "selected_transport": None,
        "selected_hotel":     None,
        "current_total":      0,
        "iteration":          0,
    }

    messages = [{"role": "system", "content": SYSTEM_PROMPT}]

    best_plan  = None
    best_diff  = float("inf")

    logs.append({
        "iteration": 0,
        "step": "THINK",
        "content": (
            f"Starting agentic planning: {source} → {destination} | "
            f"Budget: ₹{budget} | Days: {days}"
        ),
    })

    for i in range(1, MAX_ITERATIONS + 1):
        state["iteration"] = i

        state_msg = build_state_message(state, source, destination, budget, days)
        messages.append({"role": "user", "content": state_msg})

        parsed, raw_response = call_gpt(client, messages, logs, i)

        if parsed is None:
            messages.append({"role": "assistant", "content": raw_response})
            continue

        messages.append({"role": "assistant", "content": raw_response})

        think   = parsed.get("think", "")
        act     = parsed.get("act", "").strip()
        observe = parsed.get("observe", "")
        replan  = parsed.get("replan", None)

        if think:
            logs.append({"iteration": i, "step": "THINK",   "content": think})
        if act:
            logs.append({"iteration": i, "step": "ACT",     "content": f"Decided to: {act}"})
        if observe:
            logs.append({"iteration": i, "step": "OBSERVE", "content": observe})
        if replan:
            logs.append({"iteration": i, "step": "REPLAN",  "content": replan})

        # ── ACTION VALIDATION ──────────────────────────────────────────
        if act not in VALID_ACTIONS:
            logs.append({
                "iteration": i,
                "step": "OBSERVE",
                "content": f"Invalid action received: '{act}' — retrying with correction",
            })
            correction = {
                "role": "user",
                "content": (
                    f"'{act}' is not a valid action. "
                    f"Choose ONLY from: {', '.join(VALID_ACTIONS)}"
                )
            }
            messages.append(correction)
            continue

        # ── FINALIZE CHECK ─────────────────────────────────────────────
        if act == "finalize_plan":
            if not is_plan_complete(state):
                msg = "Cannot finalize — not all agents have been called yet."
                logs.append({"iteration": i, "step": "REPLAN", "content": msg})
                messages.append({"role": "user", "content": msg})
                continue

            total = compute_current_total(state, days)
            state["current_total"] = total

            if total > budget:
                msg = (
                    f"Finalization blocked — total cost ₹{total} exceeds budget ₹{budget}. "
                    f"Over by ₹{total - budget}. You must replan transport or hotel."
                )
                logs.append({"iteration": i, "step": "REPLAN", "content": msg})
                messages.append({"role": "user", "content": msg})
                continue

            logs.append({
                "iteration": i,
                "step": "THINK",
                "content": f"Plan finalized. Total ₹{total} fits within budget ₹{budget}.",
            })
            break

        # ── EXECUTE AGENT ──────────────────────────────────────────────
        if act == "call_route_agent":
            result = route_agent.run(source, destination, logs, i)
            state["route"] = result

        elif act == "call_transport_agent":
            if not state["route"]:
                msg = "Route agent must be called before transport agent."
                logs.append({"iteration": i, "step": "OBSERVE", "content": msg})
                messages.append({"role": "user", "content": msg})
                continue
            result = transport_agent.run(state["route"]["distance_km"], logs, i)
            state["transport"] = result
            state["selected_transport"] = result["cheapest"]

        elif act == "call_budget_agent":
            result = budget_agent.run(budget, days, logs, i)
            state["budget"] = result

        elif act == "call_hotel_agent":
            if not state["budget"]:
                msg = "Budget agent must be called before hotel agent."
                logs.append({"iteration": i, "step": "OBSERVE", "content": msg})
                messages.append({"role": "user", "content": msg})
                continue

            hotel_budget = state["budget"]["hotel_budget"]

            if state["selected_transport"]:
                from agents import budget_agent as ba
                transport_cost = state["selected_transport"]["cost"]
                hotel_per_night = hotel_budget // days if days > 0 else hotel_budget
                updated_budget = ba.reallocate(
                    state["budget"],
                    transport_cost,
                    hotel_per_night,
                    days,
                    budget,
                    logs,
                    i
                )
                state["budget"] = updated_budget
                hotel_budget = updated_budget["hotel_budget"]

            result = hotel_agent.run(destination, hotel_budget, days, logs, i)
            state["hotel"] = result
            state["selected_hotel"] = result["recommended"]
            state["current_total"] = compute_current_total(state, days)

        elif act == "call_places_agent":
            if not state["route"]:
                msg = "Route agent must be called before places agent."
                logs.append({"iteration": i, "step": "OBSERVE", "content": msg})
                messages.append({"role": "user", "content": msg})
                continue
            dest_coords = state["route"]["dest_coords"]
            # Now passing foursquare_api_key instead of otm_api_key
            result = places_agent.run(destination, dest_coords, foursquare_api_key, logs, i)
            state["places"] = result

        # ── TRACK BEST PLAN ────────────────────────────────────────────
        if state["selected_transport"] and state["selected_hotel"]:
            current_total = compute_current_total(state, days)
            state["current_total"] = current_total
            diff = abs(current_total - budget)
            if diff < best_diff:
                best_plan = copy.deepcopy(state)
                best_diff = diff

    else:
        logs.append({
            "iteration": MAX_ITERATIONS,
            "step": "THINK",
            "content": "Max iterations reached, returning best possible plan found during planning",
        })
        if best_plan:
            state = best_plan
            logs.append({
                "iteration": MAX_ITERATIONS,
                "step": "OBSERVE",
                "content": (
                    f"Could not fit within budget, showing closest plan — "
                    f"Best total: ₹{state['current_total']} vs budget ₹{budget}"
                ),
            })

    # ── FINAL VALIDATION ───────────────────────────────────────────────
    validation = validate_final_plan(state, budget, days)

    logs.append({
        "iteration": state["iteration"],
        "step": "OBSERVE",
        "content": (
            f"Final validation — "
            f"Transport: ₹{validation['transport_cost']} | "
            f"Hotel: ₹{validation['hotel_cost']} | "
            f"Food: ₹{validation['food_cost']} | "
            f"Activities: ₹{validation['activities_cost']} | "
            f"Total: ₹{validation['total_cost']} / ₹{budget} | "
            f"{'✅ Within budget' if validation['within_budget'] else '⚠️ Over budget'} "
            f"by ₹{validation['difference']}"
        ),
    })

    final_plan = {
        "source":        source,
        "destination":   destination,
        "days":          days,
        "transport":     state.get("selected_transport"),
        "hotel":         state.get("selected_hotel"),
        "places":        state.get("places", {}).get("places", []),
        "places_source": state.get("places", {}).get("source", "generic"),
        "budget_breakdown": state.get("budget", {}),
        "validation":    validation,
        "logs":          logs,
    }

    return final_plan, logs