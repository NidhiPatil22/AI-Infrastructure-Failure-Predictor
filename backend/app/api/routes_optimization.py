"""FastAPI endpoints for Search Space Maintenance Optimization."""
from __future__ import annotations

from typing import Any, Dict, List, Optional
from fastapi import APIRouter
from pydantic import BaseModel, Field

from app.optimization.maintenance_scheduler import (
    MaintenanceOptimizer,
    demonstrate_hill_climbing_limitation,
    run_optimization_comparison,
)

router = APIRouter(tags=["Optimization"])


class AssetOptimizationItem(BaseModel):
    asset_id: str
    asset_type: str = "Road"
    risk_score: float = Field(..., ge=0.0, le=1.0)
    cost: float = Field(..., gt=0.0)
    capacity_hours: float = Field(..., gt=0.0)
    criticality: float = Field(default=1.0, gt=0.0)


class OptimizationRequest(BaseModel):
    budget_limit: float = Field(default=50000.0, gt=0.0)
    capacity_limit: float = Field(default=160.0, gt=0.0)
    assets: Optional[List[AssetOptimizationItem]] = None


@router.post("/optimization/compare")
async def compare_optimization_algorithms(req: OptimizationRequest):
    """Executes Hill Climbing, Beam Search, and Tabu Search on assets."""
    if req.assets and len(req.assets) > 0:
        asset_list = [a.model_dump() for a in req.assets]
    else:
        # Default representative municipal asset portfolio
        asset_list = [
            {"asset_id": f"ASSET-{i:03d}", "asset_type": at, "risk_score": round(r, 2), "cost": c, "capacity_hours": h, "criticality": crit}
            for i, (at, r, c, h, crit) in enumerate([
                ("Bridge", 0.92, 14000, 40, 1.5),
                ("Water Pipeline", 0.85, 9500, 28, 1.4),
                ("Road Corridor", 0.78, 8200, 24, 1.2),
                ("Drainage Culvert", 0.71, 6000, 18, 1.1),
                ("Electrical Substation", 0.88, 12500, 35, 1.5),
                ("Road Pothole Zone", 0.65, 4500, 14, 1.0),
                ("Power Line Feeder", 0.74, 7800, 22, 1.3),
                ("Traffic Signal Grid", 0.52, 3200, 10, 0.9),
                ("Streetlight Bank", 0.44, 2100, 8, 0.8),
                ("Water Main Valve", 0.68, 5400, 16, 1.2),
            ], start=1)
        ]

    comparison_results = run_optimization_comparison(
        assets=asset_list,
        budget_limit=req.budget_limit,
        capacity_limit=req.capacity_limit,
    )
    return {
        "status": "success",
        "budget_limit": req.budget_limit,
        "capacity_limit": req.capacity_limit,
        "comparison": comparison_results,
    }


@router.get("/optimization/hill-climbing-limitation")
async def get_hill_climbing_limitation():
    """Returns the concrete counterexample demonstrating Hill Climbing local-optimum trapping."""
    return {
        "status": "success",
        "limitation_proof": demonstrate_hill_climbing_limitation(),
    }
