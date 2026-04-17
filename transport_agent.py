from data.transport import (
    PRICE_PER_KM, SPEED_KMH, FLIGHT_EXTRA_HOURS,
    BUS_MAX_KM, FLIGHT_MIN_KM
)
def calculate_option(mode, distance_km):
    """Calculate cost and duration for a transport mode."""
    cost = round(distance_km * PRICE_PER_KM[mode])

    if mode == "flight":
        duration = round(distance_km / SPEED_KMH[mode] + FLIGHT_EXTRA_HOURS, 1)
    else:
        duration = round(distance_km / SPEED_KMH[mode], 1)

    return {
        "mode": mode,
        "cost": cost,
        "duration_hours": duration,
        "available": True,
    }
def run(distance_km, logs, iteration):
    logs.append({
        "iteration": iteration,
        "step": "ACT",
        "content": f"Transport Agent calculating options for {distance_km} km distance",
    })

    options = []

    # Bus — only for short distances
    if distance_km <= BUS_MAX_KM:
        options.append(calculate_option("bus", distance_km))

    # Train — always available
    options.append(calculate_option("train", distance_km))

    # Flight — only for longer distances
    if distance_km >= FLIGHT_MIN_KM:
        options.append(calculate_option("flight", distance_km))

    # Sort by cost
    options_sorted = sorted(options, key=lambda x: x["cost"])

    cheapest = options_sorted[0]
    fastest = min(options, key=lambda x: x["duration_hours"])

    result = {
        "options": options_sorted,
        "cheapest": cheapest,
        "fastest": fastest,
    }

    summary = " | ".join(
        [f"{o['mode'].title()}: ₹{o['cost']} ({o['duration_hours']}hrs)"
         for o in options_sorted]
    )
    logs.append({
        "iteration": iteration,
        "step": "OBSERVE",
        "content": f"Transport options: {summary}",
    })

    return result