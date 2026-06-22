import streamlit as st
import calendar
from datetime import datetime, date

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

TRAININGS = {
    "Chandigarh University": [
        {"title": "AI/ML Training", "start": date(2026, 7, 1), "end": date(2026, 7, 5), "status": "scheduled"},
        {"title": "University Event", "start": date(2026, 7, 8), "end": date(2026, 7, 10), "status": "blocked"},
        {"title": "Data Science Bootcamp", "start": date(2026, 7, 14), "end": date(2026, 7, 18), "status": "upcoming"},
    ],
    "Sharda University": [
        {"title": "Generative AI Workshop", "start": date(2026, 7, 3), "end": date(2026, 7, 6), "status": "scheduled"},
        {"title": "Cloud Computing", "start": date(2026, 7, 15), "end": date(2026, 7, 17), "status": "upcoming"},
    ],
    "Galgotias University": [
        {"title": "Cyber Security", "start": date(2026, 7, 11), "end": date(2026, 7, 13), "status": "blocked"},
        {"title": "Python Training", "start": date(2026, 7, 22), "end": date(2026, 7, 24), "status": "upcoming"},
    ],
}


def get_month_key(month_number, year):
    return datetime(year, month_number, 1).strftime("%b-%y")


def get_status_for_day(day_date, university):
    for training in TRAININGS.get(university, []):
        if training["start"] <= day_date <= training["end"]:
            return training["status"], training["title"]
    return "available", "Available"


def show_budget_calendar():

    st.markdown("""
    <style>
    .main-title {
        font-size: 38px;
        font-weight: 900;
        color: #0F172A;
        margin-bottom: 4px;
    }

    .sub-title {
        font-size: 16px;
        color: #64748B;
        margin-bottom: 28px;
    }

    .calendar-wrapper {
        background: #FFFFFF;
        border: 1px solid #E5E7EB;
        border-radius: 22px;
        padding: 22px;
        box-shadow: 0 8px 24px rgba(15,23,42,0.06);
    }

    .month-heading {
        text-align: center;
        font-size: 28px;
        font-weight: 900;
        color: #0F172A;
        margin-bottom: 18px;
    }

    .calendar-grid {
        display: grid;
        grid-template-columns: repeat(7, 1fr);
        gap: 10px;
    }

    .weekday {
        text-align: center;
        font-size: 14px;
        font-weight: 800;
        color: #475569;
        padding: 8px 0;
    }

    .day-box {
        height: 78px;
        border-radius: 14px;
        border: 1px solid #E5E7EB;
        padding: 8px;
        background: #FFFFFF;
        box-sizing: border-box;
    }

    .empty-box {
        height: 78px;
        border-radius: 14px;
        background: #F8FAFC;
        opacity: 0.5;
    }

    .day-number {
        font-size: 20px;
        font-weight: 900;
        color: #0F172A;
        line-height: 1;
    }

    .event-chip {
        margin-top: 12px;
        padding: 5px 8px;
        border-radius: 999px;
        font-size: 11px;
        font-weight: 800;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
        text-align: center;
    }

    .scheduled {
        background: #FCE7F3;
        border: 1.5px solid #F9A8D4;
    }

    .blocked {
        background: #FEF3C7;
        border: 1.5px solid #FDE68A;
    }

    .upcoming {
        background: #DCFCE7;
        border: 1.5px solid #86EFAC;
    }

    .available {
        background: #FFFFFF;
    }

    .chip-scheduled {
        background: #F9A8D4;
        color: #831843;
    }

    .chip-blocked {
        background: #FDE68A;
        color: #92400E;
    }

    .chip-upcoming {
        background: #86EFAC;
        color: #166534;
    }

    .side-card {
        background: #FFFFFF;
        border: 1px solid #E5E7EB;
        border-radius: 20px;
        padding: 20px;
        box-shadow: 0 8px 24px rgba(15,23,42,0.06);
        margin-bottom: 18px;
    }

    .legend-item {
        display: flex;
        align-items: center;
        gap: 10px;
        margin-bottom: 12px;
        font-weight: 700;
        color: #334155;
    }

    .dot {
        width: 18px;
        height: 18px;
        border-radius: 50%;
        display: inline-block;
    }

    .pink { background: #F9A8D4; }
    .yellow { background: #FDE68A; }
    .green { background: #86EFAC; }

    .budget-text {
        font-size: 32px;
        font-weight: 900;
        color: #4F46E5;
    }

    .training-title {
        font-weight: 900;
        color: #0F172A;
        font-size: 15px;
    }

    .training-meta {
        color: #64748B;
        font-size: 13px;
        margin-top: 4px;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("<div class='main-title'>📅 Budget & Training Calendar</div>", unsafe_allow_html=True)
    st.markdown("<div class='sub-title'>View training schedules, blocked dates and university budgets</div>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        selected_year = st.selectbox("Select Year", [2026, 2027, 2028, 2029, 2030])

    with col2:
        month_names = [
            "January", "February", "March", "April", "May", "June",
            "July", "August", "September", "October", "November", "December"
        ]
        selected_month_name = st.selectbox("Select Month", month_names, index=6)

    with col3:
        selected_university = st.selectbox("Select University", list(DUMMY_BUDGETS.keys()))

    month_number = month_names.index(selected_month_name) + 1
    month_key = get_month_key(month_number, selected_year)
    budget = DUMMY_BUDGETS.get(selected_university, {}).get(month_key, 0)

    left, right = st.columns([2.3, 1])

    with left:
        cal = calendar.Calendar(firstweekday=6).monthdayscalendar(selected_year, month_number)

        calendar_html = f"""
        <div class="calendar-wrapper">
            <div class="month-heading">{selected_month_name} {selected_year}</div>
            <div class="calendar-grid">
        """

        week_days = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]

        for day_name in week_days:
            calendar_html += f"<div class='weekday'>{day_name}</div>"

        for week in cal:
            for day in week:
                if day == 0:
                    calendar_html += "<div class='empty-box'></div>"
                else:
                    current_date = date(selected_year, month_number, day)
                    status, title = get_status_for_day(current_date, selected_university)

                    chip = ""
                    if status != "available":
                        chip = f"<div class='event-chip chip-{status}'>{title}</div>"

                    calendar_html += f"""
                    <div class="day-box {status}">
                        <div class="day-number">{day}</div>
                        {chip}
                    </div>
                    """

        calendar_html += """
            </div>
        </div>
        """

        st.markdown(calendar_html, unsafe_allow_html=True)

    with right:
        st.markdown("""
        <div class="side-card">
            <h3 style="margin-top:0;">Legend</h3>
            <div class="legend-item"><span class="dot pink"></span> Training Scheduled</div>
            <div class="legend-item"><span class="dot yellow"></span> Blocked / Unavailable</div>
            <div class="legend-item"><span class="dot green"></span> Upcoming Training</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="side-card">
            <div style="font-size:14px;color:#64748B;font-weight:800;">University</div>
            <div style="font-size:18px;font-weight:900;color:#0F172A;">{selected_university}</div>
            <br>
            <div style="font-size:14px;color:#64748B;font-weight:800;">Month Budget</div>
            <div class="budget-text">₹{budget:,.0f}</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("### Trainings")

        found = False
        for training in TRAININGS.get(selected_university, []):
            if training["start"].month == month_number and training["start"].year == selected_year:
                found = True
                st.markdown(f"""
                <div class="side-card">
                    <div class="training-title">{training["title"]}</div>
                    <div class="training-meta">
                        {training["start"].strftime("%d %b %Y")} - {training["end"].strftime("%d %b %Y")}
                    </div>
                    <div class="training-meta">
                        Status: {training["status"].title()}
                    </div>
                </div>
                """, unsafe_allow_html=True)

        if not found:
            st.info("No trainings scheduled for this month.")
