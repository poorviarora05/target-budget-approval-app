import streamlit as st

from auth import init_session, login_page, logout_button

from modules.director_approval import show_director_approval
from modules.invoice_approval import show_invoice_approval
from modules.submit_invoice import show_submit_invoice
from modules.mediator_budget_check import show_mediator_budget_check
from modules.create_request import show_create_request
from modules.dashboard import show_dashboard
from modules.budget_calendar import show_budget_calendar
from modules.ui import apply_global_ui


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Trainer Budget Approval Tool",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# APP-SPECIFIC UI
# =========================================================

def apply_app_shell_ui():
    st.markdown(
        """
        <style>
        .sidebar-brand {
            padding: 12px 4px 18px 4px;
            margin-bottom: 8px;
        }

        .sidebar-brand-title {
            color: #ffffff;
            font-size: 21px;
            font-weight: 900;
            line-height: 1.2;
            letter-spacing: -0.03em;
        }

        .sidebar-brand-subtitle {
            color: #c7d2fe;
            font-size: 12px;
            font-weight: 650;
            margin-top: 6px;
            line-height: 1.4;
        }

        .sidebar-user-card {
            background: rgba(255, 255, 255, 0.10);
            border: 1px solid rgba(255, 255, 255, 0.14);
            border-radius: 16px;
            padding: 14px;
            margin-top: 4px;
            margin-bottom: 18px;
            box-shadow: 0 10px 24px rgba(15, 23, 42, 0.16);
        }

        .sidebar-user-label {
            color: #c7d2fe;
            font-size: 11px;
            font-weight: 750;
            text-transform: uppercase;
            letter-spacing: 0.08em;
        }

        .sidebar-user-name {
            color: #ffffff;
            font-size: 14px;
            font-weight: 850;
            margin-top: 5px;
            overflow-wrap: anywhere;
        }

        .sidebar-user-email {
            color: #cbd5e1;
            font-size: 11px;
            font-weight: 600;
            margin-top: 4px;
            overflow-wrap: anywhere;
        }

        .sidebar-user-role {
            display: inline-block;
            color: #ffffff;
            background: rgba(99, 102, 241, 0.34);
            border: 1px solid rgba(165, 180, 252, 0.24);
            border-radius: 999px;
            padding: 5px 10px;
            margin-top: 10px;
            font-size: 11px;
            font-weight: 800;
        }

        .sidebar-navigation-label {
            color: #c7d2fe;
            font-size: 11px;
            font-weight: 800;
            text-transform: uppercase;
            letter-spacing: 0.10em;
            margin: 8px 4px 10px 4px;
        }

        .app-hero {
            background:
                linear-gradient(
                    135deg,
                    rgba(255, 255, 255, 0.98),
                    rgba(248, 250, 252, 0.95)
                );
            border: 1px solid #e2e8f0;
            border-radius: 22px;
            padding: 23px 25px;
            margin-bottom: 20px;
            box-shadow: 0 12px 30px rgba(15, 23, 42, 0.06);
        }

        .app-hero-top {
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            gap: 18px;
        }

        .app-hero-title {
            color: #0f172a;
            font-size: 29px;
            font-weight: 900;
            line-height: 1.2;
            letter-spacing: -0.035em;
        }

        .app-hero-subtitle {
            color: #64748b;
            font-size: 14px;
            font-weight: 550;
            line-height: 1.6;
            margin-top: 7px;
            max-width: 780px;
        }

        .role-pill {
            display: inline-flex;
            align-items: center;
            white-space: nowrap;
            background: #eef2ff;
            color: #4338ca;
            border: 1px solid #c7d2fe;
            border-radius: 999px;
            padding: 8px 13px;
            font-size: 12px;
            font-weight: 850;
        }

        @media (max-width: 850px) {
            .app-hero-top {
                display: block;
            }

            .role-pill {
                margin-top: 14px;
            }

            .app-hero-title {
                font-size: 25px;
            }
        }
        </style>
        """,
        unsafe_allow_html=True
    )


# =========================================================
# SESSION AND LOGIN
# =========================================================

init_session()

if not st.session_state.logged_in:
    login_page()
    st.stop()


# =========================================================
# PORTAL UI
# =========================================================

apply_global_ui()
apply_app_shell_ui()


# =========================================================
# LOGGED-IN USER
# =========================================================

role = st.session_state.get("role", "")
username = st.session_state.get("username", "")
email = st.session_state.get("email", "")

display_name = username or email or "User"


# =========================================================
# ROLE-BASED NAVIGATION
# =========================================================

if role == "Requester":
    menu_options = [
        "Create Training Request",
        "Budget Calendar",
        "Dashboard"
    ]

elif role in ["Mediator", "Approver"]:
    menu_options = [
        "Approver Budget Check",
        "Budget Calendar",
        "Dashboard"
    ]

elif role == "Partner":
    menu_options = [
        "Partner Approval",
        "Budget Calendar",
        "Dashboard"
    ]

elif role == "Trainer":
    menu_options = [
        "Submit Invoice",
        "Budget Calendar",
        "Dashboard"
    ]

else:
    menu_options = [
        "Budget Calendar",
        "Dashboard"
    ]


# =========================================================
# SIDEBAR BRAND
# =========================================================

sidebar_brand_html = (
    '<div class="sidebar-brand">'
    '<div class="sidebar-brand-title">Trainer Budget</div>'
    '<div class="sidebar-brand-subtitle">'
    'Approval Management Portal'
    '</div>'
    '</div>'
)

st.sidebar.markdown(
    sidebar_brand_html,
    unsafe_allow_html=True
)


# =========================================================
# SIDEBAR USER CARD
# =========================================================

email_html = ""

if email and email != display_name:
    email_html = (
        f'<div class="sidebar-user-email">{email}</div>'
    )

sidebar_user_html = (
    '<div class="sidebar-user-card">'
    '<div class="sidebar-user-label">Signed in as</div>'
    f'<div class="sidebar-user-name">{display_name}</div>'
    f'{email_html}'
    f'<div class="sidebar-user-role">{role}</div>'
    '</div>'
)

st.sidebar.markdown(
    sidebar_user_html,
    unsafe_allow_html=True
)


# =========================================================
# SIDEBAR NAVIGATION
# =========================================================

navigation_label_html = (
    '<div class="sidebar-navigation-label">'
    'Navigation'
    '</div>'
)

st.sidebar.markdown(
    navigation_label_html,
    unsafe_allow_html=True
)


menu = st.sidebar.radio(
    label="Navigation",
    options=menu_options,
    label_visibility="collapsed",
    key="main_navigation"
)


# =========================================================
# LOGOUT
# =========================================================

logout_button()


# =========================================================
# MAIN HERO
# =========================================================

hero_html = (
    '<div class="app-hero">'
    '<div class="app-hero-top">'
    '<div>'
    '<div class="app-hero-title">'
    'Trainer Budget Approval Portal'
    '</div>'
    '<div class="app-hero-subtitle">'
    'Manage training requests, budget validation, approvals, '
    'calendars and invoices through one centralized workflow.'
    '</div>'
    '</div>'
    f'<div class="role-pill">{role} Workspace</div>'
    '</div>'
    '</div>'
)

st.markdown(
    hero_html,
    unsafe_allow_html=True
)


# =========================================================
# PAGE ROUTING
# =========================================================

if menu == "Dashboard":
    show_dashboard(
        st.session_state.role,
        st.session_state.username
    )

elif menu == "Create Training Request":
    show_create_request(
        st.session_state.username
    )

elif menu == "Budget Calendar":
    show_budget_calendar()

elif menu == "Approver Budget Check":
    show_mediator_budget_check()

elif menu == "Partner Approval":
    show_director_approval()

elif menu == "Submit Invoice":
    show_submit_invoice()

elif menu == "Partner Invoice Approval":
    show_invoice_approval()

else:
    st.warning("The selected page is not available.")