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

.hero-card {
    background: linear-gradient(
        135deg,
        #4F46E5,
        #7C3AED
    );

    padding: 30px;
    border-radius: 24px;
    color: white;
    margin-bottom: 28px;

    box-shadow:
        0 12px 32px rgba(79,70,229,0.25);
}

.hero-title {
    font-size: 38px;
    font-weight: 800;
}

.hero-subtitle {
    font-size: 16px;
    margin-top: 8px;
    opacity: 0.92;
}

.glass-card {
    background: rgba(255,255,255,0.82);

    backdrop-filter: blur(14px);

    border-radius: 22px;

    padding: 24px;

    border: 1px solid rgba(255,255,255,0.45);

    box-shadow:
        0 10px 28px rgba(15,23,42,0.08);

    margin-bottom: 20px;
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

    padding: 0.55rem 1.2rem;
}

.stButton button:hover {

    background: linear-gradient(
        135deg,
        #4338CA,
        #6D28D9
    );

    color: white;
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

# ---------------- HERO SECTION ---------------- #

st.markdown(
    """
    <div class="hero-card">

        <div class="hero-title">
            Trainer Budget Approval System
        </div>

        <div class="hero-subtitle">
            Enterprise workflow portal for training requests,
            budget validation, approvals and invoice tracking.
        </div>

    </div>
    """,
    unsafe_allow_html=True
)

# ---------------- SIDEBAR ---------------- #

role = st.session_state.role

st.sidebar.markdown("## 📊 TBAS Portal")

st.sidebar.markdown(
    f"### Role: {role}"
)

st.sidebar.markdown("---")

logout_button()

# ---------------- MENU OPTIONS ---------------- #

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

# ---------------- SIDEBAR MENU ---------------- #

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