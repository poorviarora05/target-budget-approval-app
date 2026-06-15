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
    page_icon="📊",
    layout="wide"
)

# ---------------- CUSTOM CSS ---------------- #

st.markdown("""
<style>

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

.stApp {
    background: linear-gradient(
        135deg,
        #F8FAFC,
        #EEF2FF
    );
}

section[data-testid="stSidebar"] {
    background: linear-gradient(
        180deg,
        #0F172A,
        #1E293B
    );
}

section[data-testid="stSidebar"] * {
    color: white !important;
}

.stButton button {

    border-radius: 12px;

    background: linear-gradient(
        135deg,
        #4F46E5,
        #7C3AED
    );

    color: white;

    border: none;

    font-weight: 700;
}

.stTextInput input,
.stNumberInput input,
.stTextArea textarea,
.stSelectbox div {

    border-radius: 12px !important;
}

div[data-testid="metric-container"] {

    background: white;

    border-radius: 18px;

    padding: 16px;

    border: 1px solid #E5E7EB;

    box-shadow:
        0 8px 20px rgba(0,0,0,0.05);
}

</style>
""", unsafe_allow_html=True)

# ---------------- SESSION ---------------- #

init_session()

if not st.session_state.logged_in:
    login_page()
    st.stop()

# ---------------- HEADER ---------------- #

st.title("📊 Trainer Budget Approval System")

st.caption(
    "Enterprise workflow portal for training requests, budget validation, approvals and invoice tracking."
)

st.markdown("---")

# ---------------- SIDEBAR ---------------- #

role = st.session_state.role

st.sidebar.markdown("## 📊 TBAS Portal")

st.sidebar.markdown(
    f"### Role: {role}"
)

st.sidebar.markdown("---")

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

# ---------------- SIDEBAR NAVIGATION ---------------- #

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