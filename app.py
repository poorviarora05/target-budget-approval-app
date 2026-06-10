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
    page_icon="📊",
    layout="wide"
)

st.markdown("""
<style>
.stApp {
    background: #f5f7fb;
}

section[data-testid="stSidebar"] {
    background: #111827;
}

section[data-testid="stSidebar"] * {
    color: white !important;
}

.hero-card {
    background: linear-gradient(135deg, #4F46E5, #7C3AED);
    padding: 28px;
    border-radius: 22px;
    color: white;
    margin-bottom: 25px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.12);
}

.hero-title {
    font-size: 36px;
    font-weight: 800;
}

.hero-subtitle {
    font-size: 16px;
    margin-top: 8px;
    opacity: 0.9;
}

.stButton button {
    border-radius: 10px;
    background: #4F46E5;
    color: white;
    border: none;
    font-weight: 600;
}

.stTextInput input,
.stNumberInput input,
.stTextArea textarea {
    border-radius: 10px !important;
}
</style>
""", unsafe_allow_html=True)

init_session()

if not st.session_state.logged_in:
    login_page()
    st.stop()

st.markdown("""
<div class="hero-card">
    <div class="hero-title">Trainer Budget Approval System</div>
    <div class="hero-subtitle">
        Smart workflow portal for request creation, budget validation, approvals and invoice tracking.
    </div>
</div>
""", unsafe_allow_html=True)

role = st.session_state.role

st.sidebar.markdown("## TBAS Portal")
st.sidebar.markdown(f"**Role:** {role}")
st.sidebar.markdown("---")

logout_button()

if role == "Requester":
    menu_options = ["📝 Create Request", "📊 Dashboard"]

elif role == "Mediator":
    menu_options = ["💰 Budget Check", "📊 Dashboard"]

elif role == "Director":
    menu_options = ["✅ Director Approval", "📄 Invoice Approval", "📊 Dashboard"]

elif role == "Trainer":
    menu_options = ["📤 Submit Invoice", "📊 Dashboard"]

else:
    menu_options = ["📊 Dashboard"]

menu = st.sidebar.radio("Navigation", menu_options)

if menu == "📊 Dashboard":
    show_dashboard(st.session_state.role, st.session_state.username)

elif menu == "📝 Create Request":
    show_create_request(st.session_state.username)

elif menu == "💰 Budget Check":
    show_mediator_budget_check()

elif menu == "✅ Director Approval":
    show_director_approval()

elif menu == "📤 Submit Invoice":
    show_submit_invoice()

elif menu == "📄 Invoice Approval":
    show_invoice_approval()