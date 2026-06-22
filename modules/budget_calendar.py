import streamlit as st
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

    months = [
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

    month_abbr = selected_month.split("-")[0]
    year_suffix = selected_month.split("-")[1]

    month_number = datetime.strptime(
        month_abbr,
        "%b"
    ).month

    year = int("20" + year_suffix)

    with col3:
        selected_day = st.number_input(
            "Select Date",
            min_value=1,
            max_value=calendar.monthrange(year, month_number)[1],
            value=1
        )

    budget = DUMMY_BUDGETS[selected_university][selected_month]

    selected_date = datetime(
        year,
        month_number,
        int(selected_day)
    ).date()

    st.markdown("---")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "University",
        selected_university
    )

    col2.metric(
        "Month",
        selected_month
    )

    col3.metric(
        "Selected Date",
        selected_date.strftime("%d-%b-%Y")
    )

    col4.metric(
        "Allocated Budget",
        f"₹{budget:,.0f}"
    )

    st.subheader(f"Calendar View - {selected_month}")

    cal = calendar.monthcalendar(
        year,
        month_number
    )

    week_days = [
        "Mon",
        "Tue",
        "Wed",
        "Thu",
        "Fri",
        "Sat",
        "Sun"
    ]

    header_cols = st.columns(7)

    for i, day_name in enumerate(week_days):
        header_cols[i].markdown(
            f"<div style='text-align:center; font-weight:700;'>{day_name}</div>",
            unsafe_allow_html=True
        )

    for week in cal:

        cols = st.columns(7)

        for i, day in enumerate(week):

            with cols[i]:

                if day == 0:

                    st.markdown(
                        """
                        <div style="
                            height:78px;
                            background:transparent;
                        "></div>
                        """,
                        unsafe_allow_html=True
                    )

                else:

                    is_selected = day == selected_day

                    if is_selected:
                        background = "#DBEAFE"
                        border = "#2563EB"
                        color = "#1E3A8A"
                    else:
                        background = "#FFFFFF"
                        border = "#E5E7EB"
                        color = "#111827"

                    st.markdown(
                        f"""
                        <div style="
                            background:{background};
                            border:1.5px solid {border};
                            border-radius:14px;
                            padding:14px;
                            height:78px;
                            text-align:center;
                            box-shadow:0 4px 12px rgba(15,23,42,0.04);
                        ">
                            <div style="
                                font-size:22px;
                                font-weight:800;
                                color:{color};
                            ">
                                {day}
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

    st.markdown("---")

    st.subheader("Budget Details")

    detail_col1, detail_col2 = st.columns(2)

    with detail_col1:

        st.markdown(
            f"""
            <div style="
                background:white;
                padding:22px;
                border-radius:16px;
                border:1px solid #E5E7EB;
                box-shadow:0 6px 18px rgba(15,23,42,0.05);
            ">
                <h4 style="margin-bottom:16px;">Selection Summary</h4>
                <p><b>University:</b> {selected_university}</p>
                <p><b>Month:</b> {selected_month}</p>
                <p><b>Date:</b> {selected_date.strftime("%d-%b-%Y")}</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    with detail_col2:

        st.markdown(
            f"""
            <div style="
                background:white;
                padding:22px;
                border-radius:16px;
                border:1px solid #E5E7EB;
                box-shadow:0 6px 18px rgba(15,23,42,0.05);
            ">
                <h4 style="margin-bottom:16px;">Budget Result</h4>
                <p><b>Allocated Budget:</b></p>
                <h2 style="color:#2563EB;">₹{budget:,.0f}</h2>
                <p style="color:#16A34A;"><b>Status:</b> Budget Available</p>
            </div>
            """,
            unsafe_allow_html=True
        )
