import streamlit as st
import pandas as pd
from db import get_connection
from email_utils import send_email


REQUESTS_FILE = "requests.csv"
BUDGET_MASTER_FILE = "budget.csv"

MONTHS = [
    "jan", "feb", "mar", "apr", "may", "jun",
    "jul", "aug", "sep", "oct", "nov", "dec"
]


# =========================================================
# PARTNER PREMIUM UI
# =========================================================

def apply_partner_ui():
    st.markdown(
        """
        <style>
        :root {
            --partner-primary: #4f46e5;
            --partner-primary-dark: #3730a3;
            --partner-secondary: #7c3aed;
            --partner-accent: #ec4899;

            --partner-background: #f5f7fc;
            --partner-surface: #ffffff;
            --partner-surface-soft: #f8fafc;

            --partner-text: #0f172a;
            --partner-muted: #64748b;
            --partner-border: #e2e8f0;

            --partner-success: #16a34a;
            --partner-warning: #d97706;
            --partner-danger: #dc2626;
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
            border-bottom: 1px solid rgba(226, 232, 240, 0.65);
        }

        .block-container {
            max-width: 1480px;
            padding-top: 1.5rem;
            padding-bottom: 4rem;
        }

        /* =====================================================
           HERO
        ===================================================== */

        .partner-hero {
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

        .partner-hero::before {
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

        .partner-hero-grid {
            position: relative;
            z-index: 2;

            display: flex;
            align-items: center;
            justify-content: space-between;

            gap: 24px;
        }

        .partner-hero-title {
            color: var(--partner-text);

            font-size: 35px;
            font-weight: 900;
            line-height: 1.15;
            letter-spacing: -0.045em;

            margin-bottom: 8px;
        }

        .partner-hero-subtitle {
            color: #738096;

            font-size: 15px;
            font-weight: 520;
            line-height: 1.65;

            max-width: 800px;
        }

        .partner-hero-badge {
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
           HEADINGS
        ===================================================== */

        h1,
        h2,
        h3 {
            color: var(--partner-text) !important;
            letter-spacing: -0.025em !important;
        }

        h2 {
            font-size: 24px !important;
            font-weight: 900 !important;
        }

        h3 {
            font-size: 20px !important;
            font-weight: 850 !important;
        }

        p {
            color: #475569;
        }

        /* =====================================================
           SECTION BANNER
        ===================================================== */

        .partner-section-banner {
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

        .partner-section-title {
            color: #ffffff;

            font-size: 21px;
            font-weight: 900;
            letter-spacing: -0.025em;

            margin-bottom: 5px;
        }

        .partner-section-text {
            color: rgba(255, 255, 255, 0.80);

            font-size: 13px;
            line-height: 1.55;
        }

        /* =====================================================
           INPUTS
        ===================================================== */

        label {
            color: #46536a !important;

            font-size: 13px !important;
            font-weight: 760 !important;

            letter-spacing: 0.005em;
        }

        div[data-baseweb="select"] > div,
        div[data-testid="stTextInput"] input,
        div[data-testid="stNumberInput"] input,
        div[data-testid="stTextArea"] textarea {
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

        div[data-baseweb="select"] > div,
        div[data-testid="stTextInput"] input,
        div[data-testid="stNumberInput"] input {
            min-height: 48px;
        }

        div[data-testid="stTextArea"] textarea {
            min-height: 110px;
            padding-top: 12px !important;
        }

        div[data-baseweb="select"] > div:hover,
        div[data-testid="stTextInput"] input:hover,
        div[data-testid="stNumberInput"] input:hover,
        div[data-testid="stTextArea"] textarea:hover {
            border-color: #a5b4fc !important;
        }

        div[data-testid="stTextInput"] input:focus,
        div[data-testid="stNumberInput"] input:focus,
        div[data-testid="stTextArea"] textarea:focus {
            border-color: #818cf8 !important;

            box-shadow:
                0 0 0 4px rgba(99, 102, 241, 0.10),
                0 8px 20px rgba(15, 23, 42, 0.045) !important;
        }

        div[data-baseweb="select"] span,
        div[data-baseweb="select"] div {
            color: #111827;
        }

        div[data-testid="stNumberInput"] button {
            color: #64748b !important;
            background: transparent !important;

            border: none !important;
            box-shadow: none !important;
        }

        /* =====================================================
           METRICS
        ===================================================== */

        div[data-testid="stMetric"] {
            position: relative;
            overflow: hidden;

            min-height: 125px;

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
                    var(--partner-primary),
                    var(--partner-secondary),
                    var(--partner-accent)
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
            color: var(--partner-text) !important;

            font-size: 24px !important;
            font-weight: 900 !important;
            letter-spacing: -0.03em !important;

            white-space: normal !important;
            overflow-wrap: anywhere;
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

        div[data-testid="stTabs"] button:hover {
            color: var(--partner-primary) !important;
            background: #f5f3ff;
        }

        div[data-testid="stTabs"]
        button[aria-selected="true"] {
            color: var(--partner-primary) !important;
            font-weight: 900 !important;
        }

        div[data-testid="stTabs"]
        [data-baseweb="tab-highlight"] {
            height: 3px;

            background:
                linear-gradient(
                    90deg,
                    var(--partner-primary),
                    var(--partner-secondary)
                ) !important;

            border-radius: 999px;
        }

        /* =====================================================
           EXPANDERS
        ===================================================== */

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
            color: var(--partner-text) !important;
            font-size: 15px !important;
            font-weight: 830 !important;
        }

        /* =====================================================
           TABLES
        ===================================================== */

        div[data-testid="stDataFrame"],
        .stTable {
            overflow: hidden;

            background: #ffffff;

            border: 1px solid #e1e5ee;
            border-radius: 16px;

            box-shadow:
                0 10px 26px rgba(15, 23, 42, 0.045);
        }

        div[data-testid="stTable"] th {
            color: #334155 !important;
            background: #f8fafc !important;
            font-weight: 800 !important;
        }

        /* =====================================================
           BUTTONS
        ===================================================== */

        div[data-testid="stButton"] button {
            position: relative;
            overflow: hidden;

            min-height: 48px;

            color: #ffffff !important;

            background:
                linear-gradient(
                    135deg,
                    #4338ca 0%,
                    #5b4de1 48%,
                    #7c3aed 100%
                ) !important;

            border: none !important;
            border-radius: 13px !important;

            font-weight: 850 !important;

            box-shadow:
                0 12px 25px rgba(79, 70, 229, 0.22);

            transition:
                transform 0.17s ease,
                box-shadow 0.17s ease;
        }

        div[data-testid="stButton"] button:hover {
            color: #ffffff !important;

            transform: translateY(-2px);

            box-shadow:
                0 16px 30px rgba(79, 70, 229, 0.28);
        }

        div[data-testid="stButton"] button p,
        div[data-testid="stButton"] button span {
            color: #ffffff !important;
            font-weight: 850 !important;
        }

        /* =====================================================
           ALERTS
        ===================================================== */

        div[data-testid="stAlert"] {
            border-radius: 14px;
            border-width: 1px;

            box-shadow:
                0 8px 20px rgba(15, 23, 42, 0.045);
        }

        div[data-testid="stAlert"] p {
            font-size: 14px;
            font-weight: 650;
            line-height: 1.55;
        }

        /* =====================================================
           DIALOG
        ===================================================== */

        div[role="dialog"],
        div[role="dialog"] > div {
            border-radius: 22px !important;
        }

        /* =====================================================
           SIDEBAR SAFETY
        ===================================================== */

        section[data-testid="stSidebar"] div[role="radiogroup"] {
            background: transparent !important;
            border: none !important;
            box-shadow: none !important;
            padding: 0 !important;
        }

        section[data-testid="stSidebar"] div[role="radiogroup"] label {
            background: transparent !important;
            padding: 8px 10px !important;
        }

        /* =====================================================
           SPACING
        ===================================================== */

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

            .partner-hero {
                padding: 22px 20px;
                border-radius: 20px;
            }

            .partner-hero-grid {
                display: block;
            }

            .partner-hero-title {
                font-size: 28px;
            }

            .partner-hero-badge {
                display: inline-block;
                margin-top: 16px;
            }

            div[data-testid="stMetric"] {
                min-height: 110px;
            }
        }
        </style>
        """,
        unsafe_allow_html=True
    )


def show_partner_hero():
    hero_html = (
        '<div class="partner-hero">'
        '<div class="partner-hero-grid">'
        '<div>'
        '<div class="partner-hero-title">'
        'Partner Approval &amp; Budget Review'
        '</div>'
        '<div class="partner-hero-subtitle">'
        'Review approver estimates, verify budget health, '
        'take final decisions and manage college budget allocations.'
        '</div>'
        '</div>'
        '<div class="partner-hero-badge">'
        'Partner Workspace'
        '</div>'
        '</div>'
        '</div>'
    )

    st.markdown(
        hero_html,
        unsafe_allow_html=True
    )


def partner_banner(title, text):
    banner_html = (
        '<div class="partner-section-banner">'
        f'<div class="partner-section-title">{title}</div>'
        f'<div class="partner-section-text">{text}</div>'
        '</div>'
    )

    st.markdown(
        banner_html,
        unsafe_allow_html=True
    )


# =========================================================
# HELPERS
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

        if value.lower() in [
            "nan",
            "none",
            ""
        ]:
            return 0

        return float(value)

    except:
        return 0


def clean_text(value):
    try:
        if pd.isna(value):
            return ""

        value = str(value).strip()

        if value.lower() in [
            "nan",
            "none",
            ""
        ]:
            return ""

        return value

    except:
        return ""


def normalize_text(value):
    return (
        clean_text(value)
        .lower()
        .replace(" ", "")
        .replace("-", "")
        .replace("_", "")
    )


def get_budget_values(selected_request):
    total_available_budget = safe_number(
        selected_request.get(
            "total_available_budget",
            0
        )
    )

    if total_available_budget == 0:
        total_available_budget = safe_number(
            selected_request.get(
                "available_budget",
                0
            )
        )

    trainer_cost = safe_number(
        selected_request.get(
            "trainer_cost",
            0
        )
    )

    stay_total = safe_number(
        selected_request.get(
            "stay_total",
            0
        )
    )

    travel_total = safe_number(
        selected_request.get(
            "approver_total_travel_cost",
            selected_request.get(
                "travel_total",
                0
            )
        )
    )

    food_total = safe_number(
        selected_request.get(
            "food_total",
            0
        )
    )

    material_total = safe_number(
        selected_request.get(
            "material_total",
            0
        )
    )

    other_total = safe_number(
        selected_request.get(
            "other_total",
            0
        )
    )

    estimated_budget = safe_number(
        selected_request.get(
            "estimated_budget",
            0
        )
    )

    remaining_after_approval = (
        total_available_budget
        - estimated_budget
    )

    if total_available_budget > 0:
        utilization_percentage = (
            estimated_budget
            / total_available_budget
        ) * 100

    else:
        utilization_percentage = 0

    if utilization_percentage <= 80:
        risk_level = "Low Risk"
        recommendation = (
            "Recommended for Approval"
        )

    elif utilization_percentage <= 100:
        risk_level = "Medium Risk"
        recommendation = (
            "Review Before Approval"
        )

    else:
        risk_level = "High Risk"
        recommendation = (
            "Budget Exceeded"
        )

    return {
        "total_available_budget":
            total_available_budget,

        "trainer_cost":
            trainer_cost,

        "stay_total":
            stay_total,

        "travel_total":
            travel_total,

        "food_total":
            food_total,

        "material_total":
            material_total,

        "other_total":
            other_total,

        "estimated_budget":
            estimated_budget,

        "remaining_after_approval":
            remaining_after_approval,

        "utilization_percentage":
            utilization_percentage,

        "risk_level":
            risk_level,

        "recommendation":
            recommendation
    }


# =========================================================
# BUDGET MASTER
# =========================================================

def load_budget_master():
    try:
        df = pd.read_csv(
            BUDGET_MASTER_FILE,
            encoding="latin1"
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
                "lineofbusiness": "line_of_business",
                "line_of_business": "line_of_business",
                "programme": "programme_name",
                "program": "programme_name",
                "programme_name": "programme_name",
                "program_name": "programme_name",
                "jobcode": "job_code",
                "job_code": "job_code",
                "training_hour": "training_hours",
                "training_hours": "training_hours",
                "paper": "paper_name",
                "paper_name": "paper_name",
                "batch_number": "batch_number",
                "total_budget": "total",
                "annual_total": "total",
                "grand_total": "total",
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
                "december": "dec"
            },
            inplace=True
        )

        required_columns = [
            "business_type",
            "vendor_name",
            "vendor_type",
            "line_of_business",
            "programme_name",
            "job_code",
            "batch",
            "semester",
            "year",
            "training_hours",
            "paper_name",
            "batch_number",
            "total"
        ] + MONTHS

        for column in required_columns:
            if column not in df.columns:
                df[column] = ""

        for month in MONTHS:
            df[month] = df[month].apply(
                safe_number
            )

        df["total"] = df["total"].apply(
            safe_number
        )

        for index in df.index:
            month_total = sum(
                safe_number(
                    df.loc[index, month]
                )
                for month in MONTHS
            )

            if (
                safe_number(
                    df.loc[index, "total"]
                ) == 0
                and month_total > 0
            ):
                df.loc[
                    index,
                    "total"
                ] = month_total

        return df.fillna("")

    except Exception as error:
        st.warning(
            f"Budget master loading failed: {error}"
        )

        return pd.DataFrame()


def save_budget_master(df):
    df.to_csv(
        BUDGET_MASTER_FILE,
        index=False
    )


def get_unique_values(df, column):
    if column not in df.columns:
        return []

    return (
        df[column]
        .astype(str)
        .str.strip()
        .replace(
            [
                "",
                "nan",
                "None",
                "NaN"
            ],
            pd.NA
        )
        .dropna()
        .drop_duplicates()
        .sort_values()
        .tolist()
    )


def get_index(
    options,
    value,
    default_index=0
):
    value = normalize_text(value)

    for index, option in enumerate(options):
        if normalize_text(option) == value:
            return index

    return default_index


def select_or_add(
    label,
    options,
    key,
    default_value=""
):
    clean_options = []

    for option in options:
        option = clean_text(option)

        if (
            option
            and option not in clean_options
        ):
            clean_options.append(
                option
            )

    default_value = clean_text(
        default_value
    )

    if (
        default_value
        and default_value not in clean_options
    ):
        clean_options.insert(
            0,
            default_value
        )

    final_options = (
        clean_options
        + ["Add New"]
    )

    selected = st.selectbox(
        label,
        final_options,
        index=get_index(
            final_options,
            default_value,
            0
        ),
        key=f"{key}_select"
    )

    if selected == "Add New":
        return st.text_input(
            f"Enter New {label}",
            key=f"{key}_new"
        )

    return selected


def filter_budget_master(
    df,
    business_type,
    line_of_business,
    programme_name,
    job_code,
    batch,
    semester
):
    filtered = df.copy()

    filters = {
        "business_type":
            business_type,

        "line_of_business":
            line_of_business,

        "programme_name":
            programme_name,

        "job_code":
            job_code,

        "batch":
            batch,

        "semester":
            semester
    }

    for column, value in filters.items():
        value = clean_text(value)

        if (
            column in filtered.columns
            and value
        ):
            filtered = filtered[
                filtered[column]
                .astype(str)
                .apply(normalize_text)
                == normalize_text(value)
            ]

    return filtered


# =========================================================
# MYSQL
# =========================================================

def update_partner_decision_in_mysql(
    request_id,
    status,
    remarks
):
    try:
        connection = get_connection()
        cursor = connection.cursor()

        try:
            cursor.execute(
                """
                UPDATE requests
                SET
                    request_status=%s,
                    partner_remarks=%s
                WHERE request_id=%s
                """,
                (
                    status,
                    remarks,
                    request_id
                )
            )

        except Exception:
            cursor.execute(
                """
                UPDATE requests
                SET request_status=%s
                WHERE request_id=%s
                """,
                (
                    status,
                    request_id
                )
            )

        connection.commit()

        cursor.close()
        connection.close()

    except Exception:
        pass


def save_budget_to_mysql(row_data):
    try:
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS budget_master (
                id INT AUTO_INCREMENT PRIMARY KEY,
                business_type VARCHAR(50),
                line_of_business VARCHAR(255),
                programme_name VARCHAR(255),
                job_code VARCHAR(100),
                batch VARCHAR(100),
                semester VARCHAR(100),
                year VARCHAR(20),
                training_hours DOUBLE,
                paper_name VARCHAR(255),
                jan DOUBLE,
                feb DOUBLE,
                mar DOUBLE,
                apr DOUBLE,
                may DOUBLE,
                jun DOUBLE,
                jul DOUBLE,
                aug DOUBLE,
                sep DOUBLE,
                oct DOUBLE,
                nov DOUBLE,
                `dec` DOUBLE,
                total DOUBLE
            )
            """
        )

        cursor.execute(
            """
            INSERT INTO budget_master (
                business_type,
                line_of_business,
                programme_name,
                job_code,
                batch,
                semester,
                year,
                training_hours,
                paper_name,
                jan,
                feb,
                mar,
                apr,
                may,
                jun,
                jul,
                aug,
                sep,
                oct,
                nov,
                `dec`,
                total
            )
            VALUES (
                %s,%s,%s,%s,%s,%s,%s,%s,%s,
                %s,%s,%s,%s,%s,%s,%s,%s,%s,
                %s,%s,%s,%s
            )
            """,
            (
                row_data["business_type"],
                row_data["line_of_business"],
                row_data["programme_name"],
                row_data["job_code"],
                row_data["batch"],
                row_data["semester"],
                row_data["year"],
                row_data["training_hours"],
                row_data["paper_name"],
                row_data["jan"],
                row_data["feb"],
                row_data["mar"],
                row_data["apr"],
                row_data["may"],
                row_data["jun"],
                row_data["jul"],
                row_data["aug"],
                row_data["sep"],
                row_data["oct"],
                row_data["nov"],
                row_data["dec"],
                row_data["total"]
            )
        )

        connection.commit()

        cursor.close()
        connection.close()

    except Exception:
        pass
# =========================================================
# ADD COLLEGE PAGE
# =========================================================

def show_college_master_page():
    partner_banner(
        "Add College",
        (
            "Add a new college, programme structure and "
            "monthly budget allocation to the budget master."
        )
    )

    budget_master_df = load_budget_master()

    st.markdown(
        "### College & Program Details"
    )

    column_1, column_2 = st.columns(2)

    with column_1:
        college_name = st.text_input(
            "College / University Name",
            key="college_master_name"
        )

        business_type = st.selectbox(
            "Business Type",
            [
                "B2C",
                "B2I",
                "B2B"
            ],
            key="college_master_business"
        )

        line_of_business = st.text_input(
            "Line of Business",
            key="college_master_lob"
        )

        programme_name = st.text_input(
            "Programme Name",
            key="college_master_programme"
        )

    with column_2:
        job_code = st.text_input(
            "Job Code",
            key="college_master_job"
        )

        batch = st.text_input(
            "Batch",
            key="college_master_batch"
        )

        semester = st.text_input(
            "Semester",
            key="college_master_semester"
        )

        paper_name = st.text_input(
            "Paper Name",
            key="college_master_paper"
        )

    detail_column_1, detail_column_2 = (
        st.columns(2)
    )

    with detail_column_1:
        year = st.selectbox(
            "Year",
            [
                "2026",
                "2027",
                "2028",
                "2029",
                "2030"
            ],
            key="college_master_year"
        )

    with detail_column_2:
        training_hours = st.number_input(
            "Training Hours",
            min_value=0,
            value=0,
            step=1,
            key="college_master_hours"
        )

    partner_banner(
        "Monthly Budget Allocation",
        (
            "Enter the planned budget for every month. "
            "The annual total will be calculated automatically."
        )
    )

    month_values = {}

    month_column_1, month_column_2, month_column_3 = (
        st.columns(3)
    )

    month_columns = [
        month_column_1,
        month_column_2,
        month_column_3
    ]

    for index, month in enumerate(MONTHS):
        with month_columns[index % 3]:
            month_values[month] = st.number_input(
                f"{month.upper()} Budget",
                min_value=0,
                value=0,
                step=1000,
                key=f"college_master_{month}"
            )

    annual_total = sum(
        month_values.values()
    )

    st.metric(
        "Annual Total Budget",
        f"₹{annual_total:,.0f}"
    )

    if st.button(
        "Save College",
        use_container_width=True,
        key="save_college_master_button"
    ):
        if (
            not college_name
            or not business_type
            or not programme_name
        ):
            st.error(
                (
                    "Please fill College Name, "
                    "Business Type and Programme Name."
                )
            )

            return

        new_row = {
            "college_name": college_name,
            "business_type": business_type,
            "line_of_business": line_of_business,
            "programme_name": programme_name,
            "job_code": job_code,
            "batch": batch,
            "semester": semester,
            "year": year,
            "training_hours": training_hours,
            "paper_name": paper_name,
            "batch_number": "",
            "vendor_name": "",
            "vendor_type": "",
            "total": annual_total
        }

        for month in MONTHS:
            new_row[month] = month_values[
                month
            ]

        for column in new_row.keys():
            if column not in budget_master_df.columns:
                budget_master_df[
                    column
                ] = ""

        budget_master_df = pd.concat(
            [
                budget_master_df,
                pd.DataFrame(
                    [new_row]
                )
            ],
            ignore_index=True
        )

        save_budget_master(
            budget_master_df
        )

        save_budget_to_mysql(
            {
                "business_type":
                    business_type,

                "line_of_business":
                    line_of_business,

                "programme_name":
                    programme_name,

                "job_code":
                    job_code,

                "batch":
                    batch,

                "semester":
                    semester,

                "year":
                    year,

                "training_hours":
                    training_hours,

                "paper_name":
                    paper_name,

                "jan":
                    month_values["jan"],

                "feb":
                    month_values["feb"],

                "mar":
                    month_values["mar"],

                "apr":
                    month_values["apr"],

                "may":
                    month_values["may"],

                "jun":
                    month_values["jun"],

                "jul":
                    month_values["jul"],

                "aug":
                    month_values["aug"],

                "sep":
                    month_values["sep"],

                "oct":
                    month_values["oct"],

                "nov":
                    month_values["nov"],

                "dec":
                    month_values["dec"],

                "total":
                    annual_total
            }
        )

        st.success(
            (
                "College added successfully. "
                "It is now available in budget.csv."
            )
        )


# =========================================================
# BUDGET UPDATE / ADD
# =========================================================

def show_budget_update_tab():
    partner_banner(
        "Budget Update / Add",
        (
            "Add a new budget line or update the existing "
            "monthly allocation for a programme."
        )
    )

    budget_master_df = load_budget_master()

    if budget_master_df.empty:
        st.error(
            "budget.csv not found or empty."
        )

        return

    budget_column_1, budget_column_2 = (
        st.columns(2)
    )

    with budget_column_1:
        business_type_update = st.selectbox(
            "Business Type",
            [
                "B2C",
                "B2I",
                "B2B"
            ],
            key="partner_budget_business_type"
        )

        line_update = select_or_add(
            "Line of Business",
            get_unique_values(
                budget_master_df,
                "line_of_business"
            ),
            "partner_budget_line"
        )

        programme_update = select_or_add(
            "Programme Name",
            get_unique_values(
                budget_master_df,
                "programme_name"
            ),
            "partner_budget_programme"
        )

        job_code_update = select_or_add(
            "Job Code",
            get_unique_values(
                budget_master_df,
                "job_code"
            ),
            "partner_budget_job_code"
        )

    with budget_column_2:
        batch_update = select_or_add(
            "Batch",
            get_unique_values(
                budget_master_df,
                "batch"
            ),
            "partner_budget_batch"
        )

        semester_update = select_or_add(
            "Semester",
            get_unique_values(
                budget_master_df,
                "semester"
            ),
            "partner_budget_semester"
        )

        year_update = select_or_add(
            "Year",
            (
                get_unique_values(
                    budget_master_df,
                    "year"
                )
                or [
                    "2026",
                    "2027",
                    "2028"
                ]
            ),
            "partner_budget_year"
        )

    existing_rows = filter_budget_master(
        budget_master_df,
        business_type_update,
        line_update,
        programme_update,
        job_code_update,
        batch_update,
        semester_update
    )

    if (
        not existing_rows.empty
        and "year"
        in existing_rows.columns
    ):
        year_matched_rows = existing_rows[
            existing_rows["year"]
            .astype(str)
            .apply(normalize_text)
            == normalize_text(
                year_update
            )
        ]

        if not year_matched_rows.empty:
            existing_rows = (
                year_matched_rows
            )

    existing_row = (
        existing_rows.iloc[0]
        if not existing_rows.empty
        else {}
    )

    details_column_1, details_column_2 = (
        st.columns(2)
    )

    with details_column_1:
        training_hours_update = (
            st.number_input(
                "Training Hours",
                min_value=0,
                value=(
                    int(
                        safe_number(
                            existing_row.get(
                                "training_hours",
                                0
                            )
                        )
                    )
                    if len(existing_row)
                    else 0
                ),
                step=1,
                key=(
                    "partner_budget_"
                    "training_hours"
                )
            )
        )

    with details_column_2:
        paper_name_update = select_or_add(
            "Paper Name",
            get_unique_values(
                budget_master_df,
                "paper_name"
            ),
            "partner_budget_paper",
            (
                clean_text(
                    existing_row.get(
                        "paper_name",
                        ""
                    )
                )
                if len(existing_row)
                else ""
            )
        )

    partner_banner(
        "Monthly Budget Entry",
        (
            "Update monthly values for the selected "
            "budget line. Annual total is calculated automatically."
        )
    )

    month_values = {}

    combination_key = normalize_text(
        (
            f"{business_type_update}_"
            f"{line_update}_"
            f"{programme_update}_"
            f"{job_code_update}_"
            f"{batch_update}_"
            f"{semester_update}_"
            f"{year_update}"
        )
    )

    month_column_1, month_column_2, month_column_3 = (
        st.columns(3)
    )

    month_columns = [
        month_column_1,
        month_column_2,
        month_column_3
    ]

    for index, month in enumerate(MONTHS):
        default_month_value = (
            int(
                safe_number(
                    existing_row.get(
                        month,
                        0
                    )
                )
            )
            if len(existing_row)
            else 0
        )

        with month_columns[index % 3]:
            month_values[month] = st.number_input(
                f"{month.upper()} Budget",
                min_value=0,
                value=default_month_value,
                step=1000,
                key=(
                    f"partner_{month}_"
                    f"budget_input_"
                    f"{combination_key}"
                )
            )

    annual_total = sum(
        month_values.values()
    )

    st.metric(
        "Total Annual Budget",
        f"₹{annual_total:,.0f}"
    )

    if st.button(
        "Save / Update Budget",
        use_container_width=True,
        key="partner_save_budget_master_btn"
    ):
        new_budget_row = {
            "business_type":
                business_type_update,

            "line_of_business":
                line_update,

            "programme_name":
                programme_update,

            "job_code":
                job_code_update,

            "batch":
                batch_update,

            "semester":
                semester_update,

            "year":
                year_update,

            "training_hours":
                training_hours_update,

            "paper_name":
                paper_name_update,

            "total":
                annual_total
        }

        for month in MONTHS:
            new_budget_row[
                month
            ] = month_values[
                month
            ]

        for column in new_budget_row.keys():
            if column not in budget_master_df.columns:
                budget_master_df[
                    column
                ] = ""

        match_condition = (
            (
                budget_master_df[
                    "business_type"
                ]
                .astype(str)
                .apply(normalize_text)
                == normalize_text(
                    business_type_update
                )
            )
            &
            (
                budget_master_df[
                    "line_of_business"
                ]
                .astype(str)
                .apply(normalize_text)
                == normalize_text(
                    line_update
                )
            )
            &
            (
                budget_master_df[
                    "programme_name"
                ]
                .astype(str)
                .apply(normalize_text)
                == normalize_text(
                    programme_update
                )
            )
            &
            (
                budget_master_df[
                    "job_code"
                ]
                .astype(str)
                .apply(normalize_text)
                == normalize_text(
                    job_code_update
                )
            )
            &
            (
                budget_master_df[
                    "batch"
                ]
                .astype(str)
                .apply(normalize_text)
                == normalize_text(
                    batch_update
                )
            )
            &
            (
                budget_master_df[
                    "semester"
                ]
                .astype(str)
                .apply(normalize_text)
                == normalize_text(
                    semester_update
                )
            )
        )

        if "year" in budget_master_df.columns:
            year_match = (
                budget_master_df[
                    "year"
                ]
                .astype(str)
                .apply(normalize_text)
                == normalize_text(
                    year_update
                )
            )

            blank_year = (
                budget_master_df[
                    "year"
                ]
                .astype(str)
                .apply(normalize_text)
                == ""
            )

            match_condition = (
                match_condition
                & (
                    year_match
                    | blank_year
                )
            )

        if (
            not budget_master_df.empty
            and match_condition.any()
        ):
            match_index = (
                budget_master_df[
                    match_condition
                ]
                .index[0]
            )

            for column, value in new_budget_row.items():
                budget_master_df.loc[
                    match_index,
                    column
                ] = value

            st.success(
                "Budget updated successfully."
            )

        else:
            budget_master_df = pd.concat(
                [
                    budget_master_df,
                    pd.DataFrame(
                        [new_budget_row]
                    )
                ],
                ignore_index=True
            )

            st.success(
                "New budget added successfully."
            )

        save_budget_master(
            budget_master_df
        )

        save_budget_to_mysql(
            new_budget_row
        )

        st.info(
            "Budget master updated successfully."
        )


# =========================================================
# PARTNER NOTIFICATION
# =========================================================

@st.dialog(
    "Partner Approval Alert"
)
def partner_notification_dialog(count):
    partner_banner(
        "New Approval Requests",
        (
            "Approval requests are waiting for final "
            "Partner review and decision."
        )
    )

    st.metric(
        "Pending Partner Review",
        count
    )

    if st.button(
        "Review Now",
        use_container_width=True,
        key="partner_review_notification_button"
    ):
        st.session_state[
            "partner_notification_seen"
        ] = True

        st.rerun()
# =========================================================
# MAIN PARTNER APPROVAL PAGE
# =========================================================

def show_director_approval():

    apply_partner_ui()
    show_partner_hero()

    try:
        requests_df = pd.read_csv(
            REQUESTS_FILE
        ).fillna("")

    except Exception:
        st.error(
            "No requests found."
        )

        return

    budget_master_df = load_budget_master()

    if "business_type" not in requests_df.columns:
        requests_df[
            "business_type"
        ] = ""

    if "request_status" not in requests_df.columns:
        st.error(
            "request_status column not found."
        )

        return

    all_pending = requests_df[
        requests_df[
            "request_status"
        ]
        .astype(str)
        .str.strip()
        == "Pending Director Approval"
    ]

    pending_count = len(
        all_pending
    )

    last_count = st.session_state.get(
        "partner_last_pending_count",
        None
    )

    if last_count != pending_count:
        st.session_state[
            "partner_notification_seen"
        ] = False

        st.session_state[
            "partner_last_pending_count"
        ] = pending_count

    if (
        pending_count > 0
        and not st.session_state.get(
            "partner_notification_seen",
            False
        )
    ):
        partner_notification_dialog(
            pending_count
        )

    tab_1, tab_2, tab_3 = st.tabs(
        [
            "Add College",
            "Partner Approval",
            "Budget Update / Add"
        ]
    )

    # =====================================================
    # ADD COLLEGE TAB
    # =====================================================

    with tab_1:
        show_college_master_page()

    # =====================================================
    # PARTNER APPROVAL TAB
    # =====================================================

    with tab_2:

        partner_banner(
            "Partner Approval Overview",
            (
                "Review pending requests, approved records "
                "and rejected records before taking a final decision."
            )
        )

        metric_column_1, metric_column_2, metric_column_3 = (
            st.columns(3)
        )

        with metric_column_1:
            st.metric(
                "Pending Requests",
                pending_count
            )

        with metric_column_2:
            approved_count = len(
                requests_df[
                    requests_df[
                        "request_status"
                    ]
                    .astype(str)
                    .str.strip()
                    == "Approved"
                ]
            )

            st.metric(
                "Approved Requests",
                approved_count
            )

        with metric_column_3:
            rejected_count = len(
                requests_df[
                    requests_df[
                        "request_status"
                    ]
                    .astype(str)
                    .str.strip()
                    == "Rejected"
                ]
            )

            st.metric(
                "Rejected Requests",
                rejected_count
            )

        partner_banner(
            "Request Selection",
            (
                "Choose the business type and request "
                "you want to review."
            )
        )

        selected_business_type = st.selectbox(
            "Select Business Type",
            [
                "B2C",
                "B2I",
                "B2B"
            ],
            key="partner_business_type_filter"
        )

        pending_requests = requests_df[
            (
                requests_df[
                    "request_status"
                ]
                .astype(str)
                .str.strip()
                == "Pending Director Approval"
            )
            &
            (
                requests_df[
                    "business_type"
                ]
                .astype(str)
                .apply(normalize_text)
                == normalize_text(
                    selected_business_type
                )
            )
        ]

        st.markdown(
            f"### {selected_business_type} Pending Requests"
        )

        if pending_requests.empty:
            st.success(
                (
                    f"No {selected_business_type} requests "
                    "pending for Partner approval."
                )
            )

        else:
            request_options = (
                pending_requests[
                    "request_id"
                ]
                .astype(str)
                .tolist()
            )

            selected_id = st.selectbox(
                "Select Request for Review",
                request_options,
                key=(
                    f"partner_single_request_"
                    f"{selected_business_type}"
                )
            )

            selected_request = (
                pending_requests[
                    pending_requests[
                        "request_id"
                    ]
                    .astype(str)
                    == selected_id
                ]
                .iloc[0]
            )

            values = get_budget_values(
                selected_request
            )

            business_type = clean_text(
                selected_request.get(
                    "business_type",
                    ""
                )
            )

            line_of_business = clean_text(
                selected_request.get(
                    "line_of_business",
                    ""
                )
            )

            programme_name = clean_text(
                selected_request.get(
                    "programme_name",
                    ""
                )
            )

            job_code = clean_text(
                selected_request.get(
                    "job_code",
                    ""
                )
            )

            batch = clean_text(
                selected_request.get(
                    "batch",
                    ""
                )
            )

            semester = clean_text(
                selected_request.get(
                    "semester",
                    ""
                )
            )

            budget_month = clean_text(
                selected_request.get(
                    "budget_month",
                    ""
                )
            )

            if not budget_month:
                try:
                    temporary_start_date = pd.to_datetime(
                        selected_request.get(
                            "start_date"
                        ),
                        errors="coerce"
                    )

                    month_map = {
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
                        12: "dec"
                    }

                    budget_month = month_map.get(
                        temporary_start_date.month,
                        "jan"
                    )

                except Exception:
                    budget_month = "jan"

            matched_budget_rows = filter_budget_master(
                budget_master_df,
                business_type,
                line_of_business,
                programme_name,
                job_code,
                batch,
                semester
            )

            selected_budget_row = (
                matched_budget_rows.iloc[0]
                if not matched_budget_rows.empty
                else {}
            )

            monthly_budget = (
                safe_number(
                    selected_budget_row.get(
                        budget_month,
                        0
                    )
                )
                if len(selected_budget_row)
                else safe_number(
                    selected_request.get(
                        "monthly_budget",
                        0
                    )
                )
            )

            annual_budget = (
                safe_number(
                    selected_budget_row.get(
                        "total",
                        0
                    )
                )
                if len(selected_budget_row)
                else safe_number(
                    selected_request.get(
                        "master_total_cost",
                        0
                    )
                )
            )

            approver_estimate = safe_number(
                selected_request.get(
                    "estimated_budget",
                    0
                )
            )

            if monthly_budget > 0:
                budget_used_for_check = (
                    monthly_budget
                )

            elif annual_budget > 0:
                budget_used_for_check = (
                    annual_budget
                )

            else:
                budget_used_for_check = safe_number(
                    values.get(
                        "total_available_budget",
                        0
                    )
                )

            remaining_budget = (
                budget_used_for_check
                - approver_estimate
            )

            if budget_used_for_check > 0:
                utilization = (
                    approver_estimate
                    / budget_used_for_check
                ) * 100

            else:
                utilization = 0

            if utilization <= 80:
                risk_level = "Low Risk"
                recommendation = (
                    "Recommended for Approval"
                )

            elif utilization <= 100:
                risk_level = "Medium Risk"
                recommendation = (
                    "Review Before Approval"
                )

            else:
                risk_level = "High Risk"
                recommendation = (
                    "Budget Exceeded"
                )

            partner_banner(
                "Selected Request Details & Budget Verification",
                (
                    "Verify the budget, request details and "
                    "approver cost breakdown before final approval."
                )
            )

            with st.expander(
                f"Details for Request {selected_id}",
                expanded=True
            ):

                st.markdown(
                    "### Budget Verification"
                )

                budget_metric_1, budget_metric_2, budget_metric_3, budget_metric_4 = (
                    st.columns(4)
                )

                with budget_metric_1:
                    st.metric(
                        (
                            f"{budget_month.upper()} "
                            "Monthly Budget"
                        ),
                        f"₹{monthly_budget:,.0f}"
                    )

                with budget_metric_2:
                    st.metric(
                        "Annual / Yearly Budget",
                        f"₹{annual_budget:,.0f}"
                    )

                with budget_metric_3:
                    st.metric(
                        "Approver Estimate",
                        f"₹{approver_estimate:,.0f}"
                    )

                with budget_metric_4:
                    st.metric(
                        "Remaining Budget",
                        f"₹{remaining_budget:,.0f}"
                    )

                risk_metric_1, risk_metric_2, risk_metric_3 = (
                    st.columns(3)
                )

                with risk_metric_1:
                    st.metric(
                        "Budget Used For Check",
                        f"₹{budget_used_for_check:,.0f}"
                    )

                with risk_metric_2:
                    st.metric(
                        "Utilization",
                        f"{utilization:.1f}%"
                    )

                with risk_metric_3:
                    st.metric(
                        "Risk Level",
                        risk_level
                    )

                if risk_level == "Low Risk":
                    st.success(
                        recommendation
                    )

                elif risk_level == "Medium Risk":
                    st.warning(
                        recommendation
                    )

                else:
                    st.error(
                        recommendation
                    )

                partner_banner(
                    "Request Details",
                    (
                        "Review the training programme, dates, "
                        "trainer and approver remarks."
                    )
                )

                request_table = pd.DataFrame(
                    {
                        "Field": [
                            "Request Date",
                            "Training Start Date",
                            "Training End Date",
                            "College / University",
                            "Business Type",
                            "Line of Business",
                            "Programme Name",
                            "Job Code",
                            "Batch",
                            "Semester",
                            "Training Topic",
                            "Trainer Name",
                            "Total Hours",
                            "Training Days",
                            "Approver Remarks"
                        ],

                        "Details": [
                            clean_text(
                                selected_request.get(
                                    "request_date",
                                    ""
                                )
                            ),

                            clean_text(
                                selected_request.get(
                                    "start_date",
                                    ""
                                )
                            ),

                            clean_text(
                                selected_request.get(
                                    "end_date",
                                    ""
                                )
                            ),

                            clean_text(
                                selected_request.get(
                                    "college_name",
                                    "Graphic Era"
                                )
                            ),

                            business_type,
                            line_of_business,
                            programme_name,
                            job_code,
                            batch,
                            semester,

                            clean_text(
                                selected_request.get(
                                    "training_topic",
                                    ""
                                )
                            ),

                            clean_text(
                                selected_request.get(
                                    "trainer_name",
                                    ""
                                )
                            ),

                            selected_request.get(
                                "total_hours",
                                ""
                            ),

                            selected_request.get(
                                "training_days",
                                ""
                            ),

                            selected_request.get(
                                "approver_remarks",
                                ""
                            )
                        ]
                    }
                )

                st.table(
                    request_table
                )

                partner_banner(
                    "Cost Breakdown",
                    (
                        "Review every approved cost component "
                        "and the final estimated amount."
                    )
                )

                cost_table = pd.DataFrame(
                    {
                        "Cost Component": [
                            "Trainer Fee",
                            "Stay Cost",
                            "Travel Cost",
                            "Food Cost",
                            "Training Material Cost",
                            "Other Cost",
                            "Total Estimated Budget"
                        ],

                        "Estimated Amount": [
                            f"₹{values['trainer_cost']:,.0f}",
                            f"₹{values['stay_total']:,.0f}",
                            f"₹{values['travel_total']:,.0f}",
                            f"₹{values['food_total']:,.0f}",
                            f"₹{values['material_total']:,.0f}",
                            f"₹{values['other_total']:,.0f}",
                            f"₹{approver_estimate:,.0f}"
                        ]
                    }
                )

                st.table(
                    cost_table
                )

                partner_banner(
                    "Final Budget Review",
                    (
                        "Confirm the final available budget "
                        "used for the Partner decision."
                    )
                )

                final_budget = st.number_input(
                    (
                        "Final Available Budget for "
                        f"{selected_id}"
                    ),
                    min_value=0,
                    value=(
                        int(
                            budget_used_for_check
                        )
                        if budget_used_for_check > 0
                        else 100000
                    ),
                    step=1000,
                    key=(
                        f"partner_budget_"
                        f"{selected_id}"
                    )
                )

                final_remaining = (
                    final_budget
                    - approver_estimate
                )

                if final_budget > 0:
                    final_utilization = (
                        approver_estimate
                        / final_budget
                    ) * 100

                else:
                    final_utilization = 0

                final_metric_1, final_metric_2, final_metric_3 = (
                    st.columns(3)
                )

                with final_metric_1:
                    st.metric(
                        "Final Available Budget",
                        f"₹{final_budget:,.0f}"
                    )

                with final_metric_2:
                    st.metric(
                        "Estimated Cost",
                        f"₹{approver_estimate:,.0f}"
                    )

                with final_metric_3:
                    st.metric(
                        "Final Remaining",
                        f"₹{final_remaining:,.0f}"
                    )

            partner_banner(
                "Partner Decision",
                (
                    "Add final remarks and approve or reject "
                    "the selected training request."
                )
            )

            partner_remarks = st.text_area(
                "Partner Remarks",
                key=(
                    f"partner_remarks_"
                    f"{selected_id}"
                )
            )

            decision = st.selectbox(
                "Decision",
                [
                    "Approve",
                    "Reject"
                ],
                key=(
                    f"partner_decision_"
                    f"{selected_id}"
                )
            )

            if st.button(
                "Submit Partner Decision",
                use_container_width=True,
                key=(
                    f"submit_partner_decision_"
                    f"{selected_id}"
                )
            ):

                final_status = (
                    "Approved"
                    if decision == "Approve"
                    else "Rejected"
                )

                request_index = requests_df[
                    requests_df[
                        "request_id"
                    ]
                    .astype(str)
                    == selected_id
                ].index[0]

                available_budget = st.session_state.get(
                    f"partner_budget_{selected_id}",
                    (
                        int(
                            values[
                                "total_available_budget"
                            ]
                        )
                        if values[
                            "total_available_budget"
                        ] > 0
                        else 100000
                    )
                )

                estimated_budget = values[
                    "estimated_budget"
                ]

                remaining_budget = (
                    available_budget
                    - estimated_budget
                )

                if available_budget > 0:
                    utilization_percentage = (
                        estimated_budget
                        / available_budget
                    ) * 100

                else:
                    utilization_percentage = 0

                if utilization_percentage <= 80:
                    final_risk_level = (
                        "Low Risk"
                    )

                    final_recommendation = (
                        "Recommended for Approval"
                    )

                elif utilization_percentage <= 100:
                    final_risk_level = (
                        "Medium Risk"
                    )

                    final_recommendation = (
                        "Review Before Approval"
                    )

                else:
                    final_risk_level = (
                        "High Risk"
                    )

                    final_recommendation = (
                        "Budget Exceeded"
                    )

                budget_health_score = max(
                    0,
                    round(
                        100
                        - abs(
                            100
                            - utilization_percentage
                        )
                    )
                )

                update_columns = {
                    "partner_final_available_budget":
                        available_budget,

                    "total_available_budget":
                        available_budget,

                    "available_budget":
                        available_budget,

                    "remaining_budget":
                        remaining_budget,

                    "budget_health_score":
                        budget_health_score,

                    "risk_level":
                        final_risk_level,

                    "budget_utilization":
                        utilization_percentage,

                    "partner_recommendation":
                        final_recommendation,

                    "partner_remarks":
                        str(partner_remarks),

                    "business_type":
                        selected_business_type,

                    "request_status":
                        final_status,

                    "calendar_status":
                        (
                            "Upcoming Training"
                            if decision == "Approve"
                            else "Rejected"
                        )
                }

                for column, value in update_columns.items():
                    if column not in requests_df.columns:
                        requests_df[
                            column
                        ] = ""

                    requests_df.loc[
                        request_index,
                        column
                    ] = value

                update_partner_decision_in_mysql(
                    selected_id,
                    final_status,
                    str(partner_remarks)
                )

                requests_df.to_csv(
                    REQUESTS_FILE,
                    index=False
                )

                requester_email = clean_text(
                    selected_request.get(
                        "requester_email",
                        ""
                    )
                )

                if decision == "Approve":

                    if requester_email:
                        send_email(
                            requester_email,
                            (
                                "Training Request "
                                "Approved"
                            ),
                            f"""
Your training request has been approved.

Request ID: {selected_id}
College: {clean_text(selected_request.get("college_name", ""))}
Training Topic: {clean_text(selected_request.get("training_topic", ""))}
Trainer: {clean_text(selected_request.get("trainer_name", ""))}
Start Date: {clean_text(selected_request.get("start_date", ""))}
End Date: {clean_text(selected_request.get("end_date", ""))}

Status: Approved

Please login to the portal for more details.
"""
                        )

                else:

                    if requester_email:
                        send_email(
                            requester_email,
                            (
                                "Training Request "
                                "Rejected"
                            ),
                            f"""
Your training request has been rejected by the Partner.

Request ID: {selected_id}
College: {clean_text(selected_request.get("college_name", ""))}
Training Topic: {clean_text(selected_request.get("training_topic", ""))}

Status: Rejected

Partner Remarks:
{partner_remarks}

Please review and submit a revised request if required.
"""
                        )

                new_pending_count = len(
                    requests_df[
                        requests_df[
                            "request_status"
                        ]
                        .astype(str)
                        .str.strip()
                        == "Pending Director Approval"
                    ]
                )

                st.session_state[
                    "partner_last_pending_count"
                ] = new_pending_count

                st.session_state[
                    "partner_notification_seen"
                ] = False

                if decision == "Approve":
                    st.success(
                        (
                            "Request approved successfully. "
                            "Training will now show in Budget Calendar "
                            "as Upcoming Training. Email sent to requester."
                        )
                    )

                else:
                    st.error(
                        "Request rejected."
                    )

                st.rerun()

    # =====================================================
    # BUDGET UPDATE TAB
    # =====================================================

    with tab_3:
        show_budget_update_tab()