"""Pydantic schemas for the ROVER AI Chatbot and Guided Assistant."""
from __future__ import annotations

from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class ChatMessage(BaseModel):
    """Single turn in a chat conversation."""
    role: str = Field(..., description="Message role: 'user' or 'assistant'")
    content: str = Field(..., max_length=4000, description="Text content of the message")


class ChoiceItem(BaseModel):
    """Interactive choice card or button presented by ROVER."""
    id: str = Field(..., description="Stable option ID")
    label: str = Field(..., description="Display label for button or card")
    description: Optional[str] = Field(None, description="Short explanation of what this option does")
    action_type: str = Field(
        default="workflow",
        description="Type of action: 'workflow', 'explain', 'navigate', or 'action'"
    )
    workflow: Optional[str] = Field(None, description="Target workflow identifier")
    step: Optional[str] = Field(None, description="Target step identifier")
    payload: Optional[Dict[str, Any]] = Field(default=None, description="Allowlisted execution arguments (e.g. page, route)")


class ChatRequest(BaseModel):
    """Payload sent by the frontend chat client."""
    message: Optional[str] = Field(None, max_length=2500, description="User's prompt or question")
    history: List[ChatMessage] = Field(default=[], description="Recent conversation turns (up to 10)")
    provider: Optional[str] = Field(None, description="Optional override for LLM provider ('gemini' or 'grok')")
    workflow: Optional[str] = Field("main", description="Active workflow identifier")
    step: Optional[str] = Field("menu", description="Active step in the workflow")
    selected_choice_id: Optional[str] = Field(None, description="ID of the option chosen by user")


class ChatResponse(BaseModel):
    """Structured response from the guided assistant."""
    response: str = Field(..., description="Assistant's reply in Markdown")
    choices: List[ChoiceItem] = Field(default=[], description="List of interactive choices")
    workflow: str = Field(default="main", description="Current workflow state")
    step: str = Field(default="menu", description="Current step in workflow")
    previous_step: Optional[str] = Field(None, description="Previous step for Back navigation")
    action_executed: Optional[str] = Field(None, description="Identifier of executed application action")
    action_data: Optional[Dict[str, Any]] = Field(None, description="Safe verified data returned by application action")
    provider: str = Field(..., description="LLM provider or 'system'")
    model: str = Field(..., description="Model identifier used")
    status: str = Field(default="success", description="Status code: 'success', 'unconfigured', or 'error'")
    error: Optional[str] = Field(None, description="Error detail if status is not success")


class ChatStatusResponse(BaseModel):
    """Current backend status and readiness of the AI assistant."""
    provider: str = Field(..., description="Configured LLM provider ('gemini', 'grok', or 'none')")
    configured: bool = Field(..., description="Whether a valid API key is configured in the environment")
    status: str = Field(..., description="Operational status: 'online', 'unconfigured', or 'error'")
    model: str = Field(..., description="Target model name")
    message: str = Field(..., description="Human-readable status or setup instruction")
