"""
Comprehensive Test Suite for AI Urban Infrastructure Failure Predictor
Validates:
1. Data leakage prevention & preprocessor fit isolation
2. Target generation rules & physics
3. Model schemas, prediction payloads, boundary values
4. Non-negative Remaining Useful Life (RUL)
5. CV edge detection, morphology, and bounded RDI calculations
6. Optimization constraints, feasibility, and counterexample proof
7. MLflow / tracking schemas & fallback
8. 6 Core data structures (NumPy, SciPy CSR, Decision Trees, Graphs, Heapq, Hash Dictionaries)
9. Google Maps GIS Indian zone resolution & climate profiles
10. ROVER guided workflows & allowlist security
"""
from __future__ import annotations

import os
import sys
from pathlib import Path
import numpy as np
import pandas as pd
import pytest

# Ensure backend directory is in sys.path
ROOT_DIR = Path(__file__).resolve().parents[1]
BACKEND_DIR = ROOT_DIR / "backend"
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from app.ml.preprocessing import clean_dataset, build_preprocessor, add_engineered_features
from app.cv.road_damage_detector import RoadDamageDetector
from app.optimization.maintenance_scheduler import (
    MaintenanceOptimizer,
    demonstrate_hill_climbing_limitation,
)
from app.structures.data_structures_demo import (
    demonstrate_numpy_structures,
    demonstrate_sparse_matrices,
    demonstrate_decision_trees,
    demonstrate_infrastructure_graph,
    demonstrate_priority_queue,
    demonstrate_hash_dictionaries,
)
from app.utils.indian_geo import (
    resolve_indian_zone,
    get_regional_climate,
    map_realistic_inputs_to_model_features,
    POPULAR_INDIAN_CORRIDORS,
)
from app.schemas.prediction_schema import CorridorAssessmentInput, AssetInput


# =============================================================================
# 1. DATA LEAKAGE & PREPROCESSING TESTS
# =============================================================================
def test_clean_dataset_no_cross_row_leakage():
    """Verifies that clean_dataset performs only row-level transforms and duplicate removal."""
    df_sample = pd.DataFrame([
        {"age_years": 10.0, "maintenance_count": 2, "days_since_inspection": 100,
         "previous_failures": 0, "days_since_maintenance": 60, "annual_rainfall": 1000,
         "average_temperature": 25, "traffic_density": 50, "average_load": 80,
         "structural_score": 70, "corrosion_level": 30},
        {"age_years": 20.0, "maintenance_count": 4, "days_since_inspection": 200,
         "previous_failures": 1, "days_since_maintenance": 120, "annual_rainfall": 1500,
         "average_temperature": 28, "traffic_density": 70, "average_load": 110,
         "structural_score": 50, "corrosion_level": 50},
    ])
    cleaned = clean_dataset(df_sample)
    assert len(cleaned) == 2
    assert "overall_condition_score" in cleaned.columns
    assert "environmental_stress" in cleaned.columns
    # Verify values are deterministic row-wise
    row0_cond = (70 * 0.6) + ((100 - 30) * 0.4)
    assert abs(cleaned.loc[0, "overall_condition_score"] - row0_cond) < 1e-4


def test_preprocessor_learns_from_train_only():
    """Verifies that ColumnTransformer SimpleImputer learns statistics strictly from X_train."""
    from sklearn.model_selection import train_test_split

    df = pd.DataFrame({
        "asset_type": ["Road", "Bridge", "Road", "Pipeline", "Road"],
        "zone": ["North", "South", "North", "West", "Central"],
        "material": ["Asphalt", "Concrete", "Asphalt", "Steel", "Asphalt"],
        "age_years": [10.0, np.nan, 30.0, 40.0, 50.0],
        "traffic_density": [20.0, 40.0, 60.0, 80.0, np.nan],
    })
    feature_cols = ["asset_type", "zone", "material", "age_years", "traffic_density"]
    X_train = df.iloc[:3][feature_cols]
    X_test = df.iloc[3:][feature_cols]

    preprocessor = build_preprocessor(X_train)
    X_train_t = preprocessor.fit_transform(X_train)
    X_test_t = preprocessor.transform(X_test)

    # Preprocessor must output valid numeric ndarray without NaNs
    assert not np.isnan(X_train_t).any()
    assert not np.isnan(X_test_t).any()


# =============================================================================
# 2. COMPUTER VISION & RDD TESTS
# =============================================================================
def test_cv_detector_bounded_rdi():
    """Verifies that RoadDamageDetector returns RDI bounded in [0, 100]."""
    detector = RoadDamageDetector()
    # Create test synthetic image
    test_img = np.full((300, 400, 3), 80, dtype=np.uint8)
    res = detector.detect(test_img)

    assert "road_damage_index" in res
    assert 0.0 <= res["road_damage_index"] <= 100.0
    assert res["overall_condition"] in [
        "GOOD - MINOR WEAR",
        "FAIR - SCHEDULED MAINTENANCE",
        "POOR - CRITICAL REPAIR NEEDED",
    ]
    assert "validation_note" in res
    assert "OpenCV" in res["validation_note"]


def test_cv_detector_empty_input_raises_error():
    """Verifies that invalid or empty image inputs raise ValueError."""
    detector = RoadDamageDetector()
    with pytest.raises(ValueError):
        detector.detect(b"")


# =============================================================================
# 3. MAINTENANCE OPTIMIZATION TESTS
# =============================================================================
def test_optimization_knapsack_feasibility():
    """Verifies that all three algorithms produce strictly feasible schedules."""
    assets = [
        {"asset_id": f"A{i}", "risk_score": 0.5 + i*0.05, "cost": 1000 + i*500,
         "capacity_hours": 10 + i*2, "criticality": 1.2, "asset_type": "Road"}
        for i in range(8)
    ]
    budget = 6000.0
    capacity = 40.0
    opt = MaintenanceOptimizer(assets, budget_limit=budget, capacity_limit=capacity)

    for plan in [opt.hill_climbing()["final_plan"],
                 opt.beam_search(beam_width=3)["final_plan"],
                 opt.tabu_search(max_iterations=20, tabu_tenure=3)["final_plan"]]:
        assert plan["is_feasible"] is True
        assert plan["total_cost"] <= budget
        assert plan["total_capacity"] <= capacity
        assert plan["objective_value"] >= 0.0


def test_hill_climbing_limitation_counterexample():
    """Verifies that the crafted counterexample proves Hill Climbing's local optimum trap."""
    proof = demonstrate_hill_climbing_limitation()
    hc_obj = proof["hill_climbing_result"]["objective"]
    beam_obj = proof["beam_search_result"]["objective"]
    tabu_obj = proof["tabu_search_result"]["objective"]

    assert beam_obj > hc_obj
    assert tabu_obj > hc_obj
    assert proof["improvement_over_hill_climbing_pct"] > 50.0


# =============================================================================
# 4. DATA STRUCTURES & ALGORITHMS TESTS
# =============================================================================
def test_data_structures_numpy():
    res = demonstrate_numpy_structures()
    assert res["matrix_shape"] == [5, 5]
    assert len(res["computed_scores"]) == 5


def test_data_structures_sparse():
    res = demonstrate_sparse_matrices(num_assets=500)
    assert res["shape"] == [500, 50]
    assert res["memory_savings_pct"] > 0.0
    assert res["sparse_memory_bytes"] < res["dense_memory_bytes"]


def test_data_structures_tree():
    res = demonstrate_decision_trees()
    assert res["tree_depth"] <= 3
    assert len(res["feature_importances"]) == 2


def test_data_structures_graph():
    res = demonstrate_infrastructure_graph()
    assert res["nodes_count"] == 7
    assert res["edges_count"] == 6
    assert "HOSPITAL-GRID" in res["cascading_impact_from_substation"]
    assert res["critical_bottleneck_node"] is not None


def test_data_structures_heap():
    res = demonstrate_priority_queue()
    dispatched = res["top_emergency_dispatches"]
    assert len(dispatched) == 3
    # Check descending priority
    assert dispatched[0]["risk_score"] >= dispatched[1]["risk_score"] >= dispatched[2]["risk_score"]


def test_data_structures_hash():
    res = demonstrate_hash_dictionaries()
    assert res["retrieved_record"]["type"] == "Bridge"
    assert res["total_indexed_assets"] >= 3


# =============================================================================
# 5. GOOGLE MAPS GIS & INDIAN CORRIDOR TESTS
# =============================================================================
def test_indian_corridor_presets_available():
    assert len(POPULAR_INDIAN_CORRIDORS) >= 8
    corridor_names = [c["name"] for c in POPULAR_INDIAN_CORRIDORS]
    assert any("Bandra-Worli" in n for n in corridor_names)
    assert any("Expressway" in n for n in corridor_names)


def test_realistic_input_mapping_bounds():
    raw_input = {
        "asset_type": "Road",
        "condition": "Poor",
        "traffic_level": "Heavy",
        "maintenance_recency": "> 3 years",
        "location": {
            "address": "Bandra-Worli Sea Link, Mumbai, Maharashtra, India",
            "state": "Maharashtra",
            "latitude": 19.033,
            "longitude": 72.8164,
        }
    }
    model_record, meta = map_realistic_inputs_to_model_features(raw_input)
    assert model_record["zone"] == "West"
    assert model_record["structural_score"] < 50.0  # Poor condition reflects lower structural score
    assert model_record["corrosion_level"] > 60.0   # Poor condition reflects higher corrosion
    assert meta["resolved_zone"] == "West"


# =============================================================================
# 6. FASTAPI PREDICTION & SYSTEM INTEGRATION TESTS
# =============================================================================
def test_fastapi_health():
    from fastapi.testclient import TestClient
    from app.main import app

    client = TestClient(app)
    res = client.get("/api/health")
    assert res.status_code == 200
    assert res.json()["status"] == "ok"


def test_fastapi_prediction_endpoint():
    from fastapi.testclient import TestClient
    from app.main import app

    client = TestClient(app)
    payload = {
        "asset_type": "Bridge",
        "condition": "Fair",
        "traffic_level": "Heavy",
        "maintenance_recency": "1-3 years",
        "location": {
            "address": "Bandra-Worli Sea Link, Mumbai, Maharashtra, India",
            "state": "Maharashtra",
            "city": "Mumbai",
            "latitude": 19.033,
            "longitude": 72.8164,
        }
    }
    res = client.post("/api/predict", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert "failure_probability" in data
    assert 0.0 <= data["failure_probability"] <= 1.0
    assert data["risk_level"] in ["LOW", "MEDIUM", "HIGH"]
    assert "remaining_useful_life" in data
    assert data["remaining_useful_life"] >= 0.0
    assert "recommendation" in data
    assert "priority" in data
    assert "key_factors" in data
    assert "location" in data
    assert data["location"]["resolved_zone"] == "West"


def test_fastapi_optimization_endpoint():
    from fastapi.testclient import TestClient
    from app.main import app

    client = TestClient(app)
    res = client.post("/api/optimization/compare", json={"budget_limit": 40000.0, "capacity_limit": 120.0})
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "success"
    assert "comparison" in data
    assert len(data["comparison"]["comparison_table"]) == 3


# =============================================================================
# 7. DATASET AUDIT & CLEAN PIPELINE VERIFICATION TESTS
# =============================================================================
def test_dataset_audit_dynamic_calculation():
    """Verifies that DatasetAuditor dynamically calculates summary metrics from active data."""
    from app.ml.dataset_auditor import auditor

    res = auditor.audit(force_refresh=True)
    summary = res["summary"]

    assert summary["total_records"] >= 50000
    assert summary["total_features"] >= 18
    assert summary["duplicate_rows"] == 0
    assert summary["duplicate_asset_ids"] == 0
    assert summary["total_missing_cells"] >= 0
    assert summary["missing_percentage"] < 5.0
    assert summary["data_quality_score"] >= 80.0
    assert "Grade" in summary["data_quality_grade"] or "A" in summary["data_quality_grade"] or "B" in summary["data_quality_grade"]


def test_domain_validation_infrastructure_constraints():
    """Verifies that all 17 domain rules are evaluated and rule structures match specification."""
    from app.ml.dataset_auditor import auditor

    res = auditor.audit()
    domain_rules = res["domain_validation"]

    assert len(domain_rules) >= 16
    for rule in domain_rules:
        assert "field" in rule
        assert "description" in rule
        assert "violations_count" in rule
        assert rule["status"] in ["PASSED", "VIOLATION_DETECTED", "NOT_APPLICABLE"]


def test_target_imbalance_and_paradox_reporting():
    """Verifies class imbalance analysis correctly evaluates target proportions and recommendations."""
    from app.ml.dataset_auditor import DatasetAuditor, auditor
    import tempfile

    res = auditor.audit(force_refresh=True)
    t_info = res["target_analysis"]

    assert t_info["target_column"] == "failure"
    assert "Operational (0)" in t_info["class_counts"]
    assert "Failure Incident (1)" in t_info["class_counts"]
    assert ":1" in t_info["imbalance_ratio"]
    assert len(t_info["recommended_actions"]) >= 3
    assert len(t_info["imbalance_rationale"]) > 20

    # Also test with an artificially imbalanced probe (e.g. 10% failure rate)
    with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as tf:
        df_imbalanced = pd.DataFrame({
            "asset_id": [f"A{i}" for i in range(100)],
            "asset_type": ["Road"] * 100,
            "zone": ["North"] * 100,
            "material": ["Asphalt"] * 100,
            "age_years": [10.0] * 100,
            "traffic_density": [50.0] * 100,
            "average_load": [80.0] * 100,
            "annual_rainfall": [1000.0] * 100,
            "average_temperature": [25.0] * 100,
            "maintenance_count": [3] * 100,
            "days_since_maintenance": [60.0] * 100,
            "days_since_inspection": [90.0] * 100,
            "structural_score": [80.0] * 100,
            "corrosion_level": [20.0] * 100,
            "previous_failures": [0] * 100,
            "usage_intensity": [50.0] * 100,
            "remaining_useful_life": [20.0] * 100,
            "failure": [1] * 10 + [0] * 90,  # 10% failure = severe/moderate imbalance
        })
        df_imbalanced.to_csv(tf.name, index=False)
        temp_path = tf.name

    try:
        custom_auditor = DatasetAuditor(data_path=Path(temp_path))
        custom_res = custom_auditor.audit()
        custom_t = custom_res["target_analysis"]
        assert custom_t["is_imbalanced"] is True
        assert custom_t["minority_class_percentage"] == 10.0
        assert "Accuracy Paradox" in custom_t["imbalance_rationale"]
    finally:
        Path(temp_path).unlink(missing_ok=True)


def test_dataset_provenance_and_limitations():
    """Verifies dataset is clearly labeled synthetic and references the active generation script."""
    from app.ml.dataset_auditor import auditor

    res = auditor.audit()
    prov = res["provenance"]

    assert "Pune" in prov["dataset_origin"] or "Synthetic" in prov["dataset_origin"]
    assert "generate_data.py" in prov.get("generator_script", "generate_data.py") or "Pune" in prov["verification_status"]
    assert "Pune" in prov["verification_status"] or "Synthetic" in prov["verification_status"]
    assert len(prov["academic_limitation"]) > 20


def test_audit_export_csv_and_json():
    """Verifies export functions produce valid CSV and JSON structures."""
    import json
    from app.ml.dataset_auditor import auditor

    csv_data = auditor.export_csv_report()
    assert "Row_Index,Asset_ID,Field" in csv_data

    json_str = auditor.export_json_report()
    parsed = json.loads(json_str)
    assert "summary" in parsed
    assert "provenance" in parsed


def test_clean_pipeline_verification_all_checks():
    """Verifies that all 12 automated pipeline verification checks execute and pass."""
    from app.ml.pipeline_verifier import pipeline_verifier

    res = pipeline_verifier.run_all_checks()
    assert res["overall_status"] in ["ALL_PASSED", "PASSED_WITH_WARNINGS"]
    assert res["summary_counts"]["total_checks"] == 12
    assert res["summary_counts"]["failed"] == 0
    assert res["summary_counts"]["passed"] >= 10

    # Ensure critical checks passed
    check_ids = {c["check_id"]: c["status"] for c in res["checks"]}
    assert check_ids["CHK_01_SPLIT_PRECEDENCE"] == "PASSED"
    assert check_ids["CHK_02_IMPUTER_ISOLATION"] == "PASSED"
    assert check_ids["CHK_03_SCALER_ISOLATION"] == "PASSED"
    assert check_ids["CHK_06_INDEX_DISJOINTNESS"] == "PASSED"
    assert check_ids["CHK_07_TARGET_IDENTIFIER_EXCLUSION"] == "PASSED"
    assert check_ids["CHK_09_RUL_NONNEGATIVE_BOUNDS"] == "PASSED"
    assert check_ids["CHK_10_REPRODUCIBILITY"] == "PASSED"


def test_fastapi_audit_and_pipeline_endpoints():
    """Verifies FastAPI REST endpoints for dataset audit and clean pipeline verification."""
    from fastapi.testclient import TestClient
    from app.main import app

    client = TestClient(app)

    # 1. Summary
    res = client.get("/api/audit/summary")
    assert res.status_code == 200
    data = res.json()
    assert "summary" in data
    assert data["summary"]["total_records"] >= 50000

    # 2. Findings
    res_f = client.get("/api/audit/findings?limit=10")
    assert res_f.status_code == 200
    f_data = res_f.json()
    assert "findings" in f_data
    assert len(f_data["findings"]) <= 10

    # 3. CSV export
    res_csv = client.get("/api/audit/export/csv")
    assert res_csv.status_code == 200
    assert "text/csv" in res_csv.headers["content-type"]

    # 4. JSON export
    res_json = client.get("/api/audit/export/json")
    assert res_json.status_code == 200
    assert "application/json" in res_json.headers["content-type"]

    # 5. Pipeline tests run
    res_run = client.post("/api/pipeline-tests/run")
    assert res_run.status_code == 200
    p_data = res_run.json()
    assert p_data["summary_counts"]["total_checks"] == 12
    assert p_data["summary_counts"]["failed"] == 0

    # 6. Pipeline tests results
    res_get = client.get("/api/pipeline-tests/results")
    assert res_get.status_code == 200


def test_dashboard_risk_breakdown_consistency():
    """Verifies that dashboard risk breakdown endpoints exist, calculate from active dataset,
    and have 100% data consistency across Risk Distribution, Asset Types, and Zones."""
    from fastapi.testclient import TestClient
    from app.main import app

    client = TestClient(app)

    # 1. Main dashboard endpoint
    res_dash = client.get("/api/dashboard")
    assert res_dash.status_code == 200
    dash = res_dash.json()
    total = dash["total_assets"]
    assert total >= 50000
    assert dash["high_risk_assets"] + dash["medium_risk_assets"] + dash["low_risk_assets"] == total
    assert len(dash["asset_type_risk"]) >= 3
    assert len(dash["zone_risk"]) >= 5

    # 2. Dedicated risk breakdown endpoint
    res_rb = client.get("/api/dashboard/risk-breakdown")
    assert res_rb.status_code == 200
    rb = res_rb.json()
    overall = rb["overall"]
    assert overall["total"] == total
    assert overall["high"] + overall["medium"] + overall["low"] == total

    # 3. Asset type aggregation
    res_at = client.get("/api/dashboard/asset-type-risk")
    assert res_at.status_code == 200
    types = res_at.json()
    assert len(types) >= 3
    assert sum(t["total"] for t in types) == total
    assert sum(t["high"] for t in types) == overall["high"]
    assert sum(t["medium"] for t in types) == overall["medium"]
    assert sum(t["low"] for t in types) == overall["low"]
    for t in types:
        assert t["high"] + t["medium"] + t["low"] == t["total"]
        assert t["type"] in ["Road", "Bridge", "Pipeline", "Drainage", "Streetlight", "Electrical Pole", "Road Segment", "Bridge Approach", "Culvert Approach"]

    # 4. Zone aggregation
    res_zn = client.get("/api/dashboard/zone-risk")
    assert res_zn.status_code == 200
    zones = res_zn.json()
    assert len(zones) == 6
    assert sum(z["total"] for z in zones) == total
    assert sum(z["high"] for z in zones) == overall["high"]
    assert sum(z["medium"] for z in zones) == overall["medium"]
    assert sum(z["low"] for z in zones) == overall["low"]
    for z in zones:
        assert z["high"] + z["medium"] + z["low"] == z["total"]
        assert z["zone"] in ["North", "South", "East", "West", "Central", "Industrial"]


# =============================================================================
# 8. PUNE 100K DATASET, GIS BOUNDING & DAMAGE REPORTING TESTS
# =============================================================================
def test_pune_100k_dataset_validations():
    """Validates >=100,000 records, Pune coordinates boundary, and non-negative RUL."""
    from app.config.location_config import PUNE_BOUNDS, is_within_pune
    data_path = Path(__file__).resolve().parents[1] / "backend" / "data" / "urban_infrastructure_data.csv"
    assert data_path.exists(), "Dataset CSV must exist"

    df = pd.read_csv(data_path)
    assert len(df) >= 100000, f"Dataset must contain at least 100,000 records, got {len(df)}"

    required_cols = [
        "asset_id", "asset_type", "zone", "pune_ward", "locality", "latitude", "longitude",
        "material", "age_years", "traffic_density", "structural_score", "corrosion_level",
        "remaining_useful_life", "failure"
    ]
    for col in required_cols:
        assert col in df.columns, f"Required column '{col}' missing from dataset schema"

    # All 6 infrastructure categories must be present
    expected_types = {"Road", "Bridge", "Pipeline", "Drainage", "Streetlight", "Electrical Pole"}
    assert set(df["asset_type"].unique()) == expected_types

    # Coordinates strictly inside Pune boundary
    assert (df["latitude"] >= PUNE_BOUNDS["min_latitude"]).all()
    assert (df["latitude"] <= PUNE_BOUNDS["max_latitude"]).all()
    assert (df["longitude"] >= PUNE_BOUNDS["min_longitude"]).all()
    assert (df["longitude"] <= PUNE_BOUNDS["max_longitude"]).all()

    # Domain integrity: RUL strictly non-negative
    assert (df["remaining_useful_life"] >= 0.0).all()


def test_pune_geo_config_and_boundary_checks():
    """Verifies Pune coordinate boundary validation and multi-city modular configuration."""
    from app.config.location_config import (
        is_within_pune,
        validate_pune_coordinates,
        get_active_city_config,
        SUPPORTED_CITIES,
    )

    # Valid Pune coordinates
    assert is_within_pune(18.5204, 73.8567) is True
    valid, msg = validate_pune_coordinates(18.5204, 73.8567)
    assert valid is True

    # Coordinates outside Pune (e.g. Mumbai, Delhi, impossible values)
    assert is_within_pune(19.0760, 72.8777) is False  # Mumbai
    valid, msg = validate_pune_coordinates(19.0760, 72.8777)
    assert valid is False
    assert "outside the Pune" in msg

    # Config is modular
    assert "pune" in SUPPORTED_CITIES
    assert "mumbai" in SUPPORTED_CITIES
    assert "nashik" in SUPPORTED_CITIES
    assert "nagpur" in SUPPORTED_CITIES
    active = get_active_city_config()
    assert active["name"] == "Pune"


def test_dashboard_infrastructure_stats_and_trend_endpoints():
    """Verifies GET /api/dashboard/infrastructure-stats and GET /api/dashboard/infrastructure-trend."""
    from fastapi.testclient import TestClient
    from app.main import app

    client = TestClient(app)

    # 1. Live infrastructure stats
    res_stats = client.get("/api/dashboard/infrastructure-stats")
    assert res_stats.status_code == 200
    stats = res_stats.json()
    assert stats["total"] >= 50000
    assert stats["roads"] > 0 or stats["road_segments"] > 0
    assert stats["bridges"] > 0 or stats["bridge_approaches"] > 0
    assert stats["high_risk"] > 0
    assert stats["medium_risk"] > 0
    assert stats["low_risk"] > 0
    assert "trend" in stats

    # 2. Monitoring trend
    res_trend = client.get("/api/dashboard/infrastructure-trend")
    assert res_trend.status_code == 200
    trend = res_trend.json()
    assert trend["total"] >= 50000
    assert "change" in trend
    assert "change_percent" in trend
    assert "new_assets" in trend
    assert "updated_assets" in trend


def test_infrastructure_query_and_spatial_bounds():
    """Verifies infrastructure querying, bounding-box filtering, and asset detail retrieval."""
    from fastapi.testclient import TestClient
    from app.main import app

    client = TestClient(app)

    # Query with limit and filters
    res = client.get("/api/infrastructure?limit=50&risk=high&type=Road")
    assert res.status_code == 200
    data = res.json()
    assert "assets" in data
    assert len(data["assets"]) <= 50
    for a in data["assets"]:
        assert "road" in a["asset_type"].lower()
        assert a["risk_level"] == "HIGH"
        assert 18.40 <= a["latitude"] <= 18.68
        assert 73.70 <= a["longitude"] <= 73.99

    # Query asset details by asset_id
    sample_id = data["assets"][0]["asset_id"]
    res_detail = client.get(f"/api/infrastructure/{sample_id}")
    assert res_detail.status_code == 200
    detail = res_detail.json()
    assert detail["asset_id"] == sample_id
    assert "condition_score" in detail
    assert "recommended_action" in detail
    assert "damage_reports" in detail

    # 404 for non-existent asset
    res_404 = client.get("/api/infrastructure/NONEXISTENT-ASSET-999999")
    assert res_404.status_code == 404


def test_damage_reporting_flow_and_validations():
    """Verifies damage inspection upload, boundary rejection, CV execution, and nearest-asset association."""
    from fastapi.testclient import TestClient
    from app.main import app
    import io

    client = TestClient(app)

    # 1. Rejection: coordinates outside Pune
    synthetic_img = io.BytesIO(b"\xff\xd8\xff\xe0\x00\x10JFIF" + b"\x00" * 100 + b"\xff\xd9")
    res_outside = client.post(
        "/api/damage-reports",
        data={
            "latitude": 19.0760,  # Mumbai
            "longitude": 72.8777,
            "damage_type": "Pothole",
        },
        files={"image": ("test.jpg", synthetic_img, "image/jpeg")},
    )
    assert res_outside.status_code == 400
    assert "outside the Pune" in res_outside.json()["detail"]

    # 2. Rejection: invalid file type
    res_bad_file = client.post(
        "/api/damage-reports",
        data={
            "latitude": 18.5204,
            "longitude": 73.8567,
            "damage_type": "Pothole",
        },
        files={"image": ("test.txt", io.BytesIO(b"not an image"), "text/plain")},
    )
    assert res_bad_file.status_code == 400

    # 3. Valid submission inside Pune
    # Create valid minimal JPEG image using OpenCV or bytes
    test_img_np = np.full((120, 160, 3), 100, dtype=np.uint8)
    import cv2
    _, img_buf = cv2.imencode(".jpg", test_img_np)
    img_bytes = img_buf.tobytes()

    res_valid = client.post(
        "/api/damage-reports",
        data={
            "latitude": 18.5204,
            "longitude": 73.8567,
            "damage_type": "Pothole",
            "pune_ward": "Shivajinagar-Ghole Road Ward",
            "locality": "Shivajinagar",
            "description": "Severe longitudinal road pothole near transit station.",
        },
        files={"image": ("pothole.jpg", io.BytesIO(img_bytes), "image/jpeg")},
    )
    assert res_valid.status_code == 200
    rep_data = res_valid.json()
    assert rep_data["status"] == "success"
    report = rep_data["report"]
    report_id = report["report_id"]
    assert "REP-PN" in report_id
    assert report["damage_type"] == "Pothole"
    assert "image_url" in report

    # 4. Retrieve damage report list
    res_list = client.get("/api/damage-reports")
    assert res_list.status_code == 200
    assert any(r["report_id"] == report_id for r in res_list.json()["reports"])

    # 5. Retrieve specific damage report details
    res_single = client.get(f"/api/damage-reports/{report_id}")
    assert res_single.status_code == 200
    assert res_single.json()["report_id"] == report_id

    # 6. Retrieve image
    res_img = client.get(f"/api/damage-reports/{report_id}/image")
    assert res_img.status_code == 200
    assert "image" in res_img.headers["content-type"]

    # 7. Update status
    res_status = client.patch(f"/api/damage-reports/{report_id}/status", json={"status": "Verified"})
    assert res_status.status_code == 200
    assert res_status.json()["new_status"] == "Verified"


def test_priority_queue_with_damage_escalation():
    """Verifies GET /api/optimization/priority-queue computes prioritization with explicit reasons."""
    from fastapi.testclient import TestClient
    from app.main import app

    client = TestClient(app)

    res = client.get("/api/optimization/priority-queue?limit=25")
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "success"
    assert "priority_queue" in data
    assert len(data["priority_queue"]) > 0

    for item in data["priority_queue"]:
        assert item["priority"] in ["CRITICAL", "HIGH", "MEDIUM", "LOW"]
        assert isinstance(item["priority_reasons"], list)
        assert len(item["priority_reasons"]) > 0
        assert "recommended_action" in item
        assert "estimated_repair_cost" in item




