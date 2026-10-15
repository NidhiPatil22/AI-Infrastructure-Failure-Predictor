"""ROVER Guided Task-Oriented AI Assistant UI Component for Streamlit.

Renders the visual mascot, interactive choice cards, multi-step workflows,
navigation actions, and free-text chat in both Night and Day themes.
"""
from __future__ import annotations

import base64
from pathlib import Path
from typing import Any, Dict, List, Optional

import requests
import streamlit as st

from app.ai.chat_service import chat_service
from app.ai.workflow_engine import MAIN_MENU_CHOICES, workflow_engine

# Asset paths
ASSET_DIR = Path(__file__).resolve().parents[2] / "data" / "assets"
MASCOT_IMG_PATH = ASSET_DIR / "rover_mascot.jpg"
MASCOT_THINKING_PATH = ASSET_DIR / "rover_thinking.jpg"

INITIAL_WELCOME_MESSAGE = (
    "👋 **Hello! I'm ROVER — Road Operations & Vulnerability Evaluation Robot.**\n\n"
    "Your AI assistant for road infrastructure, predictive maintenance, and smarter civil decisions.\n\n"
    "What would you like to do today? Select one of the guided tasks below, or ask any question in the chat:"
)


@st.cache_data
def get_mascot_base64(variant: str = "default") -> str:
    """Reads and caches the mascot image as a base64 data URI."""
    target_path = MASCOT_THINKING_PATH if variant == "thinking" and MASCOT_THINKING_PATH.exists() else MASCOT_IMG_PATH
    if target_path.exists():
        try:
            with open(target_path, "rb") as fh:
                encoded = base64.b64encode(fh.read()).decode("utf-8")
                return f"data:image/jpeg;base64,{encoded}"
        except Exception:
            return ""
    return ""


def _query_rover_backend(
    message: Optional[str] = None,
    history: Optional[List[Dict[str, str]]] = None,
    workflow: str = "main",
    step: str = "menu",
    selected_choice_id: Optional[str] = None,
) -> Dict[str, Any]:
    """Communicates with the ROVER backend via FastAPI or directly via python service."""
    payload = {
        "message": message,
        "history": history or [],
        "workflow": workflow,
        "step": step,
        "selected_choice_id": selected_choice_id,
    }

    # Attempt FastAPI REST call if server is running locally
    try:
        resp = requests.post(
            "http://127.0.0.1:8000/api/chat",
            json=payload,
            timeout=25,
        )
        if resp.status_code == 200:
            return resp.json()
    except Exception:
        pass

    # Seamless fallback to direct python service
    return chat_service.chat_sync(
        message=message,
        history=history,
        workflow=workflow,
        step=step,
        selected_choice_id=selected_choice_id,
    )


def render_rover_section(is_night: bool = True):
    """Renders the guided task-oriented ROVER AI Assistant section on the homepage."""

    # 1. Initialize session state
    if "rover_chat_messages" not in st.session_state:
        st.session_state["rover_chat_messages"] = [
            {"role": "assistant", "content": INITIAL_WELCOME_MESSAGE}
        ]

    if "rover_workflow" not in st.session_state:
        st.session_state["rover_workflow"] = "main"

    if "rover_step" not in st.session_state:
        st.session_state["rover_step"] = "menu"

    if "rover_choices" not in st.session_state:
        st.session_state["rover_choices"] = MAIN_MENU_CHOICES

    # 2. Get backend status
    status_info = chat_service.get_status()
    is_configured = status_info.get("configured", False)
    provider_name = status_info.get("provider", "gemini").upper()
    model_name = status_info.get("model", "gemini-2.0-flash")
    mascot_src = get_mascot_base64("default")

    # 3. Section Heading & Subtitle
    st.markdown(
        f"""
        <div class="rover-container">
            <div class="rover-header-strip">
                <div>
                    <h2 class="rover-header-title">🤖 Meet Your AI Infrastructure Assistant</h2>
                    <p class="rover-header-sub">
                        Your intelligent companion for understanding road conditions, predicting infrastructure failures, and exploring maintenance insights.
                    </p>
                </div>
                <div style="display: flex; align-items: center; gap: 8px;">
                    <div class="rover-status-badge">
                        <span class="{'rover-status-dot-active' if is_configured else 'rover-status-dot-warn'}"></span>
                        <span>{'CONNECTED · ' + provider_name if is_configured else 'TASK-MODE READY · ' + provider_name}</span>
                    </div>
                </div>
            </div>
        """,
        unsafe_allow_html=True,
    )

    # 4. Two-Column Desktop Layout
    col_mascot, col_chat = st.columns([1.1, 1.9], gap="large")

    with col_mascot:
        # Mascot Visual & Identity Card (Using new official mascot image)
        mascot_img_html = (
            f'<img src="{mascot_src}" class="mascot-avatar-img" alt="ROVER Road Mascot" />'
            if mascot_src
            else '<div style="font-size: 72px; padding-top: 30px;">🤖</div>'
        )

        st.markdown(
            f"""
            <div class="rover-mascot-card">
                <div class="mascot-avatar-wrapper">
                    {mascot_img_html}
                    <div class="mascot-radar-pulse"></div>
                </div>
                <div class="rover-identity-name">ROVER</div>
                <div class="rover-identity-sub">Road Operations & Vulnerability Evaluation Robot</div>
                <div class="rover-speech-bubble">
                    “Hello! I am ROVER 👋 Your AI assistant for road infrastructure, predictive maintenance and smarter decisions.”
                </div>
                <div style="font-size: 11px; opacity: 0.75; margin-bottom: 12px;">
                    Engine: <strong>{provider_name} ({model_name})</strong>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # 3 Compact Information Blocks (Requirement 7)
        st.markdown(
            """
            <div class="rover-feature-grid">
                <div class="rover-feature-tile">
                    <div class="rover-feature-label">🔍 Understand</div>
                    <p class="rover-feature-text">Learn about infrastructure failure prediction and road damage detection.</p>
                </div>
                <div class="rover-feature-tile">
                    <div class="rover-feature-label">🗺️ Explore</div>
                    <p class="rover-feature-text">Get guidance on the dashboard's tools, metrics, and visualizations.</p>
                </div>
                <div class="rover-feature-tile">
                    <div class="rover-feature-label">⚡ Improve</div>
                    <p class="rover-feature-text">Understand maintenance optimization and model evaluation.</p>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col_chat:
        st.markdown(
            f"""
            <div class="rover-chat-wrapper">
                <div class="chat-top-navbar">
                    <div class="chat-top-brand">
                        <span style="font-size: 20px;">🤖</span>
                        <div>
                            <strong style="color: {'#fecb00' if is_night else '#b45309'}; font-size: 15px;">ROVER</strong>
                            <small style="opacity: 0.75; font-size: 12px; margin-left: 6px;">
                                Guided Task Assistant · Workflow: {st.session_state['rover_workflow'].replace('_', ' ').title()}
                            </small>
                        </div>
                    </div>
                </div>
            """,
            unsafe_allow_html=True,
        )

        # Control Bar: Back, Main Menu, Reset Chat
        ctl_c1, ctl_c2, ctl_c3 = st.columns([1.2, 1.2, 1.2])
        is_in_substep = st.session_state["rover_workflow"] != "main" or st.session_state["rover_step"] != "menu"

        if is_in_substep:
            with ctl_c1:
                if st.button("↩️ Back", key="btn_rover_back", use_container_width=True):
                    res = _query_rover_backend(
                        workflow=st.session_state["rover_workflow"],
                        step=st.session_state["rover_step"],
                        selected_choice_id="back",
                    )
                    st.session_state["rover_workflow"] = res.get("workflow", "main")
                    st.session_state["rover_step"] = res.get("step", "menu")
                    st.session_state["rover_choices"] = res.get("choices", MAIN_MENU_CHOICES)
                    st.session_state["rover_chat_messages"].append(
                        {"role": "assistant", "content": res.get("response", "")}
                    )
                    st.rerun()

        with ctl_c2:
            if st.button("🏠 Main Menu", key="btn_rover_home", use_container_width=True):
                res = _query_rover_backend(selected_choice_id="menu")
                st.session_state["rover_workflow"] = "main"
                st.session_state["rover_step"] = "menu"
                st.session_state["rover_choices"] = MAIN_MENU_CHOICES
                st.session_state["rover_chat_messages"].append(
                    {"role": "assistant", "content": res.get("response", INITIAL_WELCOME_MESSAGE)}
                )
                st.rerun()

        with ctl_c3:
            if st.button("🗑️ Reset Chat", key="btn_rover_reset_all", use_container_width=True):
                st.session_state["rover_workflow"] = "main"
                st.session_state["rover_step"] = "menu"
                st.session_state["rover_choices"] = MAIN_MENU_CHOICES
                st.session_state["rover_chat_messages"] = [
                    {"role": "assistant", "content": INITIAL_WELCOME_MESSAGE}
                ]
                st.rerun()

        # Conversation History Container
        chat_box = st.container(height=340)
        with chat_box:
            for turn in st.session_state["rover_chat_messages"]:
                is_user = turn.get("role") == "user"
                if is_user:
                    st.markdown(
                        f"""
                        <div class="chat-bubble chat-bubble-user">
                            <div class="bubble-speaker-tag">👤 Highway Engineer / You</div>
                            <div>{turn.get('content', '')}</div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
                else:
                    st.markdown(
                        f"""
                        <div class="chat-bubble chat-bubble-rover">
                            <div class="bubble-speaker-tag">🤖 ROVER AI Assistant</div>
                            <div>{turn.get('content', '')}</div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

        # Interactive Choice Cards (Requirement 1 & 2)
        current_choices = st.session_state.get("rover_choices", MAIN_MENU_CHOICES)
        if current_choices:
            st.markdown(
                f"<div class='rover-chips-title'>👉 Select a Guided Task Option:</div>",
                unsafe_allow_html=True,
            )

            # Render 2x2 or 3x2 grid of choice cards
            num_choices = len(current_choices)
            cols = st.columns(min(num_choices, 2))

            for idx, choice in enumerate(current_choices):
                col = cols[idx % len(cols)]
                btn_label = f"{choice.get('label', 'Option')}"
                btn_desc = choice.get("description", "")

                with col:
                    clicked = st.button(
                        f"{btn_label}\n\n*{btn_desc}*",
                        key=f"choice_btn_{idx}_{choice.get('id')}",
                        use_container_width=True,
                    )
                    if clicked:
                        # Append choice selection to user history
                        st.session_state["rover_chat_messages"].append(
                            {"role": "user", "content": f"Selected: **{choice.get('label')}**"}
                        )

                        # Check if this choice has a navigation action
                        payload = choice.get("payload") or {}
                        if choice.get("action_type") == "navigate" and "page" in payload:
                            target_page = payload["page"]
                            st.session_state["current_page"] = target_page
                            st.rerun()

                        # Process state machine transition via backend
                        with st.spinner("🤖 ROVER is processing your selection..."):
                            result = _query_rover_backend(
                                workflow=choice.get("workflow") or st.session_state["rover_workflow"],
                                step=choice.get("step") or st.session_state["rover_step"],
                                selected_choice_id=choice.get("id"),
                            )

                        # If navigation action was returned by backend
                        if result.get("action_executed") == "navigate":
                            nav_data = result.get("action_data") or {}
                            if "page" in nav_data:
                                st.session_state["current_page"] = nav_data["page"]
                                st.rerun()

                        st.session_state["rover_workflow"] = result.get("workflow", st.session_state["rover_workflow"])
                        st.session_state["rover_step"] = result.get("step", st.session_state["rover_step"])
                        st.session_state["rover_choices"] = result.get("choices", MAIN_MENU_CHOICES)
                        st.session_state["rover_chat_messages"].append(
                            {"role": "assistant", "content": result.get("response", "")}
                        )
                        st.rerun()

        # Free-Chat Input Bar (Requirement 3: users can ask arbitrary questions at any time)
        free_text_query = st.chat_input(
            "Type any question about the project or select an option above...",
            key="rover_main_chat_input",
        )

        if free_text_query:
            # 1. Append user message
            st.session_state["rover_chat_messages"].append(
                {"role": "user", "content": free_text_query}
            )

            # 2. Build history payload
            history_payload = [
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state["rover_chat_messages"][:-1]
            ]

            # 3. Query backend with context
            with st.spinner("🤖 ROVER is analyzing project telemetry and reasoning..."):
                response_data = _query_rover_backend(
                    message=free_text_query,
                    history=history_payload,
                    workflow=st.session_state["rover_workflow"],
                    step=st.session_state["rover_step"],
                )

            assistant_reply = response_data.get(
                "response",
                "⚠️ I was unable to generate a response. Please check backend connection.",
            )

            # Update workflow, step, and follow-up choices
            st.session_state["rover_workflow"] = response_data.get("workflow", st.session_state["rover_workflow"])
            st.session_state["rover_step"] = response_data.get("step", "follow_up")
            st.session_state["rover_choices"] = response_data.get("choices", MAIN_MENU_CHOICES)
            st.session_state["rover_chat_messages"].append(
                {"role": "assistant", "content": assistant_reply}
            )
            st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)  # Close rover-chat-wrapper

    # Close rover-container
    st.markdown("</div>", unsafe_allow_html=True)
