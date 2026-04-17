"""
Mock hotel data organized by city tier.
Tier 1 = Metro cities
Tier 2 = Popular tourist destinations
Tier 3 = Small / unknown cities
"""

# City tier classification (lowercase)
TIER_1_CITIES = [
    "delhi", "mumbai", "bangalore", "chennai",
    "hyderabad", "kolkata", "pune"
]

TIER_2_CITIES = [
    "jaipur", "goa", "agra", "varanasi", "kochi",
    "manali", "shimla", "ooty", "mysore", "udaipur",
    "darjeeling", "rishikesh", "amritsar", "jodhpur",
    "leh", "srinagar", "aurangabad", "pushkar", "jaisalmer"
]

# All others are Tier 3

tier_1_hotels = [
    {
        "name": "Metro Budget Lodge",
        "stars": 2,
        "price_per_night": 650,
        "amenities": ["WiFi", "AC", "Hot Water"],
        "tier": "budget"
    },
    {
        "name": "City Comfort Inn",
        "stars": 2,
        "price_per_night": 850,
        "amenities": ["WiFi", "AC", "Breakfast", "TV"],
        "tier": "budget"
    },
    {
        "name": "Urban Stay Hotel",
        "stars": 3,
        "price_per_night": 1400,
        "amenities": ["WiFi", "AC", "Restaurant", "Gym", "Parking"],
        "tier": "mid"
    },
    {
        "name": "Central Park Hotel",
        "stars": 3,
        "price_per_night": 2000,
        "amenities": ["WiFi", "AC", "Restaurant", "Bar", "Gym", "Spa"],
        "tier": "mid"
    },
    {
        "name": "Grand Metropolitan",
        "stars": 4,
        "price_per_night": 3500,
        "amenities": ["WiFi", "AC", "Restaurant", "Bar", "Gym", "Spa", "Pool"],
        "tier": "luxury"
    },
    {
        "name": "The Royal Prestige",
        "stars": 5,
        "price_per_night": 6000,
        "amenities": ["WiFi", "AC", "Fine Dining", "Bar", "Spa", "Pool", "Concierge", "Valet"],
        "tier": "luxury"
    },
]

tier_2_hotels = [
    {
        "name": "Tourist Guest House",
        "stars": 2,
        "price_per_night": 500,
        "amenities": ["WiFi", "Hot Water", "Fan"],
        "tier": "budget"
    },
    {
        "name": "Traveller's Inn",
        "stars": 2,
        "price_per_night": 750,
        "amenities": ["WiFi", "AC", "Hot Water", "TV"],
        "tier": "budget"
    },
    {
        "name": "Heritage View Hotel",
        "stars": 3,
        "price_per_night": 1100,
        "amenities": ["WiFi", "AC", "Restaurant", "Garden", "Parking"],
        "tier": "mid"
    },
    {
        "name": "Nature's Retreat",
        "stars": 3,
        "price_per_night": 1800,
        "amenities": ["WiFi", "AC", "Restaurant", "Terrace", "Room Service"],
        "tier": "mid"
    },
    {
        "name": "The Scenic Resort",
        "stars": 4,
        "price_per_night": 3200,
        "amenities": ["WiFi", "AC", "Restaurant", "Pool", "Spa", "Adventure Activities"],
        "tier": "luxury"
    },
    {
        "name": "Palace Heritage Hotel",
        "stars": 5,
        "price_per_night": 5500,
        "amenities": ["WiFi", "AC", "Fine Dining", "Spa", "Pool", "Cultural Shows", "Valet"],
        "tier": "luxury"
    },
]

tier_3_hotels = [
    {
        "name": "Local Rest House",
        "stars": 1,
        "price_per_night": 350,
        "amenities": ["Hot Water", "Fan"],
        "tier": "budget"
    },
    {
        "name": "Budget Traveller Lodge",
        "stars": 2,
        "price_per_night": 550,
        "amenities": ["WiFi", "Fan", "Hot Water"],
        "tier": "budget"
    },
    {
        "name": "Town Center Hotel",
        "stars": 2,
        "price_per_night": 800,
        "amenities": ["WiFi", "AC", "Hot Water", "TV"],
        "tier": "budget"
    },
    {
        "name": "District Grand Hotel",
        "stars": 3,
        "price_per_night": 1200,
        "amenities": ["WiFi", "AC", "Restaurant", "Parking"],
        "tier": "mid"
    },
    {
        "name": "Comfort Suites",
        "stars": 3,
        "price_per_night": 1800,
        "amenities": ["WiFi", "AC", "Restaurant", "Room Service", "Gym"],
        "tier": "mid"
    },
    {
        "name": "The Regional Luxury Inn",
        "stars": 4,
        "price_per_night": 3000,
        "amenities": ["WiFi", "AC", "Restaurant", "Pool", "Spa", "Banquet"],
        "tier": "luxury"
    },
]
