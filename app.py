import streamlit as st
from auth import init_session, login_page, logout_button
from modules.dashboard import show_dashboard
from modules.create_request import show_create_request
from modules.mediator_budget_check import show_mediator_budget_check
from modules.director_approval import show_director_approval
from modules.submit_invoice import show_submit_invoice
from modules.invoice_approval import show_invoice_approval

st.set_page_config(
    page_title="Trainer Budget Approval System",
    page_icon="📊",
    layout="wide"
)

st.markdown(
    """
    <style>
    .main {
        background-color: #f7f9fc;
    }

    h1, h2, h3 {
        color: #1f2937;
    }

    .stButton button {
        border-radius: 8px;
        background-color: #2563eb;
        color: white;
        border: none;
        padding: 0.5rem 1rem;
        font-weight: 600;
    }

    .stButton button:hover {
        background-color: #1d4ed8;
        color: white;
    }

    section[data-testid="stSidebar"] {
        background-color: #111827;
    }

    section[data-testid="stSidebar"] * {
        color: white;
    }

    .block-container {
        padding-top: 2rem;
    }
    </style>
    """,
    unsafe_allow_html=True
)

init_session()

if not st.session_state.logged_in:
    login_page()
    st.stop()

st.markdown(
    """
    <h1 style='margin-bottom:0;'>Trainer Budget Approval System</h1>
    <p style='color:#6b7280; font-size:16px;'>
    Role-based portal for training requests, budget validation, approvals and invoices.
    </p>
    """,
    unsafe_allow_html=True
)

logout_button()

role = st.session_state.role

st.sidebar.markdown("## 📊 TBAS Portal")
st.sidebar.markdown(f"**Role:** {role}")
st.sidebar.markdown("---")

if role == "Requester":
    menu_options = [
        "📝 Create Training Request",
        "🏠 Dashboard"
    ]

elif role == "Mediator":
    menu_options = [
        "💰 Mediator Budget Check",
        "🏠 Dashboard"
    ]

elif role == "Director":
    menu_options = [
        "✅ Director Approval",
        "📄 Director Invoice Approval",
        "🏠 Dashboard"
    ]

elif role == "Trainer":
    menu_options = [
        "📤 Submit Invoice",
        "🏠 Dashboard"
    ]

elif role == "Admin":
    menu_options = [
        "📝 Create Training Request",
        "💰 Mediator Budget Check",
        "✅ Director Approval",
        "📤 Submit Invoice",
        "📄 Director Invoice Approval",
        "🏠 Dashboard"
    ]

else:
    menu_options = ["🏠 Dashboard"]

menu = st.sidebar.radio("Navigation", menu_options)

if menu == "🏠 Dashboard":
    show_dashboard(st.session_state.role, st.session_state.username)

elif menu == "📝 Create Training Request":
    show_create_request(st.session_state.username)

elif menu == "💰 Mediator Budget Check":
    show_mediator_budget_check()

elif menu == "✅ Director Approval":
    show_director_approval()

elif menu == "📤 Submit Invoice":
    show_submit_invoice()

elif menu == "📄 Director Invoice Approval":
    show_invoice_approval()