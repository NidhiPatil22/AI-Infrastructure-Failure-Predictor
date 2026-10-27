"""
Re-export of Pune location configuration for root backend access.
"""
from app.config.location_config import (
    ACTIVE_CITY_KEY,
    PUNE_BOUNDS,
    PUNE_CENTER,
    PUNE_ZONES,
    SUPPORTED_CITIES,
    get_active_city_config,
    is_within_pune,
    validate_pune_coordinates,
)

__all__ = [
    "ACTIVE_CITY_KEY",
    "PUNE_BOUNDS",
    "PUNE_CENTER",
    "PUNE_ZONES",
    "SUPPORTED_CITIES",
    "get_active_city_config",
    "is_within_pune",
    "validate_pune_coordinates",
]
