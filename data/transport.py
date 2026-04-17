
city_coordinates = {
    "delhi":         (28.6139, 77.2090),
    "mumbai":        (19.0760, 72.8777),
    "bangalore":     (12.9716, 77.5946),
    "chennai":       (13.0827, 80.2707),
    "hyderabad":     (17.3850, 78.4867),
    "kolkata":       (22.5726, 88.3639),
    "pune":          (18.5204, 73.8567),
    "jaipur":        (26.9124, 75.7873),
    "goa":           (15.2993, 74.1240),
    "agra":          (27.1767, 78.0081),
    "varanasi":      (25.3176, 82.9739),
    "kochi":         (9.9312,  76.2673),
    "manali":        (32.2396, 77.1887),
    "shimla":        (31.1048, 77.1734),
    "ooty":          (11.4102, 76.6950),
    "mysore":        (12.2958, 76.6394),
    "udaipur":       (24.5854, 73.7125),
    "darjeeling":    (27.0360, 88.2627),
    "rishikesh":     (30.0869, 78.2676),
    "amritsar":      (31.6340, 74.8723),
    "jodhpur":       (26.2389, 73.0243),
    "bhopal":        (23.2599, 77.4126),
    "indore":        (22.7196, 75.8577),
    "nagpur":        (21.1458, 79.0882),
    "surat":         (21.1702, 72.8311),
    "ahmedabad":     (23.0225, 72.5714),
    "lucknow":       (26.8467, 80.9462),
    "kanpur":        (26.4499, 80.3319),
    "patna":         (25.5941, 85.1376),
    "ranchi":        (23.3441, 85.3096),
    "bhubaneswar":   (20.2961, 85.8245),
    "visakhapatnam": (17.6868, 83.2185),
    "coimbatore":    (11.0168, 76.9558),
    "madurai":       (9.9252,  78.1198),
    "trichy":        (10.7905, 78.7047),
    "guwahati":      (26.1445, 91.7362),
    "shillong":      (25.5788, 91.8933),
    "imphal":        (24.8170, 93.9368),
    "aizawl":        (23.7271, 92.7176),
    "kohima":        (25.6751, 94.1086),
    "dehradun":      (30.3165, 78.0322),
    "haridwar":      (29.9457, 78.1642),
    "nainital":      (29.3919, 79.4542),
    "mussoorie":     (30.4598, 78.0644),
    "leh":           (34.1526, 77.5771),
    "srinagar":      (34.0837, 74.7973),
    "jammu":         (32.7266, 74.8570),
    "chandigarh":    (30.7333, 76.7794),
    "ludhiana":      (30.9010, 75.8573),
    "allahabad":     (25.4358, 81.8463),
    "mathura":       (27.4924, 77.6737),
    "ajmer":         (26.4499, 74.6399),
    "pushkar":       (26.4897, 74.5511),
    "bikaner":       (28.0229, 73.3119),
    "jaisalmer":     (26.9157, 70.9083),
    "mount abu":     (24.5926, 72.7156),
    "raipur":        (21.2514, 81.6296),
    "vijayawada":    (16.5062, 80.6480),
    "tirupati":      (13.6288, 79.4192),
    "puducherry":    (11.9416, 79.8083),
    "aurangabad":    (19.8762, 75.3433),
    "nashik":        (19.9975, 73.7898),
    "patiala":       (30.3398, 76.3869),
}

# Regional capital fallbacks for unknown cities
regional_fallbacks = {
    "north":     "delhi",
    "south":     "bangalore",
    "east":      "kolkata",
    "west":      "mumbai",
    "central":   "bhopal",
    "northeast": "guwahati",
}

# Pricing per km
PRICE_PER_KM = {
    "bus":    1.5,
    "train":  1.2,
    "flight": 4.5,
}

# Speed in km/h for duration calculation
SPEED_KMH = {
    "bus":    40,
    "train":  60,
    "flight": 800,
}

# Flight extra time for airport procedures (hours)
FLIGHT_EXTRA_HOURS = 2.5

# Distance limits for transport modes
BUS_MAX_KM    = 500
FLIGHT_MIN_KM = 400
