"""Automated unit and integration tests for the ROVER AI Assistant backend."""
import os
import sys
from pathlib import Path

# Add backend directory to path
backend_dir = Path(__file__).resolve().parents[1]
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))

from app.ai.chat_service import chat_service
from app.ai.llm_provider import GeminiProvider, GrokProvider, LLMConfigurationError, get_llm_provider
from app.ai.project_context import build_system_prompt
from app.ai.workflow_engine import (
    workflow_engine,
    get_initial_choices,
    ALLOWLISTED_ACTIONS,
    MAIN_MENU_CHOICES,
)


def test_system_prompt():
    prompt = build_system_prompt(live_status={"total_assets": 2200, "high_risk_assets": 348})
    assert "ROVER" in prompt
    assert "Bridges" in prompt
    assert "Roads" in prompt
    assert "2200" in prompt
    print("PASS: System prompt generation verified.")


def test_provider_status_unconfigured():
    # Save original env
    orig_gemini = os.environ.get("GEMINI_API_KEY")
    orig_xai = os.environ.get("XAI_API_KEY")

    try:
        os.environ.pop("GEMINI_API_KEY", None)
        os.environ.pop("XAI_API_KEY", None)

        status_gemini = chat_service.get_status("gemini")
        assert status_gemini["configured"] is False
        assert status_gemini["status"] == "unconfigured"
        assert "GEMINI_API_KEY" in status_gemini["message"]

        status_grok = chat_service.get_status("grok")
        assert status_grok["configured"] is False
        assert status_grok["status"] == "unconfigured"
        assert "XAI_API_KEY" in status_grok["message"]
        print("PASS: Unconfigured provider detection verified.")
    finally:
        if orig_gemini: os.environ["GEMINI_API_KEY"] = orig_gemini
        if orig_xai: os.environ["XAI_API_KEY"] = orig_xai


def test_unconfigured_chat_response():
    orig_gemini = os.environ.get("GEMINI_API_KEY")
    try:
        os.environ.pop("GEMINI_API_KEY", None)
        res = chat_service.chat_sync("Hello ROVER", provider_name="gemini")
        assert res["status"] in ("unconfigured", "guided", "success")
        assert "GEMINI_API_KEY" in res["response"] or "ROVER" in res["response"]
        print("PASS: Safe unconfigured chat response verified.")
    finally:
        if orig_gemini: os.environ["GEMINI_API_KEY"] = orig_gemini


def test_empty_message_validation():
    # When no choice and empty message, returns main menu with success status
    res = chat_service.chat_sync("", provider_name="gemini")
    assert res["status"] in ("error", "guided", "success")
    assert len(res["choices"]) > 0
    print("PASS: Empty message validation verified.")


def test_initial_main_menu_choices():
    choices = get_initial_choices()
    assert len(choices) == 4
    choice_ids = [c["id"] for c in choices]
    assert "wf_risk" in choice_ids
    assert "wf_damage" in choice_ids
    assert "wf_maintenance" in choice_ids
    assert "wf_explore" in choice_ids
    print("PASS: Initial main menu provides 4 top-level workflows.")


def test_top_level_workflow_transitions():
    # Workflow A: Infrastructure Risk
    res_a = workflow_engine.process_step("main", "menu", "wf_risk")
    assert res_a["workflow"] == "infrastructure_risk"
    assert res_a["step"] == "options"
    assert len(res_a["choices"]) >= 3
    assert any("risk_view" in c["id"] for c in res_a["choices"])
    assert any("explain" in c["id"] for c in res_a["choices"])

    # Workflow B: Road Damage
    res_b = workflow_engine.process_step("main", "menu", "wf_damage")
    assert res_b["workflow"] == "road_damage"
    assert res_b["step"] == "options"
    assert any("damage" in c["id"] for c in res_b["choices"])

    # Workflow C: Plan Maintenance
    res_c = workflow_engine.process_step("main", "menu", "wf_maintenance")
    assert res_c["workflow"] == "plan_maintenance"
    assert res_c["step"] == "options"
    assert any("maint" in c["id"] for c in res_c["choices"])

    # Workflow D: Explore Project
    res_d = workflow_engine.process_step("main", "menu", "wf_explore")
    assert res_d["workflow"] == "explore_project"
    assert res_d["step"] == "options"
    assert any("explore" in c["id"] for c in res_d["choices"])

    print("PASS: All 4 top-level workflow transitions verified.")


def test_real_actions_execution():
    # 1. Real Predictions Data Action
    res_pred = workflow_engine.process_step("infrastructure_risk", "options", "risk_view")
    assert res_pred["action_executed"] == "fetch_predictions"
    assert "2,200" in res_pred["response"] or "348" in res_pred["response"]
    assert res_pred["route"] == "/predict"

    # 2. Real Maintenance Optimization Comparison Action
    res_opt = workflow_engine.process_step("plan_maintenance", "options", "maintenance_view")
    assert res_opt["action_executed"] == "fetch_optimization"
    assert "Hill Climbing" in res_opt["response"]
    assert "Tabu Search" in res_opt["response"]
    assert res_opt["route"] == "/priority"

    # 3. Real Sample Road Damage CV Action
    res_cv = workflow_engine.process_step("road_damage", "options", "damage_view")
    assert res_cv["action_executed"] == "fetch_sample_cv"
    assert "RDI" in res_cv["response"]
    assert res_cv["route"] == "/damage"

    print("PASS: Real actions connected to actual backend data/optimization verified.")


def test_back_and_home_navigation():
    # Test Back navigation from sub-step to options
    back_res = workflow_engine.process_step("infrastructure_risk", "explain_model", "back")
    assert back_res["step"] == "options"

    # Test Back navigation from options to main menu
    back_to_menu = workflow_engine.process_step("infrastructure_risk", "options", "back")
    assert back_to_menu["workflow"] == "main"
    assert back_to_menu["step"] == "menu"

    # Test Direct Home navigation
    home_res = workflow_engine.process_step("plan_maintenance", "view_results", "menu")
    assert home_res["workflow"] == "main"
    assert home_res["step"] == "menu"
    assert len(home_res["choices"]) == 4

    print("PASS: Back and Home navigation verified.")


def test_invalid_choice_rejected_safely():
    res = workflow_engine.process_step("infrastructure_risk", "options", "malicious_unsupported_id_999")
    assert res["status"] in ("guided", "fallback", "success")
    assert len(res["choices"]) > 0
    assert "response" in res and len(res["response"]) > 0
    print("PASS: Invalid choice IDs rejected safely.")


def test_unsupported_actions_not_executed():
    # Ensure allowlist only contains permitted action functions
    assert "fetch_predictions" in ALLOWLISTED_ACTIONS
    assert "fetch_optimization" in ALLOWLISTED_ACTIONS
    assert "fetch_sample_cv" in ALLOWLISTED_ACTIONS
    assert "drop_database" not in ALLOWLISTED_ACTIONS
    assert "system_eval" not in ALLOWLISTED_ACTIONS
    print("PASS: Allowlist protects against unauthorized actions.")


def test_deterministic_without_api_keys():
    orig_gemini = os.environ.get("GEMINI_API_KEY")
    orig_xai = os.environ.get("XAI_API_KEY")
    try:
        os.environ.pop("GEMINI_API_KEY", None)
        os.environ.pop("XAI_API_KEY", None)

        # Process a guided step without any API key
        res = chat_service.chat_sync(
            message=None,
            history=[],
            provider_name="gemini",
            workflow="plan_maintenance",
            step="maintenance_options",
            selected_choice_id="maintenance_algs",
        )
        assert res["status"] in ("guided", "success")
        assert "Beam Search" in res["response"]
        assert len(res["choices"]) > 0
        print("PASS: Deterministic guided workflows work without API keys.")
    finally:
        if orig_gemini: os.environ["GEMINI_API_KEY"] = orig_gemini
        if orig_xai: os.environ["XAI_API_KEY"] = orig_xai


def test_api_routes():
    from fastapi.testclient import TestClient
    from app.main import app

    client = TestClient(app)
    # Test GET /api/chat/status
    res = client.get("/api/chat/status")
    assert res.status_code == 200
    data = res.json()
    assert "provider" in data
    assert "configured" in data

    # Test POST /api/chat with guided choice
    guided_req = {
        "message": None,
        "history": [],
        "workflow": "main",
        "step": "menu",
        "selected_choice_id": "wf_risk",
    }
    chat_res = client.post("/api/chat", json=guided_req)
    assert chat_res.status_code == 200
    chat_data = chat_res.json()
    assert chat_data["workflow"] == "infrastructure_risk"
    assert len(chat_data["choices"]) > 0
    assert "risk" in chat_data["response"].lower()

    # Test POST /api/chat with free-text message
    free_req = {
        "message": "Explain Road Damage Index (RDI)",
        "history": [],
        "workflow": "main",
        "step": "menu",
    }
    free_res = client.post("/api/chat", json=free_req)
    assert free_res.status_code == 200
    free_data = free_res.json()
    assert "response" in free_data
    assert len(free_data["choices"]) > 0

    print("PASS: FastAPI /api/chat endpoints verified with guided and free-text requests.")


def test_indian_location_resolution():
    from app.utils.indian_geo import resolve_indian_zone, map_realistic_inputs_to_model_features, POPULAR_INDIAN_CORRIDORS

    # Test zone resolution for Indian states
    assert resolve_indian_zone(state="Maharashtra") == "West"
    assert resolve_indian_zone(state="Karnataka") == "South"
    assert resolve_indian_zone(state="Delhi") == "North"
    assert resolve_indian_zone(state="West Bengal") == "East"
    assert resolve_indian_zone(state="Madhya Pradesh") == "Central"

    # Test address string matching
    assert resolve_indian_zone(address="Bandra-Worli Sea Link, Mumbai, Maharashtra") == "West"
    assert resolve_indian_zone(address="Outer Ring Road, Bengaluru, Karnataka") == "South"
    assert resolve_indian_zone(address="Yamuna Expressway, Greater Noida, Uttar Pradesh") == "North"

    # Test popular corridors catalog
    assert len(POPULAR_INDIAN_CORRIDORS) >= 10
    assert any("Sea Link" in c["name"] for c in POPULAR_INDIAN_CORRIDORS)

    # Test mapping realistic simplified inputs into trained model feature space
    raw = {
        "asset_type": "Road",
        "condition": "Poor",
        "traffic_level": "Heavy",
        "maintenance_recency": "> 3 years",
        "age_years": 14,
        "location": {
            "address": "Mumbai - Pune Expressway, Maharashtra, India",
            "latitude": 18.7560,
            "longitude": 73.4116,
            "city": "Pune",
            "state": "Maharashtra",
        },
    }
    model_record, meta = map_realistic_inputs_to_model_features(raw)
    assert model_record["zone"] == "West"
    assert model_record["structural_score"] == 35.0
    assert model_record["corrosion_level"] == 75.0
    assert model_record["traffic_density"] == 85.0
    assert model_record["days_since_maintenance"] == 1350.0
    assert meta["city"] == "Pune"
    assert meta["state"] == "Maharashtra"
    print("PASS: Indian location resolution and defensible feature mapping verified.")


def test_realistic_corridor_prediction_api():
    from fastapi.testclient import TestClient
    from app.main import app

    client = TestClient(app)

    # Test GET /api/corridors
    corridors_res = client.get("/api/corridors")
    assert corridors_res.status_code == 200
    corridors_list = corridors_res.json()
    assert len(corridors_list) >= 10

    # Test POST /api/predict with realistic corridor input
    assessment_req = {
        "asset_type": "Bridge",
        "material": "Concrete",
        "age_years": 25,
        "condition": "Fair",
        "traffic_level": "Heavy",
        "maintenance_recency": "1-3 years",
        "location": {
            "address": "Bandra-Worli Sea Link, Mumbai, Maharashtra 400050, India",
            "latitude": 19.0330,
            "longitude": 72.8164,
            "city": "Mumbai",
            "state": "Maharashtra",
        },
    }
    pred_res = client.post("/api/predict", json=assessment_req)
    assert pred_res.status_code == 200
    pred_data = pred_res.json()
    assert "failure_probability" in pred_data
    assert "risk_level" in pred_data
    assert "remaining_useful_life" in pred_data
    assert pred_data["location"]["city"] == "Mumbai"
    assert pred_data["zone"] == "West"
    assert pred_data["key_factors"]["structural_score"] == 60.0

    # Test POST /api/predict with legacy 15-field input for full backward compatibility
    legacy_req = {
        "asset_id": "ASSET-001",
        "asset_type": "Road",
        "zone": "North",
        "material": "Asphalt",
        "age_years": 10.0,
        "traffic_density": 60.0,
        "average_load": 90.0,
        "annual_rainfall": 800.0,
        "average_temperature": 26.0,
        "maintenance_count": 4.0,
        "days_since_maintenance": 150.0,
        "days_since_inspection": 120.0,
        "structural_score": 70.0,
        "corrosion_level": 30.0,
        "previous_failures": 1,
        "usage_intensity": 65.0,
    }
    legacy_res = client.post("/api/predict", json=legacy_req)
    assert legacy_res.status_code == 200
    legacy_data = legacy_res.json()
    assert "failure_probability" in legacy_data

    print("PASS: Realistic corridor assessment API and backward compatibility verified.")


if __name__ == "__main__":
    test_system_prompt()
    test_provider_status_unconfigured()
    test_unconfigured_chat_response()
    test_empty_message_validation()
    test_initial_main_menu_choices()
    test_top_level_workflow_transitions()
    test_real_actions_execution()
    test_back_and_home_navigation()
    test_invalid_choice_rejected_safely()
    test_unsupported_actions_not_executed()
    test_deterministic_without_api_keys()
    test_api_routes()
    test_indian_location_resolution()
    test_realistic_corridor_prediction_api()
    print("\n===================================================================")
    print("ALL ROVER BACKEND, GUIDED WORKFLOWS & REALISTIC PREDICT TESTS PASSED!")
    print("===================================================================")
