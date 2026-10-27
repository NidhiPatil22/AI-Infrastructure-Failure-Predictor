"""
Modular Location & Geographic Bounding Configuration.

Restricts civil infrastructure monitoring to the Pune municipal corridor
while providing a clean, pluggable architecture for future expansion
to Mumbai, Nashik, Nagpur, and other cities.
"""
from __future__ import annotations

from typing import Any, Dict, List, Optional, Tuple

# =============================================================================
# ACTIVE MONITORING SCOPE: PUNE CITY
# =============================================================================
ACTIVE_CITY_KEY = "pune"

PUNE_BOUNDS: Dict[str, float] = {
    "min_latitude": 18.4000,
    "max_latitude": 18.6800,
    "min_longitude": 73.7000,
    "max_longitude": 73.9900,
}

PUNE_CENTER: Dict[str, float] = {
    "latitude": 18.5204,
    "longitude": 73.8567,
    "default_zoom": 12,
}

# Municipal sectors and wards mapped to canonical model zones:
# ['North', 'South', 'East', 'West', 'Central', 'Industrial']
PUNE_ZONES: Dict[str, Dict[str, Any]] = {
    "West": {
        "zone_name": "West Pune",
        "bounds": {
            "min_lat": 18.4800,
            "max_lat": 18.5350,
            "min_lng": 73.7500,
            "max_lng": 73.8300,
        },
        "wards": ["Kothrud Ward", "Warje-Karvenagar Ward", "Bavdhan-Chandani Chowk Ward"],
        "localities": [
            "Kothrud",
            "Karve Nagar",
            "Warje",
            "Bavdhan",
            "Paud Road",
            "Chandani Chowk",
            "Erandwane",
            "Kothrud Depot",
        ],
    },
    "Central": {
        "zone_name": "Central Pune",
        "bounds": {
            "min_lat": 18.5000,
            "max_lat": 18.5450,
            "min_lng": 73.8300,
            "max_lng": 73.8850,
        },
        "wards": ["Shivajinagar-Ghole Road Ward", "Kasba-Vishrambaug Wada Ward", "Bhavani Peth Ward"],
        "localities": [
            "Shivajinagar",
            "Deccan Gymkhana",
            "FC Road",
            "JM Road",
            "Sadashiv Peth",
            "Kasba Peth",
            "Swargate",
            "Pune Cantonment",
            "Camp",
        ],
    },
    "North": {
        "zone_name": "North Pune",
        "bounds": {
            "min_lat": 18.5400,
            "max_lat": 18.6000,
            "min_lng": 73.7800,
            "max_lng": 73.8500,
        },
        "wards": ["Aundh-Baner Ward", "Khadki Cantonment Ward", "Bopodi Ward"],
        "localities": [
            "Aundh",
            "Baner",
            "Balewadi",
            "Pashan",
            "Khadki",
            "Bopodi",
            "Pune University Circle",
            "Someshwarwadi",
        ],
    },
    "East": {
        "zone_name": "East Pune",
        "bounds": {
            "min_lat": 18.5100,
            "max_lat": 18.5750,
            "min_lng": 73.8800,
            "max_lng": 73.9700,
        },
        "wards": ["Nagar Road-Vadgaonsheri Ward", "Hadapsar-Mundhwa Ward", "Dhole Patil Road Ward"],
        "localities": [
            "Viman Nagar",
            "Kalyani Nagar",
            "Koregaon Park",
            "Kharadi",
            "Hadapsar",
            "Magarpatta City",
            "Yerawada",
            "Wadgaon Sheri",
        ],
    },
    "South": {
        "zone_name": "South Pune",
        "bounds": {
            "min_lat": 18.4300,
            "max_lat": 18.4900,
            "min_lng": 73.8300,
            "max_lng": 73.9100,
        },
        "wards": ["Dhankawadi-Sahakarnagar Ward", "Bibwewadi Ward", "Kondhwa-Yewalewadi Ward"],
        "localities": [
            "Katraj",
            "Kondhwa",
            "Dhankawadi",
            "Bibwewadi",
            "Sahakar Nagar",
            "Ambegaon",
            "Wanowrie",
            "Undri Link",
        ],
    },
    "Industrial": {
        "zone_name": "Industrial Sector (Bhosari / Hadapsar MIDC)",
        "bounds": {
            "min_lat": 18.6000,
            "max_lat": 18.6400,
            "min_lng": 73.8100,
            "max_lng": 73.8900,
        },
        "wards": ["Bhosari MIDC Ward", "Hadapsar Industrial Ward", "Pimpri Industrial Ward"],
        "localities": [
            "Bhosari MIDC",
            "Hadapsar Industrial Estate",
            "Pimpri Industrial Corridor",
            "Chakan Link",
            "Pirangut Industrial Area",
        ],
    },
}

# Supported cities registry for multi-city extensibility
SUPPORTED_CITIES: Dict[str, Dict[str, Any]] = {
    "pune": {
        "city_id": "pune",
        "name": "Pune",
        "state": "Maharashtra",
        "country": "India",
        "is_active": True,
        "center": PUNE_CENTER,
        "bounds": PUNE_BOUNDS,
        "zones": PUNE_ZONES,
        "description": "Primary active urban civil infrastructure monitoring sector covering PMC and PCMC metropolitan corridors.",
    },
    "mumbai": {
        "city_id": "mumbai",
        "name": "Mumbai",
        "state": "Maharashtra",
        "country": "India",
        "is_active": False,
        "center": {"latitude": 19.0760, "longitude": 72.8777, "default_zoom": 12},
        "bounds": {
            "min_latitude": 18.8900,
            "max_latitude": 19.2700,
            "min_longitude": 72.7700,
            "max_longitude": 73.0500,
        },
        "description": "Planned future expansion corridor: MMRDA coastal and expressway infrastructure.",
    },
    "nashik": {
        "city_id": "nashik",
        "name": "Nashik",
        "state": "Maharashtra",
        "country": "India",
        "is_active": False,
        "center": {"latitude": 19.9975, "longitude": 73.7898, "default_zoom": 12},
        "bounds": {
            "min_latitude": 19.9000,
            "max_latitude": 20.0800,
            "min_longitude": 73.6800,
            "max_longitude": 73.8900,
        },
        "description": "Planned future expansion corridor: North Maharashtra industrial and agricultural transit corridors.",
    },
    "nagpur": {
        "city_id": "nagpur",
        "name": "Nagpur",
        "state": "Maharashtra",
        "country": "India",
        "is_active": False,
        "center": {"latitude": 21.1458, "longitude": 79.0882, "default_zoom": 12},
        "bounds": {
            "min_latitude": 21.0500,
            "max_latitude": 21.2500,
            "min_longitude": 78.9800,
            "max_longitude": 79.1800,
        },
        "description": "Planned future expansion corridor: Vidarbha central multimodal transport hub.",
    },
}


def is_within_pune(latitude: float, longitude: float) -> bool:
    """Checks whether given coordinates fall within the Pune monitoring boundary."""
    try:
        lat = float(latitude)
        lng = float(longitude)
    except (ValueError, TypeError):
        return False

    return (
        PUNE_BOUNDS["min_latitude"] <= lat <= PUNE_BOUNDS["max_latitude"]
        and PUNE_BOUNDS["min_longitude"] <= lng <= PUNE_BOUNDS["max_longitude"]
    )


def validate_pune_coordinates(latitude: float, longitude: float) -> Tuple[bool, str]:
    """Validates coordinates against Pune boundary, returning status and human-readable feedback."""
    if not is_within_pune(latitude, longitude):
        return (
            False,
            (
                f"Selected location (lat: {latitude:.4f}, lng: {longitude:.4f}) is outside the "
                f"Pune city monitoring boundary (Lat: {PUNE_BOUNDS['min_latitude']} to {PUNE_BOUNDS['max_latitude']}, "
                f"Lng: {PUNE_BOUNDS['min_longitude']} to {PUNE_BOUNDS['max_longitude']}). "
                "The current platform release is restricted to Pune municipal infrastructure."
            ),
        )
    return (True, "Location is within active Pune monitoring area.")


def get_active_city_config() -> Dict[str, Any]:
    """Returns configuration for the currently active city (Pune)."""
    return SUPPORTED_CITIES[ACTIVE_CITY_KEY]
