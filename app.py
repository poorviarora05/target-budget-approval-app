import streamlit as st
from auth import init_session, login_page, logout_button
from modules.dashboard import show_dashboard
from modules.create_request import show_create_request
from modules.mediator_budget_check import show_mediator_budget_check
from modules.director_approval import show_director_approval
from modules.submit_invoice import show_submit_invoice
from modules.invoice_approval import show_invoice_approval

# ---------------- PAGE CONFIG ---------------- #

st.set_page_config(
    page_title="TBAS Portal",
    page_icon="✨",
    layout="wide"
)

# ---------------- CUSTOM CSS ---------------- #

st.markdown(
    """
    <style>

    .main {
        background: linear-gradient(
            135deg,
            #f5f7fb,
            #eef2ff
        );
    }

    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 2rem;
        padding-left: 2rem;
        padding-right: 2rem;
    }

    section[data-testid="stSidebar"] {
        background: linear-gradient(
            180deg,
            #111827,
            #1f2937
        );
        border-right: 1px solid rgba(255,255,255,0.08);
    }

    section[data-testid="stSidebar"] * {
        color: white !important;
    }

    .hero-card {
        background: rgba(255,255,255,0.75);
        backdrop-filter: blur(14px);
        padding: 30px;
        border-radius: 24px;
        border: 1px solid rgba(255,255,255,0.25);
        box-shadow: 0 10px 30px rgba(0,0,0,0.08);
        margin-bottom: 24px;
    }

    .hero-title {
        font-size: 52px;
        font-weight: 800;
        color: #111827;
        margin-bottom: 8px;
    }

    .hero-subtitle {
        font-size: 18px;
        color: #6B7280;
    }

    .stButton > button {
        background: linear-gradient(
            135deg,
            #4F46E5,
            #7C3AED
        );

        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.65rem 1.3rem;
        font-weight: 600;
        transition: 0.3s ease;
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 20px rgba(79,70,229,0.25);
    }

    .stTextInput input,
    .stNumberInput input,
    .stTextArea textarea {
        border-radius: 12px !important;
    }

    div[data-testid="metric-container"] {
        background: white;
        border-radius: 18px;
        padding: 14px;
        border: 1px solid #e5e7eb;
        box-shadow: 0 6px 20px rgba(0,0,0,0.04);
    }

    </style>
    """,
    unsafe_allow_html=True
)

# ---------------- SESSION ---------------- #

init_session()

if not st.session_state.logged_in:
    login_page()
    st.stop()

# ---------------- HERO SECTION ---------------- #

st.markdown(
    """
    <div class="hero-card">

        <div class="hero-title">
            Trainer Budget Approval System
        </div>

        <div class="hero-subtitle">
            Smart workflow portal for request creation,
            budget validation, approvals and invoice tracking.
        </div>

    </div>
    """,
    unsafe_allow_html=True
)

# ---------------- SIDEBAR ---------------- #

role = st.session_state.role

st.sidebar.markdown("# ✨ TBAS Portal")

st.sidebar.markdown("---")

st.sidebar.markdown(
    f"### 👤 Logged in as: `{role}`"
)

logout_button()

# ---------------- MENU ---------------- #

if role == "Requester":

    menu_options = [
        "📝 Create Request",
        "📊 Dashboard"
    ]

elif role == "Mediator":

    menu_options = [
        "💰 Budget Check",
        "📊 Dashboard"
    ]

elif role == "Director":

    menu_options = [
        "✅ Director Approval",
        "📄 Invoice Approval",
        "📊 Dashboard"
    ]

elif role == "Trainer":

    menu_options = [
        "📤 Submit Invoice",
        "📊 Dashboard"
    ]

else:

    menu_options = [
        "📊 Dashboard"
    ]

menu = st.sidebar.radio(
    "Navigation",
    menu_options
)

# ---------------- ROUTING ---------------- #

if menu == "📊 Dashboard":

    show_dashboard(
        st.session_state.role,
        st.session_state.username
    )

elif menu == "📝 Create Request":

    show_create_request(
        st.session_state.username
    )

elif menu == "💰 Budget Check":

    show_mediator_budget_check()

elif menu == "✅ Director Approval":

    show_director_approval()

elif menu == "📤 Submit Invoice":

    show_submit_invoice()

elif menu == "📄 Invoice Approval":

    show_invoice_approval()