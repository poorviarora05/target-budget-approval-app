import streamlit as st
from streamlit_calendar import calendar
from datetime import datetime

DUMMY_BUDGETS = {
    "Chandigarh University": {
        "Apr-26": 100000, "May-26": 120000, "Jun-26": 90000,
        "Jul-26": 150000, "Aug-26": 110000, "Sep-26": 130000,
        "Oct-26": 95000, "Nov-26": 140000, "Dec-26": 160000,
        "Jan-27": 125000, "Feb-27": 115000, "Mar-27": 135000
    },
    "Sharda University": {
        "Apr-26": 80000, "May-26": 95000, "Jun-26": 70000,
        "Jul-26": 110000, "Aug-26": 90000, "Sep-26": 100000,
        "Oct-26": 85000, "Nov-26": 95000, "Dec-26": 120000,
        "Jan-27": 90000, "Feb-27": 85000, "Mar-27": 100000
    },
    "Galgotias University": {
        "Apr-26": 60000, "May-26": 75000, "Jun-26": 65000,
        "Jul-26": 90000, "Aug-26": 70000, "Sep-26": 85000,
        "Oct-26": 75000, "Nov-26": 80000, "Dec-26": 95000,
        "Jan-27": 70000, "Feb-27": 65000, "Mar-27": 80000
    }
}


def show_budget_calendar():

    st.header("Budget Calendar")

    col1, col2, col3 = st.columns(3)

    with col1:
        selected_university = st.selectbox(
            "Select University",
            list(DUMMY_BUDGETS.keys())
        )

    with col2:
        selected_month = st.selectbox(
            "Select Month",
            list(DUMMY_BUDGETS[selected_university].keys())
        )

    month_abbr, year_suffix = selected_month.split("-")
    month_number = datetime.strptime(month_abbr, "%b").month
    year = int("20" + year_suffix)

    budget = DUMMY_BUDGETS[selected_university][selected_month]

    calendar_options = {
        "initialView": "dayGridMonth",
        "initialDate": f"{year}-{month_number:02d}-01",
        "selectable": True,
        "height": 650,
        "headerToolbar": {
            "left": "prev,next today",
            "center": "title",
            "right": "dayGridMonth"
        },
    }

    calendar_events = []

    clicked = calendar(
        events=calendar_events,
        options=calendar_options,
        key=f"calendar_{selected_university}_{selected_month}"
    )

    selected_date = None

    if clicked and "dateClick" in clicked:
        selected_date = clicked["dateClick"]["date"]

    with col3:
        if selected_date:
            st.text_input(
                "Selected Date",
                selected_date,
                disabled=True
            )
        else:
            st.text_input(
                "Selected Date",
                "Click a date in calendar",
                disabled=True
            )

    st.markdown("---")

    if selected_date:
        st.success(f"Selected Date: {selected_date}")

    col1, col2 = st.columns(2)

    col1.metric("University", selected_university)
    col2.metric("Budget", f"₹{budget:,.0f}")
