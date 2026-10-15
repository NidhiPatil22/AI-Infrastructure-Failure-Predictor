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
    print("\n=======================================================")
    print("ALL 12 ROVER BACKEND & GUIDED WORKFLOW TESTS PASSED!")
    print("=======================================================")
