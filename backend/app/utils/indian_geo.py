"""Indian Geographic and Civil Infrastructure Mapping Utilities.

Translates real Indian locations, states, and coordinates into regional
zones and environmental baseline profiles for the predictive maintenance model,
and provides defensible mappings from high-level visible observations into model features.
"""
from __future__ import annotations

import re
from typing import Any, Dict, Optional, Tuple

# Indian State to Model Zone Mapping
# Dataset model was trained with categorical zones: 'North', 'South', 'East', 'West', 'Central', 'Industrial'
STATE_TO_ZONE: Dict[str, str] = {
    # West Zone
    "maharashtra": "West",
    "gujarat": "West",
    "goa": "West",
    "dadra and nagar haveli and daman and diu": "West",
    # South Zone
    "karnataka": "South",
    "tamil nadu": "South",
    "telangana": "South",
    "andhra pradesh": "South",
    "kerala": "South",
    "puducherry": "South",
    # North Zone
    "delhi": "North",
    "new delhi": "North",
    "uttar pradesh": "North",
    "haryana": "North",
    "punjab": "North",
    "rajasthan": "North",
    "himachal pradesh": "North",
    "jammu and kashmir": "North",
    "ladakh": "North",
    "uttarakhand": "North",
    "chandigarh": "North",
    # East Zone
    "west bengal": "East",
    "bihar": "East",
    "odisha": "East",
    "jharkhand": "East",
    "assam": "East",
    "sikkim": "East",
    "meghalaya": "East",
    "tripura": "East",
    "manipur": "East",
    "nagaland": "East",
    "mizoram": "East",
    "arunachal pradesh": "East",
    # Central Zone
    "madhya pradesh": "Central",
    "chhattisgarh": "Central",
}

# Regional Indian Climate Profiles (Annual rainfall in mm, average temperature in °C)
# Derived from Indian Meteorological Department (IMD) historical regional normals
REGIONAL_CLIMATE: Dict[str, Dict[str, float]] = {
    "West": {"annual_rainfall": 1850.0, "average_temperature": 27.5},   # Coastal & Western Ghats influence
    "South": {"annual_rainfall": 1050.0, "average_temperature": 27.0},  # Deccan & Peninsula
    "North": {"annual_rainfall": 800.0, "average_temperature": 25.0},   # Indo-Gangetic Plains & North
    "East": {"annual_rainfall": 1600.0, "average_temperature": 26.5},   # Sub-Himalayan & Delta
    "Central": {"annual_rainfall": 1150.0, "average_temperature": 26.0}, # Central Highlands
    "Industrial": {"annual_rainfall": 1200.0, "average_temperature": 28.0},
}

# Preset Indian Corridors for Quick Selection & Testing
POPULAR_INDIAN_CORRIDORS = [
    {
        "name": "Bandra-Worli Sea Link",
        "city": "Mumbai",
        "state": "Maharashtra",
        "address": "Bandra-Worli Sea Link, Mumbai, Maharashtra 400050, India",
        "latitude": 19.0330,
        "longitude": 72.8164,
        "default_asset_type": "Bridge",
        "default_material": "Concrete",
        "default_traffic": "Heavy",
    },
    {
        "name": "Mumbai - Pune Expressway",
        "city": "Pune",
        "state": "Maharashtra",
        "address": "Mumbai - Pune Expressway, Lonavala-Khandala, Maharashtra 410401, India",
        "latitude": 18.7560,
        "longitude": 73.4116,
        "default_asset_type": "Road",
        "default_material": "Concrete",
        "default_traffic": "Heavy",
    },
    {
        "name": "Atal Setu (MTHL)",
        "city": "Navi Mumbai",
        "state": "Maharashtra",
        "address": "Mumbai Trans Harbour Link (Atal Setu), Sewri-Nhava Sheva, Maharashtra, India",
        "latitude": 18.9950,
        "longitude": 72.9640,
        "default_asset_type": "Bridge",
        "default_material": "Steel",
        "default_traffic": "Heavy",
    },
    {
        "name": "Outer Ring Road (ORR)",
        "city": "Bengaluru",
        "state": "Karnataka",
        "address": "Outer Ring Road, Bellandur, Bengaluru, Karnataka 560103, India",
        "latitude": 12.9279,
        "longitude": 77.6833,
        "default_asset_type": "Road",
        "default_material": "Asphalt",
        "default_traffic": "Heavy",
    },
    {
        "name": "Durgam Cheruvu Cable Bridge",
        "city": "Hyderabad",
        "state": "Telangana",
        "address": "Durgam Cheruvu Cable Bridge, Hitec City, Hyderabad, Telangana 500081, India",
        "latitude": 17.4334,
        "longitude": 78.3872,
        "default_asset_type": "Bridge",
        "default_material": "Concrete",
        "default_traffic": "Moderate",
    },
    {
        "name": "Yamuna Expressway",
        "city": "Greater Noida",
        "state": "Uttar Pradesh",
        "address": "Yamuna Expressway, Greater Noida to Agra, Uttar Pradesh 201310, India",
        "latitude": 27.8974,
        "longitude": 77.5298,
        "default_asset_type": "Road",
        "default_material": "Concrete",
        "default_traffic": "Heavy",
    },
    {
        "name": "Vidyasagar Setu (2nd Hooghly Bridge)",
        "city": "Kolkata",
        "state": "West Bengal",
        "address": "Vidyasagar Setu, Toll Plaza, Kolkata, West Bengal 700021, India",
        "latitude": 22.5562,
        "longitude": 88.3277,
        "default_asset_type": "Bridge",
        "default_material": "Steel",
        "default_traffic": "Heavy",
    },
    {
        "name": "Samruddhi Mahamarg",
        "city": "Nagpur",
        "state": "Maharashtra",
        "address": "Hindu Hrudaysamrat Balasaheb Thackeray Maharashtra Samruddhi Mahamarg, Maharashtra, India",
        "latitude": 20.3892,
        "longitude": 78.1307,
        "default_asset_type": "Road",
        "default_material": "Concrete",
        "default_traffic": "Moderate",
    },
    {
        "name": "Chennai Bypass Corridor",
        "city": "Chennai",
        "state": "Tamil Nadu",
        "address": "Chennai Bypass Road, Porur-Tambaram, Chennai, Tamil Nadu 600116, India",
        "latitude": 13.0475,
        "longitude": 80.1415,
        "default_asset_type": "Road",
        "default_material": "Asphalt",
        "default_traffic": "Heavy",
    },
    {
        "name": "Ahmedabad - Vadodara Expressway",
        "city": "Ahmedabad",
        "state": "Gujarat",
        "address": "National Expressway 1, Anand-Nadiad, Gujarat 387001, India",
        "latitude": 22.5645,
        "longitude": 72.9289,
        "default_asset_type": "Road",
        "default_material": "Asphalt",
        "default_traffic": "Heavy",
    },
]


def resolve_indian_zone(
    address: Optional[str] = None,
    state: Optional[str] = None,
    city: Optional[str] = None,
    latitude: Optional[float] = None,
    longitude: Optional[float] = None,
) -> str:
    """Resolves an Indian location to a model-compatible regional zone ('North', 'South', 'East', 'West', 'Central', 'Industrial').

    Strictly grounded in Indian geography.
    """
    # 1. Check state string
    if state:
        clean_state = state.strip().lower()
        if clean_state in STATE_TO_ZONE:
            return STATE_TO_ZONE[clean_state]
        for s_key, z_val in STATE_TO_ZONE.items():
            if s_key in clean_state:
                return z_val

    # 2. Check address string for state or city names
    if address:
        addr_lower = address.lower()
        if "industrial" in addr_lower or "midc" in addr_lower or "gic" in addr_lower or "sez" in addr_lower:
            return "Industrial"
        for s_key, z_val in STATE_TO_ZONE.items():
            if re.search(rf"\b{re.escape(s_key)}\b", addr_lower):
                return z_val

    # 3. Coordinate fallback based on geographic boundaries of India
    if latitude is not None and longitude is not None:
        if latitude > 24.5:
            return "North"
        if latitude < 16.0:
            return "South"
        if longitude < 76.5:
            return "West"
        if longitude > 83.5:
            return "East"
        return "Central"

    return "Central"


def get_regional_climate(zone: str) -> Dict[str, float]:
    """Retrieves typical annual rainfall (mm) and temperature (°C) for the zone."""
    return REGIONAL_CLIMATE.get(zone, {"annual_rainfall": 1200.0, "average_temperature": 26.5})


# Defensible Mappings for Simplified Inputs to Model Features
DEFAULT_MATERIALS = {
    "Road": "Asphalt",
    "Bridge": "Concrete",
    "Pipeline": "Steel",
    "Drainage": "Concrete",
    "Streetlight": "Steel",
    "Electrical Pole": "Concrete",
}

MEDIAN_ASSET_AGE = {
    "Road": 12.0,
    "Bridge": 25.0,
    "Pipeline": 18.0,
    "Drainage": 20.0,
    "Streetlight": 8.0,
    "Electrical Pole": 15.0,
}


def map_realistic_inputs_to_model_features(raw_input: Dict[str, Any]) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    """Converts user-friendly, realistic inputs into exact feature variables required by model_bundle.pkl.

    Returns:
        (transformed_model_record, metadata_explanation)
    """
    asset_type = raw_input.get("asset_type", "Road")
    if asset_type == "Water Pipeline":
        asset_type = "Pipeline"
    elif asset_type == "Drainage System":
        asset_type = "Drainage"

    # Location resolution
    loc = raw_input.get("location") or {}
    addr = loc.get("address") or raw_input.get("address") or "Pune, Maharashtra, India"
    state = loc.get("state") or raw_input.get("state")
    city = loc.get("city") or raw_input.get("city")
    lat = loc.get("latitude") if loc.get("latitude") is not None else raw_input.get("latitude")
    lng = loc.get("longitude") if loc.get("longitude") is not None else raw_input.get("longitude")

    resolved_zone = resolve_indian_zone(address=addr, state=state, city=city, latitude=lat, longitude=lng)
    climate = get_regional_climate(resolved_zone)

    # Material
    material = raw_input.get("material") or DEFAULT_MATERIALS.get(asset_type, "Concrete")

    # Age in years
    raw_age = raw_input.get("age_years")
    if raw_age is not None and str(raw_age).strip() != "" and float(raw_age) >= 0:
        age_years = float(raw_age)
    else:
        age_years = MEDIAN_ASSET_AGE.get(asset_type, 16.0)

    # Visible condition mapping: Good / Fair / Poor / Unknown
    cond = (raw_input.get("condition") or "Fair").strip().capitalize()
    if cond == "Good":
        structural_score = 85.0
        corrosion_level = 15.0
        previous_failures = 0
    elif cond == "Fair":
        structural_score = 60.0
        corrosion_level = 42.0
        previous_failures = 1
    elif cond == "Poor":
        structural_score = 35.0
        corrosion_level = 75.0
        previous_failures = 3
    else:  # Unknown
        structural_score = 63.5  # dataset median
        corrosion_level = 35.0  # dataset median
        previous_failures = 1

    # Traffic / Usage Level mapping: Low / Moderate / Heavy / Unknown
    traffic = (raw_input.get("traffic_level") or "Moderate").strip().capitalize()
    if traffic == "Low":
        traffic_density = 25.0
        usage_intensity = 30.0
        average_load = 45.0
    elif traffic == "Moderate":
        traffic_density = 55.0
        usage_intensity = 55.0
        average_load = 85.0
    elif traffic == "Heavy":
        traffic_density = 85.0
        usage_intensity = 85.0
        average_load = 140.0
    else:  # Unknown
        traffic_density = 50.0
        usage_intensity = 50.0
        average_load = 80.0

    # Maintenance Recency mapping: '< 1 year' / '1-3 years' / '> 3 years' / 'Unknown'
    recency = (raw_input.get("maintenance_recency") or "1-3 years").strip()
    if "< 1" in recency or "within" in recency.lower():
        days_since_maint = 120.0
        days_since_insp = 90.0
        maintenance_count = max(2.0, min(10.0, age_years / 3.0))
    elif "1-3" in recency:
        days_since_maint = 540.0
        days_since_insp = 360.0
        maintenance_count = max(1.0, min(8.0, age_years / 5.0))
    elif "> 3" in recency or "more" in recency.lower():
        days_since_maint = 1350.0
        days_since_insp = 900.0
        maintenance_count = max(0.0, min(4.0, age_years / 8.0))
    else:  # Unknown
        days_since_maint = 240.0
        days_since_insp = 210.0
        maintenance_count = max(1.0, min(6.0, age_years / 4.0))

    # Construct the exact model input record
    model_record = {
        "asset_id": raw_input.get("asset_id", f"IND-{asset_type[:3].upper()}-CORRIDOR"),
        "asset_type": asset_type,
        "zone": resolved_zone,
        "material": material,
        "age_years": age_years,
        "traffic_density": traffic_density,
        "average_load": average_load,
        "annual_rainfall": climate["annual_rainfall"],
        "average_temperature": climate["average_temperature"],
        "maintenance_count": round(maintenance_count),
        "days_since_maintenance": days_since_maint,
        "days_since_inspection": days_since_insp,
        "structural_score": structural_score,
        "corrosion_level": corrosion_level,
        "previous_failures": previous_failures,
        "usage_intensity": usage_intensity,
    }

    # Metadata record for frontends
    metadata = {
        "address": addr,
        "latitude": lat,
        "longitude": lng,
        "city": city,
        "state": state,
        "resolved_zone": resolved_zone,
        "climate_profile": climate,
        "condition_evaluated": cond,
        "traffic_evaluated": traffic,
        "recency_evaluated": recency,
        "derived_structural_score": structural_score,
        "derived_corrosion_level": corrosion_level,
        "observation_notes": raw_input.get("observation_notes"),
    }

    return model_record, metadata
