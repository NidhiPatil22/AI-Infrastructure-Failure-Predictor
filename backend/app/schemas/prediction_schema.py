from pydantic import BaseModel, Field


class AssetInput(BaseModel):
    asset_type: str = Field(..., description='Infrastructure asset type')
    zone: str = Field(..., description='Zone where the asset is located')
    age_years: float = Field(..., ge=0, le=100)
    material: str = Field(..., description='Material used in the asset')
    traffic_density: float = Field(..., ge=0, le=100)
    average_load: float = Field(..., ge=0, le=200)
    annual_rainfall: float = Field(..., ge=0, le=5000)
    average_temperature: float = Field(..., ge=-50, le=60)
    maintenance_count: float = Field(..., ge=0, le=50)
    days_since_maintenance: float = Field(..., ge=0, le=5000)
    days_since_inspection: float = Field(..., ge=0, le=5000)
    structural_score: float = Field(..., ge=0, le=100)
    corrosion_level: float = Field(..., ge=0, le=100)
    previous_failures: int = Field(..., ge=0, le=50)
    usage_intensity: float = Field(..., ge=0, le=100)


class BatchRequest(BaseModel):
    records: list[AssetInput] = []
