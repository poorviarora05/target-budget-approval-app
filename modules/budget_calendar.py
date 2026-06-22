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

    st.markdown("""
    <style>
    .calendar-wrapper {
        background: white;
        padding: 28px;
        border-radius: 22px;
        border: 1px solid #E5E7EB;
        box-shadow: 0 10px 28px rgba(15,23,42,0.06);
        margin-top: 18px;
    }

    .calendar-title {
        font-size: 26px;
        font-weight: 800;
        color: #0F172A;
        margin-bottom: 18px;
    }

    .weekday {
        text-align: center;
        font-weight: 800;
        color: #64748B;
        font-size: 14px;
        padding-bottom: 10px;
    }

    .calendar-day {
        height: 88px;
        border-radius: 18px;
        border: 1px solid #E5E7EB;
        background: #F8FAFC;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 24px;
        font-weight: 800;
        color: #0F172A;
        box-shadow: 0 4px 12px rgba(15,23,42,0.04);
    }

    .calendar-day-selected {
        height: 88px;
        border-radius: 18px;
        border: 2px solid #2563EB;
        background: linear-gradient(135deg, #DBEAFE, #EFF6FF);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 26px;
        font-weight: 900;
        color: #1D4ED8;
        box-shadow: 0 8px 22px rgba(37,99,235,0.22);
    }

    .calendar-empty {
        height: 88px;
    }

    .budget-card {
        background: white;
        padding: 24px;
        border-radius: 20px;
        border: 1px solid #E5E7EB;
        box-shadow: 0 10px 24px rgba(15,23,42,0.06);
    }

    .budget-label {
        font-size: 14px;
        color: #64748B;
        font-weight: 700;
        margin-bottom: 8px;
    }

    .budget-value {
        font-size: 30px;
        color: #2563EB;
        font-weight: 900;
    }
    </style>
    """, unsafe_allow_html=True)

    months = [
        "Apr-26", "May-26", "Jun-26", "Jul-26",
        "Aug-26", "Sep-26", "Oct-26", "Nov-26",
        "Dec-26", "Jan-27", "Feb-27", "Mar-27"
    ]

    col1, col2, col3 = st.columns(3)

    with col1:
        selected_university = st.selectbox(
            "Select University",
            list(DUMMY_BUDGETS.keys())
        )

    with col2:
        selected_month = st.selectbox(
            "Select Month",
            months
        )

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
    budget = DUMMY_BUDGETS[selected_university][selected_month]

    st.markdown("---")

    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown(
            f"""
            <div class="budget-card">
                <div class="budget-label">University</div>
                <div style="font-size:20px;font-weight:800;color:#0F172A;">
                    {selected_university}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with c2:
        st.markdown(
            f"""
            <div class="budget-card">
                <div class="budget-label">Selected Date</div>
                <div style="font-size:20px;font-weight:800;color:#0F172A;">
                    {selected_date.strftime("%d %b %Y")}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with c3:
        st.markdown(
            f"""
            <div class="budget-card">
                <div class="budget-label">Allocated Budget</div>
                <div class="budget-value">₹{budget:,.0f}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown(
        f"""
        <div class="calendar-wrapper">
            <div class="calendar-title">{selected_month} Budget Calendar</div>
        """,
        unsafe_allow_html=True
    )

    week_days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    header_cols = st.columns(7)

    for i, day_name in enumerate(week_days):
        header_cols[i].markdown(
            f"<div class='weekday'>{day_name}</div>",
            unsafe_allow_html=True
        )

    cal = calendar.monthcalendar(year, month_number)

    for week in cal:
        cols = st.columns(7)

        for i, day in enumerate(week):
            with cols[i]:
                if day == 0:
                    st.markdown(
                        "<div class='calendar-empty'></div>",
                        unsafe_allow_html=True
                    )
                elif day == selected_day:
                    st.markdown(
                        f"<div class='calendar-day-selected'>{day}</div>",
                        unsafe_allow_html=True
                    )
                else:
                    st.markdown(
                        f"<div class='calendar-day'>{day}</div>",
                        unsafe_allow_html=True
                    )

    st.markdown("</div>", unsafe_allow_html=True)
