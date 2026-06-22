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
        {
            "title": "AI/ML Training Program",
            "start": date(2026, 7, 1),
            "end": date(2026, 7, 5),
            "status": "scheduled"
        },
        {
            "title": "University Event",
            "start": date(2026, 7, 8),
            "end": date(2026, 7, 10),
            "status": "blocked"
        },
        {
            "title": "Data Science Bootcamp",
            "start": date(2026, 7, 14),
            "end": date(2026, 7, 18),
            "status": "upcoming"
        }
    ],
    "Sharda University": [
        {
            "title": "Generative AI Workshop",
            "start": date(2026, 7, 3),
            "end": date(2026, 7, 6),
            "status": "scheduled"
        },
        {
            "title": "Cloud Computing Session",
            "start": date(2026, 7, 15),
            "end": date(2026, 7, 17),
            "status": "upcoming"
        }
    ],
    "Galgotias University": [
        {
            "title": "Cyber Security Program",
            "start": date(2026, 7, 11),
            "end": date(2026, 7, 13),
            "status": "blocked"
        },
        {
            "title": "Python Training",
            "start": date(2026, 7, 22),
            "end": date(2026, 7, 24),
            "status": "upcoming"
        }
    ]
}


def get_month_key(month_number, year):
    month_abbr = datetime(year, month_number, 1).strftime("%b")
    year_suffix = str(year)[-2:]
    return f"{month_abbr}-{year_suffix}"


def get_status_for_day(day_date, university):
    for training in TRAININGS.get(university, []):
        if training["start"] <= day_date <= training["end"]:
            return training["status"], training["title"]
    return None, ""


def show_budget_calendar():

    st.markdown("""
    <style>
    .calendar-header {
        display:flex;
        align-items:center;
        gap:14px;
        margin-bottom:22px;
    }

    .calendar-icon {
        width:58px;
        height:58px;
        border-radius:16px;
        background:#EEF2FF;
        display:flex;
        align-items:center;
        justify-content:center;
        font-size:28px;
    }

    .calendar-title-main {
        font-size:34px;
        font-weight:900;
        color:#0F172A;
        margin:0;
    }

    .calendar-subtitle {
        color:#64748B;
        margin-top:2px;
        font-size:15px;
    }

    .filter-card {
        background:white;
        padding:20px;
        border-radius:18px;
        border:1px solid #E5E7EB;
        box-shadow:0 8px 24px rgba(15,23,42,0.05);
        margin-bottom:20px;
    }

    .legend-card {
        background:white;
        padding:20px;
        border-radius:18px;
        border:1px solid #E5E7EB;
        box-shadow:0 8px 24px rgba(15,23,42,0.05);
        margin-bottom:18px;
    }

    .legend-row {
        display:flex;
        align-items:center;
        gap:12px;
        margin-bottom:16px;
        font-weight:700;
        color:#334155;
    }

    .dot {
        width:22px;
        height:22px;
        border-radius:50%;
        display:inline-block;
    }

    .dot-pink {background:#F9A8D4;}
    .dot-yellow {background:#FDE68A;}
    .dot-green {background:#BBF7D0;}

    .calendar-shell {
        background:white;
        padding:24px;
        border-radius:22px;
        border:1px solid #E5E7EB;
        box-shadow:0 10px 28px rgba(15,23,42,0.06);
    }

    .month-title {
        text-align:center;
        font-size:30px;
        font-weight:900;
        color:#0F172A;
        margin-bottom:22px;
    }

    .weekday {
        text-align:center;
        font-weight:900;
        color:#475569;
        padding-bottom:10px;
        font-size:15px;
    }

    .day-cell {
        min-height:102px;
        border-radius:16px;
        border:1px solid #E5E7EB;
        background:#FFFFFF;
        padding:10px;
        box-shadow:0 4px 12px rgba(15,23,42,0.04);
        margin-bottom:8px;
    }

    .day-empty {
        min-height:102px;
        border-radius:16px;
        background:#F8FAFC;
        opacity:0.45;
        margin-bottom:8px;
    }

    .day-number {
        font-size:22px;
        font-weight:900;
        color:#0F172A;
    }

    .day-selected {
        border:2px solid #6366F1;
        box-shadow:0 8px 20px rgba(99,102,241,0.25);
    }

    .status-scheduled {
        background:#FCE7F3;
        border-color:#F9A8D4;
    }

    .status-blocked {
        background:#FEF3C7;
        border-color:#FDE68A;
    }

    .status-upcoming {
        background:#DCFCE7;
        border-color:#BBF7D0;
    }

    .training-chip {
        margin-top:12px;
        padding:6px 8px;
        border-radius:999px;
        font-size:12px;
        font-weight:800;
        text-align:center;
        white-space:nowrap;
        overflow:hidden;
        text-overflow:ellipsis;
    }

    .chip-scheduled {
        background:#F9A8D4;
        color:#831843;
    }

    .chip-blocked {
        background:#FDE68A;
        color:#92400E;
    }

    .chip-upcoming {
        background:#BBF7D0;
        color:#166534;
    }

    .training-list-card {
        background:white;
        padding:18px;
        border-radius:18px;
        border:1px solid #E5E7EB;
        box-shadow:0 8px 24px rgba(15,23,42,0.05);
        margin-bottom:14px;
    }

    .training-card-title {
        font-size:16px;
        font-weight:900;
        color:#0F172A;
    }

    .training-card-meta {
        font-size:13px;
        color:#64748B;
        margin-top:5px;
    }

    .budget-result-card {
        background:linear-gradient(135deg,#EEF2FF,#FFFFFF);
        padding:22px;
        border-radius:20px;
        border:1px solid #C7D2FE;
        margin-top:18px;
    }

    .budget-amount {
        font-size:34px;
        font-weight:900;
        color:#4F46E5;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="calendar-header">
        <div class="calendar-icon">📅</div>
        <div>
            <div class="calendar-title-main">Budget & Training Calendar</div>
            <div class="calendar-subtitle">View training schedules, blocked dates and university budgets</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div class='filter-card'>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        selected_year = st.selectbox(
            "Select Year",
            [2026, 2027],
            index=0
        )

    with col2:
        month_names = [
            "January", "February", "March", "April", "May", "June",
            "July", "August", "September", "October", "November", "December"
        ]

        selected_month_name = st.selectbox(
            "Select Month",
            month_names,
            index=6
        )

    with col3:
        selected_university = st.selectbox(
            "Select University",
            list(DUMMY_BUDGETS.keys())
        )

    st.markdown("</div>", unsafe_allow_html=True)

    month_number = month_names.index(selected_month_name) + 1
    month_key = get_month_key(month_number, selected_year)

    budget = DUMMY_BUDGETS.get(selected_university, {}).get(month_key, 0)

    left, right = st.columns([2.2, 1])

    with left:
        st.markdown("<div class='calendar-shell'>", unsafe_allow_html=True)
        st.markdown(
            f"<div class='month-title'>{selected_month_name} {selected_year}</div>",
            unsafe_allow_html=True
        )

        week_days = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
        weekday_cols = st.columns(7)

        for i, day_name in enumerate(week_days):
            weekday_cols[i].markdown(
                f"<div class='weekday'>{day_name}</div>",
                unsafe_allow_html=True
            )

        cal = calendar.Calendar(firstweekday=6).monthdayscalendar(
            selected_year,
            month_number
        )

        if "calendar_selected_day" not in st.session_state:
            st.session_state.calendar_selected_day = 1

        max_day = calendar.monthrange(selected_year, month_number)[1]

        if st.session_state.calendar_selected_day > max_day:
            st.session_state.calendar_selected_day = 1

        for week in cal:
            cols = st.columns(7)

            for i, day in enumerate(week):
                with cols[i]:
                    if day == 0:
                        st.markdown(
                            "<div class='day-empty'></div>",
                            unsafe_allow_html=True
                        )
                    else:
                        current_date = date(
                            selected_year,
                            month_number,
                            day
                        )

                        status, title = get_status_for_day(
                            current_date,
                            selected_university
                        )

                        classes = "day-cell"

                        if status:
                            classes += f" status-{status}"

                        if day == st.session_state.calendar_selected_day:
                            classes += " day-selected"

                        if st.button(
                            str(day),
                            key=f"day_{selected_year}_{month_number}_{day}",
                            use_container_width=True
                        ):
                            st.session_state.calendar_selected_day = day
                            st.rerun()

                        chip_html = ""

                        if status:
                            chip_html = f"""
                            <div class="training-chip chip-{status}">
                                {title}
                            </div>
                            """

                        st.markdown(
                            f"""
                            <div class="{classes}">
                                <div class="day-number">{day}</div>
                                {chip_html}
                            </div>
                            """,
                            unsafe_allow_html=True
                        )

        st.markdown("</div>", unsafe_allow_html=True)

    with right:
        st.markdown("""
        <div class="legend-card">
            <h3 style="margin-top:0;">Legend</h3>
            <div class="legend-row"><span class="dot dot-pink"></span> Training Scheduled</div>
            <div class="legend-row"><span class="dot dot-yellow"></span> Blocked / Unavailable</div>
            <div class="legend-row"><span class="dot dot-green"></span> Upcoming Training</div>
        </div>
        """, unsafe_allow_html=True)

        selected_date = date(
            selected_year,
            month_number,
            st.session_state.calendar_selected_day
        )

        status, title = get_status_for_day(
            selected_date,
            selected_university
        )

        status_text = "Available"

        if status == "scheduled":
            status_text = "Training Scheduled"
        elif status == "blocked":
            status_text = "Blocked / Unavailable"
        elif status == "upcoming":
            status_text = "Upcoming Training"

        st.markdown(
            f"""
            <div class="budget-result-card">
                <div style="font-size:14px;color:#64748B;font-weight:800;">Selected Date</div>
                <div style="font-size:24px;font-weight:900;color:#0F172A;">
                    {selected_date.strftime("%d %B %Y")}
                </div>
                <br>
                <div style="font-size:14px;color:#64748B;font-weight:800;">University</div>
                <div style="font-size:17px;font-weight:800;color:#0F172A;">
                    {selected_university}
                </div>
                <br>
                <div style="font-size:14px;color:#64748B;font-weight:800;">Budget</div>
                <div class="budget-amount">₹{budget:,.0f}</div>
                <br>
                <div style="font-size:14px;color:#64748B;font-weight:800;">Date Status</div>
                <div style="font-size:16px;font-weight:900;color:#0F172A;">
                    {status_text}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown("### Trainings")

        trainings = TRAININGS.get(selected_university, [])

        for training in trainings:
            if (
                training["start"].month == month_number
                and training["start"].year == selected_year
            ):
                st.markdown(
                    f"""
                    <div class="training-list-card">
                        <div class="training-card-title">{training["title"]}</div>
                        <div class="training-card-meta">
                            {training["start"].strftime("%d %b %Y")} - {training["end"].strftime("%d %b %Y")}
                        </div>
                        <div class="training-card-meta">
                            Status: {training["status"].title()}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
