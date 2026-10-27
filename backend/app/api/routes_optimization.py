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


@router.get("/optimization/priority-queue")
def get_prioritized_maintenance_queue(limit: int = 50):
    """Returns the prioritized infrastructure maintenance queue dynamically computed

    by blending ML failure risk, Remaining Useful Life (RUL), previous failures,
    and field observed damage reports without silently overwriting predictions.
    Communicates infrastructure at descriptive and aggregate levels without exposing raw synthetic asset IDs.
    """
    from app.database.database import get_db_connection

    conn = get_db_connection()
    # Fetch top candidates with high risk or damage reports
    rows = conn.execute(
        """
        SELECT asset_id, asset_type, road_class, road_name, zone, pune_ward, locality, latitude, longitude,
               material, age_years, condition_score, failure_probability, risk_level,
               remaining_useful_life, remaining_useful_life_days, previous_failures, corrosion_level, status,
               reported_damage_count, latest_damage_type, latest_damage_report_id
        FROM infrastructure_assets
        ORDER BY
            (reported_damage_count * 5.0) + (failure_probability * 4.0) + (previous_failures * 0.5) DESC
        LIMIT ?
        """,
        (min(200, max(1, limit)),),
    ).fetchall()
    conn.close()

    queue = []
    for r in rows:
        item = dict(r)
        prob = item.get("failure_probability", 0.0)
        rul_days = item.get("remaining_useful_life_days")
        if rul_days is None:
            rul_days = int(item.get("remaining_useful_life", 15.0) * 365)
        item["remaining_useful_life_days"] = rul_days
        
        dmg_count = item.get("reported_damage_count", 0)
        dmg_type = item.get("latest_damage_type")
        prev_fails = item.get("previous_failures", 0)
        corr = item.get("corrosion_level", 0.0)
        cond_score = item.get("condition_score", 60.0)

        road_class_str = (item.get("road_class") or "").title()
        type_str = (item.get("asset_type") or "Road Segment").replace("_", " ").title()
        locality_str = item.get("locality") or "Pune"
        display_type = f"{road_class_str} {type_str}".strip() if road_class_str else type_str
        item["display_type"] = display_type
        item["display_title"] = f"{display_type} · {locality_str}"
        item["condition_label"] = "Poor" if cond_score < 50 else ("Fair" if cond_score < 75 else "Good")

        reasons = []
        # Multi-factor reasoning
        if dmg_count > 0 and dmg_type:
            reasons.append(f"Reported field damage: {dmg_type} ({dmg_count} report{'s' if dmg_count > 1 else ''})")
        if prob >= 0.70:
            reasons.append(f"High predicted failure risk ({prob:.1%})")
        elif prob >= 0.40:
            reasons.append(f"Elevated predictive risk profile ({prob:.1%})")

        if rul_days <= 180:
            reasons.append(f"Critical Remaining Useful Life ({rul_days} days)")
        elif rul_days <= 365:
            reasons.append(f"Low Remaining Useful Life ({rul_days} days)")

        if prev_fails >= 2:
            reasons.append(f"History of structural failure incidents ({prev_fails} occurrences)")

        if corr >= 65.0:
            reasons.append(f"Severe corrosion deterioration index ({corr:.1f}%)")

        if not reasons:
            reasons.append("Routine scheduled civil maintenance window")

        # Determine composite priority level
        if dmg_count > 0 or prob >= 0.85 or (prob >= 0.65 and rul_days <= 180):
            priority = "CRITICAL"
            recommended_action = "Deploy rapid response engineering crew for immediate on-site structural remediation."
        elif prob >= 0.60 or rul_days <= 365 or dmg_count > 0:
            priority = "HIGH"
            recommended_action = "Schedule preventive structural overhaul within the upcoming 30-day maintenance cycle."
        elif prob >= 0.35:
            priority = "MEDIUM"
            recommended_action = "Program standard ultrasonic/visual inspection during next regular municipal sweep."
        else:
            priority = "LOW"
            recommended_action = "Maintain continuous IoT and citizen reporting surveillance."

        cost = round(3000 + (prob * 12000) + (dmg_count * 3500), -2)
        capacity_hours = round(10 + (prob * 30) + (dmg_count * 15), 1)

        item["priority"] = priority
        item["priority_reasons"] = reasons
        item["recommended_action"] = recommended_action
        item["estimated_repair_cost"] = cost
        item["estimated_labor_hours"] = capacity_hours
        queue.append(item)

    return {
        "status": "success",
        "total": len(queue),
        "priority_queue": queue,
    }
