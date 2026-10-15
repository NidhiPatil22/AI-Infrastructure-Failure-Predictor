"""High-level AI Chat Service orchestrator for ROVER.

Coordinates project context, conversation pruning, provider invocation,
and safe error response handling.
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

logger = logging.getLogger("rover_chat_service")


class RoverChatService:
    """Orchestrates ROVER chatbot conversations for FastAPI and Streamlit."""

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
            # Keep only the last MAX_HISTORY_TURNS turns
            sliced = history[-self.MAX_HISTORY_TURNS :]
            for turn in sliced:
                role = "assistant" if turn.get("role") in ("assistant", "model") else "user"
                content = str(turn.get("content", "")).strip()
                if content:
                    cleaned.append({"role": role, "content": content[: self.MAX_MESSAGE_CHARS]})

        # Append latest user question
        cleaned.append({"role": "user", "content": new_message[: self.MAX_MESSAGE_CHARS]})
        return cleaned

    def _fetch_live_telemetry(self) -> Optional[Dict[str, Any]]:
        """Safely gathers live summary stats from database/models without throwing."""
        try:
            from app.api.routes_dashboard import get_dashboard_summary
            return get_dashboard_summary()
        except Exception:
            return None

    async def chat_async(
        self,
        message: str,
        history: Optional[List[Dict[str, str]]] = None,
        provider_name: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Processes a chat request asynchronously for FastAPI."""
        clean_msg = (message or "").strip()
        if not clean_msg:
            return {
                "response": "Please enter a question or topic about road infrastructure.",
                "provider": "system",
                "model": "validator",
                "status": "error",
                "error": "Empty message submitted.",
            }

        try:
            provider = self._get_provider(provider_name)
            telemetry = self._fetch_live_telemetry()
            system_prompt = build_system_prompt(live_status=telemetry)
            messages = self._clean_history(history, clean_msg)

            answer = await provider.generate_response(messages, system_prompt=system_prompt)
            return {
                "response": answer,
                "provider": provider.name,
                "model": provider.model,
                "status": "success",
                "error": None,
            }
        except LLMConfigurationError as exc:
            return {
                "response": f"⚠️ **ROVER Setup Needed:**\n\n{str(exc)}",
                "provider": provider_name or "unconfigured",
                "model": "none",
                "status": "unconfigured",
                "error": str(exc),
            }
        except LLMProviderError as exc:
            return {
                "response": f"⚠️ **Assistant Communication Notice:**\n\n{str(exc)}",
                "provider": provider_name or "error",
                "model": "none",
                "status": "error",
                "error": str(exc),
            }
        except Exception as exc:
            logger.exception("Unexpected error during chat generation")
            return {
                "response": "⚠️ An unexpected internal error occurred while processing your request. Please try again.",
                "provider": provider_name or "unknown",
                "model": "none",
                "status": "error",
                "error": str(exc),
            }

    def chat_sync(
        self,
        message: str,
        history: Optional[List[Dict[str, str]]] = None,
        provider_name: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Synchronous chat processing for Streamlit."""
        clean_msg = (message or "").strip()
        if not clean_msg:
            return {
                "response": "Please enter a question or topic about road infrastructure.",
                "provider": "system",
                "model": "validator",
                "status": "error",
                "error": "Empty message submitted.",
            }

        try:
            provider = self._get_provider(provider_name)
            telemetry = self._fetch_live_telemetry()
            system_prompt = build_system_prompt(live_status=telemetry)
            messages = self._clean_history(history, clean_msg)

            answer = provider.generate_response_sync(messages, system_prompt=system_prompt)
            return {
                "response": answer,
                "provider": provider.name,
                "model": provider.model,
                "status": "success",
                "error": None,
            }
        except LLMConfigurationError as exc:
            return {
                "response": f"⚠️ **ROVER Setup Needed:**\n\n{str(exc)}",
                "provider": provider_name or "unconfigured",
                "model": "none",
                "status": "unconfigured",
                "error": str(exc),
            }
        except LLMProviderError as exc:
            return {
                "response": f"⚠️ **Assistant Communication Notice:**\n\n{str(exc)}",
                "provider": provider_name or "error",
                "model": "none",
                "status": "error",
                "error": str(exc),
            }
        except Exception as exc:
            logger.exception("Unexpected error during synchronous chat generation")
            return {
                "response": "⚠️ An unexpected internal error occurred while processing your request. Please try again.",
                "provider": provider_name or "unknown",
                "model": "none",
                "status": "error",
                "error": str(exc),
            }


# Default singleton instance
chat_service = RoverChatService()
