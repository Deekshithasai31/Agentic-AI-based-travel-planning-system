"""
Validator — validates final travel plan against budget constraints.
All calculations in Python, not GPT.
"""


def validate_final_plan(state, budget, days):
    """
    Compute final costs and check if plan is within budget.
    Returns a structured validation result.
    """
    transport = state.get("selected_transport", {})
    hotel     = state.get("selected_hotel", {})
    budget_s  = state.get("budget", {})

    transport_cost  = transport.get("cost", 0)
    hotel_per_night = hotel.get("price_per_night", 0)
    hotel_cost      = hotel_per_night * days
    food_cost       = budget_s.get("food_budget", 0)
    activities_cost = budget_s.get("activities_budget", 0)

    total_cost = transport_cost + hotel_cost + food_cost + activities_cost

    within_budget  = total_cost <= budget
    difference     = budget - total_cost
    savings_label  = "saved" if within_budget else "over"

    return {
        "transport_cost":    transport_cost,
        "hotel_cost":        hotel_cost,
        "food_cost":         food_cost,
        "activities_cost":   activities_cost,
        "total_cost":        total_cost,
        "budget":            budget,
        "within_budget":     within_budget,
        "difference":        abs(difference),
        "savings_or_excess": savings_label,
    }


def is_plan_complete(state):
    """Check if all required agents have returned results."""
    return (
        bool(state.get("route")) and
        bool(state.get("transport")) and
        bool(state.get("hotel")) and
        bool(state.get("budget")) and
        bool(state.get("places")) and
        state.get("selected_transport") is not None and
        state.get("selected_hotel") is not None
    )