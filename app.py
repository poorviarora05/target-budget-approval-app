from modules.director_approval import show_director_approval
from modules.invoice_approval import show_invoice_approval
from modules.submit_invoice import show_submit_invoice
from modules.mediator_budget_check import show_mediator_budget_check
from modules.create_request import show_create_request
import streamlit as st
from auth import init_session, login_page, logout_button
from modules.dashboard import show_dashboard

st.set_page_config(
    page_title="Trainer Budget Approval Tool",
    layout="wide"
)

init_session()

if not st.session_state.logged_in:
    login_page()
    st.stop()

st.title("Trainer Budget Approval and Invoice Management System")

logout_button()

role = st.session_state.role

if role == "Requester":
    menu_options = [
        "Create Training Request",
        "Dashboard"
    ]

elif role == "Mediator":
    menu_options = [
        "Mediator Budget Check",
        "Dashboard"
    ]

elif role == "Director":
    menu_options = [
        "Director Approval",
        "Director Invoice Approval",
        "Dashboard"
    ]

elif role == "Trainer":
    menu_options = [
        "Submit Invoice",
        "Dashboard"
    ]

elif role == "Admin":
    menu_options = [
        "Create Training Request",
        "Mediator Budget Check",
        "Director Approval",
        "Submit Invoice",
        "Director Invoice Approval",
        "Dashboard"
    ]

else:
    menu_options = ["Dashboard"]

menu = st.sidebar.selectbox("Choose Module", menu_options)

if menu == "Dashboard":
    show_dashboard(st.session_state.role, st.session_state.username)

elif menu == "Create Training Request":
    show_create_request(st.session_state.username)

elif menu == "Mediator Budget Check":
    show_mediator_budget_check()

elif menu == "Director Approval":
    show_director_approval()

elif menu == "Submit Invoice":
    show_submit_invoice()

elif menu == "Director Invoice Approval":
    show_invoice_approval()