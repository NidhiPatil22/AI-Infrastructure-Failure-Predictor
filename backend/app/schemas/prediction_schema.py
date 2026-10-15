from __future__ import annotations

from typing import Optional, Union
from pydantic import BaseModel, Field


class LocationData(BaseModel):
    """Real-world location coordinates and address metadata."""
    address: str = Field(..., description="Full human-readable address or landmark name")
    latitude: Optional[float] = Field(None, description="Geographic latitude coordinate")
    longitude: Optional[float] = Field(None, description="Geographic longitude coordinate")
    city: Optional[str] = Field(None, description="City name (e.g. Pune, Mumbai, Bengaluru)")
    state: Optional[str] = Field(None, description="State name (e.g. Maharashtra, Karnataka)")
    postal_code: Optional[str] = Field(None, description="Postal / PIN code")
    place_id: Optional[str] = Field(None, description="Google Maps Place ID if available")


class CorridorAssessmentInput(BaseModel):
    """Simplified, realistic user-facing infrastructure assessment schema.

    Replaces unrealistic numerical percentages with observable civil engineering parameters.
    """
    location: Optional[LocationData] = Field(None, description="Selected geographical location in India")
    asset_type: str = Field("Road", description="Asset type (Road, Bridge, Pipeline, Drainage, Streetlight, Electrical Pole)")
    age_years: Optional[float] = Field(None, ge=0, le=100, description="Approximate age in years (or null if unknown)")
    condition: str = Field("Fair", description="Visible physical condition: Good, Fair, Poor, or Unknown")
    traffic_level: str = Field("Moderate", description="Traffic/usage level: Low, Moderate, Heavy, or Unknown")
    maintenance_recency: str = Field("1-3 years", description="Maintenance recency: '< 1 year', '1-3 years', '> 3 years', or 'Unknown'")
    material: Optional[str] = Field(None, description="Primary structural material (Asphalt, Concrete, Steel, etc.)")
    observation_notes: Optional[str] = Field(None, description="Optional engineering inspection notes")


class AssetInput(BaseModel):
    """Legacy 15-field technical sensor schema preserved for full backward compatibility."""
    asset_type: str = Field(..., description="Infrastructure asset type")
    zone: str = Field("Central", description="Zone where the asset is located")
    age_years: float = Field(..., ge=0, le=100)
    material: str = Field("Concrete", description="Material used in the asset")
    traffic_density: float = Field(50.0, ge=0, le=100)
    average_load: float = Field(80.0, ge=0, le=200)
    annual_rainfall: float = Field(1200.0, ge=0, le=5000)
    average_temperature: float = Field(25.0, ge=-50, le=60)
    maintenance_count: float = Field(3.0, ge=0, le=50)
    days_since_maintenance: float = Field(180.0, ge=0, le=5000)
    days_since_inspection: float = Field(180.0, ge=0, le=5000)
    structural_score: float = Field(65.0, ge=0, le=100)
    corrosion_level: float = Field(35.0, ge=0, le=100)
    previous_failures: int = Field(1, ge=0, le=50)
    usage_intensity: float = Field(50.0, ge=0, le=100)
    location: Optional[LocationData] = None


class BatchRequest(BaseModel):
    records: list[Union[CorridorAssessmentInput, AssetInput]] = []
