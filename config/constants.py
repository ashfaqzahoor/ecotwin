SUPPORTED_CITIES = {
    "Delhi": {"lat": 28.6139, "lon": 77.2090, "country": "IN"},
    "Mumbai": {"lat": 19.0760, "lon": 72.8777, "country": "IN"},
    "Bengaluru": {"lat": 12.9716, "lon": 77.5946, "country": "IN"},
    "Hyderabad": {"lat": 17.3850, "lon": 78.4867, "country": "IN"},
    "Chennai": {"lat": 13.0827, "lon": 80.2707, "country": "IN"},
    "Kolkata": {"lat": 22.5726, "lon": 88.3639, "country": "IN"},
    "Pune": {"lat": 18.5204, "lon": 73.8567, "country": "IN"},
    "Ahmedabad": {"lat": 23.0225, "lon": 72.5714, "country": "IN"},
    "Jaipur": {"lat": 26.9124, "lon": 75.7873, "country": "IN"},
    "Lucknow": {"lat": 26.8467, "lon": 80.9462, "country": "IN"},
    "Kanpur": {"lat": 26.4499, "lon": 80.3319, "country": "IN"},
    "Nagpur": {"lat": 21.1458, "lon": 79.0882, "country": "IN"},
    "Indore": {"lat": 22.7196, "lon": 75.8577, "country": "IN"},
    "Bhopal": {"lat": 23.2599, "lon": 77.4126, "country": "IN"},
    "Patna": {"lat": 25.5941, "lon": 85.1376, "country": "IN"},
    "Chandigarh": {"lat": 30.7333, "lon": 76.7794, "country": "IN"},
    "Amritsar": {"lat": 31.6340, "lon": 74.8723, "country": "IN"},
    "Ludhiana": {"lat": 30.9010, "lon": 75.8573, "country": "IN"},
    "Surat": {"lat": 21.1702, "lon": 72.8311, "country": "IN"},
    "Vadodara": {"lat": 22.3072, "lon": 73.1812, "country": "IN"},
    "Rajkot": {"lat": 22.3039, "lon": 70.8022, "country": "IN"},
    "Kochi": {"lat": 9.9312, "lon": 76.2673, "country": "IN"},
    "Thiruvananthapuram": {"lat": 8.5241, "lon": 76.9366, "country": "IN"},
    "Coimbatore": {"lat": 11.0168, "lon": 76.9558, "country": "IN"},
    "Visakhapatnam": {"lat": 17.6868, "lon": 83.2185, "country": "IN"},
    "Vijayawada": {"lat": 16.5062, "lon": 80.6480, "country": "IN"},
    "Bhubaneswar": {"lat": 20.2961, "lon": 85.8245, "country": "IN"},
    "Guwahati": {"lat": 26.1445, "lon": 91.7362, "country": "IN"},
    "Jammu": {"lat": 32.7266, "lon": 74.8570, "country": "IN"},
    "Srinagar": {"lat": 34.0837, "lon": 74.7973, "country": "IN"},
}

POLLUTANTS = ["pm25", "pm10", "no2", "o3", "co", "so2"]
FORECAST_TARGETS = ["pm25", "pm10", "no2", "o3", "temperature", "energy_demand"]

# WHO-oriented operational thresholds for an MVP alerting workflow.
WHO_LIMITS = {
    "pm25": 15.0,
    "pm10": 45.0,
    "no2": 25.0,
    "o3": 60.0,
    "co": 4.0,
    "so2": 40.0,
    "temperature": 40.0,
}

SCENARIO_EFFECTS = {
    "traffic_reduction": {"pm25": -0.18, "pm10": -0.10, "no2": -0.28, "co": -0.22, "energy_demand": -0.03},
    "green_cover_increase": {"pm25": -0.08, "pm10": -0.07, "o3": -0.04, "temperature": -0.10, "energy_demand": -0.08},
    "industrial_emissions_reduction": {"pm25": -0.20, "pm10": -0.18, "so2": -0.30, "no2": -0.10},
    "public_transport_adoption": {"pm25": -0.12, "pm10": -0.07, "no2": -0.22, "co": -0.20, "energy_demand": -0.02},
}
