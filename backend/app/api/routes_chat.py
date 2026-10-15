"""FastAPI route definitions for the ROVER AI Infrastructure Assistant."""
from __future__ import annotations

from typing import Optional
from fastapi import APIRouter, Query

from app.ai.chat_service import chat_service
from app.schemas.chat_schema import ChatRequest, ChatResponse, ChatStatusResponse

router = APIRouter(tags=["AI Assistant"])


@router.post("/chat", response_model=ChatResponse)
async def chat_with_rover(payload: ChatRequest):
    """Processes a user message through the ROVER AI Infrastructure Assistant.

    Validates inputs, attaches verified project context, passes conversation
    history to either Google Gemini or xAI Grok securely on the backend,
    and returns the assistant's formatted markdown response.
    """
    history_dicts = [turn.model_dump() for turn in payload.history]
    result = await chat_service.chat_async(
        message=payload.message,
        history=history_dicts,
        provider_name=payload.provider,
    )
    return ChatResponse(**result)


@router.get("/chat/status", response_model=ChatStatusResponse)
async def get_rover_status(provider: Optional[str] = Query(None, description="Optional provider to check")):
    """Returns the operational and credential readiness status of ROVER."""
    status_info = chat_service.get_status(requested_provider=provider)
    return ChatStatusResponse(**status_info)
