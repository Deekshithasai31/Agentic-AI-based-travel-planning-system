
INITIAL_ALLOCATION = {
    "transport": 0.35,
    "hotel":     0.40,
    "food":      0.15,
    "activities": 0.10,
}
def allocate(total_budget, days, logs, iteration):
    logs.append({
        "iteration": iteration,
        "step": "ACT",
        "content": f"Budget Agent allocating ₹{total_budget} across categories for {days} days",
    })
    allocation = {
        "transport_budget":   round(total_budget * INITIAL_ALLOCATION["transport"]),
        "hotel_budget":       round(total_budget * INITIAL_ALLOCATION["hotel"]),
        "food_budget":        round(total_budget * INITIAL_ALLOCATION["food"]),
        "activities_budget":  round(total_budget * INITIAL_ALLOCATION["activities"]),
        "reallocation_log":   [],
        "status": "OK",
    }
    allocation["total_allocated"] = (
        allocation["transport_budget"] +
        allocation["hotel_budget"] +
        allocation["food_budget"] +
        allocation["activities_budget"]
    )
    logs.append({
        "iteration": iteration,
        "step": "OBSERVE",
        "content": (
            f"Budget allocated — "
            f"Transport: ₹{allocation['transport_budget']} | "
            f"Hotel: ₹{allocation['hotel_budget']} | "
            f"Food: ₹{allocation['food_budget']} | "
            f"Activities: ₹{allocation['activities_budget']}"
        ),
    })
    return allocation


def reallocate(allocation, transport_cost, hotel_cost_per_night, days, total_budget, logs, iteration):
    logs.append({
        "iteration": iteration,
        "step": "ACT",
        "content": "Budget Agent checking if reallocation is needed",
    })

    alloc = dict(allocation)
    alloc["reallocation_log"] = list(allocation.get("reallocation_log", []))
    transport_excess = transport_cost - alloc["transport_budget"]
    if transport_excess > 0:
        reason = (
            f"Transport exceeded allocation by ₹{transport_excess}. "
            f"Reducing hotel budget from ₹{alloc['hotel_budget']} "
            f"to ₹{alloc['hotel_budget'] - transport_excess}."
        )
        alloc["hotel_budget"] -= transport_excess
        alloc["transport_budget"] = transport_cost
        alloc["reallocation_log"].append(reason)
        logs.append({
            "iteration": iteration,
            "step": "REPLAN",
            "content": reason,
        })

    # Check hotel overage
    hotel_total = hotel_cost_per_night * days
    hotel_excess = hotel_total - alloc["hotel_budget"]
    if hotel_excess > 0:
        # First reduce activities
        activities_cut = min(alloc["activities_budget"], hotel_excess)
        alloc["activities_budget"] -= activities_cut
        hotel_excess -= activities_cut

        # Then reduce food if still over
        if hotel_excess > 0:
            food_cut = min(alloc["food_budget"], hotel_excess)
            alloc["food_budget"] -= food_cut
            hotel_excess -= food_cut

        alloc["hotel_budget"] = hotel_cost_per_night * days

        reason = (
            f"Hotel cost ₹{hotel_cost_per_night}/night × {days} days = "
            f"₹{hotel_cost_per_night * days} exceeded hotel budget. "
            f"Reduced activities to ₹{alloc['activities_budget']} and "
            f"food to ₹{alloc['food_budget']}."
        )
        alloc["reallocation_log"].append(reason)
        logs.append({
            "iteration": iteration,
            "step": "REPLAN",
            "content": reason,
        })

    # Final total
    alloc["total_allocated"] = (
        alloc["transport_budget"] +
        alloc["hotel_budget"] +
        alloc["food_budget"] +
        alloc["activities_budget"]
    )

    if alloc["total_allocated"] > total_budget:
        alloc["status"] = "OVER"
    elif alloc["total_allocated"] > total_budget * 0.90:
        alloc["status"] = "TIGHT"
    else:
        alloc["status"] = "OK"

    logs.append({
        "iteration": iteration,
        "step": "OBSERVE",
        "content": (
            f"After reallocation — Total: ₹{alloc['total_allocated']} / ₹{total_budget} | "
            f"Status: {alloc['status']}"
        ),
    })

    return alloc
def run(total_budget, days, logs, iteration):

    return allocate(total_budget, days, logs, iteration)