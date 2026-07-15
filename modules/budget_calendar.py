import streamlit as st
import pandas as pd
import calendar
from datetime import date
from textwrap import dedent
import streamlit.components.v1 as components


REQUESTS_FILE = "requests.csv"
BUDGET_MASTER_FILE = "budget.csv"


MONTHS = {
    1: "jan",
    2: "feb",
    3: "mar",
    4: "apr",
    5: "may",
    6: "jun",
    7: "jul",
    8: "aug",
    9: "sep",
    10: "oct",
    11: "nov",
    12: "dec",
}


MONTH_NAMES = [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December",
]


# =========================================================
# BASIC HELPERS
# =========================================================

def safe_number(value):
    try:
        if pd.isna(value):
            return 0

        value = (
            str(value)
            .replace(",", "")
            .replace("₹", "")
            .strip()
        )

        if value.lower() in ["nan", "none", ""]:
            return 0

        return float(value)

    except Exception:
        return 0


def clean_text(value):
    try:
        if pd.isna(value):
            return ""

        value = str(value).strip()

        if value.lower() in ["nan", "none", ""]:
            return ""

        return value

    except Exception:
        return ""


def normalize(value):
    return (
        clean_text(value)
        .lower()
        .replace(" ", "")
        .replace("_", "")
        .replace("-", "")
    )


# =========================================================
# PREMIUM UI
# =========================================================

def apply_budget_calendar_ui():
    st.markdown(
        dedent(
            """
            <style>
            :root {
                --calendar-primary: #4f46e5;
                --calendar-primary-dark: #3730a3;
                --calendar-secondary: #7c3aed;
                --calendar-accent: #ec4899;
                --calendar-bg: #f5f7fc;
                --calendar-surface: #ffffff;
                --calendar-text: #0f172a;
                --calendar-text-soft: #64748b;
                --calendar-border: #e2e8f0;
            }

            /* =================================================
               PAGE
            ================================================= */

            .stApp {
                background:
                    radial-gradient(
                        circle at 88% 2%,
                        rgba(79, 70, 229, 0.09),
                        transparent 25%
                    ),
                    radial-gradient(
                        circle at 10% 40%,
                        rgba(124, 58, 237, 0.04),
                        transparent 28%
                    ),
                    linear-gradient(
                        180deg,
                        #f9faff 0%,
                        #f4f6fb 100%
                    );
            }

            [data-testid="stAppViewContainer"] {
                background: transparent;
            }

            [data-testid="stHeader"] {
                background: rgba(248, 250, 252, 0.82);
                backdrop-filter: blur(18px);
                border-bottom: 1px solid rgba(226, 232, 240, 0.65);
            }

            .block-container {
                max-width: 1480px;
                padding-top: 1.5rem;
                padding-bottom: 4rem;
            }

            /* =================================================
               HERO
            ================================================= */

            .calendar-hero {
                position: relative;
                overflow: hidden;

                background:
                    radial-gradient(
                        circle at 92% 12%,
                        rgba(99, 102, 241, 0.20),
                        transparent 27%
                    ),
                    radial-gradient(
                        circle at 77% 90%,
                        rgba(236, 72, 153, 0.08),
                        transparent 29%
                    ),
                    linear-gradient(
                        135deg,
                        #ffffff 0%,
                        #fafaff 52%,
                        #f4f2ff 100%
                    );

                border: 1px solid #e0e4ef;
                border-radius: 25px;

                padding: 28px 30px;
                margin-bottom: 22px;

                box-shadow:
                    0 20px 46px rgba(15, 23, 42, 0.075),
                    inset 0 1px 0 rgba(255, 255, 255, 0.96);
            }

            .calendar-hero::before {
                content: "";
                position: absolute;
                top: -125px;
                right: -65px;
                width: 230px;
                height: 230px;
                border-radius: 50%;

                background:
                    linear-gradient(
                        135deg,
                        rgba(79, 70, 229, 0.15),
                        rgba(124, 58, 237, 0.04)
                    );
            }

            .calendar-hero-grid {
                position: relative;
                z-index: 2;

                display: flex;
                align-items: center;
                justify-content: space-between;
                gap: 24px;
            }

            .calendar-hero-title {
                color: var(--calendar-text);
                font-size: 35px;
                font-weight: 900;
                line-height: 1.15;
                letter-spacing: -0.045em;
                margin-bottom: 8px;
            }

            .calendar-hero-subtitle {
                color: #738096;
                font-size: 15px;
                font-weight: 520;
                line-height: 1.65;
                max-width: 780px;
            }

            .calendar-hero-badge {
                flex-shrink: 0;
                color: #4338ca;
                background: rgba(238, 242, 255, 0.96);

                border: 1px solid #c7d2fe;
                border-radius: 999px;

                padding: 11px 17px;

                font-size: 13px;
                font-weight: 850;
                white-space: nowrap;

                box-shadow:
                    0 9px 20px rgba(79, 70, 229, 0.11);
            }

            /* =================================================
               BORDERED CONTAINERS
            ================================================= */

            div[data-testid="stVerticalBlockBorderWrapper"] {
                background:
                    linear-gradient(
                        180deg,
                        rgba(255, 255, 255, 0.98) 0%,
                        rgba(252, 253, 255, 0.98) 100%
                    );

                border: 1px solid #e1e5ee !important;
                border-radius: 21px !important;

                padding: 4px;

                box-shadow:
                    0 14px 34px rgba(15, 23, 42, 0.055),
                    inset 0 1px 0 rgba(255, 255, 255, 0.95);
            }

            /* =================================================
               SECTION HEADERS
            ================================================= */

            .calendar-section-header {
                display: flex;
                align-items: center;
                gap: 12px;
                margin-bottom: 5px;
            }

            .calendar-section-number {
                width: 39px;
                height: 39px;

                display: flex;
                align-items: center;
                justify-content: center;

                color: #ffffff;

                background:
                    linear-gradient(
                        135deg,
                        var(--calendar-primary),
                        var(--calendar-secondary)
                    );

                border-radius: 12px;

                font-size: 13px;
                font-weight: 900;

                box-shadow:
                    0 9px 19px rgba(79, 70, 229, 0.24);
            }

            .calendar-section-title {
                color: var(--calendar-text);
                font-size: 20px;
                font-weight: 850;
                line-height: 1.25;
                letter-spacing: -0.025em;
            }

            .calendar-section-subtitle {
                color: #8792a7;
                font-size: 13px;
                line-height: 1.55;
                margin-left: 51px;
                margin-bottom: 18px;
            }

            /* =================================================
               LABELS AND INPUTS
            ================================================= */

            label {
                color: #46536a !important;
                font-size: 13px !important;
                font-weight: 760 !important;
            }

            div[data-testid="stDateInput"] input,
            div[data-testid="stTextInput"] input,
            div[data-testid="stNumberInput"] input {
                min-height: 48px;

                color: #111827 !important;
                background: #ffffff !important;

                border: 1px solid #dbe2ed !important;
                border-radius: 13px !important;

                font-size: 14px !important;
                font-weight: 550 !important;

                box-shadow:
                    0 4px 12px rgba(15, 23, 42, 0.028);
            }

            div[data-testid="stDateInput"] input:focus,
            div[data-testid="stTextInput"] input:focus,
            div[data-testid="stNumberInput"] input:focus {
                border-color: #818cf8 !important;

                box-shadow:
                    0 0 0 4px rgba(99, 102, 241, 0.11),
                    0 8px 20px rgba(15, 23, 42, 0.045) !important;
            }

            div[data-baseweb="select"] > div {
                min-height: 48px;

                color: #111827 !important;
                background: #ffffff !important;

                border: 1px solid #dbe2ed !important;
                border-radius: 13px !important;

                box-shadow:
                    0 4px 12px rgba(15, 23, 42, 0.028);
            }

            div[data-baseweb="select"] > div:hover {
                border-color: #a5b4fc !important;

                box-shadow:
                    0 0 0 3px rgba(99, 102, 241, 0.06),
                    0 7px 18px rgba(15, 23, 42, 0.04);
            }

            div[data-baseweb="select"] span,
            div[data-baseweb="select"] div {
                color: #111827;
            }

            /* =================================================
               EXPANDERS
            ================================================= */

            div[data-testid="stExpander"] {
                overflow: hidden;

                background:
                    linear-gradient(
                        180deg,
                        #ffffff 0%,
                        #fcfdff 100%
                    );

                border: 1px solid #e1e5ee !important;
                border-radius: 20px !important;

                margin-top: 14px;
                margin-bottom: 18px;

                box-shadow:
                    0 14px 34px rgba(15, 23, 42, 0.05);
            }

            div[data-testid="stExpander"] details summary {
                color: var(--calendar-text) !important;
                padding-top: 6px;
                padding-bottom: 6px;
                font-size: 15px !important;
                font-weight: 830 !important;
            }

            /* =================================================
               METRICS
            ================================================= */

            div[data-testid="stMetric"] {
                position: relative;
                overflow: hidden;

                min-height: 130px;

                background:
                    radial-gradient(
                        circle at 90% 0%,
                        rgba(99, 102, 241, 0.11),
                        transparent 35%
                    ),
                    linear-gradient(
                        145deg,
                        #ffffff 0%,
                        #fafbff 100%
                    );

                border: 1px solid #dde3ee;
                border-radius: 18px;

                padding: 20px;

                box-shadow:
                    0 14px 32px rgba(15, 23, 42, 0.055),
                    inset 0 1px 0 rgba(255, 255, 255, 0.96);

                transition:
                    transform 0.18s ease,
                    border-color 0.18s ease,
                    box-shadow 0.18s ease;
            }

            div[data-testid="stMetric"]::before {
                content: "";
                position: absolute;

                top: 0;
                left: 20px;
                right: 20px;

                height: 3px;

                border-radius: 0 0 999px 999px;

                background:
                    linear-gradient(
                        90deg,
                        var(--calendar-primary),
                        var(--calendar-secondary),
                        var(--calendar-accent)
                    );
            }

            div[data-testid="stMetric"]:hover {
                transform: translateY(-3px);
                border-color: #c7d2fe;

                box-shadow:
                    0 19px 40px rgba(15, 23, 42, 0.075),
                    0 5px 14px rgba(79, 70, 229, 0.06);
            }

            div[data-testid="stMetricLabel"] p {
                color: #788397 !important;
                font-size: 12px !important;
                font-weight: 800 !important;
                line-height: 1.4 !important;
            }

            div[data-testid="stMetricValue"] {
                color: var(--calendar-text) !important;
                font-size: 25px !important;
                font-weight: 900 !important;
                letter-spacing: -0.03em !important;
                white-space: normal !important;
                overflow-wrap: anywhere;
            }

            /* =================================================
               SUMMARY BANNERS
            ================================================= */

            .summary-banner {
                position: relative;
                overflow: hidden;

                color: #ffffff;

                background:
                    radial-gradient(
                        circle at 91% 5%,
                        rgba(255, 255, 255, 0.18),
                        transparent 30%
                    ),
                    linear-gradient(
                        135deg,
                        #3730a3 0%,
                        #5148c8 48%,
                        #7c3aed 100%
                    );

                border: 1px solid rgba(255, 255, 255, 0.15);
                border-radius: 20px;

                padding: 21px 23px;
                margin-top: 20px;
                margin-bottom: 15px;

                box-shadow:
                    0 17px 36px rgba(67, 56, 202, 0.22),
                    inset 0 1px 0 rgba(255, 255, 255, 0.22);
            }

            .summary-banner-title {
                color: #ffffff;
                font-size: 21px;
                font-weight: 900;
                letter-spacing: -0.025em;
                margin-bottom: 5px;
            }

            .summary-banner-text {
                color: rgba(255, 255, 255, 0.79);
                font-size: 13px;
                line-height: 1.55;
            }

            /* =================================================
               TABS
            ================================================= */

            div[data-testid="stTabs"] {
                background:
                    linear-gradient(
                        180deg,
                        #ffffff 0%,
                        #fcfdff 100%
                    );

                border: 1px solid #e1e5ee;
                border-radius: 20px;

                padding: 9px 13px 16px;
                margin-top: 18px;

                box-shadow:
                    0 14px 34px rgba(15, 23, 42, 0.05);
            }

            div[data-testid="stTabs"] [data-baseweb="tab-list"] {
                gap: 6px;
                border-bottom: 1px solid #e2e8f0;
            }

            div[data-testid="stTabs"] button {
                color: #64748b;
                font-size: 13px;
                font-weight: 780;
                padding-left: 14px;
                padding-right: 14px;
            }

            div[data-testid="stTabs"] button[aria-selected="true"] {
                color: var(--calendar-primary) !important;
                font-weight: 900 !important;
            }

            div[data-testid="stTabs"] [data-baseweb="tab-highlight"] {
                height: 3px;

                background:
                    linear-gradient(
                        90deg,
                        var(--calendar-primary),
                        var(--calendar-secondary)
                    ) !important;

                border-radius: 999px;
            }

            /* =================================================
               DATAFRAME AND ALERTS
            ================================================= */

            div[data-testid="stDataFrame"] {
                overflow: hidden;
                background: #ffffff;

                border: 1px solid #e1e5ee;
                border-radius: 16px;

                padding: 3px;

                box-shadow:
                    0 10px 26px rgba(15, 23, 42, 0.045);
            }

            div[data-testid="stAlert"] {
                border-radius: 14px;
                border-width: 1px;
                padding: 13px 15px;

                box-shadow:
                    0 8px 20px rgba(15, 23, 42, 0.045);
            }

            div[data-testid="stAlert"] p {
                font-size: 14px;
                font-weight: 650;
                line-height: 1.55;
            }

            div[data-testid="stHorizontalBlock"] {
                gap: 1rem;
            }

            @media (max-width: 900px) {
                .block-container {
                    padding-top: 1rem;
                    padding-left: 1rem;
                    padding-right: 1rem;
                }

                .calendar-hero {
                    padding: 22px 20px;
                    border-radius: 20px;
                }

                .calendar-hero-grid {
                    display: block;
                }

                .calendar-hero-title {
                    font-size: 28px;
                }

                .calendar-hero-badge {
                    display: inline-block;
                    margin-top: 17px;
                }

                .calendar-section-subtitle {
                    margin-left: 0;
                    margin-top: 8px;
                }

                div[data-testid="stMetric"] {
                    min-height: 112px;
                }
            }
            </style>
            """
        ),
        unsafe_allow_html=True,
    )


def show_calendar_hero():
    hero_html = (
        '<div class="calendar-hero">'
        '<div class="calendar-hero-grid">'
        '<div>'
        '<div class="calendar-hero-title">Budget &amp; Training Calendar</div>'
        '<div class="calendar-hero-subtitle">'
        'Track approved trainings, monthly allocations, university-level '
        'consumption and yearly budget utilization from one consolidated workspace.'
        '</div>'
        '</div>'
        '<div class="calendar-hero-badge">Budget Operations</div>'
        '</div>'
        '</div>'
    )

    st.markdown(
        hero_html,
        unsafe_allow_html=True
    )


def section_header(number, title, subtitle=""):
    header_html = (
        '<div class="calendar-section-header">'
        f'<div class="calendar-section-number">{number}</div>'
        f'<div class="calendar-section-title">{title}</div>'
        '</div>'
    )

    if subtitle:
        header_html += (
            f'<div class="calendar-section-subtitle">{subtitle}</div>'
        )

    st.markdown(
        header_html,
        unsafe_allow_html=True
    )


def summary_banner(title, text):
    banner_html = (
        '<div class="summary-banner">'
        f'<div class="summary-banner-title">{title}</div>'
        f'<div class="summary-banner-text">{text}</div>'
        '</div>'
    )

    st.markdown(
        banner_html,
        unsafe_allow_html=True
    )


def wrap_card(label, value):
    card_html = (
        '<div class="budget-info-card">'
        f'<div class="budget-info-label">{label}</div>'
        f'<div class="budget-info-value">{value}</div>'
        '</div>'
    )

    st.markdown(
        card_html,
        unsafe_allow_html=True
    )


# =========================================================
# BUDGET MASTER
# =========================================================

def load_budget_master():
    try:
        df = pd.read_csv(
            BUDGET_MASTER_FILE,
            encoding="latin1",
        )

        df.columns = (
            df.columns
            .astype(str)
            .str.strip()
            .str.lower()
            .str.replace(" ", "_")
            .str.replace("/", "_")
            .str.replace(".", "", regex=False)
            .str.replace("-", "_")
        )

        df.rename(
            columns={
                "business": "business_type",
                "business_type": "business_type",
                "line_of_business": "line_of_business",
                "programme_name": "programme_name",
                "program_name": "programme_name",
                "job_code": "job_code",
                "training_hour": "training_hours",
                "training_hours": "training_hours",
                "paper_name": "paper_name",
                "batch_number": "batch_number",
                "january": "jan",
                "february": "feb",
                "march": "mar",
                "april": "apr",
                "june": "jun",
                "july": "jul",
                "august": "aug",
                "sept": "sep",
                "september": "sep",
                "october": "oct",
                "november": "nov",
                "december": "dec",
            },
            inplace=True,
        )

        required_columns = [
            "business_type",
            "line_of_business",
            "programme_name",
            "job_code",
            "batch",
            "semester",
            "year",
            "training_hours",
            "paper_name",
            "total",
        ] + list(MONTHS.values())

        for column in required_columns:
            if column not in df.columns:
                df[column] = ""

        for month in MONTHS.values():
            df[month] = df[month].apply(
                safe_number
            )

        df["total"] = df["total"].apply(
            safe_number
        )

        return df.fillna("")

    except Exception as error:
        st.error(
            f"Budget master loading failed: {error}"
        )

        return pd.DataFrame()


def get_unique_values(df, column):
    if column not in df.columns:
        return []

    return (
        df[column]
        .astype(str)
        .str.strip()
        .replace("", pd.NA)
        .dropna()
        .drop_duplicates()
        .sort_values()
        .tolist()
    )


def filter_df(df, column, value):
    if column not in df.columns or not value:
        return df

    return df[
        df[column]
        .astype(str)
        .apply(normalize)
        == normalize(value)
    ]


def get_exact_budget_row(
    df,
    business_type,
    programme_name,
    job_code,
    batch,
    semester,
):
    filtered = df.copy()

    filtered = filter_df(
        filtered,
        "business_type",
        business_type,
    )

    filtered = filter_df(
        filtered,
        "programme_name",
        programme_name,
    )

    filtered = filter_df(
        filtered,
        "job_code",
        job_code,
    )

    filtered = filter_df(
        filtered,
        "batch",
        batch,
    )

    filtered = filter_df(
        filtered,
        "semester",
        semester,
    )

    if filtered.empty:
        return pd.Series(dtype="object")

    return filtered.iloc[0]


def get_month_budget(selected_row, month_number):
    month_column = MONTHS.get(
        month_number
    )

    if selected_row.empty or not month_column:
        return 0

    return safe_number(
        selected_row.get(
            month_column,
            0,
        )
    )


def get_yearly_budget(selected_row):
    if selected_row.empty:
        return 0

    return sum(
        safe_number(
            selected_row.get(
                month,
                0,
            )
        )
        for month in MONTHS.values()
    )


# =========================================================
# APPROVED TRAININGS
# =========================================================

def get_approved_trainings(
    business_type,
    programme_name,
    job_code,
    batch,
    semester,
):
    try:
        df = pd.read_csv(
            REQUESTS_FILE
        ).fillna("")

    except Exception:
        return []

    if "request_status" not in df.columns:
        return []

    if "calendar_status" not in df.columns:
        df["calendar_status"] = ""

    approved_df = df[
        (
            df["request_status"]
            .astype(str)
            .str.strip()
            .isin(
                [
                    "Approved",
                    "Partner Approved",
                    "Director Approved",
                ]
            )
        )
        |
        (
            df["calendar_status"]
            .astype(str)
            .str.strip()
            == "Upcoming Training"
        )
    ].copy()

    if (
        "business_type" in approved_df.columns
        and business_type
    ):
        exact = approved_df[
            approved_df["business_type"]
            .astype(str)
            .apply(normalize)
            == normalize(business_type)
        ]

        if not exact.empty:
            approved_df = exact

    if (
        "programme_name" in approved_df.columns
        and programme_name
    ):
        exact = approved_df[
            approved_df["programme_name"]
            .astype(str)
            .apply(normalize)
            == normalize(programme_name)
        ]

        if not exact.empty:
            approved_df = exact

    trainings = []
    today_date = date.today()

    for _, row in approved_df.iterrows():
        start_date = pd.to_datetime(
            row.get("start_date", ""),
            errors="coerce",
        )

        end_date = pd.to_datetime(
            row.get("end_date", ""),
            errors="coerce",
        )

        if pd.isna(start_date) or pd.isna(end_date):
            continue

        start_date = start_date.date()
        end_date = end_date.date()

        status = (
            "upcoming"
            if end_date >= today_date
            else "scheduled"
        )

        trainings.append(
            {
                "request_id": clean_text(
                    row.get("request_id", "")
                ),

                "college_name": clean_text(
                    row.get(
                        "college_name",
                        "Not Available",
                    )
                ),

                "training_topic": clean_text(
                    row.get(
                        "training_topic",
                        "Training",
                    )
                ),

                "trainer_name": clean_text(
                    row.get(
                        "trainer_name",
                        "Not Assigned",
                    )
                ),

                "business_type": clean_text(
                    row.get("business_type", "")
                ),

                "programme_name": clean_text(
                    row.get("programme_name", "")
                ),

                "job_code": clean_text(
                    row.get("job_code", "")
                ),

                "batch": clean_text(
                    row.get("batch", "")
                ),

                "semester": clean_text(
                    row.get("semester", "")
                ),

                "start_date": start_date,
                "end_date": end_date,

                "cost": safe_number(
                    row.get(
                        "estimated_budget",
                        row.get(
                            "total_expected_budget",
                            0,
                        ),
                    )
                ),

                "status": status,
            }
        )

    return trainings


def get_training_for_day(day_date, trainings):
    for training in trainings:
        if (
            training["start_date"]
            <= day_date
            <= training["end_date"]
        ):
            return training

    return None


def get_yearly_exhausted(
    trainings,
    financial_year_start,
):
    financial_year_start_date = date(
        financial_year_start,
        4,
        1,
    )

    financial_year_end_date = date(
        financial_year_start + 1,
        3,
        31,
    )

    exhausted = 0

    for training in trainings:
        if (
            financial_year_start_date
            <= training["start_date"]
            <= financial_year_end_date
        ):
            exhausted += training["cost"]

    return exhausted


# =========================================================
# SUMMARIES
# =========================================================

def show_training_overview(trainings):
    section_header(
        "01",
        "Training Operations Overview",
        (
            "Review approved trainings, assigned trainers, "
            "dates and budget values for the selected filters."
        ),
    )

    if not trainings:
        st.info(
            "No approved trainings available yet for selected filters."
        )

        return

    rows = []

    for training in trainings:
        rows.append(
            {
                "Request ID": training["request_id"],
                "College": training["college_name"],
                "Training": training["training_topic"],
                "Trainer": training["trainer_name"],

                "Date Range": (
                    f"{training['start_date'].strftime('%d %b %Y')}"
                    f" - "
                    f"{training['end_date'].strftime('%d %b %Y')}"
                ),

                "Budget": (
                    f"₹{training['cost']:,.0f}"
                ),

                "Status": (
                    training["status"].title()
                ),
            }
        )

    st.dataframe(
        pd.DataFrame(rows),
        use_container_width=True,
        hide_index=True,
    )


def show_monthly_summary(
    trainings,
    selected_college,
    selected_month,
    selected_year,
    total_budget,
):
    monthly_trainings = [
        training
        for training in trainings
        if (
            training["start_date"].month
            == selected_month
            and training["start_date"].year
            == selected_year
        )
    ]

    total_budget_used = sum(
        training["cost"]
        for training in monthly_trainings
    )

    total_budget_left = (
        total_budget
        - total_budget_used
    )

    section_header(
        "02",
        "Monthly University Budget Summary",
        (
            f"Budget performance for {selected_college} "
            f"during {MONTH_NAMES[selected_month - 1]} "
            f"{selected_year}."
        ),
    )

    column_1, column_2, column_3, column_4 = (
        st.columns(4)
    )

    with column_1:
        st.metric(
            "Total Budget",
            f"₹{total_budget:,.0f}",
        )

    with column_2:
        st.metric(
            "Budget Used",
            f"₹{total_budget_used:,.0f}",
        )

    with column_3:
        st.metric(
            "Budget Left",
            f"₹{total_budget_left:,.0f}",
        )

    with column_4:
        st.metric(
            "Trainings",
            len(monthly_trainings),
        )


def show_business_year_summary(
    trainings,
    budget_df,
    selected_business_type,
    selected_year,
    selected_college,
):
    section_header(
        "03",
        "Business Year Budget Summary",
        (
            "Compare annual allocation, consumed amount, "
            "remaining budget and university-level usage."
        ),
    )

    filtered_budget = budget_df.copy()

    if selected_business_type != "ALL":
        filtered_budget = filter_df(
            filtered_budget,
            "business_type",
            selected_business_type,
        )

    if "year" in filtered_budget.columns:
        filtered_budget = filtered_budget[
            filtered_budget["year"]
            .astype(str)
            .str.strip()
            == str(selected_year)
        ]

    filtered_trainings = [
        training
        for training in trainings
        if training["start_date"].year
        == selected_year
    ]

    if selected_business_type != "ALL":
        filtered_trainings = [
            training
            for training in filtered_trainings
            if normalize(
                training["business_type"]
            )
            == normalize(
                selected_business_type
            )
        ]

    if selected_college != "ALL":
        filtered_trainings = [
            training
            for training in filtered_trainings
            if normalize(
                training["college_name"]
            )
            == normalize(
                selected_college
            )
        ]

    total_budget = (
        filtered_budget["total"]
        .apply(safe_number)
        .sum()
        if "total" in filtered_budget.columns
        else 0
    )

    consumed = sum(
        training["cost"]
        for training in filtered_trainings
    )

    remaining = total_budget - consumed

    utilization = (
        (consumed / total_budget) * 100
        if total_budget > 0
        else 0
    )

    metric_1, metric_2, metric_3, metric_4 = (
        st.columns(4)
    )

    with metric_1:
        st.metric(
            "Total Budget Allocated",
            f"₹{total_budget:,.0f}",
        )

    with metric_2:
        st.metric(
            "Budget Exhausted",
            f"₹{consumed:,.0f}",
        )

    with metric_3:
        st.metric(
            "Remaining Budget",
            f"₹{remaining:,.0f}",
        )

    with metric_4:
        st.metric(
            "Utilization",
            f"{utilization:.1f}%",
        )

    rows = []

    colleges = sorted(
        set(
            training["college_name"]
            for training in filtered_trainings
            if training["college_name"]
        )
    )

    if selected_college != "ALL":
        colleges = [
            selected_college
        ]

    for college in colleges:
        college_trainings = [
            training
            for training in filtered_trainings
            if normalize(
                training["college_name"]
            )
            == normalize(college)
        ]

        college_consumed = sum(
            training["cost"]
            for training in college_trainings
        )

        rows.append(
            {
                "University": college,
                "Trainings": len(
                    college_trainings
                ),
                "Budget Exhausted": (
                    f"₹{college_consumed:,.0f}"
                ),
            }
        )

    if rows:
        st.dataframe(
            pd.DataFrame(rows),
            use_container_width=True,
            hide_index=True,
            height=250,
        )

    else:
        st.info(
            "No trainings found for selected filters."
        )


# =========================================================
# CALENDAR HTML
# =========================================================

def build_calendar_html(
    selected_year,
    selected_month,
    selected_date,
    trainings,
):
    month_calendar = (
        calendar.Calendar(firstweekday=6)
        .monthdayscalendar(
            selected_year,
            selected_month,
        )
    )

    month_title = (
        MONTH_NAMES[selected_month - 1]
    )

    today_date = date.today()

    html = f"""
    <style>
        * {{
            box-sizing: border-box;
        }}

        body {{
            margin: 0;
            padding: 0;
            background: transparent;

            font-family:
                Inter,
                -apple-system,
                BlinkMacSystemFont,
                "Segoe UI",
                Arial,
                sans-serif;
        }}

        .calendar-wrapper {{
            position: relative;
            overflow: hidden;

            background:
                radial-gradient(
                    circle at 93% 3%,
                    rgba(99, 102, 241, 0.09),
                    transparent 26%
                ),
                linear-gradient(
                    180deg,
                    #ffffff 0%,
                    #fcfdff 100%
                );

            border: 1px solid #e1e5ee;
            border-radius: 25px;

            padding: 26px;

            box-shadow:
                0 18px 42px rgba(15, 23, 42, 0.075);
        }}

        .calendar-wrapper::before {{
            content: "";
            position: absolute;

            top: 0;
            left: 28px;
            right: 28px;

            height: 4px;

            border-radius: 0 0 999px 999px;

            background:
                linear-gradient(
                    90deg,
                    #4f46e5,
                    #7c3aed,
                    #ec4899
                );
        }}

        .calendar-header {{
            display: flex;
            align-items: center;
            justify-content: space-between;

            gap: 20px;

            margin-top: 5px;
            margin-bottom: 23px;
        }}

        .calendar-title {{
            color: #0f172a;
            font-size: 29px;
            font-weight: 900;
            line-height: 1.15;
            letter-spacing: -0.045em;
        }}

        .calendar-subtitle {{
            color: #7b8798;
            font-size: 13px;
            font-weight: 600;
            line-height: 1.55;
            margin-top: 6px;
        }}

        .calendar-badge {{
            flex-shrink: 0;

            color: #4338ca;
            background: #eef2ff;

            border: 1px solid #c7d2fe;
            border-radius: 999px;

            padding: 10px 15px;

            font-size: 12px;
            font-weight: 850;
        }}

        .calendar-grid {{
            display: grid;
            grid-template-columns: repeat(7, 1fr);
            gap: 11px;
        }}

        .weekday {{
            color: #667085;
            background: #f8fafc;

            border: 1px solid #edf0f5;
            border-radius: 10px;

            padding: 10px 4px;

            text-align: center;

            font-size: 12px;
            font-weight: 900;

            letter-spacing: 0.055em;
            text-transform: uppercase;
        }}

        .day-box,
        .empty-box {{
            min-height: 123px;
            border-radius: 17px;
            box-sizing: border-box;
        }}

        .day-box {{
            position: relative;
            overflow: hidden;

            background:
                linear-gradient(
                    145deg,
                    #ffffff 0%,
                    #fcfdff 100%
                );

            border: 1px solid #e4e8f0;
            padding: 12px;

            box-shadow:
                0 4px 12px rgba(15, 23, 42, 0.025);

            transition:
                transform 0.18s ease,
                border-color 0.18s ease,
                box-shadow 0.18s ease;
        }}

        .day-box:hover {{
            transform: translateY(-3px);
            border-color: #c7d2fe;

            box-shadow:
                0 12px 24px rgba(15, 23, 42, 0.085);
        }}

        .empty-box {{
            background:
                linear-gradient(
                    145deg,
                    #f8fafc,
                    #f5f7fa
                );

            border: 1px dashed #e8ebf0;
            opacity: 0.72;
        }}

        .day-number {{
            display: inline-flex;
            align-items: center;
            justify-content: center;

            min-width: 34px;
            height: 34px;

            color: #0f172a;
            background: rgba(255, 255, 255, 0.78);

            border: 1px solid rgba(226, 232, 240, 0.95);
            border-radius: 10px;

            padding: 0 8px;

            font-size: 16px;
            font-weight: 900;

            margin-bottom: 10px;
        }}

        .event-chip {{
            overflow: hidden;

            display: -webkit-box;
            -webkit-line-clamp: 3;
            -webkit-box-orient: vertical;

            color: #172033;
            background: rgba(255, 255, 255, 0.73);

            border: 1px solid rgba(255, 255, 255, 0.90);
            border-radius: 11px;

            padding: 8px 9px;

            font-size: 11px;
            font-weight: 800;
            line-height: 1.35;
        }}

        .scheduled {{
            background:
                radial-gradient(
                    circle at 95% 5%,
                    rgba(236, 72, 153, 0.12),
                    transparent 35%
                ),
                linear-gradient(
                    145deg,
                    #fdf2f8,
                    #fff1f2
                );

            border: 1.5px solid #f9a8d4;
        }}

        .upcoming {{
            background:
                radial-gradient(
                    circle at 95% 5%,
                    rgba(34, 197, 94, 0.11),
                    transparent 35%
                ),
                linear-gradient(
                    145deg,
                    #ecfdf5,
                    #f0fdf4
                );

            border: 1.5px solid #86efac;
        }}

        .today {{
            border: 2px solid #0f172a !important;

            box-shadow:
                0 0 0 4px rgba(15, 23, 42, 0.07);
        }}

        .today .day-number {{
            color: #ffffff;
            background: #0f172a;
            border-color: #0f172a;
        }}

        .selected {{
            border: 2px solid #4f46e5 !important;

            box-shadow:
                0 0 0 5px rgba(79, 70, 229, 0.13),
                0 14px 28px rgba(79, 70, 229, 0.13);
        }}

        .selected .day-number {{
            color: #ffffff;

            background:
                linear-gradient(
                    135deg,
                    #4f46e5,
                    #7c3aed
                );

            border-color: transparent;
        }}

        .legend {{
            display: flex;
            flex-wrap: wrap;
            gap: 11px;
            margin-top: 22px;
        }}

        .legend-item {{
            display: flex;
            align-items: center;

            color: #475569;
            background: #f8fafc;

            border: 1px solid #e6eaf0;
            border-radius: 999px;

            padding: 8px 11px;

            font-size: 12px;
            font-weight: 800;
        }}

        .dot {{
            width: 11px;
            height: 11px;
            display: inline-block;
            border-radius: 999px;
            margin-right: 7px;
        }}

        .pink {{
            background: #f472b6;
        }}

        .green {{
            background: #4ade80;
        }}

        .blue {{
            background: #4f46e5;
        }}

        .dark {{
            background: #0f172a;
        }}
    </style>

    <div class="calendar-wrapper">
        <div class="calendar-header">
            <div>
                <div class="calendar-title">
                    {month_title} {selected_year}
                </div>

                <div class="calendar-subtitle">
                    Approved training schedule and budget-blocking view
                </div>
            </div>

            <div class="calendar-badge">
                Selected: {selected_date.strftime("%d %b %Y")}
            </div>
        </div>

        <div class="calendar-grid">
    """

    for day_name in [
        "Sun",
        "Mon",
        "Tue",
        "Wed",
        "Thu",
        "Fri",
        "Sat",
    ]:
        html += (
            f"""
            <div class="weekday">
                {day_name}
            </div>
            """
        )

    for week in month_calendar:
        for day_number in week:
            if day_number == 0:
                html += (
                    """
                    <div class="empty-box"></div>
                    """
                )

            else:
                current_date = date(
                    selected_year,
                    selected_month,
                    day_number,
                )

                training = get_training_for_day(
                    current_date,
                    trainings,
                )

                status_class = ""
                event_title = ""

                if training:
                    status_class = training.get(
                        "status",
                        "upcoming",
                    )

                    event_title = training[
                        "training_topic"
                    ]

                today_class = (
                    "today"
                    if current_date == today_date
                    else ""
                )

                selected_class = (
                    "selected"
                    if current_date == selected_date
                    else ""
                )

                event_html = ""

                if event_title:
                    event_html = (
                        f"""
                        <div class="event-chip">
                            {event_title}
                        </div>
                        """
                    )

                html += (
                    f"""
                    <div class="day-box {status_class} {today_class} {selected_class}">
                        <div class="day-number">
                            {day_number}
                        </div>

                        {event_html}
                    </div>
                    """
                )

    html += """
        </div>

        <div class="legend">
            <div class="legend-item">
                <span class="dot pink"></span>
                Past / Scheduled
            </div>

            <div class="legend-item">
                <span class="dot green"></span>
                Upcoming Training
            </div>

            <div class="legend-item">
                <span class="dot blue"></span>
                Selected Date
            </div>

            <div class="legend-item">
                <span class="dot dark"></span>
                Today
            </div>
        </div>
    </div>
    """

    return html


# =========================================================
# MAIN PAGE
# =========================================================

def show_budget_calendar():

    apply_budget_calendar_ui()
    show_calendar_hero()

    user_role = st.session_state.get(
        "role",
        "",
    )

    budget_df = load_budget_master()

    if budget_df.empty:
        st.error(
            "No budget data found in budget.csv."
        )

        return

    summary_trainings = get_approved_trainings(
        "",
        "",
        "",
        "",
        "",
    )

    # =====================================================
    # CALENDAR PERIOD
    # =====================================================

    with st.container(border=True):

        section_header(
            "01",
            "Calendar Period",
            (
                "Choose the year, month, date and business type "
                "for the calendar and monthly budget view."
            ),
        )

        filter_1, filter_2, filter_3, filter_4 = (
            st.columns(4)
        )

        with filter_1:
            selected_year = st.selectbox(
                "Year",
                [
                    2026,
                    2027,
                    2028,
                    2029,
                    2030,
                ],
                key="calendar_year",
            )

        with filter_2:
            selected_month_name = st.selectbox(
                "Month",
                MONTH_NAMES,
                index=6,
                key="calendar_month",
            )

        selected_month = (
            MONTH_NAMES.index(
                selected_month_name
            )
            + 1
        )

        maximum_day = calendar.monthrange(
            selected_year,
            selected_month,
        )[1]

        default_selected_date = date(
            selected_year,
            selected_month,
            min(15, maximum_day),
        )

        with filter_3:
            selected_date = st.date_input(
                "Date",
                value=default_selected_date,
                min_value=date(
                    selected_year,
                    selected_month,
                    1,
                ),
                max_value=date(
                    selected_year,
                    selected_month,
                    maximum_day,
                ),
                key="calendar_selected_date",
            )

        with filter_4:
            business_type = st.selectbox(
                "Business Type",
                [
                    "B2B",
                    "B2C",
                    "B2I",
                ],
                index=2,
                key="calendar_business_type",
            )

    # =====================================================
    # ADVANCED BUDGET FILTERS
    # =====================================================

    with st.expander(
        "Advanced Budget Filters",
        expanded=True,
    ):

        section_header(
            "02",
            "Budget Line Selection",
            (
                "Select the university and exact budget-master "
                "line used for monthly and yearly calculations."
            ),
        )

        budget_filter_1, budget_filter_2, budget_filter_3 = (
            st.columns(3)
        )

        with budget_filter_1:
            college_options = []

            try:
                request_df = pd.read_csv(
                    REQUESTS_FILE
                ).fillna("")

                if "college_name" in request_df.columns:
                    college_options = (
                        request_df["college_name"]
                        .astype(str)
                        .str.strip()
                        .replace("", pd.NA)
                        .dropna()
                        .drop_duplicates()
                        .sort_values()
                        .tolist()
                    )

            except Exception:
                pass

            if not college_options:
                college_options = [
                    "Not Available"
                ]

            selected_college = st.selectbox(
                "University",
                college_options,
                key="calendar_college",
            )

        filtered_df = filter_df(
            budget_df,
            "business_type",
            business_type,
        )

        with budget_filter_2:
            programme_name = st.selectbox(
                "Programme Name",
                (
                    get_unique_values(
                        filtered_df,
                        "programme_name",
                    )
                    or ["Not Available"]
                ),
                key="calendar_programme",
            )

        filtered_df = filter_df(
            filtered_df,
            "programme_name",
            programme_name,
        )

        with budget_filter_3:
            job_code = st.selectbox(
                "Job Code",
                (
                    get_unique_values(
                        filtered_df,
                        "job_code",
                    )
                    or ["Not Available"]
                ),
                key="calendar_job_code",
            )

        filtered_df = filter_df(
            filtered_df,
            "job_code",
            job_code,
        )

        budget_filter_4, budget_filter_5 = (
            st.columns(2)
        )

        with budget_filter_4:
            batch = st.selectbox(
                "Batch",
                (
                    get_unique_values(
                        filtered_df,
                        "batch",
                    )
                    or ["Not Available"]
                ),
                key="calendar_batch",
            )

        filtered_df = filter_df(
            filtered_df,
            "batch",
            batch,
        )

        with budget_filter_5:
            semester = st.selectbox(
                "Semester",
                (
                    get_unique_values(
                        filtered_df,
                        "semester",
                    )
                    or ["Not Available"]
                ),
                key="calendar_semester",
            )

    # =====================================================
    # CALCULATIONS
    # =====================================================

    selected_row = get_exact_budget_row(
        budget_df,
        business_type,
        programme_name,
        job_code,
        batch,
        semester,
    )

    month_budget = get_month_budget(
        selected_row,
        selected_month,
    )

    trainings = get_approved_trainings(
        business_type,
        programme_name,
        job_code,
        batch,
        semester,
    )

    trainings = [
        training
        for training in trainings
        if normalize(
            training["college_name"]
        )
        == normalize(
            selected_college
        )
    ]

    monthly_trainings = [
        training
        for training in trainings
        if (
            training["start_date"].month
            == selected_month
            and training["start_date"].year
            == selected_year
        )
    ]

    budget_used = sum(
        training["cost"]
        for training in monthly_trainings
    )

    budget_left = (
        month_budget
        - budget_used
    )

    # =====================================================
    # MONTHLY SNAPSHOT
    # =====================================================

    summary_banner(
        "Monthly Budget Snapshot",
        (
            f"Budget position for {selected_college} during "
            f"{selected_month_name} {selected_year}."
        ),
    )

    metric_1, metric_2, metric_3, metric_4 = (
        st.columns(4)
    )

    with metric_1:
        st.metric(
            "Month Budget",
            f"₹{month_budget:,.0f}",
        )

    with metric_2:
        st.metric(
            "Budget Used",
            f"₹{budget_used:,.0f}",
        )

    with metric_3:
        st.metric(
            "Budget Left",
            f"₹{budget_left:,.0f}",
        )

    with metric_4:
        st.metric(
            "Trainings",
            len(monthly_trainings),
        )

    # =====================================================
    # COLLEGE BUDGET VIEW
    # =====================================================

    with st.expander(
        "College Budget View",
        expanded=True,
    ):

        section_header(
            "03",
            "College Budget View",
            (
                "Review yearly budget allocation and consumption "
                "across business types and universities."
            ),
        )

        college_budget_options = [
            "ALL"
        ]

        for training in summary_trainings:
            college_name = training[
                "college_name"
            ]

            if (
                college_name
                and college_name
                not in college_budget_options
            ):
                college_budget_options.append(
                    college_name
                )

        college_filter_1, college_filter_2, college_filter_3 = (
            st.columns(3)
        )

        with college_filter_1:
            selected_budget_college = st.selectbox(
                "College",
                college_budget_options,
                key="calendar_college_budget_view",
            )

        with college_filter_2:
            selected_budget_business_type = st.selectbox(
                "Business Type",
                [
                    "ALL",
                    "B2B",
                    "B2C",
                    "B2I",
                ],
                index=0,
                key="calendar_budget_business_type",
            )

        with college_filter_3:
            if "year" in budget_df.columns:
                year_options = (
                    budget_df["year"]
                    .astype(str)
                    .str.strip()
                    .replace("", pd.NA)
                    .dropna()
                    .drop_duplicates()
                    .sort_values()
                    .tolist()
                )

            else:
                year_options = [
                    "2026",
                    "2027",
                    "2028",
                    "2029",
                    "2030",
                ]

            if not year_options:
                year_options = [
                    "2026",
                    "2027",
                    "2028",
                    "2029",
                    "2030",
                ]

            selected_budget_year = st.selectbox(
                "Budget Year",
                year_options,
                index=0,
                key="calendar_budget_year",
            )

        selected_budget_year = int(
            float(
                selected_budget_year
            )
        )

        show_business_year_summary(
            summary_trainings,
            budget_df,
            selected_budget_business_type,
            selected_budget_year,
            selected_budget_college,
        )

    # =====================================================
    # CALENDAR VIEW
    # =====================================================

    summary_banner(
        "Training Calendar",
        (
            "Past trainings are shown in pink, upcoming "
            "trainings in green, and the selected date in purple."
        ),
    )

    calendar_html = build_calendar_html(
        selected_year,
        selected_month,
        selected_date,
        trainings,
    )

    components.html(
        calendar_html,
        height=670,
        scrolling=True,
    )

    # =====================================================
    # DETAILS TABS
    # =====================================================

    if user_role == "Requester":
        tab_1, tab_2 = st.tabs(
            [
                "Training Overview",
                "Monthly Summary",
            ]
        )

    else:
        tab_1, tab_2, tab_3 = st.tabs(
            [
                "Training Overview",
                "Monthly Summary",
                "Yearly Budget",
            ]
        )

    with tab_1:
        show_training_overview(
            trainings
        )

    with tab_2:
        show_monthly_summary(
            trainings,
            selected_college,
            selected_month,
            selected_year,
            month_budget,
        )

    if user_role != "Requester":
        with tab_3:

            section_header(
                "04",
                "Yearly Budget Checker",
                (
                    "Compare annual available budget, exhausted "
                    "amount and utilization for the selected budget line."
                ),
            )

            yearly_filter_1, yearly_filter_2 = (
                st.columns(2)
            )

            with yearly_filter_1:
                financial_year_start = st.selectbox(
                    "Financial Year",
                    [
                        2026,
                        2027,
                        2028,
                        2029,
                    ],
                    format_func=lambda year: (
                        f"{year}-"
                        f"{str(year + 1)[-2:]}"
                    ),
                    key="calendar_financial_year",
                )

            with yearly_filter_2:
                st.write(
                    "Selected Budget Line"
                )

                st.info(
                    (
                        f"{business_type} | "
                        f"{programme_name} | "
                        f"{job_code} | "
                        f"Batch {batch} | "
                        f"Sem {semester}"
                    )
                )

            total_budget = get_yearly_budget(
                selected_row
            )

            exhausted_year = get_yearly_exhausted(
                trainings,
                financial_year_start,
            )

            left_year = (
                total_budget
                - exhausted_year
            )

            utilization = (
                (
                    exhausted_year
                    / total_budget
                )
                * 100
                if total_budget > 0
                else 0
            )

            yearly_metric_1, yearly_metric_2, yearly_metric_3, yearly_metric_4 = (
                st.columns(4)
            )

            with yearly_metric_1:
                st.metric(
                    "Total Available Budget",
                    f"₹{total_budget:,.0f}",
                )

            with yearly_metric_2:
                st.metric(
                    "Total Exhausted",
                    f"₹{exhausted_year:,.0f}",
                )

            with yearly_metric_3:
                st.metric(
                    "Total Left",
                    f"₹{left_year:,.0f}",
                )

            with yearly_metric_4:
                st.metric(
                    "Utilization",
                    f"{utilization:.1f}%",
                )