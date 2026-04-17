
import math
from data.transport import city_coordinates, regional_fallbacks


def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # Earth radius in km
    d_lat = math.radians(lat2 - lat1)
    d_lon = math.radians(lon2 - lon1)
    a = (math.sin(d_lat / 2) ** 2 +
         math.cos(math.radians(lat1)) *
         math.cos(math.radians(lat2)) *
         math.sin(d_lon / 2) ** 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return round(R * c, 1)


def get_city_coords(city_name, logs, iteration):
    city = city_name.lower().strip()

    if city in city_coordinates:
        return city_coordinates[city], False

    # Try partial match
    for key in city_coordinates:
        if city in key or key in city:
            logs.append({
                "iteration": iteration,
                "step": "OBSERVE",
                "content": f"Partial match found: '{city_name}' matched to '{key}'",
            })
            return city_coordinates[key], False

    # Fallback to regional capital based on rough guess
    # Default to Delhi as central fallback
    fallback_city = "delhi"
    logs.append({
        "iteration": iteration,
        "step": "OBSERVE",
        "content": f"City not found, using regional estimate — '{city_name}' defaulting to {fallback_city} coordinates",
    })
    return city_coordinates[fallback_city], True


def get_recommended_modes(distance_km):
    """Recommend transport modes based on distance."""
    modes = ["train"]  # train always available
    if distance_km < 500:
        modes.insert(0, "bus")
    if distance_km > 400:
        modes.append("flight")
    return modes


def run(source, destination, logs, iteration):
    logs.append({
        "iteration": iteration,
        "step": "ACT",
        "content": f"Route Agent calculating distance: {source} → {destination}",
    })

    source_coords, source_fallback = get_city_coords(source, logs, iteration)
    dest_coords, dest_fallback = get_city_coords(destination, logs, iteration)

    distance_km = haversine(
        source_coords[0], source_coords[1],
        dest_coords[0], dest_coords[1]
    )

    recommended_modes = get_recommended_modes(distance_km)

    # Rough duration by fastest reasonable mode
    if distance_km > 400:
        duration_hours = round(distance_km / 800 + 2.5, 1)  # flight estimate
    elif distance_km > 200:
        duration_hours = round(distance_km / 60, 1)  # train estimate
    else:
        duration_hours = round(distance_km / 40, 1)  # bus estimate

    result = {
        "distance_km": distance_km,
        "duration_hours": duration_hours,
        "recommended_modes": recommended_modes,
        "source_coords": source_coords,
        "dest_coords": dest_coords,
        "fallback_used": source_fallback or dest_fallback,
    }

    logs.append({
        "iteration": iteration,
        "step": "OBSERVE",
        "content": (
            f"Distance: {distance_km} km | "
            f"Recommended modes: {', '.join(recommended_modes)} | "
            f"Fallback used: {source_fallback or dest_fallback}"
        ),
    })

    return result