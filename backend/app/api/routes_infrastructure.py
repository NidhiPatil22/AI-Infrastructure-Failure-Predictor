from __future__ import annotations

from typing import Any, Dict, List, Optional
from fastapi import APIRouter, HTTPException, Query

from app.config.location_config import PUNE_BOUNDS, PUNE_CENTER, PUNE_ZONES, get_active_city_config
from app.database.database import (
    get_asset_by_id,
    query_infrastructure_assets,
)

router = APIRouter()


@router.get('/infrastructure')
def get_infrastructure_assets(
    limit: int = Query(default=100, ge=1, le=2500),
    offset: int = Query(default=0, ge=0),
    risk: Optional[str] = Query(default=None),
    type: Optional[str] = Query(default=None),
    zone: Optional[str] = Query(default=None),
    ward: Optional[str] = Query(default=None),
    min_lat: Optional[float] = Query(default=None),
    max_lat: Optional[float] = Query(default=None),
    min_lng: Optional[float] = Query(default=None),
    max_lng: Optional[float] = Query(default=None),
    search: Optional[str] = Query(default=None),
):
    """Queries monitored infrastructure assets in Pune with spatial bounds,

    multi-attribute filtering, and high-performance pagination.
    """
    res = query_infrastructure_assets(
        limit=limit,
        offset=offset,
        risk=risk,
        asset_type=type,
        zone=zone,
        ward=ward,
        min_lat=min_lat,
        max_lat=max_lat,
        min_lng=min_lng,
        max_lng=max_lng,
        search=search,
    )
    return res


@router.get('/infrastructure/config')
def get_infrastructure_geo_config():
    """Returns active city geographic configuration, monitoring boundaries, and Pune zones."""
    return {
        "status": "success",
        "active_city": get_active_city_config(),
        "pune_bounds": PUNE_BOUNDS,
        "pune_center": PUNE_CENTER,
        "pune_zones": PUNE_ZONES,
    }


@router.get('/infrastructure/{asset_id}')
def get_infrastructure_asset_detail(asset_id: str):
    """Retrieves comprehensive monitoring diagnostic details for an asset,

    including sensor metrics, AI predictions, and linked field damage inspection reports.
    """
    asset = get_asset_by_id(asset_id.strip())
    if not asset:
        raise HTTPException(status_code=404, detail=f"Infrastructure asset '{asset_id}' not found.")
    return asset
