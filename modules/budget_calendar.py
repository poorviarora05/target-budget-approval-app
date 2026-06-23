import streamlit as st
import calendar
from datetime import datetime, date
import streamlit.components.v1 as components
import pandas as pd


REQUESTS_FILE = "requests.csv"


DUMMY_BUDGETS = {
    "Chandigarh University": {
        "Apr-26": 100000, "May-26": 120000, "Jun-26": 90000,
        "Jul-26": 70000, "Aug-26": 110000, "Sep-26": 130000,
        "Oct-26": 95000, "Nov-26": 140000, "Dec-26": 160000,
        "Jan-27": 125000, "Feb-27": 115000, "Mar-27": 135000,
        "Apr-27": 100000, "May-27": 120000, "Jun-27": 90000,
        "Jul-27": 150000, "Aug-27": 110000, "Sep-27": 130000,
        "Oct-27": 95000, "Nov-27": 140000, "Dec-27": 160000,
        "Jan-28": 125000, "Feb-28": 115000, "Mar-28": 135000,
    },
    "Sharda University": {
        "Apr-26": 80000, "May-26": 95000, "Jun-26": 70000,
        "Jul-26": 110000, "Aug-26": 90000, "Sep-26": 100000,
        "Oct-26": 85000, "Nov-26": 95000, "Dec-26": 120000,
        "Jan-27": 90000, "Feb-27": 85000, "Mar-27": 100000,
        "Apr-27": 80000, "May-27": 95000, "Jun-27": 70000,
        "Jul-27": 110000, "Aug-27": 90000, "Sep-27": 100000,
        "Oct-27": 85000, "Nov-27": 95000, "Dec-27": 120000,
        "Jan-28": 90000, "Feb-28": 85000, "Mar-28": 100000,
    },
    "Galgotias University": {
        "Apr-26": 60000, "May-26": 75000, "Jun-26": 65000,
        "Jul-26": 90000, "Aug-26": 70000, "Sep-26": 85000,
        "Oct-26": 75000, "Nov-26": 80000, "Dec-26": 95000,
        "Jan-27": 70000, "Feb-27": 65000, "Mar-27": 80000,
        "Apr-27": 60000, "May-27": 75000, "Jun-27": 65000,
        "Jul-27": 90000, "Aug-27": 70000, "Sep-27": 85000,
        "Oct-27": 75000, "Nov-27": 80000, "Dec-27": 95000,
        "Jan-28": 70000, "Feb-28": 65000, "Mar-28": 80000,
    },
}


TRAININGS = {
    "Chandigarh University": [
        {
            "title": "AI/ML Training",
            "start": date(2026, 7, 3),
            "end": date(2026, 7, 7),
            "status": "scheduled",
            "cost": 50000,
        },
        {
            "title": "University Event",
            "start": date(2026, 7, 10),
            "end": date(2026, 7, 11),
            "status": "blocked",
            "cost": 0,
        },
        {
            "title": "Data Science Bootcamp",
            "start": date(2026, 7, 18),
            "end": date(2026, 7, 20),
            "status": "upcoming",
            "cost": 15000,
        },
    ],
    "Sharda University": [
        {
            "title": "Generative AI Workshop",
            "start": date(2026, 7, 3),
            "end": date(2026, 7, 6),
            "status": "scheduled",
            "cost": 45000,
        },
        {
            "title": "Cloud Computing Session",
            "start": date(2026, 7, 15),
            "end": date(2026, 7, 17),
            "status": "upcoming",
            "cost": 25000,
        },
    ],
    "Galgotias University": [
        {
            "title": "Cyber Security Program",
            "start": date(2026, 7, 11),
            "end": date(2026, 7, 13),
            "status": "blocked",
            "cost": 30000,
        },
        {
            "title": "Python Training",
            "start": date(2026, 7, 22),
            "end": date(2026, 7, 24),
            "status": "upcoming",
            "cost": 20000,
        },
    ],
}


def safe_number(value):
    try:
        if pd.isna(value):
            return 0
        return float(value)
    except:
        return 0


def format_university_name(value):
    text = str(value).strip()

    if not text:
        return ""

    lower_text = text.lower()

    if "chandigarh" in lower_text:
        return "Chandigarh University"

    if "sharda" in lower_text:
        return "Sharda University"

    if "galgotias" in lower_text:
        return "Galgotias University"

    return text.title()


def get_month_key(month_number, year):
    return datetime(year, month_number, 1).strftime("%b-%y")


def get_approved_trainings_from_requests():
    try:
        requests_df = pd.read_csv(REQUESTS_FILE)
    except:
        return {}

    if "request_status" not in requests_df.columns:
        return {}

    approved_requests = requests_df[
        requests_df["request_status"].isin(["Approved", "Director Approved"])
    ]

    dynamic_trainings = {}

    for _, row in approved_requests.iterrows():
        university = format_university_name(row.get("college_name", ""))

        if not university:
            continue

        try:
            start_date = pd.to_datetime(row.get("start_date")).date()
            end_date = pd.to_datetime(row.get("end_date")).date()
        except:
            continue

        title = str(row.get("training_topic", "Approved Training")).strip()

        if not title:
            title = "Approved Training"

        cost = safe_number(
            row.get(
                "partner_final_available_budget",
                row.get(
                    "estimated_budget",
                    row.get("total_expected_budget", 0)
                )
            )
        )

        training = {
            "title": title.title(),
            "start": start_date,
            "end": end_date,
            "status": "scheduled",
            "cost": cost,
        }

        if university not in dynamic_trainings:
            dynamic_trainings[university] = []

        dynamic_trainings[university].append(training)

    return dynamic_trainings


def get_all_trainings():
    all_trainings = {}

    for university, trainings in TRAININGS.items():
        all_trainings[university] = trainings.copy()

    approved_trainings = get_approved_trainings_from_requests()

    for university, trainings in approved_trainings.items():
        if university not in all_trainings:
            all_trainings[university] = []

        all_trainings[university].extend(trainings)

    return all_trainings


def get_training_for_day(day_date, university):
    all_trainings = get_all_trainings()

    for training in all_trainings.get(university, []):
        if training["start"] <= day_date <= training["end"]:
            return training

    return None


def get_budget_usage(university, month_number, year, selected_date):
    exhausted = 0
    all_trainings = get_all_trainings()

    for training in all_trainings.get(university, []):
        same_month = (
            training["start"].month == month_number
            and training["start"].year == year
        )

        if same_month and training["end"] <= selected_date:
            exhausted += training.get("cost", 0)

    return exhausted


def get_financial_year_months(fy_start_year):
    return [
        f"Apr-{str(fy_start_year)[-2:]}",
        f"May-{str(fy_start_year)[-2:]}",
        f"Jun-{str(fy_start_year)[-2:]}",
        f"Jul-{str(fy_start_year)[-2:]}",
        f"Aug-{str(fy_start_year)[-2:]}",
        f"Sep-{str(fy_start_year)[-2:]}",
        f"Oct-{str(fy_start_year)[-2:]}",
        f"Nov-{str(fy_start_year)[-2:]}",
        f"Dec-{str(fy_start_year)[-2:]}",
        f"Jan-{str(fy_start_year + 1)[-2:]}",
        f"Feb-{str(fy_start_year + 1)[-2:]}",
        f"Mar-{str(fy_start_year + 1)[-2:]}",
    ]


def get_yearly_budget_summary(university, fy_start_year):
    fy_months = get_financial_year_months(fy_start_year)

    total_available = sum(
        DUMMY_BUDGETS.get(university, {}).get(month_key, 0)
        for month_key in fy_months
    )

    fy_start_date = date(fy_start_year, 4, 1)
    fy_end_date = date(fy_start_year + 1, 3, 31)

    total_exhausted = 0
    all_trainings = get_all_trainings()

    for training in all_trainings.get(university, []):
        if fy_start_date <= training["start"] <= fy_end_date:
            total_exhausted += training.get("cost", 0)

    total_left = total_available - total_exhausted

    if total_available > 0:
        utilization = (total_exhausted / total_available) * 100
    else:
        utilization = 0

    return total_available, total_exhausted, total_left, utilization


def show_budget_calendar():
    st.markdown("## Budget & Training Calendar")
    st.caption("View training schedules, blocked dates, monthly budgets and yearly utilization")

    month_names = [
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December",
    ]

    all_trainings = get_all_trainings()
    university_options = sorted(
        set(list(DUMMY_BUDGETS.keys()) + list(all_trainings.keys()))
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        selected_year = st.selectbox(
            "Select Year",
            [2026, 2027, 2028, 2029, 2030],
        )

    with col2:
        selected_month_name = st.selectbox(
            "Select Month",
            month_names,
            index=6,
        )

    month_number = month_names.index(selected_month_name) + 1
    max_day = calendar.monthrange(selected_year, month_number)[1]

    with col3:
        selected_university = st.selectbox(
            "Select University",
            university_options,
        )

    with col4:
        selected_date = st.date_input(
            "Check Budget On",
            value=date(selected_year, month_number, 15),
            min_value=date(selected_year, month_number, 1),
            max_value=date(selected_year, month_number, max_day),
        )

    month_key = get_month_key(month_number, selected_year)
    month_budget = DUMMY_BUDGETS.get(selected_university, {}).get(month_key, 0)

    exhausted_amount = get_budget_usage(
        selected_university,
        month_number,
        selected_year,
        selected_date,
    )

    left_amount = month_budget - exhausted_amount

    selected_training = get_training_for_day(selected_date, selected_university)

    if selected_training:
        selected_status = selected_training["status"]
        selected_title = selected_training["title"]
        selected_cost = selected_training.get("cost", 0)
    else:
        selected_status = "available"
        selected_title = ""
        selected_cost = 0

    if selected_status == "scheduled":
        selected_status_text = "Training Scheduled"
    elif selected_status == "blocked":
        selected_status_text = "Blocked / Unavailable"
    elif selected_status == "upcoming":
        selected_status_text = "Upcoming Training"
    else:
        selected_status_text = "Available"

    cal = calendar.Calendar(firstweekday=6).monthdayscalendar(
        selected_year,
        month_number,
    )

    days_html = ""

    for day_name in ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]:
        days_html += f'<div class="weekday">{day_name}</div>'

    for week in cal:
        for day in week:
            if day == 0:
                days_html += '<div class="empty-box"></div>'
            else:
                current_date = date(selected_year, month_number, day)
                training = get_training_for_day(current_date, selected_university)

                if training:
                    status = training["status"]
                    title = training["title"]
                else:
                    status = "available"
                    title = ""

                selected_class = "selected-day" if current_date == selected_date else ""

                event_html = ""
                if title:
                    event_html = f'<div class="event-name">{title}</div>'

                days_html += f'''
                <div class="day-box {status} {selected_class}">
                    <div class="day-number">{day}</div>
                    {event_html}
                </div>
                '''

    training_cards = ""
    found = False

    for training in all_trainings.get(selected_university, []):
        same_month = (
            training["start"].month == month_number
            and training["start"].year == selected_year
        )

        if same_month:
            found = True
            training_cards += f'''
            <div class="training-card">
                <div class="training-title">{training["title"]}</div>
                <div class="training-meta">
                    {training["start"].strftime("%d %b %Y")} - {training["end"].strftime("%d %b %Y")}
                </div>
                <div class="training-meta">Status: {training["status"].title()}</div>
                <div class="training-cost">Cost: ₹{training.get("cost", 0):,.0f}</div>
            </div>
            '''

    if not found:
        training_cards = '<div class="no-training">No trainings scheduled for this month.</div>'

    selected_event_line = ""
    if selected_title:
        selected_event_line = f'''
        <div class="info-item">
            <div class="label">Event</div>
            <div class="value">{selected_title}</div>
        </div>

        <div class="info-item">
            <div class="label">Event Cost</div>
            <div class="value">₹{selected_cost:,.0f}</div>
        </div>
        '''

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

        .calendar-card {{
            background: #ffffff;
            border: 1px solid #E5E7EB;
            border-radius: 24px;
            box-shadow: 0 10px 26px rgba(15,23,42,0.06);
            padding: 24px;
            margin-bottom: 24px;
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
            gap: 12px;
        }}

        .weekday {{
            text-align: center;
            font-size: 15px;
            font-weight: 900;
            color: #475569;
            padding: 8px 0;
        }}

        .day-box,
        .empty-box {{
            min-height: 120px;
            border-radius: 16px;
            box-sizing: border-box;
        }}

        .day-box {{
            border: 1px solid #E5E7EB;
            background: #ffffff;
            padding: 12px;
            overflow: visible;
        }}

        .empty-box {{
            background: #F8FAFC;
            opacity: 0.45;
        }}

        .day-number {{
            font-size: 24px;
            font-weight: 900;
            line-height: 1;
            margin-bottom: 12px;
        }}

        .event-name {{
            font-size: 13px;
            font-weight: 900;
            color: #0F172A;
            line-height: 1.25;
            text-align: center;
            overflow-wrap: break-word;
            white-space: normal;
            padding: 8px;
            border-radius: 12px;
            background: rgba(255,255,255,0.65);
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

        .selected-day {{
            border: 3px solid #2563EB !important;
            box-shadow: 0 0 0 4px rgba(37,99,235,0.15);
        }}

        .bottom-layout {{
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 20px;
        }}

        .side-card {{
            background: #ffffff;
            border: 1px solid #E5E7EB;
            border-radius: 22px;
            padding: 22px;
            box-shadow: 0 10px 26px rgba(15,23,42,0.06);
        }}

        .side-heading {{
            font-size: 24px;
            font-weight: 900;
            margin-bottom: 18px;
        }}

        .legend-row {{
            display: flex;
            align-items: center;
            gap: 12px;
            margin-bottom: 13px;
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
        .blue {{ background: #2563EB; }}

        .info-item {{
            margin-bottom: 16px;
        }}

        .label {{
            font-size: 13px;
            color: #64748B;
            font-weight: 900;
            margin-bottom: 5px;
        }}

        .value {{
            font-size: 16px;
            font-weight: 900;
            color: #0F172A;
            line-height: 1.3;
        }}

        .budget {{
            font-size: 30px;
            font-weight: 900;
            color: #4F46E5;
            margin-bottom: 16px;
        }}

        .exhausted {{
            font-size: 28px;
            font-weight: 900;
            color: #DC2626;
            margin-bottom: 16px;
        }}

        .left {{
            font-size: 28px;
            font-weight: 900;
            color: #16A34A;
        }}

        .training-card {{
            background: #F8FAFC;
            border: 1px solid #E5E7EB;
            border-radius: 16px;
            padding: 14px;
            margin-bottom: 12px;
        }}

        .training-title {{
            font-size: 15px;
            font-weight: 900;
        }}

        .training-meta {{
            font-size: 13px;
            color: #64748B;
            margin-top: 5px;
        }}

        .training-cost {{
            margin-top: 7px;
            font-size: 14px;
            font-weight: 900;
            color: #4F46E5;
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
        <div class="calendar-card">
            <div class="month-title">{selected_month_name} {selected_year}</div>
            <div class="calendar-grid">
                {days_html}
            </div>
        </div>

        <div class="bottom-layout">
            <div class="side-card">
                <div class="side-heading">Legend</div>
                <div class="legend-row"><span class="dot pink"></span>Training Scheduled</div>
                <div class="legend-row"><span class="dot yellow"></span>Blocked / Unavailable</div>
                <div class="legend-row"><span class="dot green"></span>Upcoming Training</div>
                <div class="legend-row"><span class="dot blue"></span>Selected Date</div>
            </div>

            <div class="side-card">
                <div class="side-heading">Monthly Summary</div>

                <div class="info-item">
                    <div class="label">Check Budget On</div>
                    <div class="value">{selected_date.strftime("%d %B %Y")}</div>
                </div>

                <div class="info-item">
                    <div class="label">Date Status</div>
                    <div class="value">{selected_status_text}</div>
                </div>

                {selected_event_line}

                <div class="info-item">
                    <div class="label">University</div>
                    <div class="value">{selected_university}</div>
                </div>

                <div class="label">Month Budget</div>
                <div class="budget">₹{month_budget:,.0f}</div>

                <div class="label">Exhausted Amount</div>
                <div class="exhausted">₹{exhausted_amount:,.0f}</div>

                <div class="label">Left Amount</div>
                <div class="left">₹{left_amount:,.0f}</div>
            </div>

            <div class="side-card">
                <div class="side-heading">Trainings</div>
                {training_cards}
            </div>
        </div>
    </body>
    </html>
    '''

    components.html(html, height=1250, scrolling=True)

    st.markdown("---")
    st.subheader("Yearly Budget Checker")

    fy_col1, fy_col2 = st.columns(2)

    with fy_col1:
        selected_fy_start = st.selectbox(
            "Select Financial Year",
            [2026, 2027],
            format_func=lambda y: f"{y}-{str(y + 1)[-2:]}",
        )

    with fy_col2:
        yearly_university = st.selectbox(
            "Select University for Yearly Budget",
            university_options,
            key="yearly_budget_university",
        )

    yearly_available, yearly_exhausted, yearly_left, yearly_utilization = (
        get_yearly_budget_summary(yearly_university, selected_fy_start)
    )

    y1, y2, y3, y4 = st.columns(4)

    y1.metric("Total Available Budget", f"₹{yearly_available:,.0f}")
    y2.metric("Total Exhausted Budget", f"₹{yearly_exhausted:,.0f}")
    y3.metric("Total Left Budget", f"₹{yearly_left:,.0f}")
    y4.metric("Utilization", f"{yearly_utilization:.1f}%")
