"""ROVER AI Assistant UI Component for the Road Infrastructure Dashboard.

Renders the visual mascot, interactive chat interface, suggested chips,
and project feature overviews in both Night and Day themes.
"""
from __future__ import annotations

import base64
from pathlib import Path
from typing import Any, Dict, List

import requests
import streamlit as st

from app.ai.chat_service import chat_service

# Asset path
ASSET_DIR = Path(__file__).resolve().parents[2] / "data" / "assets"
MASCOT_IMG_PATH = ASSET_DIR / "rover_mascot.jpg"

SUGGESTED_CHIPS = [
    ("1. What can this project do?", "What can this project do?"),
    ("2. How does failure prediction work?", "How does failure prediction work?"),
    ("3. Explain road damage detection", "Explain road damage detection"),
    ("4. Remaining useful life (RUL)?", "What is the predicted remaining useful life?"),
    ("5. Maintenance optimization?", "How does maintenance optimization work?"),
    ("6. Help me navigate dashboard", "Help me navigate the dashboard"),
]

INITIAL_WELCOME_MESSAGE = (
    "👋 **Greetings, Engineer! I am ROVER — Road Operations & Vulnerability Evaluation Robot.**\n\n"
    "I am your built-in AI companion for this Road Infrastructure Predictive Maintenance Suite. "
    "You can ask me about:\n"
    "- 🔮 **Failure Risk Prediction:** How Random Forest & GBDT models forecast structural deterioration across 6 asset categories\n"
    "- 🛣️ **Computer Vision Inspection:** How OpenCV filtering & YOLO locate surface cracks, potholes, and calculate the Road Damage Index (RDI)\n"
    "- ⏳ **Remaining Useful Life (RUL):** How linear regression and random forest regressors estimate lifespan in operational years\n"
    "- ⚡ **Combinatorial Knapsack Optimization:** How Hill Climbing, Beam Search, and Tabu Search allocate repair budgets\n"
    "- 🗺️ **Dashboard Navigation:** Guidance on using all 10 analytical modules\n\n"
    "*Click any suggested question below or type your inquiry to begin!*"
)


@st.cache_data
def get_mascot_base64() -> str:
    """Reads and caches the mascot image as a base64 data URI."""
    if MASCOT_IMG_PATH.exists():
        try:
            with open(MASCOT_IMG_PATH, "rb") as fh:
                encoded = base64.b64encode(fh.read()).decode("utf-8")
                return f"data:image/jpeg;base64,{encoded}"
        except Exception:
            return ""
    return ""


def _query_rover_backend(message: str, history: List[Dict[str, str]]) -> Dict[str, Any]:
    """Communicates with the ROVER backend via FastAPI or directly via python service."""
    # Attempt FastAPI REST call if server is running locally
    try:
        resp = requests.post(
            "http://127.0.0.1:8000/api/chat",
            json={"message": message, "history": history},
            timeout=25,
        )
        if resp.status_code == 200:
            return resp.json()
    except Exception:
        pass

    # Seamless fallback to direct python service
    return chat_service.chat_sync(message=message, history=history)


def render_rover_section(is_night: bool = True):
    """Renders the prominent full-width ROVER AI Assistant section on the homepage."""

    # 1. Initialize session state
    if "rover_chat_messages" not in st.session_state:
        st.session_state["rover_chat_messages"] = [
            {"role": "assistant", "content": INITIAL_WELCOME_MESSAGE}
        ]

    # 2. Get backend status
    status_info = chat_service.get_status()
    is_configured = status_info.get("configured", False)
    provider_name = status_info.get("provider", "gemini").upper()
    model_name = status_info.get("model", "gemini-2.0-flash")
    mascot_src = get_mascot_base64()

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
                        <span>{'CONNECTED · ' + provider_name if is_configured else 'SETUP NEEDED · ' + provider_name}</span>
                    </div>
                </div>
            </div>
        """,
        unsafe_allow_html=True,
    )

    # 4. Two-Column Desktop Layout
    col_mascot, col_chat = st.columns([1.1, 1.9], gap="large")

    with col_mascot:
        # Mascot Visual & Identity Card
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
                    “Ready for civil analysis. I monitor 2,200 municipal assets across 6 structural categories with multi-modal AI.”
                </div>
                <div style="font-size: 11px; opacity: 0.75; margin-bottom: 12px;">
                    LLM Engine: <strong>{provider_name} ({model_name})</strong>
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

        # Quick config helper if unconfigured
        if not is_configured:
            st.info(
                f"ℹ️ **Configure {provider_name}:** Add `GEMINI_API_KEY=your_key` or `XAI_API_KEY=your_key` to `.env` to unlock live responses.",
                icon="🔑",
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
                            <small style="opacity: 0.75; font-size: 12px; margin-left: 6px;">AI Infrastructure Assistant</small>
                        </div>
                    </div>
                </div>
            """,
            unsafe_allow_html=True,
        )

        # Reset button in top right of chat panel
        chat_head_c1, chat_head_c2 = st.columns([3.5, 1.5])
        with chat_head_c2:
            if st.button("🗑️ Reset Chat", key="btn_reset_rover_conversation", use_container_width=True):
                st.session_state["rover_chat_messages"] = [
                    {"role": "assistant", "content": INITIAL_WELCOME_MESSAGE}
                ]
                st.rerun()

        # Conversation History Container
        chat_box = st.container(height=380)
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

        # Suggested Question Chips (Requirement 3)
        st.markdown(
            f"<div style='font-size: 12px; font-weight: 700; color: {'#fecb00' if is_night else '#b45309'}; text-transform: uppercase; margin: 12px 0 6px 0; letter-spacing: 0.5px;'>⚡ Suggested Inquiries for ROVER:</div>",
            unsafe_allow_html=True,
        )
        chip_col1, chip_col2, chip_col3 = st.columns(3)
        for idx, (chip_label, prompt_query) in enumerate(SUGGESTED_CHIPS):
            target_col = [chip_col1, chip_col2, chip_col3][idx % 3]
            if target_col.button(chip_label, key=f"rover_chip_btn_{idx}", use_container_width=True):
                st.session_state["rover_pending_query"] = prompt_query
                st.rerun()

        # Chat Input Box
        chat_input_val = st.chat_input(
            "Ask ROVER about infrastructure, road damage, or predictive maintenance...",
            key="rover_main_chat_input",
        )

        # Processing: Check if user submitted via text or clicked a chip
        query_to_send = None
        if st.session_state.get("rover_pending_query"):
            query_to_send = st.session_state.pop("rover_pending_query")
        elif chat_input_val:
            query_to_send = chat_input_val

        if query_to_send:
            # 1. Append user message to history
            st.session_state["rover_chat_messages"].append(
                {"role": "user", "content": query_to_send}
            )

            # 2. Build history payload for backend
            history_payload = [
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state["rover_chat_messages"][:-1]
            ]

            # 3. Call backend with visual spinner
            with st.spinner("🤖 ROVER is analyzing project telemetry and reasoning..."):
                response_data = _query_rover_backend(
                    message=query_to_send,
                    history=history_payload,
                )

            assistant_reply = response_data.get(
                "response",
                "⚠️ I was unable to generate a response. Please check backend connection.",
            )

            # 4. Append assistant response and refresh
            st.session_state["rover_chat_messages"].append(
                {"role": "assistant", "content": assistant_reply}
            )
            st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)  # Close rover-chat-wrapper

    # Close rover-container
    st.markdown("</div>", unsafe_allow_html=True)
