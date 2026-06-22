import streamlit as st
import pandas as pd
import calendar
from datetime import datetime

DUMMY_BUDGETS = {
    "Chandigarh University": {
        "Apr-26": 100000,
        "May-26": 120000,
        "Jun-26": 90000,
        "Jul-26": 150000,
        "Aug-26": 110000,
        "Sep-26": 130000,
        "Oct-26": 95000,
        "Nov-26": 140000,
        "Dec-26": 160000,
        "Jan-27": 125000,
        "Feb-27": 115000,
        "Mar-27": 135000
    },
    "Sharda University": {
        "Apr-26": 80000,
        "May-26": 95000,
        "Jun-26": 70000,
        "Jul-26": 110000,
        "Aug-26": 90000,
        "Sep-26": 100000,
        "Oct-26": 85000,
        "Nov-26": 95000,
        "Dec-26": 120000,
        "Jan-27": 90000,
        "Feb-27": 85000,
        "Mar-27": 100000
    },
    "Galgotias University": {
        "Apr-26": 60000,
        "May-26": 75000,
        "Jun-26": 65000,
        "Jul-26": 90000,
        "Aug-26": 70000,
        "Sep-26": 85000,
        "Oct-26": 75000,
        "Nov-26": 80000,
        "Dec-26": 95000,
        "Jan-27": 70000,
        "Feb-27": 65000,
        "Mar-27": 80000
    }
}


def show_budget_calendar():

    st.header("Budget Calendar")

    col1, col2, col3 = st.columns(3)

    with col1:
        selected_date = st.date_input(
            "Select Date",
            value=datetime.today()
        )

    with col2:
        selected_month = st.selectbox(
            "Select Month",
            [
                "Apr-26",
                "May-26",
                "Jun-26",
                "Jul-26",
                "Aug-26",
                "Sep-26",
                "Oct-26",
                "Nov-26",
                "Dec-26",
                "Jan-27",
                "Feb-27",
                "Mar-27"
            ]
        )

    with col3:
        selected_university = st.selectbox(
            "Select University",
            list(DUMMY_BUDGETS.keys())
        )

    budget = DUMMY_BUDGETS[selected_university][selected_month]

    st.subheader("Budget Result")

    col1, col2, col3 = st.columns(3)

    col1.metric("Selected Date", selected_date.strftime("%d-%b-%Y"))
    col2.metric("University", selected_university)
    col3.metric("Budget", f"₹{budget:,.0f}")

    month_abbr = selected_month.split("-")[0]
    year_suffix = selected_month.split("-")[1]

    month_number = datetime.strptime(month_abbr, "%b").month
    year = int("20" + year_suffix)

    st.subheader(f"Calendar View - {selected_month}")

    cal = calendar.monthcalendar(year, month_number)

    week_days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

    header_cols = st.columns(7)

    for i, day in enumerate(week_days):
        header_cols[i].markdown(f"**{day}**")

    for week in cal:

        cols = st.columns(7)

        for i, day in enumerate(week):

            with cols[i]:

                if day == 0:
                    st.write("")
                else:
                    current_day = datetime(year, month_number, day).date()

                    if current_day == selected_date:
                        bg_color = "#DBEAFE"
                        border_color = "#2563EB"
                    else:
                        bg_color = "#FFFFFF"
                        border_color = "#E5E7EB"

                    st.markdown(
                        f"""
                        <div style="
                            background:{bg_color};
                            border:1px solid {border_color};
                            border-radius:12px;
                            padding:10px;
                            min-height:90px;
                        ">
                            <b>{day}</b><br>
                            <span style="font-size:13px;">₹{budget:,.0f}</span>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
