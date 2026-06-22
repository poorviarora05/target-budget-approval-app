import streamlit as st
import calendar
from datetime import datetime, date
import streamlit.components.v1 as components


DUMMY_BUDGETS = {
    "Chandigarh University": {
        "Apr-26": 100000, "May-26": 120000, "Jun-26": 90000,
        "Jul-26": 150000, "Aug-26": 110000, "Sep-26": 130000,
        "Oct-26": 95000, "Nov-26": 140000, "Dec-26": 160000,
        "Jan-27": 125000, "Feb-27": 115000, "Mar-27": 135000,
    },
    "Sharda University": {
        "Apr-26": 80000, "May-26": 95000, "Jun-26": 70000,
        "Jul-26": 110000, "Aug-26": 90000, "Sep-26": 100000,
        "Oct-26": 85000, "Nov-26": 95000, "Dec-26": 120000,
        "Jan-27": 90000, "Feb-27": 85000, "Mar-27": 100000,
    },
    "Galgotias University": {
        "Apr-26": 60000, "May-26": 75000, "Jun-26": 65000,
        "Jul-26": 90000, "Aug-26": 70000, "Sep-26": 85000,
        "Oct-26": 75000, "Nov-26": 80000, "Dec-26": 95000,
        "Jan-27": 70000, "Feb-27": 65000, "Mar-27": 80000,
    },
}


TRAININGS = {
    "Chandigarh University": [
        {"title": "AI/ML Training", "start": date(2026, 7, 1), "end": date(2026, 7, 5), "status": "scheduled"},
        {"title": "University Event", "start": date(2026, 7, 8), "end": date(2026, 7, 10), "status": "blocked"},
        {"title": "Data Science Bootcamp", "start": date(2026, 7, 14), "end": date(2026, 7, 18), "status": "upcoming"},
    ],
    "Sharda University": [
        {"title": "Generative AI Workshop", "start": date(2026, 7, 3), "end": date(2026, 7, 6), "status": "scheduled"},
        {"title": "Cloud Computing Session", "start": date(2026, 7, 15), "end": date(2026, 7, 17), "status": "upcoming"},
    ],
    "Galgotias University": [
        {"title": "Cyber Security Program", "start": date(2026, 7, 11), "end": date(2026, 7, 13), "status": "blocked"},
        {"title": "Python Training", "start": date(2026, 7, 22), "end": date(2026, 7, 24), "status": "upcoming"},
    ],
}


def get_month_key(month_number, year):
    return datetime(year, month_number, 1).strftime("%b-%y")


def get_status_for_day(day_date, university):
    for training in TRAININGS.get(university, []):
        if training["start"] <= day_date <= training["end"]:
            return training["status"], training["title"]
    return "available", ""


def show_budget_calendar():
    st.markdown("## 📅 Budget & Training Calendar")
    st.caption("View training schedules, blocked dates and university budgets")

    month_names = [
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
    ]

    col1, col2, col3 = st.columns(3)

    with col1:
        selected_year = st.selectbox("Select Year", [2026, 2027, 2028, 2029, 2030])

    with col2:
        selected_month_name = st.selectbox("Select Month", month_names, index=6)

    with col3:
        selected_university = st.selectbox("Select University", list(DUMMY_BUDGETS.keys()))

    month_number = month_names.index(selected_month_name) + 1
    month_key = get_month_key(month_number, selected_year)
    budget = DUMMY_BUDGETS.get(selected_university, {}).get(month_key, 0)

    cal = calendar.Calendar(firstweekday=6).monthdayscalendar(selected_year, month_number)

    days_html = ""

    for day_name in ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]:
        days_html += f'<div class="weekday">{day_name}</div>'

    for week in cal:
        for day in week:
            if day == 0:
                days_html += '<div class="empty-box"></div>'
            else:
                current_date = date(selected_year, month_number, day)
                status, title = get_status_for_day(current_date, selected_university)

                chip = ""
                if status != "available":
                    chip = f'<div class="chip chip-{status}">{title}</div>'

                days_html += f'''
                <div class="day-box {status}">
                    <div class="day-number">{day}</div>
                    {chip}
                </div>
                '''

    training_cards = ""

    found = False
    for training in TRAININGS.get(selected_university, []):
        if training["start"].month == month_number and training["start"].year == selected_year:
            found = True
            training_cards += f'''
            <div class="training-card">
                <div class="training-title">{training["title"]}</div>
                <div class="training-meta">
                    {training["start"].strftime("%d %b %Y")} - {training["end"].strftime("%d %b %Y")}
                </div>
                <div class="training-meta">Status: {training["status"].title()}</div>
            </div>
            '''

    if not found:
        training_cards = '<div class="no-training">No trainings scheduled for this month.</div>'

    html = f'''
    <!DOCTYPE html>
    <html>
    <head>
    <style>
        body {{
            margin: 0;
            padding: 0;
            font-family: Arial, sans-serif;
            background: transparent;
            color: #0F172A;
        }}

        .layout {{
            display: grid;
            grid-template-columns: 2.4fr 1fr;
            gap: 24px;
            width: 100%;
            box-sizing: border-box;
        }}

        .calendar-card, .side-card {{
            background: #ffffff;
            border: 1px solid #E5E7EB;
            border-radius: 24px;
            box-shadow: 0 10px 26px rgba(15,23,42,0.06);
        }}

        .calendar-card {{
            padding: 24px;
        }}

        .month-title {{
            text-align: center;
            font-size: 34px;
            font-weight: 900;
            margin-bottom: 24px;
        }}

        .calendar-grid {{
            display: grid;
            grid-template-columns: repeat(7, 1fr);
            gap: 10px;
        }}

        .weekday {{
            text-align: center;
            font-size: 14px;
            font-weight: 900;
            color: #475569;
            padding: 8px 0;
        }}

        .day-box, .empty-box {{
            height: 78px;
            border-radius: 15px;
            box-sizing: border-box;
        }}

        .day-box {{
            border: 1px solid #E5E7EB;
            background: #ffffff;
            padding: 8px;
            overflow: hidden;
        }}

        .empty-box {{
            background: #F8FAFC;
            opacity: 0.45;
        }}

        .day-number {{
            font-size: 22px;
            font-weight: 900;
            line-height: 1;
        }}

        .chip {{
            margin-top: 13px;
            padding: 5px 8px;
            border-radius: 999px;
            font-size: 11px;
            font-weight: 900;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
            text-align: center;
        }}

        .scheduled {{
            background: #FCE7F3;
            border: 1.5px solid #F9A8D4;
        }}

        .blocked {{
            background: #FEF3C7;
            border: 1.5px solid #FDE68A;
        }}

        .upcoming {{
            background: #DCFCE7;
            border: 1.5px solid #86EFAC;
        }}

        .chip-scheduled {{
            background: #F9A8D4;
            color: #831843;
        }}

        .chip-blocked {{
            background: #FDE68A;
            color: #92400E;
        }}

        .chip-upcoming {{
            background: #86EFAC;
            color: #166534;
        }}

        .side-card {{
            padding: 24px;
            margin-bottom: 20px;
        }}

        .side-heading {{
            font-size: 28px;
            font-weight: 900;
            margin-bottom: 22px;
        }}

        .legend-row {{
            display: flex;
            align-items: center;
            gap: 12px;
            margin-bottom: 16px;
            font-size: 15px;
            font-weight: 800;
            color: #334155;
        }}

        .dot {{
            width: 18px;
            height: 18px;
            border-radius: 50%;
            display: inline-block;
            flex-shrink: 0;
        }}

        .pink {{ background: #F9A8D4; }}
        .yellow {{ background: #FDE68A; }}
        .green {{ background: #86EFAC; }}

        .label {{
            font-size: 14px;
            color: #64748B;
            font-weight: 900;
            margin-bottom: 6px;
        }}

        .university {{
            font-size: 21px;
            font-weight: 900;
            margin-bottom: 24px;
            line-height: 1.3;
        }}

        .budget {{
            font-size: 36px;
            font-weight: 900;
            color: #4F46E5;
        }}

        .training-heading {{
            font-size: 26px;
            font-weight: 900;
            margin: 10px 0 14px 0;
        }}

        .training-card {{
            background: white;
            border: 1px solid #E5E7EB;
            border-radius: 18px;
            padding: 16px;
            margin-bottom: 14px;
            box-shadow: 0 8px 20px rgba(15,23,42,0.05);
        }}

        .training-title {{
            font-size: 16px;
            font-weight: 900;
        }}

        .training-meta {{
            font-size: 13px;
            color: #64748B;
            margin-top: 5px;
        }}

        .no-training {{
            background: #F8FAFC;
            border: 1px solid #E5E7EB;
            border-radius: 14px;
            padding: 14px;
            color: #64748B;
            font-weight: 700;
        }}
    </style>
    </head>
    <body>
        <div class="layout">
            <div class="calendar-card">
                <div class="month-title">{selected_month_name} {selected_year}</div>
                <div class="calendar-grid">
                    {days_html}
                </div>
            </div>

            <div>
                <div class="side-card">
                    <div class="side-heading">Legend</div>
                    <div class="legend-row"><span class="dot pink"></span>Training Scheduled</div>
                    <div class="legend-row"><span class="dot yellow"></span>Blocked / Unavailable</div>
                    <div class="legend-row"><span class="dot green"></span>Upcoming Training</div>
                </div>

                <div class="side-card">
                    <div class="label">University</div>
                    <div class="university">{selected_university}</div>

                    <div class="label">Month Budget</div>
                    <div class="budget">₹{budget:,.0f}</div>
                </div>

                <div class="training-heading">Trainings</div>
                {training_cards}
            </div>
        </div>
    </body>
    </html>
    '''

    components.html(html, height=720, scrolling=False)
