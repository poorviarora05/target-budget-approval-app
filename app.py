import streamlit as st
from auth import init_session, login_page, logout_button
from modules.dashboard import show_dashboard
from modules.create_request import show_create_request
from modules.mediator_budget_check import show_mediator_budget_check
from modules.director_approval import show_director_approval
from modules.submit_invoice import show_submit_invoice
from modules.invoice_approval import show_invoice_approval

st.set_page_config(
    page_title="TBAS Portal",
    page_icon="",
    layout="wide"
)

st.markdown("""
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

.stApp {
    background: #F5F7FB;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
}

section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0B1220 0%, #111827 100%);
}

section[data-testid="stSidebar"] * {
    color: white !important;
}

.sidebar-title {
    font-size: 25px;
    font-weight: 800;
    letter-spacing: 0.3px;
    margin-bottom: 4px;
}

.sidebar-subtitle {
    font-size: 13px;
    color: #CBD5E1 !important;
    margin-bottom: 24px;
}

.sidebar-meta {
    background: rgba(255,255,255,0.08);
    padding: 14px;
    border-radius: 12px;
    border: 1px solid rgba(255,255,255,0.08);
    margin-bottom: 18px;
}

.hero-card {
    background: #FFFFFF;
    padding: 34px 40px;
    border-radius: 20px;
    border: 1px solid #E5E7EB;
    box-shadow: 0 10px 25px rgba(15,23,42,0.06);
    margin-bottom: 28px;
}

.hero-title {
    font-size: 42px;
    font-weight: 800;
    color: #0F172A;
    margin-bottom: 8px;
}

.hero-subtitle {
    font-size: 16px;
    color: #64748B;
}

.stButton button {
    border-radius: 10px;
    background: #2563EB;
    color: white;
    border: none;
    font-weight: 700;
}

.stButton button:hover {
    background: #1D4ED8;
    color: white;
}

.stTextInput input,
.stNumberInput input,
.stTextArea textarea {
    border-radius: 10px !important;
}

div[data-testid="metric-container"] {
    background: white;
    border-radius: 14px;
    padding: 16px;
    border: 1px solid #E5E7EB;
    box-shadow: 0 6px 18px rgba(15,23,42,0.05);
}

div[role="radiogroup"] label {
    background: rgba(255,255,255,0.08);
    padding: 11px 13px;
    border-radius: 10px;
    margin-bottom: 8px;
    border: 1px solid rgba(255,255,255,0.08);
}

div[role="radiogroup"] label:hover {
    background: rgba(255,255,255,0.15);
}
</style>
""", unsafe_allow_html=True)


init_session()

if not st.session_state.logged_in:
    login_page()
    st.stop()


role = st.session_state.role
username = st.session_state.username

st.sidebar.markdown("""
<div class="sidebar-title">TBAS Portal</div>
<div class="sidebar-subtitle">Training Budget Approval System</div>
""", unsafe_allow_html=True)

st.sidebar.markdown(
    f"""
    <div class="sidebar-meta">
        <b>Role</b><br>{role}<br><br>
        <b>Logged in as</b><br>{username}
    </div>
    """,
    unsafe_allow_html=True
)

logout_button()

st.sidebar.markdown("---")

if role == "Requester":
    menu_options = [
        "Create Request",
        "Dashboard"
    ]

elif role == "Approver":
    menu_options = [
        "Approver Review",
        "Dashboard"
    ]

elif role == "Partner":
    menu_options = [
        "Partner Approval",
        "Invoice Approval",
        "Dashboard"
    ]

elif role == "Trainer":
    menu_options = [
        "Submit Invoice",
        "Dashboard"
    ]

else:
    menu_options = [
        "Dashboard"
    ]

menu = st.sidebar.radio("Navigation", menu_options)


st.markdown("""
<div class="hero-card">
    <div class="hero-title">Trainer Budget Approval System</div>
    <div class="hero-subtitle">
        Enterprise workflow portal for training requests, budget validation, approvals and invoice management.
    </div>
</div>
""", unsafe_allow_html=True)


if menu == "Dashboard":
    show_dashboard(
        role,
        username
    )

elif menu == "Create Request":
    show_create_request(
        username
    )

elif menu == "Approver Review":
    show_mediator_budget_check()

elif menu == "Partner Approval":
    show_director_approval()

elif menu == "Submit Invoice":
    show_submit_invoice()

elif menu == "Invoice Approval":
    show_invoice_approval()