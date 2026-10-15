"""Modular LLM Provider Integration for ROVER Assistant.

Supports Google Gemini and xAI Grok with strict server-side credential isolation,
environment-based configuration, and robust error translation.
"""
from __future__ import annotations

from abc import ABC, abstractmethod
import os
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import httpx

# Load .env if present (check both root and backend)
try:
    from dotenv import load_dotenv
    root_dir = Path(__file__).resolve().parents[3]
    load_dotenv(root_dir / ".env")
    backend_dir = Path(__file__).resolve().parents[2]
    load_dotenv(backend_dir / ".env")
except Exception:
    pass


class LLMConfigurationError(Exception):
    """Raised when an LLM provider is missing required configuration or API keys."""
    pass


class LLMProviderError(Exception):
    """Raised when an external LLM API call fails or encounters rate limits/timeouts."""
    pass


def _mask_key(key: Optional[str]) -> str:
    """Masks an API key for safe debugging without exposure."""
    if not key or len(key) < 8:
        return "[NOT SET]"
    return f"{key[:4]}...{key[-4:]}"


class BaseLLMProvider(ABC):
    """Abstract base class for LLM providers."""

    def __init__(self, name: str, model: str):
        self.name = name
        self.model = model

    @abstractmethod
    def is_configured(self) -> bool:
        """Returns True if the provider has the necessary credentials."""
        pass

    @abstractmethod
    def get_status(self) -> Dict[str, Any]:
        """Returns readiness status and diagnostic message."""
        pass

    @abstractmethod
    async def generate_response(
        self,
        messages: List[Dict[str, str]],
        system_prompt: str,
    ) -> str:
        """Generates an assistant response asynchronously."""
        pass

    @abstractmethod
    def generate_response_sync(
        self,
        messages: List[Dict[str, str]],
        system_prompt: str,
    ) -> str:
        """Synchronous version for environments like Streamlit."""
        pass


class GeminiProvider(BaseLLMProvider):
    """Google Gemini integration using official REST API endpoint."""

    DEFAULT_MODEL = "gemini-2.0-flash"

    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None):
        model_name = model or os.getenv("GEMINI_MODEL") or self.DEFAULT_MODEL
        super().__init__(name="gemini", model=model_name)
        self.api_key = api_key or os.getenv("GEMINI_API_KEY", "").strip()
        self.timeout = float(os.getenv("LLM_TIMEOUT", "30.0"))

    def is_configured(self) -> bool:
        return bool(self.api_key and len(self.api_key) > 5)

    def get_status(self) -> Dict[str, Any]:
        if self.is_configured():
            return {
                "provider": "gemini",
                "configured": True,
                "status": "online",
                "model": self.model,
                "message": f"Gemini active (Model: {self.model})",
            }
        return {
            "provider": "gemini",
            "configured": False,
            "status": "unconfigured",
            "model": self.model,
            "message": "GEMINI_API_KEY not found in environment. Set GEMINI_API_KEY in your .env file.",
        }

    def _prepare_payload(self, messages: List[Dict[str, str]], system_prompt: str) -> Dict[str, Any]:
        """Transforms conversation turns into the Gemini v1beta schema."""
        contents: List[Dict[str, Any]] = []
        for msg in messages:
            role = "user" if msg.get("role") == "user" else "model"
            content = msg.get("content", "").strip()
            if content:
                contents.append({"role": role, "parts": [{"text": content}]})

        if not contents:
            contents = [{"role": "user", "parts": [{"text": "Hello"}]}]

        return {
            "system_instruction": {
                "parts": [{"text": system_prompt}]
            },
            "contents": contents,
            "generationConfig": {
                "temperature": 0.4,
                "topP": 0.9,
                "maxOutputTokens": 1200,
            },
        }

    def _parse_response(self, data: Dict[str, Any]) -> str:
        """Safely extracts text from Gemini response body."""
        candidates = data.get("candidates", [])
        if not candidates:
            feedback = data.get("promptFeedback", {})
            if feedback.get("blockReason"):
                raise LLMProviderError(f"Gemini response was blocked: {feedback.get('blockReason')}")
            raise LLMProviderError("Gemini returned an empty response.")

        parts = candidates[0].get("content", {}).get("parts", [])
        if not parts:
            raise LLMProviderError("Gemini candidate contains no content parts.")

        return parts[0].get("text", "").strip()

    def _handle_error(self, exc: Exception) -> LLMProviderError:
        """Sanitizes exceptions and produces user-actionable error messages without leaking keys."""
        if isinstance(exc, httpx.HTTPStatusError):
            status = exc.response.status_code
            if status in (401, 403):
                return LLMProviderError(
                    "Gemini API authentication failed (HTTP 401/403). Please verify that GEMINI_API_KEY is valid and has Gemini API enabled."
                )
            if status == 429:
                return LLMProviderError(
                    "Gemini API rate limit exceeded (HTTP 429). Please wait a few moments and try your question again."
                )
            if status == 404:
                return LLMProviderError(
                    f"Gemini model '{self.model}' was not found (HTTP 404). Check GEMINI_MODEL in your .env file."
                )
            return LLMProviderError(f"Gemini API error (HTTP {status}): {exc.response.text[:200]}")
        if isinstance(exc, httpx.TimeoutException):
            return LLMProviderError("Gemini API request timed out. Please check your internet connection and try again.")
        return LLMProviderError(f"Gemini connection error: {str(exc)}")

    async def generate_response(
        self,
        messages: List[Dict[str, str]],
        system_prompt: str,
    ) -> str:
        if not self.is_configured():
            raise LLMConfigurationError(
                "Gemini provider is selected, but GEMINI_API_KEY is not configured. "
                "Add GEMINI_API_KEY=your_key to your .env file or environment variables."
            )

        endpoint = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model}:generateContent"
        payload = self._prepare_payload(messages, system_prompt)

        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                response = await client.post(
                    endpoint,
                    params={"key": self.api_key},
                    json=payload,
                    headers={"Content-Type": "application/json"},
                )
                response.raise_for_status()
                return self._parse_response(response.json())
            except Exception as exc:
                raise self._handle_error(exc) from None

    def generate_response_sync(
        self,
        messages: List[Dict[str, str]],
        system_prompt: str,
    ) -> str:
        if not self.is_configured():
            raise LLMConfigurationError(
                "Gemini provider is selected, but GEMINI_API_KEY is not configured. "
                "Add GEMINI_API_KEY=your_key to your .env file or environment variables."
            )

        endpoint = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model}:generateContent"
        payload = self._prepare_payload(messages, system_prompt)

        with httpx.Client(timeout=self.timeout) as client:
            try:
                response = client.post(
                    endpoint,
                    params={"key": self.api_key},
                    json=payload,
                    headers={"Content-Type": "application/json"},
                )
                response.raise_for_status()
                return self._parse_response(response.json())
            except Exception as exc:
                raise self._handle_error(exc) from None


class GrokProvider(BaseLLMProvider):
    """xAI Grok integration using official OpenAI-compatible REST API."""

    DEFAULT_MODEL = "grok-2-latest"
    API_URL = "https://api.x.ai/v1/chat/completions"

    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None):
        model_name = model or os.getenv("XAI_MODEL") or self.DEFAULT_MODEL
        super().__init__(name="grok", model=model_name)
        self.api_key = api_key or os.getenv("XAI_API_KEY", "").strip()
        self.timeout = float(os.getenv("LLM_TIMEOUT", "30.0"))

    def is_configured(self) -> bool:
        return bool(self.api_key and len(self.api_key) > 5)

    def get_status(self) -> Dict[str, Any]:
        if self.is_configured():
            return {
                "provider": "grok",
                "configured": True,
                "status": "online",
                "model": self.model,
                "message": f"xAI Grok active (Model: {self.model})",
            }
        return {
            "provider": "grok",
            "configured": False,
            "status": "unconfigured",
            "model": self.model,
            "message": "XAI_API_KEY not found in environment. Set XAI_API_KEY in your .env file.",
        }

    def _prepare_payload(self, messages: List[Dict[str, str]], system_prompt: str) -> Dict[str, Any]:
        chat_messages = [{"role": "system", "content": system_prompt}]
        for msg in messages:
            role = "assistant" if msg.get("role") in ("assistant", "model") else "user"
            content = msg.get("content", "").strip()
            if content:
                chat_messages.append({"role": role, "content": content})

        return {
            "model": self.model,
            "messages": chat_messages,
            "temperature": 0.4,
            "max_tokens": 1200,
        }

    def _parse_response(self, data: Dict[str, Any]) -> str:
        choices = data.get("choices", [])
        if not choices:
            raise LLMProviderError("xAI Grok returned an empty response.")
        return choices[0].get("message", {}).get("content", "").strip()

    def _handle_error(self, exc: Exception) -> LLMProviderError:
        if isinstance(exc, httpx.HTTPStatusError):
            status = exc.response.status_code
            if status in (401, 403):
                return LLMProviderError(
                    "xAI Grok API authentication failed (HTTP 401/403). Please verify that XAI_API_KEY is valid."
                )
            if status == 429:
                return LLMProviderError(
                    "xAI Grok rate limit reached (HTTP 429). Please wait a moment and try again."
                )
            if status == 404:
                return LLMProviderError(
                    f"xAI Grok model '{self.model}' was not found (HTTP 404). Check XAI_MODEL in your .env file."
                )
            return LLMProviderError(f"xAI Grok API error (HTTP {status}): {exc.response.text[:200]}")
        if isinstance(exc, httpx.TimeoutException):
            return LLMProviderError("xAI Grok API request timed out. Please check your network and try again.")
        return LLMProviderError(f"xAI Grok connection error: {str(exc)}")

    async def generate_response(
        self,
        messages: List[Dict[str, str]],
        system_prompt: str,
    ) -> str:
        if not self.is_configured():
            raise LLMConfigurationError(
                "Grok provider is selected, but XAI_API_KEY is not configured. "
                "Add XAI_API_KEY=your_key to your .env file or environment variables."
            )

        payload = self._prepare_payload(messages, system_prompt)
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                response = await client.post(self.API_URL, json=payload, headers=headers)
                response.raise_for_status()
                return self._parse_response(response.json())
            except Exception as exc:
                raise self._handle_error(exc) from None

    def generate_response_sync(
        self,
        messages: List[Dict[str, str]],
        system_prompt: str,
    ) -> str:
        if not self.is_configured():
            raise LLMConfigurationError(
                "Grok provider is selected, but XAI_API_KEY is not configured. "
                "Add XAI_API_KEY=your_key to your .env file or environment variables."
            )

        payload = self._prepare_payload(messages, system_prompt)
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        with httpx.Client(timeout=self.timeout) as client:
            try:
                response = client.post(self.API_URL, json=payload, headers=headers)
                response.raise_for_status()
                return self._parse_response(response.json())
            except Exception as exc:
                raise self._handle_error(exc) from None


def get_llm_provider(requested_provider: Optional[str] = None) -> BaseLLMProvider:
    """Factory returning the configured BaseLLMProvider based on environment variables or explicit override.

    Respects LLM_PROVIDER ('gemini' or 'grok').
    Does NOT silently fall back to an unconfigured provider if the specified provider is active.
    """
    provider_name = (requested_provider or os.getenv("LLM_PROVIDER") or "").strip().lower()

    # If not explicitly set in LLM_PROVIDER, inspect configured keys
    if not provider_name:
        if os.getenv("GEMINI_API_KEY"):
            provider_name = "gemini"
        elif os.getenv("XAI_API_KEY"):
            provider_name = "grok"
        else:
            # Default to gemini (most common) so setup guidance points to GEMINI_API_KEY
            provider_name = "gemini"

    if provider_name == "gemini":
        return GeminiProvider()
    elif provider_name in ("grok", "xai"):
        return GrokProvider()
    else:
        raise LLMConfigurationError(
            f"Unsupported LLM_PROVIDER '{provider_name}'. Supported options are 'gemini' and 'grok'."
        )
