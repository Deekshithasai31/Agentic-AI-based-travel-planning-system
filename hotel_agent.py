"""
Hotel Agent — finds suitable hotels based on destination
city tier and available budget per night.
"""

from data.hotels import (
    tier_1_hotels, tier_2_hotels, tier_3_hotels,
    TIER_1_CITIES, TIER_2_CITIES
)


def get_city_tier(destination):
    """Classify destination city into tier 1, 2, or 3."""
    city = destination.lower().strip()
    if city in TIER_1_CITIES:
        return 1
    elif city in TIER_2_CITIES:
        return 2
    else:
        return 3


def get_hotels_for_tier(tier):
    """Return hotel list for a given tier."""
    if tier == 1:
        return tier_1_hotels
    elif tier == 2:
        return tier_2_hotels
    else:
        return tier_3_hotels


def run(destination, hotel_budget, days, logs, iteration):
    """
    Main hotel agent function.
    Finds hotels that fit within the nightly budget.
    """
    logs.append({
        "iteration": iteration,
        "step": "ACT",
        "content": f"Hotel Agent searching hotels in {destination} | Budget: ₹{hotel_budget} total for {days} days",
    })

    tier = get_city_tier(destination)
    all_hotels = get_hotels_for_tier(tier)

    # Max price per night we can afford
    max_per_night = hotel_budget // days if days > 0 else hotel_budget

    logs.append({
        "iteration": iteration,
        "step": "OBSERVE",
        "content": f"{destination} classified as Tier {tier} city | Max per night: ₹{max_per_night}",
    })

    # Filter hotels that fit the nightly budget
    affordable = [h for h in all_hotels if h["price_per_night"] <= max_per_night]

    budget_stretch = False

    if affordable:
        # Pick best affordable hotel (highest stars within budget)
        recommended = max(affordable, key=lambda h: (h["stars"], -h["price_per_night"]))
    else:
        # No hotel fits — return cheapest available
        recommended = min(all_hotels, key=lambda h: h["price_per_night"])
        budget_stretch = True
        logs.append({
            "iteration": iteration,
            "step": "OBSERVE",
            "content": (
                f"No hotels in budget (₹{max_per_night}/night). "
                f"Recommending closest option: {recommended['name']} at ₹{recommended['price_per_night']}/night. "
                f"Budget stretch applied."
            ),
        })

    total_hotel_cost = recommended["price_per_night"] * days

    result = {
        "recommended": {
            **recommended,
            "total_cost": total_hotel_cost,
        },
        "all_options": affordable if affordable else all_hotels,
        "budget_stretch": budget_stretch,
        "city_tier": tier,
        "max_per_night": max_per_night,
    }

    logs.append({
        "iteration": iteration,
        "step": "OBSERVE",
        "content": (
            f"Hotel selected: {recommended['name']} ⭐{recommended['stars']} | "
            f"₹{recommended['price_per_night']}/night × {days} = ₹{total_hotel_cost} | "
            f"Budget stretch: {budget_stretch}"
        ),
    })

    return result