import streamlit as st
import pandas as pd
import re
from db import get_connection
from email_utils import send_email


REQUESTS_FILE = "requests.csv"
BUDGET_MASTER_FILE = "budget.csv"

PARTNER_EMAIL = "partner@gmail.com"

MONTHS = [
    "jan", "feb", "mar", "apr", "may", "jun",
    "jul", "aug", "sep", "oct", "nov", "dec"
]

MONTH_ORDER = {
    "jan": 1, "feb": 2, "mar": 3, "apr": 4,
    "may": 5, "jun": 6, "jul": 7, "aug": 8,
    "sep": 9, "oct": 10, "nov": 11, "dec": 12
}


def get_dynamic_month_columns(df):
    """Return month-year columns such as apr_26 ... mar_27 in date order."""
    month_columns = []

    for column in df.columns:
        match = re.fullmatch(
            r"(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)_(\\d{2})",
            str(column).strip().lower()
        )

        if match:
            month_name, year_suffix = match.groups()
            full_year = 2000 + int(year_suffix)

            month_columns.append(
                (
                    full_year,
                    MONTH_ORDER[month_name],
                    column
                )
            )

    month_columns.sort(
        key=lambda item: (
            item[0],
            item[1]
        )
    )

    return [
        item[2]
        for item in month_columns
    ]


def financial_year_from_month_column(column):
    match = re.fullmatch(
        r"(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)_(\\d{2})",
        str(column).strip().lower()
    )

    if not match:
        return ""

    month_name, year_suffix = match.groups()
    year = 2000 + int(year_suffix)

    start_year = (
        year
        if MONTH_ORDER[month_name] >= 4
        else year - 1
    )

    return f"{start_year}-{str(start_year + 1)[-2:]}"


def get_financial_year_options(df):
    options = []

    for column in get_dynamic_month_columns(df):
        financial_year = financial_year_from_month_column(
            column
        )

        if (
            financial_year
            and financial_year not in options
        ):
            options.append(financial_year)

    return options


def get_financial_year_month_columns(df, financial_year):
    try:
        start_year = int(
            str(financial_year).split("-")[0]
        )
    except Exception:
        return []

    expected_columns = [
        f"apr_{str(start_year)[-2:]}",
        f"may_{str(start_year)[-2:]}",
        f"jun_{str(start_year)[-2:]}",
        f"jul_{str(start_year)[-2:]}",
        f"aug_{str(start_year)[-2:]}",
        f"sep_{str(start_year)[-2:]}",
        f"oct_{str(start_year)[-2:]}",
        f"nov_{str(start_year)[-2:]}",
        f"dec_{str(start_year)[-2:]}",
        f"jan_{str(start_year + 1)[-2:]}",
        f"feb_{str(start_year + 1)[-2:]}",
        f"mar_{str(start_year + 1)[-2:]}"
    ]

    return expected_columns


def month_column_label(column):
    parts = str(column).split("_")

    if len(parts) != 2:
        return str(column).upper()

    return f"{parts[0].upper()}-{parts[1]}"


def annual_budget_for_financial_year(row, month_columns):
    return sum(
        safe_number(
            row.get(month_column, 0),
            0
        )
        for month_column in month_columns
    )


# =========================================================
# PREMIUM APPROVER UI
# =========================================================

def apply_approver_ui():
    st.markdown(
        """
        <style>
        :root {
            --ap-primary: #4f46e5;
            --ap-primary-dark: #3730a3;
            --ap-secondary: #7c3aed;
            --ap-accent: #ec4899;

            --ap-background: #f5f7fc;
            --ap-surface: #ffffff;
            --ap-surface-soft: #f8fafc;

            --ap-text: #0f172a;
            --ap-muted: #64748b;
            --ap-border: #e2e8f0;

            --ap-success: #16a34a;
            --ap-warning: #d97706;
            --ap-danger: #dc2626;
        }

        /* =====================================================
           PAGE BACKGROUND
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

        .approver-hero {
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

        .approver-hero::before {
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

        .approver-hero-grid {
            position: relative;
            z-index: 2;

            display: flex;
            align-items: center;
            justify-content: space-between;

            gap: 24px;
        }

        .approver-hero-title {
            color: var(--ap-text);

            font-size: 35px;
            font-weight: 900;
            line-height: 1.15;
            letter-spacing: -0.045em;

            margin-bottom: 8px;
        }

        .approver-hero-subtitle {
            color: #738096;

            font-size: 15px;
            font-weight: 520;
            line-height: 1.65;

            max-width: 800px;
        }

        .approver-hero-badge {
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
           TYPOGRAPHY
        ===================================================== */

        h1,
        h2,
        h3 {
            color: var(--ap-text) !important;
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

        .approver-section-banner {
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

        .approver-section-title {
            color: #ffffff;

            font-size: 21px;
            font-weight: 900;
            letter-spacing: -0.025em;

            margin-bottom: 5px;
        }

        .approver-section-text {
            color: rgba(255, 255, 255, 0.80);

            font-size: 13px;
            line-height: 1.55;
        }

        /* =====================================================
           INPUT LABELS
        ===================================================== */

        label {
            color: #46536a !important;

            font-size: 13px !important;
            font-weight: 760 !important;

            letter-spacing: 0.005em;
        }

        /* =====================================================
           INPUTS
        ===================================================== */

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

        div[data-testid="stNumberInput"] button:hover {
            color: var(--ap-primary) !important;
            background: #eef2ff !important;
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
                    var(--ap-primary),
                    var(--ap-secondary),
                    var(--ap-accent)
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
            color: var(--ap-text) !important;

            font-size: 24px !important;
            font-weight: 900 !important;
            letter-spacing: -0.03em !important;

            white-space: normal !important;
            overflow-wrap: anywhere;
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

        div[data-testid="stTable"] table {
            border-radius: 16px;
            overflow: hidden;
        }

        div[data-testid="stTable"] th {
            color: #334155 !important;
            background: #f8fafc !important;

            font-weight: 800 !important;
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
           NAVIGATION RADIO
        ===================================================== */

        /* Fix Sidebar Navigation */

section[data-testid="stSidebar"] div[role="radiogroup"]{
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
    padding: 0 !important;
}

section[data-testid="stSidebar"] div[role="radiogroup"] label{
    background: transparent !important;
    border-radius: 12px !important;
    padding: 8px 10px !important;
}

section[data-testid="stSidebar"] div[role="radiogroup"] p{
    color: white !important;
    font-weight: 700 !important;
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
           DIALOG
        ===================================================== */

        div[role="dialog"] {
            border-radius: 22px !important;
        }

        div[role="dialog"] > div {
            border-radius: 22px !important;
        }

        /* =====================================================
           COLUMNS
        ===================================================== */

        div[data-testid="stHorizontalBlock"] {
            gap: 1rem;
        }

        /* =====================================================
           RESPONSIVE
        ===================================================== */

        @media (max-width: 900px) {
            .block-container {
                padding-top: 1rem;
                padding-left: 1rem;
                padding-right: 1rem;
            }

            .approver-hero {
                padding: 22px 20px;
                border-radius: 20px;
            }

            .approver-hero-grid {
                display: block;
            }

            .approver-hero-title {
                font-size: 28px;
            }

            .approver-hero-badge {
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


def show_approver_hero():
    hero_html = (
        '<div class="approver-hero">'
        '<div class="approver-hero-grid">'
        '<div>'
        '<div class="approver-hero-title">'
        'Approver Cost Estimation'
        '</div>'
        '<div class="approver-hero-subtitle">'
        'Review requester details, verify budget availability, '
        'calculate approved costs and manage college budget records.'
        '</div>'
        '</div>'
        '<div class="approver-hero-badge">'
        'Approver Workspace'
        '</div>'
        '</div>'
        '</div>'
    )

    st.markdown(
        hero_html,
        unsafe_allow_html=True
    )


def approver_banner(title, text):
    banner_html = (
        '<div class="approver-section-banner">'
        f'<div class="approver-section-title">{title}</div>'
        f'<div class="approver-section-text">{text}</div>'
        '</div>'
    )

    st.markdown(
        banner_html,
        unsafe_allow_html=True
    )


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
            ""
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
            ""
        ]:
            return default

        return float(value)

    except Exception:
        return default


def normalize_text(value):
    return (
        clean_value(value)
        .lower()
        .replace(" ", "")
        .replace("-", "")
        .replace("_", "")
    )


# =========================================================
# COLUMN NORMALIZATION
# =========================================================

def normalize_columns(df):
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

    rename_map = {
        "business": "business_type",
        "business_type": "business_type",

        "vendor_name": "vendor_name",
        "vendor_type": "vendor_type",

        "lineofbusiness": "line_of_business",
        "line_of_business": "line_of_business",

        "programme": "programme_name",
        "program": "programme_name",
        "programme_name": "programme_name",
        "program_name": "programme_name",

        "jobcode": "job_code",
        "job_code": "job_code",

        "batches": "batch",
        "batch_no": "batch",
        "batch_number": "batch_number",

        "sem": "semester",
        "semester": "semester",

        "training_hour": "training_hours",
        "training_hours": "training_hours",

        "paper": "paper_name",
        "paper_name": "paper_name",

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
        "december": "dec",

        "jan_budget": "jan",
        "feb_budget": "feb",
        "mar_budget": "mar",
        "apr_budget": "apr",
        "may_budget": "may",
        "jun_budget": "jun",
        "jul_budget": "jul",
        "aug_budget": "aug",
        "sep_budget": "sep",
        "oct_budget": "oct",
        "nov_budget": "nov",
        "dec_budget": "dec"
    }

    df.rename(
        columns=rename_map,
        inplace=True
    )

    return df


# =========================================================
# BUDGET MASTER HELPERS
# =========================================================

def load_budget_master():
    try:
        df = pd.read_csv(
            BUDGET_MASTER_FILE,
            encoding="latin1"
        )

        df = normalize_columns(df)

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
        ]

        for column in required_columns:
            if column not in df.columns:
                df[column] = ""

        # Pandas changes duplicate headers to Training hours.1 / Total.1.
        # After normalization these become training_hours1 / total1.
        duplicate_training_hours = next(
            (
                column
                for column in [
                    "training_hours1",
                    "training_hours_1"
                ]
                if column in df.columns
            ),
            None
        )

        if duplicate_training_hours:
            blank_training_hours = (
                df["training_hours"]
                .astype(str)
                .str.strip()
                .isin(
                    [
                        "",
                        "nan",
                        "None",
                        "NaN"
                    ]
                )
            )

            df.loc[
                blank_training_hours,
                "training_hours"
            ] = df.loc[
                blank_training_hours,
                duplicate_training_hours
            ]

        dynamic_month_columns = get_dynamic_month_columns(
            df
        )

        for month_column in dynamic_month_columns:
            df[month_column] = df[
                month_column
            ].apply(
                lambda value:
                safe_number(value, 0)
            )

        # Keep old month columns supported without converting
        # dated columns such as Jul-26 into plain Jul.
        for month in MONTHS:
            if month in df.columns:
                df[month] = df[
                    month
                ].apply(
                    lambda value:
                    safe_number(value, 0)
                )

        df["training_hours"] = df[
            "training_hours"
        ].apply(
            lambda value:
            safe_number(value, 0)
        )

        duplicate_total = next(
            (
                column
                for column in [
                    "total1",
                    "total_1"
                ]
                if column in df.columns
            ),
            None
        )

        if duplicate_total:
            df["annual_total"] = df[
                duplicate_total
            ].apply(
                lambda value:
                safe_number(value, 0)
            )
        else:
            df["annual_total"] = df[
                "total"
            ].apply(
                lambda value:
                safe_number(value, 0)
            )

        if dynamic_month_columns:
            calculated_total = df[
                dynamic_month_columns
            ].sum(
                axis=1
            )

            df["annual_total"] = df[
                "annual_total"
            ].where(
                df["annual_total"] > 0,
                calculated_total
            )

        df["total"] = df[
            "annual_total"
        ]

        return df.fillna("")

    except Exception as error:
        st.error(
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
        option = clean_value(option)

        if (
            option
            and option not in clean_options
        ):
            clean_options.append(option)

    default_value = clean_value(
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
    semester,
    year=None
):
    filtered = df.copy()

    filters = {
        "business_type": business_type,
        "line_of_business": line_of_business,
        "programme_name": programme_name,
        "job_code": job_code,
        "batch": batch,
        "semester": semester
    }

    if (
        year is not None
        and "year" in filtered.columns
        and filtered["year"]
        .astype(str)
        .str.strip()
        .replace(
            [
                "nan",
                "None",
                "NaN"
            ],
            ""
        )
        .ne("")
        .any()
    ):
        filters["year"] = year

    for column, value in filters.items():
        value = clean_value(value)

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
# MYSQL REQUEST HELPERS
# =========================================================

def update_status_in_mysql(
    request_id,
    status
):
    try:
        connection = get_connection()
        cursor = connection.cursor()

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


def update_request_in_mysql(
    request_id,
    data
):
    try:
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            """
            UPDATE requests
            SET
                business_type=%s,
                line_of_business=%s,
                programme_name=%s,
                job_code=%s,
                batch=%s,
                semester=%s,
                training_hours_from_master=%s,
                paper_name=%s,
                master_total_cost=%s,
                training_days=%s,
                hours_per_day=%s,
                total_hours=%s,
                rate_per_hour=%s,
                trainer_cost=%s,
                stay_per_day=%s,
                food_per_day=%s,
                approver_local_travel_per_day=%s,
                approver_local_travel_total=%s,
                approver_outstation_travel_mode=%s,
                approver_going_travel_cost=%s,
                approver_return_travel_cost=%s,
                approver_outstation_travel_total=%s,
                approver_total_travel_cost=%s,
                stay_total=%s,
                food_total=%s,
                estimated_budget=%s,
                budget_difference=%s,
                total_available_budget=%s,
                remaining_after_approval=%s,
                budget_month=%s,
                approver_remarks=%s,
                request_status=%s
            WHERE request_id=%s
            """,
            (
                data["business_type"],
                data["line_of_business"],
                data["programme_name"],
                data["job_code"],
                data["batch"],
                data["semester"],
                data["training_hours_from_master"],
                data["paper_name"],
                data["master_total_cost"],
                data["training_days"],
                data["hours_per_day"],
                data["total_hours"],
                data["rate_per_hour"],
                data["trainer_cost"],
                data["stay_per_day"],
                data["food_per_day"],
                data[
                    "approver_local_travel_per_day"
                ],
                data[
                    "approver_local_travel_total"
                ],
                data[
                    "approver_outstation_travel_mode"
                ],
                data[
                    "approver_going_travel_cost"
                ],
                data[
                    "approver_return_travel_cost"
                ],
                data[
                    "approver_outstation_travel_total"
                ],
                data[
                    "approver_total_travel_cost"
                ],
                data["stay_total"],
                data["food_total"],
                data["estimated_budget"],
                data["budget_difference"],
                data["total_available_budget"],
                data[
                    "remaining_after_approval"
                ],
                data["budget_month"],
                data["approver_remarks"],
                data["request_status"],
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
    approver_banner(
        "Add College",
        (
            "Add a new college, programme structure and "
            "monthly budget allocation to the budget master."
        )
    )

    budget_master_df = load_budget_master()

    st.markdown("### College & Program Details")

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

    column_3, column_4 = st.columns(2)

    with column_3:
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

    with column_4:
        training_hours = st.number_input(
            "Training Hours",
            min_value=0,
            value=0,
            step=1,
            key="college_master_hours"
        )

    approver_banner(
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
                "business_type": business_type,
                "line_of_business": line_of_business,
                "programme_name": programme_name,
                "job_code": job_code,
                "batch": batch,
                "semester": semester,
                "year": year,
                "training_hours": training_hours,
                "paper_name": paper_name,
                "jan": month_values["jan"],
                "feb": month_values["feb"],
                "mar": month_values["mar"],
                "apr": month_values["apr"],
                "may": month_values["may"],
                "jun": month_values["jun"],
                "jul": month_values["jul"],
                "aug": month_values["aug"],
                "sep": month_values["sep"],
                "oct": month_values["oct"],
                "nov": month_values["nov"],
                "dec": month_values["dec"],
                "total": annual_total
            }
        )

        st.success(
            (
                "College added successfully. "
                "It is now available in budget.csv."
            )
        )


# =========================================================
# REQUESTER DETAILS PAGE
# =========================================================

def show_requester_details_page(
    pending_requests,
    requests_df
):
    approver_banner(
        "Requester Details",
        (
            "Review the original training requirement and "
            "requester budget before unlocking estimation."
        )
    )

    if pending_requests.empty:
        st.info(
            "No requests pending for Approver."
        )

        return

    request_id_tab_1 = st.selectbox(
        "Select Request",
        pending_requests[
            "request_id"
        ],
        key="approver_request_details_select"
    )

    selected_request_tab_1 = (
        pending_requests[
            pending_requests["request_id"]
            == request_id_tab_1
        ]
        .iloc[0]
    )

    request_summary_column_1, request_summary_column_2, request_summary_column_3 = (
        st.columns(3)
    )

    with request_summary_column_1:
        st.metric(
            "Request ID",
            request_id_tab_1
        )

    with request_summary_column_2:
        st.metric(
            "Training Days",
            clean_value(
                selected_request_tab_1.get(
                    "training_days",
                    0
                ),
                "0"
            )
        )

    with request_summary_column_3:
        requester_summary_budget = safe_number(
            selected_request_tab_1.get(
                "total_expected_budget",
                0
            )
        )

        st.metric(
            "Requester Budget",
            f"₹{requester_summary_budget:,.0f}"
        )

    st.markdown(
        "### Request Information"
    )

    requester_details = pd.DataFrame(
        {
            "Field": [
                "Request Date",
                "Training Start Date",
                "Training End Date",
                "Business Type",
                "Line of Business",
                "Programme Name",
                "Job Code",
                "Batch",
                "Semester",
                "Training Hours",
                "Paper Name",
                "Master Total Cost",
                "Training Topic",
                "Trainer Name",
                "Trainer Type",
                "Purpose / Remarks"
            ],

            "Details": [
                clean_value(
                    selected_request_tab_1.get(
                        "request_date",
                        ""
                    )
                ),

                clean_value(
                    selected_request_tab_1.get(
                        "start_date",
                        ""
                    )
                ),

                clean_value(
                    selected_request_tab_1.get(
                        "end_date",
                        ""
                    )
                ),

                clean_value(
                    selected_request_tab_1.get(
                        "business_type",
                        ""
                    )
                ),

                clean_value(
                    selected_request_tab_1.get(
                        "line_of_business",
                        ""
                    )
                ),

                clean_value(
                    selected_request_tab_1.get(
                        "programme_name",
                        ""
                    )
                ),

                clean_value(
                    selected_request_tab_1.get(
                        "job_code",
                        ""
                    )
                ),

                clean_value(
                    selected_request_tab_1.get(
                        "batch",
                        ""
                    )
                ),

                clean_value(
                    selected_request_tab_1.get(
                        "semester",
                        ""
                    )
                ),

                clean_value(
                    selected_request_tab_1.get(
                        "training_hours_from_master",
                        ""
                    )
                ),

                clean_value(
                    selected_request_tab_1.get(
                        "paper_name",
                        ""
                    )
                ),

                clean_value(
                    selected_request_tab_1.get(
                        "master_total_cost",
                        ""
                    )
                ),

                clean_value(
                    selected_request_tab_1.get(
                        "training_topic",
                        ""
                    )
                ),

                clean_value(
                    selected_request_tab_1.get(
                        "trainer_name",
                        ""
                    )
                ),

                clean_value(
                    selected_request_tab_1.get(
                        "trainer_type",
                        ""
                    )
                ),

                clean_value(
                    selected_request_tab_1.get(
                        "purpose",
                        ""
                    )
                )
            ]
        }
    )

    st.table(
        requester_details
    )

    requester_total_budget = safe_number(
        selected_request_tab_1.get(
            "total_expected_budget",
            0
        )
    )

    approver_banner(
        "Requester Budget Estimation",
        (
            "Review the training, travel, stay and food "
            "cost values submitted by the requester."
        )
    )

    requester_budget_table = pd.DataFrame(
        {
            "Component": [
                "Training Days",
                "Total Hours",
                "Rate Per Hour",
                "Training Cost",
                "Local Travel",
                "Outstation Travel",
                "Total Travel Cost",
                "Stay Cost",
                "Food Cost",
                "Total Requester Budget"
            ],

            "Requester Value": [
                clean_value(
                    selected_request_tab_1.get(
                        "training_days",
                        0
                    ),
                    "0"
                ),

                clean_value(
                    selected_request_tab_1.get(
                        "total_hours",
                        0
                    ),
                    "0"
                ),

                f"₹{safe_number(selected_request_tab_1.get('rate_per_hour', 0)):,.0f}",

                f"₹{safe_number(selected_request_tab_1.get('training_cost', 0)):,.0f}",

                f"₹{safe_number(selected_request_tab_1.get('local_travel_total', 0)):,.0f}",

                f"₹{safe_number(selected_request_tab_1.get('outstation_travel_total', 0)):,.0f}",

                f"₹{safe_number(selected_request_tab_1.get('total_travel_cost', 0)):,.0f}",

                f"₹{safe_number(selected_request_tab_1.get('stay_cost', 0)):,.0f}",

                f"₹{safe_number(selected_request_tab_1.get('food_cost', 0)):,.0f}",

                f"₹{requester_total_budget:,.0f}"
            ]
        }
    )

    st.table(
        requester_budget_table
    )

    action_column_1, action_column_2 = (
        st.columns(2)
    )

    with action_column_1:
        if st.button(
            "Approve for Estimation",
            use_container_width=True,
            key=(
                f"approve_estimation_"
                f"{request_id_tab_1}"
            )
        ):
            st.session_state[
                "approved_for_estimation"
            ][request_id_tab_1] = True

            st.session_state[
                "selected_estimation_request"
            ] = request_id_tab_1

            st.session_state[
                "approver_current_page"
            ] = "Approver Budget Calculation"

            st.session_state[
                "approver_popup_shown"
            ] = True

            st.session_state[
                "go_to_calculation"
            ] = True

            st.success(
                (
                    "Request approved for estimation. "
                    "Opening budget calculation."
                )
            )

            st.rerun()

    with action_column_2:
        if st.button(
            "Reject & Send Back to Requester",
            use_container_width=True,
            key=(
                f"reject_request_"
                f"{request_id_tab_1}"
            )
        ):
            request_index = requests_df[
                requests_df["request_id"]
                == request_id_tab_1
            ].index[0]

            requests_df.loc[
                request_index,
                "request_status"
            ] = "Sent Back to Requester"

            requests_df.to_csv(
                REQUESTS_FILE,
                index=False
            )

            update_status_in_mysql(
                request_id_tab_1,
                "Sent Back to Requester"
            )

            send_email(
                clean_value(
                    selected_request_tab_1.get(
                        "created_by",
                        ""
                    )
                ),

                (
                    "Training Request Sent "
                    "Back by Approver"
                ),

                f"""
Your training request has been sent back by the Approver.

Request ID: {request_id_tab_1}
College: {clean_value(selected_request_tab_1.get("college_name", ""))}
Training Topic: {clean_value(selected_request_tab_1.get("training_topic", ""))}

Please review and submit the request again.
"""
            )

            if (
                request_id_tab_1
                in st.session_state[
                    "approved_for_estimation"
                ]
            ):
                del st.session_state[
                    "approved_for_estimation"
                ][request_id_tab_1]

            if (
                st.session_state.get(
                    "selected_estimation_request",
                    ""
                )
                == request_id_tab_1
            ):
                st.session_state[
                    "selected_estimation_request"
                ] = ""

            st.warning(
                "Request sent back to Requester."
            )

            st.rerun()


# =========================================================
# APPROVER BUDGET CALCULATION PAGE
# =========================================================

def show_approver_calculation_page(
    pending_requests,
    requests_df,
    budget_df
):
    approver_banner(
        "Approver Budget Calculation",
        (
            "Confirm programme details, verify available budget "
            "and calculate the final approver estimate."
        )
    )

    if pending_requests.empty:
        st.info(
            "No requests pending for Approver."
        )

        return

    request_list = (
        pending_requests[
            "request_id"
        ]
        .tolist()
    )

    default_request = st.session_state.get(
        "selected_estimation_request",
        ""
    )

    default_index = (
        request_list.index(
            default_request
        )
        if default_request in request_list
        else 0
    )

    request_id = st.selectbox(
        "Select Request",
        request_list,
        index=default_index,
        key=(
            "approver_calculation_"
            "request_select"
        )
    )

    selected_request = (
        pending_requests[
            pending_requests["request_id"]
            == request_id
        ]
        .iloc[0]
    )

    requester_total_budget = safe_number(
        selected_request.get(
            "total_expected_budget",
            0
        )
    )

    if not st.session_state[
        "approved_for_estimation"
    ].get(
        request_id,
        False
    ):
        st.warning(
            (
                "First approve this request from "
                "Requester Details to unlock estimation."
            )
        )

        return

    st.success(
        "Estimation unlocked for this request."
    )

    approver_banner(
        "Select / Confirm Program Details",
        (
            "Confirm the budget-master classification "
            "used for this training request."
        )
    )

    business_options = [
        "B2C",
        "B2I",
        "B2B"
    ]

    request_business_type = clean_value(
        selected_request.get(
            "business_type",
            "B2I"
        ),
        "B2I"
    )

    program_column_1, program_column_2 = (
        st.columns(2)
    )

    with program_column_1:
        business_type = st.selectbox(
            "Business Type",
            business_options,
            index=get_index(
                business_options,
                request_business_type,
                1
            ),
            key=f"business_type_{request_id}"
        )

        line_of_business = select_or_add(
            "Line of Business",
            get_unique_values(
                budget_df,
                "line_of_business"
            ),
            f"lob_{request_id}",
            clean_value(
                selected_request.get(
                    "line_of_business",
                    ""
                )
            )
        )

        programme_name = select_or_add(
            "Programme Name",
            get_unique_values(
                budget_df,
                "programme_name"
            ),
            f"program_{request_id}",
            clean_value(
                selected_request.get(
                    "programme_name",
                    ""
                )
            )
        )

    with program_column_2:
        job_code = select_or_add(
            "Job Code",
            get_unique_values(
                budget_df,
                "job_code"
            ),
            f"job_{request_id}",
            clean_value(
                selected_request.get(
                    "job_code",
                    ""
                )
            )
        )

        batch = select_or_add(
            "Batch",
            get_unique_values(
                budget_df,
                "batch"
            ),
            f"batch_{request_id}",
            clean_value(
                selected_request.get(
                    "batch",
                    ""
                )
            )
        )

        semester = select_or_add(
            "Semester",
            get_unique_values(
                budget_df,
                "semester"
            ),
            f"semester_{request_id}",
            clean_value(
                selected_request.get(
                    "semester",
                    ""
                )
            )
        )

    selection_column_1, selection_column_2 = (
        st.columns(2)
    )

    year_options = get_financial_year_options(
        budget_df
    )

    if not year_options:
        year_options = [
            "2026-27"
        ]

    with selection_column_1:
        year = st.selectbox(
            "Budget Financial Year",
            year_options,
            index=0,
            key=f"year_{request_id}"
        )

    financial_year_month_columns = (
        get_financial_year_month_columns(
            budget_df,
            year
        )
    )

    with selection_column_2:
        budget_month = st.selectbox(
            "Budget Month",
            financial_year_month_columns,
            index=0,
            format_func=month_column_label,
            key=f"budget_month_{request_id}"
        )

    selected_budget_rows = filter_budget_master(
        budget_df,
        business_type,
        line_of_business,
        programme_name,
        job_code,
        batch,
        semester,
        year
    )

    selected_master = (
        selected_budget_rows.iloc[0]
        if not selected_budget_rows.empty
        else {}
    )

    training_hours_from_master = (
        safe_number(
            selected_master.get(
                "training_hours",
                0
            )
        )
        if len(selected_master)
        else safe_number(
            selected_request.get(
                "training_hours_from_master",
                0
            )
        )
    )

    paper_name = (
        clean_value(
            selected_master.get(
                "paper_name",
                ""
            )
        )
        if len(selected_master)
        else clean_value(
            selected_request.get(
                "paper_name",
                ""
            )
        )
    )

    monthly_available_budget = (
        safe_number(
            selected_master.get(
                budget_month,
                0
            )
        )
        if len(selected_master)
        else 0
    )

    annual_available_budget = (
        annual_budget_for_financial_year(
            selected_master,
            financial_year_month_columns
        )
        if len(selected_master)
        else safe_number(
            selected_request.get(
                "master_total_cost",
                0
            )
        )
    )

    if (
        annual_available_budget <= 0
        and len(selected_master)
    ):
        annual_available_budget = safe_number(
            selected_master.get(
                "annual_total",
                selected_master.get(
                    "total",
                    0
                )
            )
        )

    total_available_budget = (
        monthly_available_budget
        if monthly_available_budget > 0
        else annual_available_budget
    )

    approver_banner(
        "Budget Verification",
        (
            "Compare monthly allocation, annual budget "
            "and requester expected cost."
        )
    )

    verification_column_1, verification_column_2, verification_column_3, verification_column_4 = (
        st.columns(4)
    )

    with verification_column_1:
        st.metric(
            (
                f"{month_column_label(budget_month)} "
                "Monthly Budget"
            ),
            f"₹{monthly_available_budget:,.0f}"
        )

    with verification_column_2:
        st.metric(
            "Annual / Yearly Budget",
            f"₹{annual_available_budget:,.0f}"
        )

    with verification_column_3:
        st.metric(
            "Requester Expected Budget",
            f"₹{requester_total_budget:,.0f}"
        )

    with verification_column_4:
        st.metric(
            "Budget Used For Approval",
            f"₹{total_available_budget:,.0f}"
        )

    if selected_budget_rows.empty:
        st.warning(
            (
                "No matching budget found from Excel. "
                "Please verify Budget Master."
            )
        )

    elif monthly_available_budget <= 0:
        st.warning(
            (
                f"{month_column_label(budget_month)} month ka "
                "budget 0 hai. Approver should "
                "verify annual budget."
            )
        )

    elif (
        requester_total_budget
        > monthly_available_budget
    ):
        st.error(
            (
                "Requester expected budget selected "
                "monthly budget se zyada hai."
            )
        )

    else:
        st.success(
            (
                "Requester expected budget selected "
                "monthly budget ke andar hai."
            )
        )

    st.markdown(
        "### Program Details"
    )

    program_table = pd.DataFrame(
        {
            "Field": [
                "Business Type",
                "Line of Business",
                "Programme Name",
                "Job Code",
                "Batch",
                "Semester",
                "Year",
                "Selected Month",
                "Training Hours",
                "Paper Name",
                "Monthly Budget",
                "Annual Budget",
                "Budget Used"
            ],

            "Value": [
                business_type,
                line_of_business,
                programme_name,
                job_code,
                batch,
                semester,
                year,
                month_column_label(budget_month),
                training_hours_from_master,
                paper_name,
                f"₹{monthly_available_budget:,.0f}",
                f"₹{annual_available_budget:,.0f}",
                f"₹{total_available_budget:,.0f}"
            ]
        }
    )

    st.table(
        program_table
    )

    approver_banner(
        "Training Cost Calculation",
        (
            "Enter training duration and approved trainer "
            "rate to calculate total programme cost."
        )
    )

    default_training_days = max(
        1,
        int(
            safe_number(
                selected_request.get(
                    "training_days",
                    1
                ),
                1
            )
        )
    )

    training_column_1, training_column_2, training_column_3 = (
        st.columns(3)
    )

    with training_column_1:
        training_days = st.number_input(
            "Total Training Days",
            min_value=1,
            value=default_training_days,
            key=f"training_days_{request_id}"
        )

    with training_column_2:
        hours_per_day = st.number_input(
            "Hours Per Day",
            min_value=1,
            value=6,
            key=f"hours_per_day_{request_id}"
        )

    total_hours = (
        training_days
        * hours_per_day
    )

    with training_column_3:
        rate_per_hour = st.number_input(
            "Trainer Rate Per Hour",
            min_value=0,
            value=int(
                safe_number(
                    selected_request.get(
                        "rate_per_hour",
                        3000
                    ),
                    3000
                )
            ),
            key=f"rate_per_hour_{request_id}"
        )

    trainer_cost = (
        total_hours
        * rate_per_hour
    )

    training_metric_1, training_metric_2 = (
        st.columns(2)
    )

    with training_metric_1:
        st.metric(
            "Total Program Hours",
            total_hours
        )

    with training_metric_2:
        st.metric(
            "Trainer Cost",
            f"₹{trainer_cost:,.0f}"
        )

    approver_banner(
        "Additional Requirements Cost",
        (
            "Add daily stay and food expenses "
            "for the complete training duration."
        )
    )

    additional_column_1, additional_column_2 = (
        st.columns(2)
    )

    with additional_column_1:
        stay_per_day = st.number_input(
            "Stay Cost Per Day",
            min_value=0,
            value=0,
            key=f"stay_per_day_{request_id}"
        )

    with additional_column_2:
        food_per_day = st.number_input(
            "Food Cost Per Day",
            min_value=0,
            value=0,
            key=f"food_per_day_{request_id}"
        )

    approver_banner(
        "Travel Cost Details",
        (
            "Calculate local and outstation travel "
            "expenses for this training."
        )
    )

    travel_column_1, travel_column_2 = (
        st.columns(2)
    )

    with travel_column_1:
        approver_local_travel_per_day = (
            st.number_input(
                (
                    "Local Taxi / Daily Travel "
                    "Cost Per Day (₹)"
                ),
                min_value=0,
                value=0,
                key=f"local_travel_{request_id}"
            )
        )

    approver_local_travel_total = (
        approver_local_travel_per_day
        * training_days
    )

    with travel_column_2:
        approver_outstation_travel_mode = (
            st.selectbox(
                "Outstation Travel Mode",
                [
                    "Flight",
                    "Train",
                    "Bus",
                    "Car"
                ],
                key=f"travel_mode_{request_id}"
            )
        )

    fare_column_1, fare_column_2 = (
        st.columns(2)
    )

    with fare_column_1:
        approver_going_travel_cost = (
            st.number_input(
                "Going Travel Cost (₹)",
                min_value=0,
                value=0,
                key=f"going_travel_{request_id}"
            )
        )

    with fare_column_2:
        approver_return_travel_cost = (
            st.number_input(
                "Return Travel Cost (₹)",
                min_value=0,
                value=0,
                key=f"return_travel_{request_id}"
            )
        )

    approver_outstation_travel_total = (
        approver_going_travel_cost
        + approver_return_travel_cost
    )

    approver_total_travel_cost = (
        approver_local_travel_total
        + approver_outstation_travel_total
    )

    travel_metric_1, travel_metric_2, travel_metric_3 = (
        st.columns(3)
    )

    with travel_metric_1:
        st.metric(
            "Local Travel Total",
            f"₹{approver_local_travel_total:,.0f}"
        )

    with travel_metric_2:
        st.metric(
            (
                "Outstation Travel "
                f"({approver_outstation_travel_mode})"
            ),
            f"₹{approver_outstation_travel_total:,.0f}"
        )

    with travel_metric_3:
        st.metric(
            "Total Travel Cost",
            f"₹{approver_total_travel_cost:,.0f}"
        )
    stay_total = (
        stay_per_day
        * training_days
    )

    food_total = (
        food_per_day
        * training_days
    )

    approver_estimated_budget = (
        trainer_cost
        + approver_total_travel_cost
        + stay_total
        + food_total
    )

    remaining_after_approval = (
        total_available_budget
        - approver_estimated_budget
    )

    approver_banner(
        "Available Budget vs Approver Estimate",
        (
            "Compare the selected available budget with "
            "the final approver cost calculation."
        )
    )

    estimate_column_1, estimate_column_2, estimate_column_3 = (
        st.columns(3)
    )

    with estimate_column_1:
        st.metric(
            "Available Budget",
            f"₹{total_available_budget:,.0f}"
        )

    with estimate_column_2:
        st.metric(
            "Approver Estimated Budget",
            f"₹{approver_estimated_budget:,.0f}"
        )

    with estimate_column_3:
        st.metric(
            "Balance After Approval",
            f"₹{remaining_after_approval:,.0f}"
        )

    if total_available_budget <= 0:
        st.warning(
            (
                "Budget is 0. Matching row found nahi hui "
                "ya selected month ka budget 0 hai."
            )
        )

    elif (
        approver_estimated_budget
        > total_available_budget
    ):
        st.error(
            (
                "Approver estimated budget exceeds "
                "the available budget."
            )
        )

    else:
        st.success(
            (
                "Approver estimated budget is "
                "within the available budget."
            )
        )

    approver_banner(
        "Requester vs Approver Budget Comparison",
        (
            "Review the difference between the requester "
            "estimate and the final approver estimate."
        )
    )

    difference = (
        approver_estimated_budget
        - requester_total_budget
    )

    comparison_column_1, comparison_column_2, comparison_column_3 = (
        st.columns(3)
    )

    with comparison_column_1:
        st.metric(
            "Requester Budget",
            f"₹{requester_total_budget:,.0f}"
        )

    with comparison_column_2:
        st.metric(
            "Approver Budget",
            f"₹{approver_estimated_budget:,.0f}"
        )

    with comparison_column_3:
        st.metric(
            "Difference",
            f"₹{difference:,.0f}"
        )

    approver_banner(
        "Approver Decision",
        (
            "Add final remarks and either send the "
            "request to Partner or return it to Requester."
        )
    )

    approver_remarks = st.text_area(
        "Approver Remarks",
        key=f"remarks_{request_id}"
    )

    decision = st.selectbox(
        "Decision",
        [
            "Approve and Send to Partner",
            "Send Back to Requester"
        ],
        key=f"decision_{request_id}"
    )

    if st.button(
        "Submit Estimation / Decision",
        use_container_width=True,
        key=f"submit_decision_{request_id}"
    ):
        request_index = requests_df[
            requests_df["request_id"]
            == request_id
        ].index[0]

        new_status = (
            "Pending Director Approval"
            if decision
            == "Approve and Send to Partner"
            else "Sent Back to Requester"
        )

        update_data = {
            "business_type": business_type,

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

            "training_hours_from_master":
                training_hours_from_master,

            "paper_name":
                paper_name,

            "master_total_cost":
                total_available_budget,

            "training_days":
                training_days,

            "hours_per_day":
                hours_per_day,

            "total_hours":
                total_hours,

            "rate_per_hour":
                rate_per_hour,

            "trainer_cost":
                trainer_cost,

            "stay_per_day":
                stay_per_day,

            "food_per_day":
                food_per_day,

            "approver_local_travel_per_day":
                approver_local_travel_per_day,

            "approver_local_travel_total":
                approver_local_travel_total,

            "approver_outstation_travel_mode":
                approver_outstation_travel_mode,

            "approver_going_travel_cost":
                approver_going_travel_cost,

            "approver_return_travel_cost":
                approver_return_travel_cost,

            "approver_outstation_travel_total":
                approver_outstation_travel_total,

            "approver_total_travel_cost":
                approver_total_travel_cost,

            "stay_total":
                stay_total,

            "food_total":
                food_total,

            "estimated_budget":
                approver_estimated_budget,

            "budget_difference":
                difference,

            "total_available_budget":
                total_available_budget,

            "remaining_after_approval":
                remaining_after_approval,

            "budget_month":
                budget_month,

            "approver_remarks":
                str(approver_remarks),

            "request_status":
                new_status
        }

        for column, value in update_data.items():
            if column not in requests_df.columns:
                requests_df[
                    column
                ] = ""

            requests_df.loc[
                request_index,
                column
            ] = value

        requests_df.to_csv(
            REQUESTS_FILE,
            index=False
        )

        update_request_in_mysql(
            request_id,
            update_data
        )

        if (
            decision
            == "Approve and Send to Partner"
        ):
            send_email(
                PARTNER_EMAIL,

                (
                    "Training Request Awaiting "
                    "Partner Approval"
                ),

                f"""
Approver has approved a training request.

Request ID: {request_id}
College: {clean_value(selected_request.get("college_name", ""))}
Training Topic: {clean_value(selected_request.get("training_topic", ""))}
Trainer: {clean_value(selected_request.get("trainer_name", ""))}
Estimated Budget: ₹{approver_estimated_budget:,.0f}

Please login for final approval.
"""
            )

        if (
            request_id
            in st.session_state[
                "approved_for_estimation"
            ]
        ):
            del st.session_state[
                "approved_for_estimation"
            ][request_id]

        if (
            st.session_state.get(
                "selected_estimation_request",
                ""
            )
            == request_id
        ):
            st.session_state[
                "selected_estimation_request"
            ] = ""

        st.session_state[
            "approver_current_page"
        ] = "Requester Details"

        if (
            decision
            == "Approve and Send to Partner"
        ):
            st.success(
                (
                    "Complete estimation sent to Partner "
                    "successfully. Email sent to Partner."
                )
            )

        else:
            st.warning(
                "Request sent back to Requester."
            )

        st.rerun()


# =========================================================
# BUDGET UPDATE / ADD PAGE
# =========================================================

def show_budget_update_page():
    approver_banner(
        "Budget Update / Add",
        (
            "Add a new budget line or update the existing "
            "monthly allocation for a programme."
        )
    )

    budget_master_df = load_budget_master()

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
            key="budget_business_type"
        )

        line_update = select_or_add(
            "Line of Business",
            get_unique_values(
                budget_master_df,
                "line_of_business"
            ),
            "budget_line"
        )

        programme_update = select_or_add(
            "Programme Name",
            get_unique_values(
                budget_master_df,
                "programme_name"
            ),
            "budget_programme"
        )

        job_code_update = select_or_add(
            "Job Code",
            get_unique_values(
                budget_master_df,
                "job_code"
            ),
            "budget_job_code"
        )

    with budget_column_2:
        batch_update = select_or_add(
            "Batch",
            get_unique_values(
                budget_master_df,
                "batch"
            ),
            "budget_batch"
        )

        semester_update = select_or_add(
            "Semester",
            get_unique_values(
                budget_master_df,
                "semester"
            ),
            "budget_semester"
        )

        financial_year_options = (
            get_financial_year_options(
                budget_master_df
            )
            or [
                "2026-27"
            ]
        )

        year_update = select_or_add(
            "Financial Year",
            financial_year_options,
            "budget_year",
            financial_year_options[0]
        )

    financial_year_month_columns = (
        get_financial_year_month_columns(
            budget_master_df,
            year_update
        )
    )

    for month_column in financial_year_month_columns:
        if month_column not in budget_master_df.columns:
            budget_master_df[
                month_column
            ] = 0

    existing_rows = filter_budget_master(
        budget_master_df,
        business_type_update,
        line_update,
        programme_update,
        job_code_update,
        batch_update,
        semester_update
    )

    existing_row = (
        existing_rows.iloc[0]
        if not existing_rows.empty
        else {}
    )

    detail_column_1, detail_column_2 = (
        st.columns(2)
    )

    with detail_column_1:
        training_hours_update = st.number_input(
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
            key="budget_training_hours"
        )

    with detail_column_2:
        paper_name_update = select_or_add(
            "Paper Name",
            get_unique_values(
                budget_master_df,
                "paper_name"
            ),
            "budget_paper",
            (
                clean_value(
                    existing_row.get(
                        "paper_name",
                        ""
                    )
                )
                if len(existing_row)
                else ""
            )
        )

    approver_banner(
        "Monthly Budget Entry",
        (
            "Update monthly values for the selected "
            "financial year. Annual total is calculated automatically."
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

    month_display_columns = [
        month_column_1,
        month_column_2,
        month_column_3
    ]

    for index, month_column in enumerate(
        financial_year_month_columns
    ):
        default_month_value = (
            int(
                safe_number(
                    existing_row.get(
                        month_column,
                        0
                    )
                )
            )
            if len(existing_row)
            else 0
        )

        with month_display_columns[index % 3]:
            month_values[month_column] = (
                st.number_input(
                    f"{month_column_label(month_column)} Budget",
                    min_value=0,
                    value=default_month_value,
                    step=1000,
                    key=(
                        f"{month_column}_budget_input_"
                        f"{combination_key}"
                    )
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
        key="save_budget_master_btn"
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

            "annual_total":
                annual_total,

            "total":
                annual_total
        }

        for month_column in financial_year_month_columns:
            new_budget_row[
                month_column
            ] = month_values[
                month_column
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

        # Existing MySQL structure is retained. The selected financial-year
        # months are mapped into its Jan-Dec fields without changing the DB.
        mysql_row = {
            "business_type": business_type_update,
            "line_of_business": line_update,
            "programme_name": programme_update,
            "job_code": job_code_update,
            "batch": batch_update,
            "semester": semester_update,
            "year": year_update,
            "training_hours": training_hours_update,
            "paper_name": paper_name_update,
            "total": annual_total
        }

        for month in MONTHS:
            matching_column = next(
                (
                    column
                    for column in financial_year_month_columns
                    if column.startswith(
                        f"{month}_"
                    )
                ),
                None
            )

            mysql_row[month] = (
                month_values.get(
                    matching_column,
                    0
                )
                if matching_column
                else 0
            )

        save_budget_to_mysql(
            mysql_row
        )

        st.info(
            "Budget master updated successfully."
        )


# =========================================================
# MAIN APPROVER PAGE
# =========================================================

def show_mediator_budget_check():

    apply_approver_ui()
    show_approver_hero()

    budget_df = load_budget_master()

    if budget_df.empty:
        st.error(
            "budget.csv not found or empty."
        )

        return

    try:
        requests_df = pd.read_csv(
            REQUESTS_FILE
        ).fillna("")

    except Exception:
        requests_df = pd.DataFrame()

    pending_requests = pd.DataFrame()

    if (
        not requests_df.empty
        and "request_status"
        in requests_df.columns
    ):
        pending_requests = requests_df[
            requests_df[
                "request_status"
            ]
            .astype(str)
            .str.strip()
            == "Pending Mediator Review"
        ]

    if (
        "approver_popup_shown"
        not in st.session_state
    ):
        st.session_state[
            "approver_popup_shown"
        ] = False

    if (
        "approved_for_estimation"
        not in st.session_state
    ):
        st.session_state[
            "approved_for_estimation"
        ] = {}

    if (
        "selected_estimation_request"
        not in st.session_state
    ):
        st.session_state[
            "selected_estimation_request"
        ] = ""

    if (
        "approver_current_page"
        not in st.session_state
    ):
        st.session_state[
            "approver_current_page"
        ] = "Requester Details"

    page_options = [
        "Add College",
        "Requester Details",
        "Approver Budget Calculation",
        "Budget Update / Add"
    ]

    current_page = st.session_state.get(
        "approver_current_page",
        "Requester Details"
    )

    if st.session_state.get(
        "go_to_calculation",
        False
    ):
        current_page = (
            "Approver Budget Calculation"
        )

        st.session_state[
            "approver_current_page"
        ] = "Approver Budget Calculation"

        st.session_state[
            "go_to_calculation"
        ] = False

    @st.dialog(
        "New Request Received"
    )
    def new_request_popup():
        st.markdown(
            (
                "### Requester request pending\n\n"
                f"You have **{len(pending_requests)}** "
                "requester request(s) waiting for approval.\n\n"
                "Please review them from "
                "**Requester Details**."
            )
        )

        if st.button(
            "Okay, Review Now",
            use_container_width=True,
            key="approver_popup_review_button"
        ):
            st.session_state[
                "approver_popup_shown"
            ] = True

            st.session_state[
                "approver_current_page"
            ] = "Requester Details"

            st.rerun()

    if (
        not pending_requests.empty
        and not st.session_state[
            "approver_popup_shown"
        ]
        and current_page
        == "Requester Details"
    ):
        new_request_popup()

    approver_banner(
        "Approver Navigation",
        (
            "Choose the section you want to review "
            "or update."
        )
    )

    page = st.radio(
        "Choose Section",
        page_options,
        index=(
            page_options.index(
                current_page
            )
            if current_page
            in page_options
            else 0
        ),
        horizontal=True
    )

    if st.session_state.get(
        "go_to_calculation",
        False
    ):
        page = (
            "Approver Budget Calculation"
        )

        st.session_state[
            "go_to_calculation"
        ] = False

    st.session_state[
        "approver_current_page"
    ] = page

    if page == "Add College":
        show_college_master_page()

    elif page == "Requester Details":
        show_requester_details_page(
            pending_requests,
            requests_df
        )

    elif (
        page
        == "Approver Budget Calculation"
    ):
        show_approver_calculation_page(
            pending_requests,
            requests_df,
            budget_df
        )

    elif page == "Budget Update / Add":
        show_budget_update_page()
