import streamlit as st
import pandas as pd
import calendar
from datetime import date


REQUESTS_FILE = "requests.csv"
INVOICES_FILE = "invoices.csv"
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

def clean_value(value, default=""):
    try:
        if pd.isna(value):
            return default

        value = str(value).strip()

        if value.lower() in [
            "nan",
            "none",
            "nat",
            "",
        ]:
            return default

        return value

    except Exception:
        return default


def safe_number(value, default=0):
    try:
        if pd.isna(value):
            return default

        value = (
            str(value)
            .replace(",", "")
            .replace("₹", "")
            .strip()
        )

        if value.lower() in [
            "nan",
            "none",
            "nat",
            "",
        ]:
            return default

        return float(value)

    except Exception:
        return default


def normalize(value):
    return (
        clean_value(value)
        .lower()
        .replace(" ", "")
        .replace("_", "")
        .replace("-", "")
    )


def status_count(df, status):
    if (
        df.empty
        or "request_status" not in df.columns
    ):
        return 0

    return len(
        df[
            df["request_status"]
            .astype(str)
            .str.strip()
            .str.lower()
            == status.lower()
        ]
    )


# =========================================================
# DASHBOARD UI
# =========================================================

def apply_dashboard_ui():
    st.markdown(
        """
        <style>
        :root {
            --dashboard-primary: #4f46e5;
            --dashboard-primary-dark: #3730a3;
            --dashboard-secondary: #7c3aed;
            --dashboard-accent: #ec4899;

            --dashboard-background: #f5f7fc;
            --dashboard-surface: #ffffff;
            --dashboard-surface-soft: #f8fafc;

            --dashboard-text: #0f172a;
            --dashboard-text-soft: #64748b;
            --dashboard-border: #e2e8f0;

            --dashboard-success: #16a34a;
            --dashboard-warning: #d97706;
            --dashboard-danger: #dc2626;
        }

        /* =====================================================
           PAGE
        ===================================================== */

        .stApp {
            background:
                radial-gradient(
                    circle at 88% 2%,
                    rgba(79, 70, 229, 0.09),
                    transparent 25%
                ),
                radial-gradient(
                    circle at 10% 42%,
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
            border-bottom: 1px solid rgba(226, 232, 240, 0.64);
        }

        .block-container {
            max-width: 1480px;
            padding-top: 1.5rem;
            padding-bottom: 4rem;
        }

        /* =====================================================
           HERO HEADER
        ===================================================== */

        .dashboard-hero {
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

        .dashboard-hero::before {
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

        .dashboard-hero-grid {
            position: relative;
            z-index: 2;

            display: flex;
            align-items: center;
            justify-content: space-between;

            gap: 24px;
        }

        .dashboard-hero-title {
            color: var(--dashboard-text);

            font-size: 35px;
            font-weight: 900;
            line-height: 1.15;
            letter-spacing: -0.045em;

            margin-bottom: 8px;
        }

        .dashboard-hero-subtitle {
            color: #738096;

            font-size: 15px;
            font-weight: 520;
            line-height: 1.65;

            max-width: 800px;
        }

        .dashboard-hero-badge {
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

        /* =====================================================
           SECTION HEADERS
        ===================================================== */

        .dashboard-section {
            display: flex;
            align-items: center;

            gap: 12px;

            margin-top: 26px;
            margin-bottom: 6px;
        }

        .dashboard-section-number {
            width: 39px;
            height: 39px;

            display: flex;
            align-items: center;
            justify-content: center;

            color: #ffffff;

            background:
                linear-gradient(
                    135deg,
                    var(--dashboard-primary),
                    var(--dashboard-secondary)
                );

            border-radius: 12px;

            font-size: 13px;
            font-weight: 900;

            box-shadow:
                0 9px 19px rgba(79, 70, 229, 0.24);
        }

        .dashboard-section-title {
            color: var(--dashboard-text);

            font-size: 21px;
            font-weight: 850;
            line-height: 1.25;
            letter-spacing: -0.025em;
        }

        .dashboard-section-subtitle {
            color: #8792a7;

            font-size: 13px;
            line-height: 1.55;

            margin-left: 51px;
            margin-bottom: 18px;
        }

        /* =====================================================
           SUMMARY BANNERS
        ===================================================== */

        .dashboard-banner {
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

            margin-top: 24px;
            margin-bottom: 15px;

            box-shadow:
                0 17px 36px rgba(67, 56, 202, 0.22),
                inset 0 1px 0 rgba(255, 255, 255, 0.22);
        }

        .dashboard-banner-title {
            color: #ffffff;

            font-size: 21px;
            font-weight: 900;
            letter-spacing: -0.025em;

            margin-bottom: 5px;
        }

        .dashboard-banner-text {
            color: rgba(255, 255, 255, 0.80);

            font-size: 13px;
            line-height: 1.55;
        }

        /* =====================================================
           METRICS
        ===================================================== */

        div[data-testid="stMetric"] {
            position: relative;
            overflow: hidden;

            min-height: 128px;

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
                    var(--dashboard-primary),
                    var(--dashboard-secondary),
                    var(--dashboard-accent)
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

            letter-spacing: 0.015em !important;
        }

        div[data-testid="stMetricValue"] {
            color: var(--dashboard-text) !important;

            font-size: 25px !important;
            font-weight: 900 !important;
            letter-spacing: -0.03em !important;

            white-space: normal !important;
            overflow-wrap: anywhere;
        }

        /* =====================================================
           FILTERS
        ===================================================== */

        label {
            color: #46536a !important;

            font-size: 13px !important;
            font-weight: 760 !important;
        }

        div[data-baseweb="select"] > div {
            min-height: 48px;

            color: #111827 !important;
            background: #ffffff !important;

            border: 1px solid #dbe2ed !important;
            border-radius: 13px !important;

            box-shadow:
                0 4px 12px rgba(15, 23, 42, 0.028);

            transition:
                border-color 0.16s ease,
                box-shadow 0.16s ease;
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

        /* =====================================================
           TABS
        ===================================================== */

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
            gap: 5px;

            border-bottom: 1px solid #e2e8f0;
        }

        div[data-testid="stTabs"] button {
            color: #64748b;

            font-size: 12px;
            font-weight: 780;

            padding-left: 12px;
            padding-right: 12px;
        }

        div[data-testid="stTabs"] button:hover {
            color: var(--dashboard-primary) !important;
            background: #f5f3ff;
        }

        div[data-testid="stTabs"]
        button[aria-selected="true"] {
            color: var(--dashboard-primary) !important;
            font-weight: 900 !important;
        }

        div[data-testid="stTabs"]
        [data-baseweb="tab-highlight"] {
            height: 3px;

            background:
                linear-gradient(
                    90deg,
                    var(--dashboard-primary),
                    var(--dashboard-secondary)
                ) !important;

            border-radius: 999px;
        }

        /* =====================================================
           DATAFRAME
        ===================================================== */

        div[data-testid="stDataFrame"] {
            overflow: hidden;

            background: #ffffff;

            border: 1px solid #e1e5ee;
            border-radius: 16px;

            padding: 3px;

            box-shadow:
                0 10px 26px rgba(15, 23, 42, 0.045);
        }

        /* =====================================================
           PROGRESS BAR
        ===================================================== */

        div[data-testid="stProgress"] > div {
            overflow: hidden;

            background: #e8ecf3;

            border-radius: 999px;
        }

        div[data-testid="stProgress"] > div > div {
            height: 10px;

            border-radius: 999px;

            background:
                linear-gradient(
                    90deg,
                    var(--dashboard-primary),
                    var(--dashboard-secondary)
                ) !important;
        }

        /* =====================================================
           OCCUPANCY CARDS
        ===================================================== */

        .occupancy-card {
            position: relative;
            overflow: hidden;

            background:
                radial-gradient(
                    circle at 94% 4%,
                    rgba(99, 102, 241, 0.10),
                    transparent 34%
                ),
                linear-gradient(
                    145deg,
                    #ffffff 0%,
                    #fbfcff 100%
                );

            border: 1px solid #e0e5ee;
            border-radius: 16px;

            padding: 16px 18px;
            margin-bottom: 10px;

            box-shadow:
                0 9px 22px rgba(15, 23, 42, 0.045);
        }

        .occupancy-name {
            color: var(--dashboard-text);

            font-size: 15px;
            font-weight: 850;

            margin-bottom: 5px;
        }

        .occupancy-details {
            color: #748095;

            font-size: 12px;
            font-weight: 600;
            line-height: 1.5;
        }

        .occupancy-status {
            display: inline-block;

            color: #4338ca;
            background: #eef2ff;

            border: 1px solid #c7d2fe;
            border-radius: 999px;

            padding: 4px 9px;
            margin-left: 5px;

            font-size: 11px;
            font-weight: 850;
        }

        /* =====================================================
           ALERTS
        ===================================================== */

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

        hr {
            border: none;
            border-top: 1px solid #e2e8f0;

            margin: 24px 0;
        }

        @media (max-width: 900px) {
            .block-container {
                padding-top: 1rem;
                padding-left: 1rem;
                padding-right: 1rem;
            }

            .dashboard-hero {
                padding: 22px 20px;
                border-radius: 20px;
            }

            .dashboard-hero-grid {
                display: block;
            }

            .dashboard-hero-title {
                font-size: 28px;
            }

            .dashboard-hero-badge {
                display: inline-block;
                margin-top: 17px;
            }

            .dashboard-section-subtitle {
                margin-left: 0;
                margin-top: 8px;
            }

            div[data-testid="stMetric"] {
                min-height: 110px;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def show_dashboard_hero(role, username):
    safe_role = clean_value(
        role,
        "Portal User",
    )

    safe_username = clean_value(
        username,
        "User",
    )

    hero_html = (
        '<div class="dashboard-hero">'
        '<div class="dashboard-hero-grid">'
        '<div>'
        '<div class="dashboard-hero-title">'
        'Training Operations Dashboard'
        '</div>'
        '<div class="dashboard-hero-subtitle">'
        f'Welcome back, {safe_username}. Track universities, budgets, '
        'trainers, occupancy, clashes and approval operations from one '
        'consolidated workspace.'
        '</div>'
        '</div>'
        f'<div class="dashboard-hero-badge">{safe_role} Workspace</div>'
        '</div>'
        '</div>'
    )

    st.markdown(
        hero_html,
        unsafe_allow_html=True,
    )


def dashboard_section(
    number,
    title,
    subtitle="",
):
    section_html = (
        '<div class="dashboard-section">'
        f'<div class="dashboard-section-number">{number}</div>'
        f'<div class="dashboard-section-title">{title}</div>'
        '</div>'
    )

    if subtitle:
        section_html += (
            '<div class="dashboard-section-subtitle">'
            f'{subtitle}'
            '</div>'
        )

    st.markdown(
        section_html,
        unsafe_allow_html=True,
    )


def dashboard_banner(title, text):
    banner_html = (
        '<div class="dashboard-banner">'
        f'<div class="dashboard-banner-title">{title}</div>'
        f'<div class="dashboard-banner-text">{text}</div>'
        '</div>'
    )

    st.markdown(
        banner_html,
        unsafe_allow_html=True,
    )


def occupancy_card(
    trainer,
    status,
    trainings,
    occupied_days,
    maximum_days,
    occupancy,
):
    card_html = (
        '<div class="occupancy-card">'
        f'<div class="occupancy-name">{trainer}'
        f'<span class="occupancy-status">{status}</span>'
        '</div>'
        '<div class="occupancy-details">'
        f'{trainings} training(s) &nbsp;•&nbsp; '
        f'{occupied_days}/{maximum_days} occupied days &nbsp;•&nbsp; '
        f'{occupancy:.1f}% occupied'
        '</div>'
        '</div>'
    )

    st.markdown(
        card_html,
        unsafe_allow_html=True,
    )


# =========================================================
# BUDGET MASTER
# =========================================================

def load_budget_master():
    try:
        df = pd.read_csv(
            BUDGET_MASTER_FILE,
            encoding="latin1",
        ).fillna("")

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
                "total_budget": "total",
                "annual_total": "total",
                "grand_total": "total",
            },
            inplace=True,
        )

        for month in MONTHS.values():
            if month not in df.columns:
                df[month] = 0

            df[month] = df[month].apply(
                safe_number
            )

        return df

    except Exception:
        return pd.DataFrame()


# =========================================================
# STATUS CARDS
# =========================================================

def show_status_cards(df):
    total_requests = len(df)

    pending_mediator = status_count(
        df,
        "Pending Mediator Review",
    )

    pending_partner = status_count(
        df,
        "Pending Director Approval",
    )

    approved = (
        status_count(
            df,
            "Approved",
        )
        + status_count(
            df,
            "Partner Approved",
        )
        + status_count(
            df,
            "Director Approved",
        )
    )

    rejected = (
        status_count(
            df,
            "Rejected",
        )
        + status_count(
            df,
            "Director Rejected",
        )
        + status_count(
            df,
            "Partner Rejected",
        )
    )

    column_1, column_2, column_3, column_4, column_5 = (
        st.columns(5)
    )

    with column_1:
        st.metric(
            "Total Requests",
            total_requests,
        )

    with column_2:
        st.metric(
            "Pending Approver",
            pending_mediator,
        )

    with column_3:
        st.metric(
            "Pending Partner",
            pending_partner,
        )

    with column_4:
        st.metric(
            "Approved",
            approved,
        )

    with column_5:
        st.metric(
            "Rejected",
            rejected,
        )


# =========================================================
# REQUEST TABLE
# =========================================================

def show_request_table(df, title):
    dashboard_section(
        "05",
        title,
        (
            "Review the latest request records, budgets, "
            "trainers and approval status."
        ),
    )

    if df.empty:
        st.info(
            "No records available."
        )

        return

    display_columns = [
        "request_id",
        "college_name",
        "business_type",
        "training_topic",
        "trainer_name",
        "training_days",
        "total_hours",
        "estimated_budget",
        "total_expected_budget",
        "request_status",
        "created_at",
        "request_date",
    ]

    available_columns = [
        column
        for column in display_columns
        if column in df.columns
    ]

    if not available_columns:
        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True,
        )

        return

    display_df = df[
        available_columns
    ].copy()

    rename_map = {
        "request_id": "Request ID",
        "college_name": "University",
        "business_type": "Business Type",
        "training_topic": "Training Topic",
        "trainer_name": "Trainer",
        "training_days": "Days",
        "total_hours": "Hours",
        "estimated_budget": "Estimated Budget",
        "total_expected_budget": "Requester Budget",
        "request_status": "Status",
        "created_at": "Created At",
        "request_date": "Request Date",
    }

    display_df.rename(
        columns=rename_map,
        inplace=True,
    )

    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True,
    )


# =========================================================
# TRAINING HELPERS
# =========================================================

def get_budget_amount(row):
    amount = safe_number(
        row.get(
            "estimated_budget",
            0,
        )
    )

    if amount == 0:
        amount = safe_number(
            row.get(
                "total_expected_budget",
                0,
            )
        )

    if amount == 0:
        amount = safe_number(
            row.get(
                "total_estimated_cost",
                0,
            )
        )

    return amount


def get_training_status(row):
    today = pd.Timestamp(
        date.today()
    )

    start_date = row.get(
        "start_date_parsed"
    )

    end_date = row.get(
        "end_date_parsed"
    )

    if (
        pd.isna(start_date)
        or pd.isna(end_date)
    ):
        return "Unknown"

    if start_date <= today <= end_date:
        return "Ongoing"

    if end_date < today:
        return "Completed"

    return "Upcoming"


# =========================================================
# MONTHLY TRAINING AND BUDGET DASHBOARD
# =========================================================

def show_monthly_training_budget_dashboard(
    requests_df,
):
    dashboard_banner(
        "Monthly Training & Budget Dashboard",
        (
            "Filter the operational view by year, month, "
            "university and trainer to review budget usage "
            "and training activity."
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
            key="dashboard_budget_year",
        )

    with filter_2:
        selected_month_name = st.selectbox(
            "Month",
            MONTH_NAMES,
            index=date.today().month - 1,
            key="dashboard_budget_month",
        )

    if "college_name" in requests_df.columns:
        universities = (
            requests_df["college_name"]
            .astype(str)
            .str.strip()
            .replace("", pd.NA)
            .dropna()
            .drop_duplicates()
            .sort_values()
            .tolist()
        )

    else:
        universities = []

    universities = [
        "ALL"
    ] + universities

    with filter_3:
        selected_university = st.selectbox(
            "University",
            universities,
            key="dashboard_university",
        )

    selected_month = (
        MONTH_NAMES.index(
            selected_month_name
        )
        + 1
    )

    month_column = MONTHS[
        selected_month
    ]

    month_start = pd.Timestamp(
        date(
            selected_year,
            selected_month,
            1,
        )
    )

    last_day = calendar.monthrange(
        selected_year,
        selected_month,
    )[1]

    month_end = pd.Timestamp(
        date(
            selected_year,
            selected_month,
            last_day,
        )
    )

    approved_statuses = [
        "Approved",
        "Partner Approved",
        "Director Approved",
    ]

    df = requests_df.copy()

    if "request_status" not in df.columns:
        st.info(
            "request_status column not found."
        )

        return

    if "calendar_status" not in df.columns:
        df["calendar_status"] = ""

    df = df[
        (
            df["request_status"]
            .astype(str)
            .str.strip()
            .isin(
                approved_statuses
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

    if "start_date" not in df.columns:
        df["start_date"] = ""

    if "end_date" not in df.columns:
        df["end_date"] = ""

    df["start_date_parsed"] = pd.to_datetime(
        df["start_date"],
        errors="coerce",
    )

    df["end_date_parsed"] = pd.to_datetime(
        df["end_date"],
        errors="coerce",
    )

    df = df.dropna(
        subset=[
            "start_date_parsed",
            "end_date_parsed",
        ]
    )

    monthly_df = df[
        (
            df["start_date_parsed"]
            <= month_end
        )
        &
        (
            df["end_date_parsed"]
            >= month_start
        )
    ].copy()

    if selected_university != "ALL":
        monthly_df = monthly_df[
            monthly_df["college_name"]
            .astype(str)
            .apply(normalize)
            == normalize(
                selected_university
            )
        ]

    monthly_df["budget_used"] = (
        monthly_df.apply(
            get_budget_amount,
            axis=1,
        )
    )

    monthly_df["training_status"] = (
        monthly_df.apply(
            get_training_status,
            axis=1,
        )
    )

    trainer_options = [
        "ALL"
    ]

    if "trainer_name" in monthly_df.columns:
        trainer_options += sorted(
            monthly_df["trainer_name"]
            .astype(str)
            .str.strip()
            .replace("", pd.NA)
            .dropna()
            .drop_duplicates()
            .tolist()
        )

    with filter_4:
        selected_trainer = st.selectbox(
            "Trainer",
            trainer_options,
            key="dashboard_trainer_filter",
        )

    trainer_df = monthly_df.copy()

    if selected_trainer != "ALL":
        trainer_df = trainer_df[
            trainer_df["trainer_name"]
            .astype(str)
            .apply(normalize)
            == normalize(
                selected_trainer
            )
        ]

    budget_master_df = load_budget_master()

    if (
        not budget_master_df.empty
        and month_column
        in budget_master_df.columns
    ):
        monthly_available_budget = (
            budget_master_df[
                month_column
            ]
            .apply(safe_number)
            .sum()
        )

    else:
        monthly_available_budget = (
            monthly_df["budget_used"].sum()
            if not monthly_df.empty
            else 0
        )

    budget_used = (
        monthly_df["budget_used"].sum()
        if not monthly_df.empty
        else 0
    )

    budget_left = (
        monthly_available_budget
        - budget_used
    )

    total_trainings = len(
        monthly_df
    )

    dashboard_section(
        "02",
        "Monthly Budget Snapshot",
        (
            f"Budget and training activity for "
            f"{selected_month_name} {selected_year}."
        ),
    )

    metric_1, metric_2, metric_3, metric_4 = (
        st.columns(4)
    )

    with metric_1:
        st.metric(
            "Budget",
            f"₹{monthly_available_budget:,.0f}",
        )

    with metric_2:
        st.metric(
            "Consumed",
            f"₹{budget_used:,.0f}",
        )

    with metric_3:
        st.metric(
            "Remaining",
            f"₹{budget_left:,.0f}",
        )

    with metric_4:
        st.metric(
            "Trainings",
            total_trainings,
        )

    if monthly_df.empty:
        st.info(
            (
                "No approved trainings found for "
                f"{selected_month_name} {selected_year}."
            )
        )

        return

    tab_1, tab_2, tab_3, tab_4, tab_5, tab_6 = st.tabs(
        [
            "Ongoing Trainings",
            "Trainer Tracker",
            "Occupancy",
            "University Summary",
            "Utilization",
            "Clash / Month Summary",
        ]
    )

    # =====================================================
    # ONGOING TRAININGS
    # =====================================================

    with tab_1:
        dashboard_section(
            "01",
            "Ongoing Training Programs",
            (
                "Review all approved training programs "
                "overlapping with the selected month."
            ),
        )

        ongoing_columns = [
            column
            for column in [
                "request_id",
                "trainer_name",
                "college_name",
                "training_topic",
                "start_date",
                "end_date",
                "budget_used",
                "training_status",
            ]
            if column in monthly_df.columns
        ]

        ongoing_df = monthly_df[
            ongoing_columns
        ].copy()

        ongoing_df.rename(
            columns={
                "request_id": "Request ID",
                "trainer_name": "Trainer",
                "college_name": "University",
                "training_topic": "Program",
                "start_date": "Start Date",
                "end_date": "End Date",
                "budget_used": "Budget",
                "training_status": "Status",
            },
            inplace=True,
        )

        if "Budget" in ongoing_df.columns:
            ongoing_df["Budget"] = (
                ongoing_df["Budget"]
                .apply(
                    lambda value:
                    f"₹{safe_number(value):,.0f}"
                )
            )

        st.dataframe(
            ongoing_df,
            use_container_width=True,
            hide_index=True,
            height=300,
        )

    # =====================================================
    # TRAINER TRACKER
    # =====================================================

    with tab_2:
        dashboard_section(
            "02",
            "Trainer Wise Training Tracker",
            (
                "Track the selected trainer's universities, "
                "subjects, date ranges and allocated budgets."
            ),
        )

        if trainer_df.empty:
            st.info(
                "No trainings found for selected trainer in this month."
            )

        else:
            trainer_display_columns = [
                column
                for column in [
                    "request_id",
                    "trainer_name",
                    "college_name",
                    "training_topic",
                    "start_date",
                    "end_date",
                    "budget_used",
                    "training_status",
                ]
                if column in trainer_df.columns
            ]

            trainer_display = trainer_df[
                trainer_display_columns
            ].copy()

            trainer_display.rename(
                columns={
                    "request_id": "Request ID",
                    "trainer_name": "Trainer",
                    "college_name": "University",
                    "training_topic": "Subject",
                    "start_date": "From",
                    "end_date": "To",
                    "budget_used": "Budget",
                    "training_status": "Status",
                },
                inplace=True,
            )

            if "Budget" in trainer_display.columns:
                trainer_display["Budget"] = (
                    trainer_display["Budget"]
                    .apply(
                        lambda value:
                        f"₹{safe_number(value):,.0f}"
                    )
                )

            st.dataframe(
                trainer_display,
                use_container_width=True,
                hide_index=True,
                height=280,
            )

            trainer_month_summary = (
                trainer_df
                .groupby(
                    "trainer_name",
                    dropna=False,
                )
                .agg(
                    Trainings=(
                        "request_id",
                        "count",
                    ),
                    Total_Budget=(
                        "budget_used",
                        "sum",
                    ),
                )
                .reset_index()
            )

            trainer_month_summary.rename(
                columns={
                    "trainer_name": "Trainer",
                    "Total_Budget": "Total Budget",
                },
                inplace=True,
            )

            trainer_month_summary[
                "Total Budget"
            ] = trainer_month_summary[
                "Total Budget"
            ].apply(
                lambda value:
                f"₹{safe_number(value):,.0f}"
            )

            dashboard_section(
                "03",
                "Selected Trainer Monthly Summary",
                (
                    "Consolidated training count and budget "
                    "for the selected trainer."
                ),
            )

            st.dataframe(
                trainer_month_summary,
                use_container_width=True,
                hide_index=True,
                height=180,
            )

    # =====================================================
    # OCCUPANCY
    # =====================================================

    with tab_3:
        dashboard_section(
            "03",
            "Trainer Occupancy",
            (
                "Review trainer availability against the "
                "maximum monthly capacity of 20 training days."
            ),
        )

        maximum_training_days_per_month = 20
        occupancy_rows = []

        if "trainer_name" in monthly_df.columns:
            for trainer in (
                monthly_df["trainer_name"]
                .dropna()
                .unique()
            ):
                trainer_name = clean_value(
                    trainer
                )

                if not trainer_name:
                    continue

                trainer_month_df = monthly_df[
                    monthly_df["trainer_name"]
                    .astype(str)
                    .apply(normalize)
                    == normalize(
                        trainer_name
                    )
                ].copy()

                occupied_days = 0

                for _, row in (
                    trainer_month_df.iterrows()
                ):
                    start = row[
                        "start_date_parsed"
                    ]

                    end = row[
                        "end_date_parsed"
                    ]

                    if (
                        pd.isna(start)
                        or pd.isna(end)
                    ):
                        continue

                    start = max(
                        start,
                        month_start,
                    )

                    end = min(
                        end,
                        month_end,
                    )

                    days = (
                        end - start
                    ).days + 1

                    if days > 0:
                        occupied_days += days

                occupancy = (
                    occupied_days
                    / maximum_training_days_per_month
                ) * 100

                occupancy_rows.append(
                    {
                        "Trainer": trainer_name,
                        "Trainings": len(
                            trainer_month_df
                        ),
                        "Occupied Days": occupied_days,
                        "Occupancy": occupancy,
                    }
                )

        if occupancy_rows:
            occupancy_df = pd.DataFrame(
                occupancy_rows
            )

            for _, row in occupancy_df.iterrows():
                trainer = row["Trainer"]

                trainings = int(
                    row["Trainings"]
                )

                occupied_days = int(
                    row["Occupied Days"]
                )

                occupancy = float(
                    row["Occupancy"]
                )

                if occupancy <= 60:
                    status = "Available"

                elif occupancy <= 90:
                    status = "Busy"

                else:
                    status = "Overbooked"

                occupancy_card(
                    trainer,
                    status,
                    trainings,
                    occupied_days,
                    maximum_training_days_per_month,
                    occupancy,
                )

                st.progress(
                    min(
                        occupancy / 100,
                        1.0,
                    )
                )

        else:
            st.info(
                "No trainer occupancy data available for this month."
            )

    # =====================================================
    # UNIVERSITY SUMMARY
    # =====================================================

    with tab_4:
        dashboard_section(
            "04",
            "University Wise Summary",
            (
                "Compare the number of trainings and "
                "consumed budget across universities."
            ),
        )

        if (
            selected_university == "ALL"
            and "college_name"
            in monthly_df.columns
        ):
            university_summary = (
                monthly_df
                .groupby(
                    "college_name",
                    dropna=False,
                )
                .agg(
                    Trainings=(
                        "request_id",
                        "count",
                    ),
                    Consumed=(
                        "budget_used",
                        "sum",
                    ),
                )
                .reset_index()
            )

            university_summary.rename(
                columns={
                    "college_name": "University",
                },
                inplace=True,
            )

            university_summary[
                "Consumed"
            ] = university_summary[
                "Consumed"
            ].apply(
                lambda value:
                f"₹{safe_number(value):,.0f}"
            )

            st.dataframe(
                university_summary,
                use_container_width=True,
                hide_index=True,
                height=250,
            )

        else:
            st.info(
                (
                    "University summary is available "
                    "when University filter is set to ALL."
                )
            )

        dashboard_section(
            "05",
            "Trainer List",
            (
                "Trainer assignment list for all trainings "
                "in the selected month."
            ),
        )

        if "trainer_name" in monthly_df.columns:
            trainer_list = monthly_df[
                [
                    "trainer_name",
                    "college_name",
                    "training_topic",
                    "training_status",
                ]
            ].copy()

            trainer_list.rename(
                columns={
                    "trainer_name": "Trainer",
                    "college_name": "University",
                    "training_topic": "Program",
                    "training_status": "Status",
                },
                inplace=True,
            )

            st.dataframe(
                trainer_list,
                use_container_width=True,
                hide_index=True,
                height=250,
            )

    # =====================================================
    # UTILIZATION
    # =====================================================

    with tab_5:
        dashboard_section(
            "05",
            "Trainer Utilization",
            (
                "Compare the number of trainings and "
                "total assigned budget trainer-wise."
            ),
        )

        if "trainer_name" in monthly_df.columns:
            trainer_summary = (
                monthly_df
                .groupby(
                    "trainer_name",
                    dropna=False,
                )
                .agg(
                    Trainings=(
                        "request_id",
                        "count",
                    ),
                    Total_Budget=(
                        "budget_used",
                        "sum",
                    ),
                )
                .reset_index()
            )

            trainer_summary.rename(
                columns={
                    "trainer_name": "Trainer",
                    "Total_Budget": "Total Budget",
                },
                inplace=True,
            )

            trainer_summary[
                "Total Budget"
            ] = trainer_summary[
                "Total Budget"
            ].apply(
                lambda value:
                f"₹{safe_number(value):,.0f}"
            )

            st.dataframe(
                trainer_summary,
                use_container_width=True,
                hide_index=True,
                height=260,
            )

    # =====================================================
    # CLASH AND MONTH SUMMARY
    # =====================================================

    with tab_6:
        dashboard_section(
            "06",
            "Trainer Clash Check",
            (
                "Identify overlapping trainer assignments "
                "within the selected month."
            ),
        )

        clashes = []

        if "trainer_name" in monthly_df.columns:
            for trainer in (
                monthly_df["trainer_name"]
                .dropna()
                .unique()
            ):
                trainer_name = clean_value(
                    trainer
                )

                if not trainer_name:
                    continue

                clash_df = monthly_df[
                    monthly_df["trainer_name"]
                    .astype(str)
                    .apply(normalize)
                    == normalize(
                        trainer_name
                    )
                ].sort_values(
                    "start_date_parsed"
                )

                for index in range(
                    len(clash_df) - 1
                ):
                    current = clash_df.iloc[
                        index
                    ]

                    next_training = clash_df.iloc[
                        index + 1
                    ]

                    current_end = current[
                        "end_date_parsed"
                    ]

                    next_start = next_training[
                        "start_date_parsed"
                    ]

                    if current_end >= next_start:
                        clashes.append(
                            {
                                "Trainer": trainer_name,

                                "First University": clean_value(
                                    current.get(
                                        "college_name",
                                        "",
                                    )
                                ),

                                "First Program": clean_value(
                                    current.get(
                                        "training_topic",
                                        "",
                                    )
                                ),

                                "First Dates": (
                                    f"{clean_value(current.get('start_date', ''))}"
                                    f" to "
                                    f"{clean_value(current.get('end_date', ''))}"
                                ),

                                "Second University": clean_value(
                                    next_training.get(
                                        "college_name",
                                        "",
                                    )
                                ),

                                "Second Program": clean_value(
                                    next_training.get(
                                        "training_topic",
                                        "",
                                    )
                                ),

                                "Second Dates": (
                                    f"{clean_value(next_training.get('start_date', ''))}"
                                    f" to "
                                    f"{clean_value(next_training.get('end_date', ''))}"
                                ),
                            }
                        )

        if clashes:
            st.error(
                "Trainer clashes detected."
            )

            st.dataframe(
                pd.DataFrame(
                    clashes
                ),
                use_container_width=True,
                hide_index=True,
                height=250,
            )

        else:
            st.success(
                "No trainer clashes found."
            )

        dashboard_section(
            "07",
            "Approved Amount by Month",
            (
                "Review approved training expenditure "
                "for every month of the selected year."
            ),
        )

        year_df = df[
            df["start_date_parsed"]
            .dt.year
            == selected_year
        ].copy()

        if selected_university != "ALL":
            year_df = year_df[
                year_df["college_name"]
                .astype(str)
                .apply(normalize)
                == normalize(
                    selected_university
                )
            ]

        year_df["budget_used"] = (
            year_df.apply(
                get_budget_amount,
                axis=1,
            )
        )

        month_rows = []

        for month_number, month_name in enumerate(
            MONTH_NAMES,
            start=1,
        ):
            month_total = year_df[
                year_df["start_date_parsed"]
                .dt.month
                == month_number
            ]["budget_used"].sum()

            month_rows.append(
                {
                    "Month": month_name,
                    "Approved Amount": (
                        f"₹{safe_number(month_total):,.0f}"
                    ),
                }
            )

        st.dataframe(
            pd.DataFrame(
                month_rows
            ),
            use_container_width=True,
            hide_index=True,
            height=300,
        )


# =========================================================
# MAIN DASHBOARD
# =========================================================

def show_dashboard(role, username):

    apply_dashboard_ui()

    show_dashboard_hero(
        role,
        username,
    )

    try:
        requests_df = pd.read_csv(
            REQUESTS_FILE
        ).fillna("")

    except Exception:
        requests_df = pd.DataFrame()

    try:
        invoices_df = pd.read_csv(
            INVOICES_FILE
        ).fillna("")

    except Exception:
        invoices_df = pd.DataFrame()

    if requests_df.empty:
        st.info(
            "No requests found yet."
        )

        return

    dashboard_section(
        "01",
        "Request Status Overview",
        (
            "Monitor total requests and their current "
            "approval position across the workflow."
        ),
    )

    show_status_cards(
        requests_df
    )

    dashboard_section(
        "02",
        "Financial Overview",
        (
            "Review estimated budgets, requester budgets "
            "and uploaded invoice activity."
        ),
    )

    financial_column_1, financial_column_2, financial_column_3 = (
        st.columns(3)
    )

    with financial_column_1:
        total_estimated_budget = 0

        if "estimated_budget" in requests_df.columns:
            total_estimated_budget = (
                requests_df[
                    "estimated_budget"
                ]
                .apply(safe_number)
                .sum()
            )

        st.metric(
            "Total Estimated Budget",
            f"₹{total_estimated_budget:,.0f}",
        )

    with financial_column_2:
        total_requester_budget = 0

        if (
            "total_expected_budget"
            in requests_df.columns
        ):
            total_requester_budget = (
                requests_df[
                    "total_expected_budget"
                ]
                .apply(safe_number)
                .sum()
            )

        st.metric(
            "Total Requester Budget",
            f"₹{total_requester_budget:,.0f}",
        )

    with financial_column_3:
        invoice_count = (
            len(invoices_df)
            if not invoices_df.empty
            else 0
        )

        st.metric(
            "Invoices",
            invoice_count,
        )

    show_monthly_training_budget_dashboard(
        requests_df
    )

    if "request_status" in requests_df.columns:
        dashboard_section(
            "03",
            "Request Status Summary",
            (
                "Detailed count of records grouped by "
                "their current workflow status."
            ),
        )

        status_summary = (
            requests_df[
                "request_status"
            ]
            .astype(str)
            .str.strip()
            .replace(
                "",
                "Unknown",
            )
            .value_counts()
            .reset_index()
        )

        status_summary.columns = [
            "Status",
            "Count",
        ]

        st.dataframe(
            status_summary,
            use_container_width=True,
            hide_index=True,
        )

    show_request_table(
        requests_df,
        "Recent Training Requests",
    )

    if not invoices_df.empty:
        dashboard_section(
            "06",
            "Recent Invoices",
            (
                "Review recently submitted invoice records "
                "and their current processing status."
            ),
        )

        invoice_columns = [
            column
            for column in [
                "invoice_id",
                "request_id",
                "college_name",
                "amount",
                "invoice_status",
                "created_at",
            ]
            if column in invoices_df.columns
        ]

        if invoice_columns:
            invoice_display_df = invoices_df[
                invoice_columns
            ].copy()

            invoice_display_df.rename(
                columns={
                    "invoice_id": "Invoice ID",
                    "request_id": "Request ID",
                    "college_name": "University",
                    "amount": "Amount",
                    "invoice_status": "Status",
                    "created_at": "Created At",
                },
                inplace=True,
            )

            if "Amount" in invoice_display_df.columns:
                invoice_display_df[
                    "Amount"
                ] = invoice_display_df[
                    "Amount"
                ].apply(
                    lambda value:
                    f"₹{safe_number(value):,.0f}"
                )

            st.dataframe(
                invoice_display_df,
                use_container_width=True,
                hide_index=True,
            )

        else:
            st.dataframe(
                invoices_df,
                use_container_width=True,
                hide_index=True,
            )