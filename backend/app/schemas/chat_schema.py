"""Pydantic schemas for the ROVER AI Chatbot Assistant."""
from __future__ import annotations

from typing import List, Optional
from pydantic import BaseModel, Field


class ChatMessage(BaseModel):
    """Single turn in a chat conversation."""
    role: str = Field(..., description="Message role: 'user' or 'assistant'")
    content: str = Field(..., max_length=4000, description="Text content of the message")


class ChatRequest(BaseModel):
    """Payload sent by the frontend chat client."""
    message: str = Field(..., min_length=1, max_length=2500, description="User's prompt or question")
    history: List[ChatMessage] = Field(default=[], description="Recent conversation turns (up to 10)")
    provider: Optional[str] = Field(None, description="Optional override for LLM provider ('gemini' or 'grok')")


class ChatResponse(BaseModel):
    """Structured response from the assistant."""
    response: str = Field(..., description="Assistant's reply in Markdown")
    provider: str = Field(..., description="LLM provider that generated the response ('gemini' or 'grok')")
    model: str = Field(..., description="Model identifier used")
    status: str = Field(default="success", description="Status code: 'success' or 'error'")
    error: Optional[str] = Field(None, description="Error detail if status is not success")


class ChatStatusResponse(BaseModel):
    """Current backend status and readiness of the AI assistant."""
    provider: str = Field(..., description="Configured LLM provider ('gemini', 'grok', or 'none')")
    configured: bool = Field(..., description="Whether a valid API key is configured in the environment")
    status: str = Field(..., description="Operational status: 'online', 'unconfigured', or 'error'")
    model: str = Field(..., description="Target model name")
    message: str = Field(..., description="Human-readable status or setup instruction")
