"""High-level AI Chat Service orchestrator for ROVER.

Coordinates guided task-oriented workflows, conversation history,
LLM provider invocation (Gemini/Grok), and allowlisted application actions.
"""
from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional

from app.ai.llm_provider import (
    BaseLLMProvider,
    LLMConfigurationError,
    LLMProviderError,
    get_llm_provider,
)
from app.ai.project_context import build_system_prompt
from app.ai.workflow_engine import (
    MAIN_MENU_CHOICES,
    WORKFLOW_STEPS,
    workflow_engine,
)

logger = logging.getLogger("rover_chat_service")


class RoverChatService:
    """Orchestrates ROVER chatbot conversations and guided task workflows."""

    MAX_HISTORY_TURNS = 10
    MAX_MESSAGE_CHARS = 2500

    def __init__(self, provider: Optional[BaseLLMProvider] = None):
        self._custom_provider = provider

    def _get_provider(self, requested_provider: Optional[str] = None) -> BaseLLMProvider:
        if self._custom_provider is not None:
            return self._custom_provider
        return get_llm_provider(requested_provider)

    def get_status(self, requested_provider: Optional[str] = None) -> Dict[str, Any]:
        """Returns the readiness status of the configured LLM provider."""
        try:
            provider = self._get_provider(requested_provider)
            return provider.get_status()
        except Exception as exc:
            return {
                "provider": requested_provider or "unknown",
                "configured": False,
                "status": "error",
                "model": "unknown",
                "message": f"Provider configuration error: {str(exc)}",
            }

    def _clean_history(
        self,
        history: Optional[List[Dict[str, str]]],
        new_message: str,
    ) -> List[Dict[str, str]]:
        """Validates and trims history to recent turns, appending the new message."""
        cleaned: List[Dict[str, str]] = []
        if history:
            sliced = history[-self.MAX_HISTORY_TURNS :]
            for turn in sliced:
                role = "assistant" if turn.get("role") in ("assistant", "model") else "user"
                content = str(turn.get("content", "")).strip()
                if content:
                    cleaned.append({"role": role, "content": content[: self.MAX_MESSAGE_CHARS]})

        if new_message:
            cleaned.append({"role": "user", "content": new_message[: self.MAX_MESSAGE_CHARS]})
        return cleaned

    def _fetch_live_telemetry(self) -> Optional[Dict[str, Any]]:
        """Safely gathers live summary stats from database/models without throwing."""
        try:
            from app.api.routes_dashboard import get_dashboard_summary
            return get_dashboard_summary()
        except Exception:
            return None

    def _infer_contextual_choices(self, text: str, current_wf: Optional[str]) -> Tuple[List[Dict[str, Any]], str]:
        """Suggests 3-4 helpful contextual choices for free-text inquiries."""
        lowered = text.lower()
        if any(w in lowered for w in ["damage", "crack", "pothole", "cv", "vision", "rdi", "image", "photo"]):
            return (
                WORKFLOW_STEPS["road_damage"]["options"]["choices"][:3] + [
                    {"id": "main_menu", "label": "🏠 Main Menu", "description": "Return to top choices", "action_type": "workflow", "workflow": "main", "step": "menu"}
                ],
                "road_damage",
            )
        elif any(w in lowered for w in ["optimize", "knapsack", "hill", "beam", "tabu", "budget", "schedule", "priority"]):
            return (
                WORKFLOW_STEPS["plan_maintenance"]["options"]["choices"][:3] + [
                    {"id": "main_menu", "label": "🏠 Main Menu", "description": "Return to top choices", "action_type": "workflow", "workflow": "main", "step": "menu"}
                ],
                "plan_maintenance",
            )
        elif any(w in lowered for w in ["predict", "risk", "fail", "score", "corrosion", "life", "rul", "bridge"]):
            return (
                WORKFLOW_STEPS["infrastructure_risk"]["options"]["choices"][:3] + [
                    {"id": "main_menu", "label": "🏠 Main Menu", "description": "Return to top choices", "action_type": "workflow", "workflow": "main", "step": "menu"}
                ],
                "infrastructure_risk",
            )
        elif any(w in lowered for w in ["project", "architecture", "automl", "mlflow", "data structure", "fastapi", "docker"]):
            return (
                WORKFLOW_STEPS["explore_project"]["options"]["choices"][:3] + [
                    {"id": "main_menu", "label": "🏠 Main Menu", "description": "Return to top choices", "action_type": "workflow", "workflow": "main", "step": "menu"}
                ],
                "explore_project",
            )
        elif current_wf and current_wf in WORKFLOW_STEPS and "options" in WORKFLOW_STEPS[current_wf]:
            return (
                WORKFLOW_STEPS[current_wf]["options"]["choices"][:3] + [
                    {"id": "main_menu", "label": "🏠 Main Menu", "description": "Return to top choices", "action_type": "workflow", "workflow": "main", "step": "menu"}
                ],
                current_wf,
            )
        return MAIN_MENU_CHOICES, "main"

    async def chat_async(
        self,
        message: Optional[str] = None,
        history: Optional[List[Dict[str, str]]] = None,
        provider_name: Optional[str] = None,
        workflow: Optional[str] = "main",
        step: Optional[str] = "menu",
        selected_choice_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Processes guided choices or free-text chat asynchronously for FastAPI."""
        # 1. If user clicked a structured option card / button
        if selected_choice_id:
            if selected_choice_id in ("back", "nav_back"):
                wf_result = workflow_engine.process_back(workflow, step)
            elif selected_choice_id in ("menu", "main_menu", "home"):
                wf_result = workflow_engine.get_main_menu()
            else:
                wf_result = workflow_engine.process_choice(
                    workflow=workflow,
                    step=step,
                    choice_id=selected_choice_id,
                )
            wf_result.setdefault("provider", "guided_engine")
            wf_result.setdefault("model", "task_state_machine")
            return wf_result

        # 2. Free-text chat processing
        clean_msg = (message or "").strip()
        if not clean_msg:
            # If no message and no choice, return current workflow state or main menu
            return workflow_engine.get_main_menu()

        # Handle text triggers for menu / home
        if clean_msg.lower() in ("home", "menu", "main menu", "start over", "reset"):
            return workflow_engine.get_main_menu()

        try:
            provider = self._get_provider(provider_name)
            telemetry = self._fetch_live_telemetry()
            system_prompt = build_system_prompt(live_status=telemetry)
            messages = self._clean_history(history, clean_msg)

            answer = await provider.generate_response(messages, system_prompt=system_prompt)
            follow_up_choices, active_wf = self._infer_contextual_choices(clean_msg, workflow)

            return {
                "response": answer,
                "choices": follow_up_choices,
                "workflow": active_wf,
                "step": "follow_up",
                "previous_step": f"{active_wf}:options",
                "action_executed": None,
                "action_data": None,
                "provider": provider.name,
                "model": provider.model,
                "status": "success",
                "error": None,
            }
        except LLMConfigurationError as exc:
            # Safe guided fallback even without API key!
            follow_up_choices, active_wf = self._infer_contextual_choices(clean_msg, workflow)
            return {
                "response": (
                    f"⚠️ **ROVER Setup Notice:**\n\n{str(exc)}\n\n"
                    f"*You can still use all guided task workflows below without an API key:*"
                ),
                "choices": follow_up_choices,
                "workflow": active_wf,
                "step": "options",
                "provider": provider_name or "unconfigured",
                "model": "none",
                "status": "unconfigured",
                "error": str(exc),
            }
        except LLMProviderError as exc:
            follow_up_choices, active_wf = self._infer_contextual_choices(clean_msg, workflow)
            return {
                "response": f"⚠️ **Communication Notice:**\n\n{str(exc)}",
                "choices": follow_up_choices,
                "workflow": active_wf,
                "step": "options",
                "provider": provider_name or "error",
                "model": "none",
                "status": "error",
                "error": str(exc),
            }
        except Exception as exc:
            logger.exception("Unexpected error during chat generation")
            return {
                "response": "⚠️ An unexpected error occurred while processing your request. Please select a task below.",
                "choices": MAIN_MENU_CHOICES,
                "workflow": "main",
                "step": "menu",
                "provider": provider_name or "unknown",
                "model": "none",
                "status": "error",
                "error": str(exc),
            }

    def chat_sync(
        self,
        message: Optional[str] = None,
        history: Optional[List[Dict[str, str]]] = None,
        provider_name: Optional[str] = None,
        workflow: Optional[str] = "main",
        step: Optional[str] = "menu",
        selected_choice_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Synchronous chat and guided choice processing for Streamlit."""
        # 1. If user clicked a structured option card / button
        if selected_choice_id:
            if selected_choice_id in ("back", "nav_back"):
                wf_result = workflow_engine.process_back(workflow, step)
            elif selected_choice_id in ("menu", "main_menu", "home"):
                wf_result = workflow_engine.get_main_menu()
            else:
                wf_result = workflow_engine.process_choice(
                    workflow=workflow,
                    step=step,
                    choice_id=selected_choice_id,
                )
            wf_result.setdefault("provider", "guided_engine")
            wf_result.setdefault("model", "task_state_machine")
            return wf_result

        clean_msg = (message or "").strip()
        if not clean_msg:
            return workflow_engine.get_main_menu()

        if clean_msg.lower() in ("home", "menu", "main menu", "start over", "reset"):
            return workflow_engine.get_main_menu()

        try:
            provider = self._get_provider(provider_name)
            telemetry = self._fetch_live_telemetry()
            system_prompt = build_system_prompt(live_status=telemetry)
            messages = self._clean_history(history, clean_msg)

            answer = provider.generate_response_sync(messages, system_prompt=system_prompt)
            follow_up_choices, active_wf = self._infer_contextual_choices(clean_msg, workflow)

            return {
                "response": answer,
                "choices": follow_up_choices,
                "workflow": active_wf,
                "step": "follow_up",
                "previous_step": f"{active_wf}:options",
                "action_executed": None,
                "action_data": None,
                "provider": provider.name,
                "model": provider.model,
                "status": "success",
                "error": None,
            }
        except LLMConfigurationError as exc:
            follow_up_choices, active_wf = self._infer_contextual_choices(clean_msg, workflow)
            return {
                "response": (
                    f"⚠️ **ROVER Setup Notice:**\n\n{str(exc)}\n\n"
                    f"*You can still use all guided task workflows below without an API key:*"
                ),
                "choices": follow_up_choices,
                "workflow": active_wf,
                "step": "options",
                "provider": provider_name or "unconfigured",
                "model": "none",
                "status": "unconfigured",
                "error": str(exc),
            }
        except LLMProviderError as exc:
            follow_up_choices, active_wf = self._infer_contextual_choices(clean_msg, workflow)
            return {
                "response": f"⚠️ **Communication Notice:**\n\n{str(exc)}",
                "choices": follow_up_choices,
                "workflow": active_wf,
                "step": "options",
                "provider": provider_name or "error",
                "model": "none",
                "status": "error",
                "error": str(exc),
            }
        except Exception as exc:
            logger.exception("Unexpected error during synchronous chat generation")
            return {
                "response": "⚠️ An unexpected error occurred while processing your request. Please select a task below.",
                "choices": MAIN_MENU_CHOICES,
                "workflow": "main",
                "step": "menu",
                "provider": provider_name or "unknown",
                "model": "none",
                "status": "error",
                "error": str(exc),
            }


# Default singleton instance
chat_service = RoverChatService()
