
import requests

CITY_FALLBACKS = {
    "manali": [
        "Hadimba Devi Temple", "Solang Valley", "Rohtang Pass",
        "Mall Road Manali", "Vashisht Hot Springs", "Old Manali Village",
        "Jogini Waterfall", "Manu Temple"
    ],
    "goa": [
        "Baga Beach", "Calangute Beach", "Basilica of Bom Jesus",
        "Fort Aguada", "Dudhsagar Waterfalls", "Anjuna Flea Market",
        "Chapora Fort", "Palolem Beach"
    ],
    "jaipur": [
        "Amber Fort", "Hawa Mahal", "City Palace Jaipur",
        "Jantar Mantar", "Nahargarh Fort", "Jal Mahal",
        "Johari Bazaar", "Albert Hall Museum"
    ],
    "agra": [
        "Taj Mahal", "Agra Fort", "Fatehpur Sikri",
        "Mehtab Bagh", "Itmad-ud-Daulah Tomb", "Akbar's Tomb",
        "Kinari Bazaar", "Dayal Bagh Temple"
    ],
    "varanasi": [
        "Dashashwamedh Ghat", "Kashi Vishwanath Temple", "Sarnath",
        "Manikarnika Ghat", "Assi Ghat", "Ramnagar Fort",
        "Tulsi Manas Temple", "Banaras Hindu University"
    ],
    "delhi": [
        "Red Fort", "Qutub Minar", "India Gate",
        "Humayun's Tomb", "Lotus Temple", "Akshardham Temple",
        "Chandni Chowk", "National Museum"
    ],
    "mumbai": [
        "Gateway of India", "Marine Drive", "Elephanta Caves",
        "Chhatrapati Shivaji Terminus", "Juhu Beach", "Siddhivinayak Temple",
        "Colaba Causeway", "Dharavi"
    ],
    "udaipur": [
        "City Palace Udaipur", "Lake Pichola", "Jag Mandir",
        "Sajjangarh Monsoon Palace", "Jagdish Temple", "Fateh Sagar Lake",
        "Bagore Ki Haveli", "Shilpgram"
    ],
    "jodhpur": [
        "Mehrangarh Fort", "Jaswant Thada", "Umaid Bhawan Palace",
        "Mandore Gardens", "Clock Tower Market", "Rao Jodha Desert Rock Park",
        "Toorji Ka Jhalra", "Sardar Market"
    ],
    "jaisalmer": [
        "Jaisalmer Fort", "Sam Sand Dunes", "Patwon Ki Haveli",
        "Gadisar Lake", "Nathmal Ki Haveli", "Bada Bagh",
        "Desert Cultural Centre", "Salim Singh Ki Haveli"
    ],
    "rishikesh": [
        "Laxman Jhula", "Ram Jhula", "Triveni Ghat",
        "Neelkanth Mahadev Temple", "Beatles Ashram", "Rajaji National Park",
        "Parmarth Niketan Ashram", "Jumpin Heights Adventure"
    ],
    "shimla": [
        "Mall Road Shimla", "The Ridge", "Jakhu Temple",
        "Christ Church", "Kufri", "Chadwick Falls",
        "Viceregal Lodge", "Indian Institute of Advanced Study"
    ],
    "ooty": [
        "Ooty Lake", "Botanical Garden Ooty", "Doddabetta Peak",
        "Nilgiri Mountain Railway", "Rose Garden Ooty", "Pykara Lake",
        "Mudumalai National Park", "Toda Settlements"
    ],
    "mysore": [
        "Mysore Palace", "Chamundeshwari Temple", "Brindavan Gardens",
        "St. Philomena's Church", "Mysore Zoo", "Jaganmohan Palace",
        "Karanji Lake", "Devaraja Market"
    ],
    "kochi": [
        "Fort Kochi Beach", "Chinese Fishing Nets", "Mattancherry Palace",
        "Jewish Synagogue Mattancherry", "St. Francis Church", "Marine Drive Kochi",
        "Cherai Beach", "Kerala Folklore Museum"
    ],
    "amritsar": [
        "Golden Temple", "Jallianwala Bagh", "Wagah Border",
        "Durgiana Temple", "Partition Museum", "Ram Bagh Garden",
        "Hall Bazaar", "Gobindgarh Fort"
    ],
    "darjeeling": [
        "Tiger Hill", "Darjeeling Himalayan Railway", "Happy Valley Tea Estate",
        "Batasia Loop", "Peace Pagoda Darjeeling", "Padmaja Naidu Zoo",
        "Observatory Hill", "Ghoom Monastery"
    ],
    "leh": [
        "Pangong Lake", "Nubra Valley", "Shanti Stupa",
        "Leh Palace", "Magnetic Hill", "Hemis Monastery",
        "Thiksey Monastery", "Khardung La Pass"
    ],
    "srinagar": [
        "Dal Lake", "Mughal Gardens", "Hazratbal Shrine",
        "Shankaracharya Temple", "Nigeen Lake", "Gulmarg",
        "Pahalgam", "Sonamarg"
    ],
    "pushkar": [
        "Pushkar Lake", "Brahma Temple", "Savitri Temple",
        "Pushkar Camel Fair Grounds", "Rose Garden Pushkar", "Rangji Temple",
        "Old Rangji Temple", "Pushkar Bazaar"
    ],
    "aurangabad": [
        "Ajanta Caves", "Ellora Caves", "Bibi Ka Maqbara",
        "Daulatabad Fort", "Panchakki", "Aurangabad Caves",
        "Salim Ali Lake", "Himroo Weaving Centre"
    ],
}

GENERIC_FALLBACK = [
    "City Museum", "Main Market & Bazaar", "Local Temple",
    "City Park & Gardens", "Heritage Walk Area", "Scenic Viewpoint",
    "Cultural Center", "Botanical Garden",
]

FOURSQUARE_BASE = "https://api.foursquare.com/v3/places/search"


def fetch_from_foursquare(lat, lon, api_key, destination, logs, iteration):
    try:
        headers = {
            "Authorization": api_key,
            "Accept": "application/json",
        }
        params = {
            "ll":         f"{lat},{lon}",
            "radius":     8000,
            "categories": "16032,16025,16026,16027",   # Travel & Transport / Sights & Outdoors
            "limit":      15,
            "sort":       "RATING",
            "fields":     "name,categories,rating,location",
        }

        response = requests.get(
            FOURSQUARE_BASE, headers=headers, params=params, timeout=8
        )

        if response.status_code == 401:
            logs.append({
                "iteration": iteration,
                "step": "OBSERVE",
                "content": "Foursquare API key invalid — using curated fallback places",
            })
            return None

        if response.status_code != 200:
            logs.append({
                "iteration": iteration,
                "step": "OBSERVE",
                "content": f"Foursquare API error HTTP {response.status_code} — using curated fallback",
            })
            return None

        data = response.json()
        results = data.get("results", [])

        if not results:
            logs.append({
                "iteration": iteration,
                "step": "OBSERVE",
                "content": f"Foursquare returned no results for {destination} — using curated fallback",
            })
            return None

        # Extract clean place names, filter unnamed or very short
        places = []
        for item in results:
            name = item.get("name", "").strip()
            if name and len(name) > 3:
                places.append(name)

        if not places:
            return None

        return places[:8]

    except requests.exceptions.Timeout:
        logs.append({
            "iteration": iteration,
            "step": "OBSERVE",
            "content": "Foursquare API timed out — using curated fallback places",
        })
        return None
    except Exception as e:
        logs.append({
            "iteration": iteration,
            "step": "OBSERVE",
            "content": f"Foursquare API error: {str(e)} — using curated fallback places",
        })
        return None


def get_curated_fallback(destination):
    city = destination.lower().strip()
    return CITY_FALLBACKS.get(city, GENERIC_FALLBACK).copy()


def run(destination, dest_coords, foursquare_api_key, logs, iteration):
    logs.append({
        "iteration": iteration,
        "step": "ACT",
        "content": f"Places Agent fetching tourist spots for {destination}",
    })

    lat, lon = dest_coords
    places = None
    source = "fallback"

    # Try Foursquare if API key provided
    if foursquare_api_key and foursquare_api_key.strip() and foursquare_api_key != "apikey":
        places = fetch_from_foursquare(lat, lon, foursquare_api_key, destination, logs, iteration)
        if places:
            source = "foursquare"

    # Fall back to curated city-specific list
    if not places:
        places = get_curated_fallback(destination)
        city_key = destination.lower().strip()
        source = "curated" if city_key in CITY_FALLBACKS else "generic"

        logs.append({
            "iteration": iteration,
            "step": "OBSERVE",
            "content": (
                f"Using {'city-specific curated' if source == 'curated' else 'generic'} "
                f"places list for {destination}"
            ),
        })

    result = {
        "places": places,
        "source": source,
        "fallback_used": source != "foursquare",
    }

    logs.append({
        "iteration": iteration,
        "step": "OBSERVE",
        "content": (
            f"Places source: {source.upper()} | "
            f"Found {len(places)} places: {', '.join(places[:4])}..."
        ),
    })

    return result