import streamlit as st
import calendar
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

    months = [
        "Apr-26", "May-26", "Jun-26", "Jul-26",
        "Aug-26", "Sep-26", "Oct-26", "Nov-26",
        "Dec-26", "Jan-27", "Feb-27", "Mar-27"
    ]

    col1, col2, col3 = st.columns(3)

    with col1:
        university = st.selectbox("Select University", list(DUMMY_BUDGETS.keys()))

    with col2:
        selected_month = st.selectbox("Select Month", months)

    month_abbr, year_suffix = selected_month.split("-")
    month_number = datetime.strptime(month_abbr, "%b").month
    year = int("20" + year_suffix)
    max_day = calendar.monthrange(year, month_number)[1]

    with col3:
        selected_date = st.date_input(
            "Select Date",
            value=datetime(year, month_number, 1).date(),
            min_value=datetime(year, month_number, 1).date(),
            max_value=datetime(year, month_number, max_day).date()
        )

    selected_day = selected_date.day
    budget = DUMMY_BUDGETS[university][selected_month]

    st.markdown("---")

    c1, c2, c3 = st.columns(3)
    c1.metric("University", university)
    c2.metric("Selected Date", selected_date.strftime("%d-%b-%Y"))
    c3.metric("Budget", f"₹{budget:,.0f}")

    st.subheader(f"{selected_month} Calendar")

    week_days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    header_cols = st.columns(7)

    for i, day_name in enumerate(week_days):
        header_cols[i].markdown(f"**{day_name}**")

    month_calendar = calendar.monthcalendar(year, month_number)

    for week in month_calendar:
        cols = st.columns(7)

        for i, day in enumerate(week):
            with cols[i]:
                if day == 0:
                    st.write("")
                elif day == selected_day:
                    st.markdown(
                        f"""
                        <div style="
                            background:#DBEAFE;
                            border:2px solid #2563EB;
                            border-radius:14px;
                            padding:22px;
                            text-align:center;
                            font-size:24px;
                            font-weight:800;
                            color:#1D4ED8;
                        ">
                            {day}
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                else:
                    st.markdown(
                        f"""
                        <div style="
                            background:white;
                            border:1px solid #E5E7EB;
                            border-radius:14px;
                            padding:22px;
                            text-align:center;
                            font-size:24px;
                            font-weight:800;
                            color:#111827;
                        ">
                            {day}
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
