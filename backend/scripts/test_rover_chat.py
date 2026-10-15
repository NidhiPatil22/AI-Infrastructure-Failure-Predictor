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
        assert res["status"] == "unconfigured"
        assert "GEMINI_API_KEY" in res["response"]
        print("PASS: Safe unconfigured chat response verified.")
    finally:
        if orig_gemini: os.environ["GEMINI_API_KEY"] = orig_gemini


def test_empty_message_validation():
    res = chat_service.chat_sync("", provider_name="gemini")
    assert res["status"] == "error"
    assert "Please enter a question" in res["response"]
    print("PASS: Empty message validation verified.")


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

    # Test POST /api/chat
    chat_res = client.post("/api/chat", json={"message": "What is this project about?", "history": []})
    assert chat_res.status_code == 200
    chat_data = chat_res.json()
    assert "response" in chat_data
    assert "provider" in chat_data
    print("PASS: FastAPI /api/chat endpoints verified.")


if __name__ == "__main__":
    test_system_prompt()
    test_provider_status_unconfigured()
    test_unconfigured_chat_response()
    test_empty_message_validation()
    test_api_routes()
    print("\nALL ROVER BACKEND TESTS PASSED SUCCESSFULLY!")
