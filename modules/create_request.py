import streamlit as st
import pandas as pd
from datetime import datetime
from db import get_connection
from email_utils import send_email

REQUESTS_FILE = "requests.csv"
BUDGET_MASTER_FILE = "budget.csv"

MONTH_MAP = {
    1: "jan", 2: "feb", 3: "mar", 4: "apr",
    5: "may", 6: "jun", 7: "jul", 8: "aug",
    9: "sep", 10: "oct", 11: "nov", 12: "dec"
}


def safe_number(value):
    try:
        if pd.isna(value):
            return 0

        value = str(value).replace(",", "").replace("₹", "").strip()

        if value.lower() in ["nan", "none", ""]:
            return 0

        return float(value)

    except:
        return 0


def clean_text(value):
    try:
        if pd.isna(value):
            return ""

        value = str(value).strip()

        if value.lower() in ["nan", "none", ""]:
            return ""

        return value

    except:
        return ""


def apply_requester_ui():
    st.markdown(
        """
        <style>
        /* =====================================================
           REQUESTER PAGE VARIABLES
        ===================================================== */

        :root {
            --request-primary: #4f46e5;
            --request-primary-dark: #4338ca;
            --request-secondary: #7c3aed;
            --request-accent: #ec4899;

            --request-background: #f6f7fb;
            --request-surface: #ffffff;
            --request-surface-soft: #f8fafc;

            --request-text: #0f172a;
            --request-text-soft: #64748b;
            --request-border: #e2e8f0;

            --request-success: #15803d;
            --request-warning: #b45309;
            --request-danger: #b91c1c;
        }

        /* =====================================================
           MAIN PAGE
        ===================================================== */

        .stApp {
            background:
                radial-gradient(
                    circle at 85% 0%,
                    rgba(79, 70, 229, 0.075),
                    transparent 25%
                ),
                radial-gradient(
                    circle at 15% 35%,
                    rgba(124, 58, 237, 0.035),
                    transparent 28%
                ),
                linear-gradient(
                    180deg,
                    #f8faff 0%,
                    #f5f7fb 100%
                );
        }

        [data-testid="stAppViewContainer"] {
            background: transparent;
        }

        [data-testid="stHeader"] {
            background: rgba(248, 250, 252, 0.78);
            backdrop-filter: blur(18px);
            border-bottom: 1px solid rgba(226, 232, 240, 0.55);
        }

        .block-container {
            max-width: 1450px;
            padding-top: 2.1rem;
            padding-bottom: 4rem;
        }

        /* =====================================================
           TYPOGRAPHY
        ===================================================== */

        h1 {
            color: var(--request-text) !important;
            font-size: 38px !important;
            font-weight: 900 !important;
            letter-spacing: -0.045em !important;
            line-height: 1.15 !important;
            margin-bottom: 6px !important;
        }

        h2 {
            color: var(--request-text) !important;
            font-weight: 850 !important;
            letter-spacing: -0.03em !important;
        }

        h3 {
            color: var(--request-text) !important;
            font-weight: 800 !important;
        }

        p {
            color: #475569;
        }

        [data-testid="stCaptionContainer"] {
            margin-top: -2px;
            margin-bottom: 24px;
        }

        [data-testid="stCaptionContainer"] p {
            color: #8994a8 !important;
            font-size: 15px !important;
            font-weight: 520 !important;
            line-height: 1.6 !important;
        }

        /* =====================================================
           SECTION HEADINGS
        ===================================================== */

        .section-title {
            position: relative;
            color: var(--request-text);
            font-size: 22px;
            font-weight: 850;
            line-height: 1.3;
            letter-spacing: -0.025em;
            margin-top: 34px;
            margin-bottom: 7px;
            padding-left: 15px;
        }

        .section-title::before {
            content: "";
            position: absolute;
            left: 0;
            top: 3px;
            width: 5px;
            height: 24px;
            border-radius: 999px;
            background:
                linear-gradient(
                    180deg,
                    var(--request-primary),
                    var(--request-secondary)
                );
            box-shadow: 0 4px 12px rgba(79, 70, 229, 0.28);
        }

        .section-subtitle {
            color: #7b879b;
            font-size: 14px;
            font-weight: 520;
            line-height: 1.55;
            margin-left: 15px;
            margin-bottom: 20px;
        }

        /* =====================================================
           INPUT LABELS
        ===================================================== */

        label {
            color: #475569 !important;
            font-size: 13px !important;
            font-weight: 750 !important;
            letter-spacing: 0.005em;
        }

        /* =====================================================
           TEXT INPUTS / NUMBER INPUTS / DATE INPUTS
        ===================================================== */

        div[data-testid="stTextInput"] input,
        div[data-testid="stNumberInput"] input,
        div[data-testid="stDateInput"] input,
        div[data-testid="stTextArea"] textarea {
            color: #111827 !important;
            background:
                linear-gradient(
                    180deg,
                    #ffffff 0%,
                    #fcfdff 100%
                ) !important;

            border: 1px solid #dbe3ef !important;
            border-radius: 13px !important;

            min-height: 48px;
            padding-left: 15px !important;
            padding-right: 15px !important;

            font-size: 14px !important;
            font-weight: 550 !important;

            box-shadow:
                0 3px 10px rgba(15, 23, 42, 0.025),
                inset 0 1px 0 rgba(255, 255, 255, 0.9);

            transition:
                border-color 0.16s ease,
                box-shadow 0.16s ease,
                transform 0.16s ease;
        }

        div[data-testid="stTextArea"] textarea {
            min-height: 120px;
            padding-top: 13px !important;
            line-height: 1.6;
        }

        div[data-testid="stTextInput"] input:hover,
        div[data-testid="stNumberInput"] input:hover,
        div[data-testid="stDateInput"] input:hover,
        div[data-testid="stTextArea"] textarea:hover {
            border-color: #b9c4d5 !important;
        }

        div[data-testid="stTextInput"] input:focus,
        div[data-testid="stNumberInput"] input:focus,
        div[data-testid="stDateInput"] input:focus,
        div[data-testid="stTextArea"] textarea:focus {
            border-color: #818cf8 !important;

            box-shadow:
                0 0 0 4px rgba(99, 102, 241, 0.11),
                0 7px 18px rgba(15, 23, 42, 0.05) !important;
        }

        div[data-testid="stTextInput"] input:disabled {
            color: #475569 !important;
            background: #f1f5f9 !important;
            border-color: #e2e8f0 !important;
            opacity: 1 !important;
            -webkit-text-fill-color: #475569 !important;
        }

        /* =====================================================
           SELECT BOX
        ===================================================== */

        div[data-baseweb="select"] > div {
            color: #111827 !important;

            background:
                linear-gradient(
                    180deg,
                    #ffffff 0%,
                    #fcfdff 100%
                ) !important;

            border: 1px solid #dbe3ef !important;
            border-radius: 13px !important;

            min-height: 48px;

            box-shadow:
                0 3px 10px rgba(15, 23, 42, 0.025),
                inset 0 1px 0 rgba(255, 255, 255, 0.9);

            transition:
                border-color 0.16s ease,
                box-shadow 0.16s ease;
        }

        div[data-baseweb="select"] > div:hover {
            border-color: #a5b4fc !important;
            box-shadow:
                0 0 0 3px rgba(99, 102, 241, 0.06),
                0 6px 16px rgba(15, 23, 42, 0.035);
        }

        div[data-baseweb="select"] span,
        div[data-baseweb="select"] div {
            color: #111827;
        }

        /* =====================================================
           NUMBER INPUT BUTTONS
        ===================================================== */

        div[data-testid="stNumberInput"] button {
            color: #64748b !important;
            background: transparent !important;
            border: none !important;
            box-shadow: none !important;
        }

        div[data-testid="stNumberInput"] button:hover {
            color: var(--request-primary) !important;
            background: #eef2ff !important;
        }

        /* =====================================================
           CUSTOM INFORMATION CARD
        ===================================================== */

        .custom-card {
            position: relative;
            overflow: hidden;

            background:
                radial-gradient(
                    circle at 92% 5%,
                    rgba(99, 102, 241, 0.11),
                    transparent 34%
                ),
                linear-gradient(
                    145deg,
                    #ffffff 0%,
                    #fbfcff 100%
                );

            border: 1px solid #dde4f0;
            border-radius: 18px;

            padding: 21px 22px;
            min-height: 135px;

            box-shadow:
                0 14px 34px rgba(15, 23, 42, 0.055),
                0 3px 8px rgba(15, 23, 42, 0.025),
                inset 0 1px 0 rgba(255, 255, 255, 0.95);

            transition:
                transform 0.18s ease,
                box-shadow 0.18s ease,
                border-color 0.18s ease;
        }

        .custom-card::before {
            content: "";
            position: absolute;
            top: 0;
            left: 22px;
            right: 22px;
            height: 3px;
            border-radius: 0 0 999px 999px;

            background:
                linear-gradient(
                    90deg,
                    var(--request-primary),
                    var(--request-secondary),
                    var(--request-accent)
                );

            opacity: 0.82;
        }

        .custom-card:hover {
            transform: translateY(-2px);
            border-color: #c7d2fe;

            box-shadow:
                0 18px 40px rgba(15, 23, 42, 0.075),
                0 5px 12px rgba(79, 70, 229, 0.06);
        }

        .custom-label {
            color: #768297;
            font-size: 12px;
            font-weight: 800;
            letter-spacing: 0.025em;
            text-transform: none;

            margin-top: 4px;
            margin-bottom: 13px;
        }

        .custom-value {
            color: var(--request-text);
            font-size: 23px;
            font-weight: 900;
            line-height: 1.25;
            letter-spacing: -0.025em;

            word-wrap: break-word;
            overflow-wrap: anywhere;
        }

        /* =====================================================
           STREAMLIT METRIC CARDS
        ===================================================== */

        div[data-testid="stMetric"] {
            position: relative;
            overflow: hidden;

            background:
                radial-gradient(
                    circle at 90% 0%,
                    rgba(99, 102, 241, 0.085),
                    transparent 34%
                ),
                linear-gradient(
                    145deg,
                    #ffffff 0%,
                    #fbfcff 100%
                );

            border: 1px solid #dde4f0;
            border-radius: 18px;

            padding: 19px 20px;
            min-height: 135px;

            box-shadow:
                0 14px 34px rgba(15, 23, 42, 0.05),
                0 3px 8px rgba(15, 23, 42, 0.025),
                inset 0 1px 0 rgba(255, 255, 255, 0.95);

            transition:
                transform 0.18s ease,
                box-shadow 0.18s ease,
                border-color 0.18s ease;
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
                    var(--request-primary),
                    var(--request-secondary)
                );

            opacity: 0.75;
        }

        div[data-testid="stMetric"]:hover {
            transform: translateY(-2px);
            border-color: #c7d2fe;

            box-shadow:
                0 18px 40px rgba(15, 23, 42, 0.07),
                0 5px 12px rgba(79, 70, 229, 0.055);
        }

        div[data-testid="stMetricLabel"] {
            margin-top: 2px;
        }

        div[data-testid="stMetricLabel"] p {
            color: #768297 !important;
            font-size: 12px !important;
            font-weight: 800 !important;
            letter-spacing: 0.015em !important;
        }

        div[data-testid="stMetricValue"] {
            color: var(--request-text) !important;
            font-size: 25px !important;
            font-weight: 900 !important;
            letter-spacing: -0.03em !important;

            white-space: normal !important;
            word-break: break-word;
            overflow-wrap: anywhere;
        }

        div[data-testid="stMetricDelta"] {
            font-weight: 750 !important;
        }

        /* =====================================================
           COLUMNS
        ===================================================== */

        div[data-testid="stHorizontalBlock"] {
            gap: 1rem;
        }

        /* =====================================================
           SUBMIT BUTTON
        ===================================================== */

        div[data-testid="stButton"] {
            margin-top: 10px;
        }

        div[data-testid="stButton"] button {
            position: relative;
            overflow: hidden;

            width: 100%;
            min-height: 52px;

            color: #ffffff !important;

            background:
                linear-gradient(
                    135deg,
                    #4338ca 0%,
                    #5b4de1 44%,
                    #7c3aed 100%
                ) !important;

            border: 1px solid rgba(255, 255, 255, 0.12) !important;
            border-radius: 14px !important;

            font-size: 14px !important;
            font-weight: 850 !important;
            letter-spacing: 0.01em;

            box-shadow:
                0 12px 26px rgba(79, 70, 229, 0.24),
                inset 0 1px 0 rgba(255, 255, 255, 0.22);

            transition:
                transform 0.17s ease,
                box-shadow 0.17s ease,
                filter 0.17s ease;
        }

        div[data-testid="stButton"] button::before {
            content: "";
            position: absolute;
            top: 0;
            left: -120%;
            width: 70%;
            height: 100%;

            background:
                linear-gradient(
                    90deg,
                    transparent,
                    rgba(255, 255, 255, 0.18),
                    transparent
                );

            transform: skewX(-20deg);
            transition: left 0.45s ease;
        }

        div[data-testid="stButton"] button:hover {
            color: #ffffff !important;

            background:
                linear-gradient(
                    135deg,
                    #3730a3 0%,
                    #4f46e5 45%,
                    #6d28d9 100%
                ) !important;

            transform: translateY(-2px);

            box-shadow:
                0 16px 32px rgba(79, 70, 229, 0.30),
                inset 0 1px 0 rgba(255, 255, 255, 0.25);
        }

        div[data-testid="stButton"] button:hover::before {
            left: 140%;
        }

        div[data-testid="stButton"] button:active {
            transform: translateY(0);
            box-shadow:
                0 9px 20px rgba(79, 70, 229, 0.22),
                inset 0 1px 0 rgba(255, 255, 255, 0.20);
        }

        div[data-testid="stButton"] button p,
        div[data-testid="stButton"] button span {
            position: relative;
            z-index: 2;

            color: #ffffff !important;
            font-weight: 850 !important;
            margin: 0 !important;
        }

        /* =====================================================
           ALERTS
        ===================================================== */

        div[data-testid="stAlert"] {
            border-radius: 14px;
            border-width: 1px;
            padding: 14px 16px;

            box-shadow:
                0 8px 20px rgba(15, 23, 42, 0.045);
        }

        div[data-testid="stAlert"] p {
            font-size: 14px;
            font-weight: 650;
            line-height: 1.55;
        }

        /* =====================================================
           POPOVERS AND DATE PICKER
        ===================================================== */

        div[data-baseweb="popover"] {
            border-radius: 14px !important;
            overflow: hidden;
            box-shadow: 0 20px 45px rgba(15, 23, 42, 0.16) !important;
        }

        /* =====================================================
           SCROLLBAR
        ===================================================== */

        ::-webkit-scrollbar {
            width: 9px;
            height: 9px;
        }

        ::-webkit-scrollbar-track {
            background: transparent;
        }

        ::-webkit-scrollbar-thumb {
            background: #cbd5e1;
            border-radius: 999px;
            border: 2px solid transparent;
            background-clip: padding-box;
        }

        ::-webkit-scrollbar-thumb:hover {
            background: #94a3b8;
            border: 2px solid transparent;
            background-clip: padding-box;
        }

        /* =====================================================
           RESPONSIVE
        ===================================================== */

        @media (max-width: 900px) {
            .block-container {
                padding-top: 1.3rem;
                padding-left: 1rem;
                padding-right: 1rem;
            }

            h1 {
                font-size: 30px !important;
            }

            .section-title {
                font-size: 20px;
                margin-top: 27px;
            }

            .custom-card,
            div[data-testid="stMetric"] {
                min-height: 115px;
            }

            div[data-testid="stHorizontalBlock"] {
                gap: 0.65rem;
            }
        }
        </style>
        """,
        unsafe_allow_html=True
    )


def info_card(label, value):
    st.markdown(
        f"""
        <div class="custom-card">
            <div class="custom-label">{label}</div>
            <div class="custom-value">{value}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


def get_college_code(college_name):
    college_name = str(college_name).strip().lower()

    college_codes = {
        "graphic era": "GE",
        "graphic era university": "GE",
        "chandigarh university": "CU",
        "sharda university": "SU",
        "galgotias university": "GU",
        "amity university": "AU",
        "lovely professional university": "LPU",
        "manav rachna university": "MRU",
        "upes": "UPES",
        "bennett university": "BU",
        "niit university": "NU",
        "vit": "VIT",
        "srm university": "SRM",
        "kiit": "KIIT",
        "bits pilani": "BITS",
        "delhi university": "DU",
        "indraprastha university": "GGSIPU",
        "guru gobind singh indraprastha university": "GGSIPU",
        "thapar university": "TIET",
        "northcap university": "NCU",
        "kr mangalam university": "KRM",
        "gd goenka university": "GDG",
        "SSMRV College": "ssmrv",
        "IMS University Ghaziabad": "ims",
        "Rajagiri College": "RG"
    }

    if college_name in college_codes:
        return college_codes[college_name]

    words = college_name.split()

    if len(words) >= 2:
        return (words[0][0] + words[1][0]).upper()

    return college_name[:2].upper()


def generate_request_id(college_name, business_type, requests_df):
    college_code = get_college_code(college_name)
    business_code = clean_text(business_type).upper()

    prefix = f"{college_code}_{business_code}"

    if requests_df.empty or "request_id" not in requests_df.columns:
        return f"{prefix}_001"

    existing_ids = requests_df["request_id"].astype(str).tolist()

    matching_ids = [
        rid for rid in existing_ids
        if rid.startswith(f"{prefix}_")
    ]

    numbers = []

    for rid in matching_ids:
        try:
            numbers.append(int(rid.split("_")[-1]))
        except:
            pass

    next_number = max(numbers) + 1 if numbers else 1

    return f"{prefix}_{next_number:03d}"


def load_budget_master():
    try:
        df = pd.read_csv(BUDGET_MASTER_FILE, encoding="latin1")

        df.columns = (
            df.columns.astype(str)
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
                "december": "dec"
            },
            inplace=True
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
            "total"
        ] + list(MONTH_MAP.values())

        for col in required_columns:
            if col not in df.columns:
                df[col] = ""

        for month in MONTH_MAP.values():
            df[month] = df[month].apply(safe_number)

        df["total"] = df["total"].apply(safe_number)

        return df.fillna("")

    except:
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


def save_request_to_mysql(new_request):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO requests (
                request_id, created_by, college_name, business_type,
                line_of_business, programme_name, job_code, batch,
                semester, training_hours_from_master, paper_name,
                master_total_cost, request_date, start_date, end_date,
                training_days, training_topic, trainer_name, trainer_type,
                total_hours, rate_per_hour, training_cost,
                local_travel_per_day, local_travel_total,
                outstation_travel_mode, going_travel_cost,
                return_travel_cost, outstation_travel_total,
                total_travel_cost, stay_cost, food_cost,
                additional_cost, total_expected_budget,
                purpose, request_status, created_at
            )
            VALUES (
                %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
                %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
                %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
                %s,%s,%s,%s,%s,%s
            )
            """,
            (
                new_request["request_id"],
                new_request["created_by"],
                new_request["college_name"],
                new_request["business_type"],
                new_request["line_of_business"],
                new_request["programme_name"],
                new_request["job_code"],
                new_request["batch"],
                new_request["semester"],
                new_request["training_hours_from_master"],
                new_request["paper_name"],
                new_request["master_total_cost"],
                new_request["request_date"],
                new_request["start_date"],
                new_request["end_date"],
                new_request["training_days"],
                new_request["training_topic"],
                new_request["trainer_name"],
                new_request["trainer_type"],
                new_request["total_hours"],
                new_request["rate_per_hour"],
                new_request["training_cost"],
                new_request["local_travel_per_day"],
                new_request["local_travel_total"],
                new_request["outstation_travel_mode"],
                new_request["going_travel_cost"],
                new_request["return_travel_cost"],
                new_request["outstation_travel_total"],
                new_request["total_travel_cost"],
                new_request["stay_cost"],
                new_request["food_cost"],
                new_request["additional_cost"],
                new_request["total_expected_budget"],
                new_request["purpose"],
                new_request["request_status"],
                new_request["created_at"],
            )
        )

        conn.commit()
        cursor.close()
        conn.close()

    except:
        pass


def show_create_request(username):

    apply_requester_ui()

    st.title("Create Training Request")

    st.caption(
        "Submit training requirement with budget estimation for approval review."
    )

    try:
        requests_df = pd.read_csv(REQUESTS_FILE)

    except:
        requests_df = pd.DataFrame()

    budget_df = load_budget_master()
    current_date = datetime.now().date()

    st.markdown(
        '<div class="section-title">College Details</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="section-subtitle">
            Select the institution and business category for this request.
        </div>
        """,
        unsafe_allow_html=True
    )

    c1, c2, c3 = st.columns(3)

    with c1:
        college_name = st.selectbox(
            "College / University",
            [
                "Graphic Era",
                "Chandigarh University",
                "Sharda University",
                "Galgotias University",
                "Amity University",
                "UPES",
                "Bennett University",
                "Lovely Professional University",
                "Manav Rachna University",
                "VIT",
                "SRM University",
                "KIIT",
                "BITS Pilani",
                "Delhi University",
                "Indraprastha University",
                "Thapar University",
                "Northcap University",
                "KR Mangalam University",
                "GD Goenka University",
                "SSMRV UNIVERSITY",
                "RAJAGIRI UNIVERSITY",
                "IMS UNIVERSITY GHAZIABAD"
            ]
        )

    with c2:
        business_type = st.selectbox(
            "Business Type",
            ["B2C", "B2I", "B2B"]
        )

    with c3:
        preview_request_id = generate_request_id(
            college_name,
            business_type,
            requests_df
        )

        info_card(
            "Generated Request ID",
            preview_request_id
        )

    st.markdown(
        '<div class="section-title">Program Details</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="section-subtitle">
            These details are fetched from the budget master file.
        </div>
        """,
        unsafe_allow_html=True
    )

    filtered_df = budget_df.copy()

    if "business_type" in filtered_df.columns:
        filtered_df = filtered_df[
            filtered_df["business_type"]
            .astype(str)
            .str.strip() == business_type
        ]

    p1, p2 = st.columns(2)

    with p1:
        line_options = get_unique_values(
            filtered_df,
            "line_of_business"
        )

        line_of_business = st.selectbox(
            "Line of Business",
            line_options if line_options else ["Not Available"]
        )

    if "line_of_business" in filtered_df.columns:
        filtered_df = filtered_df[
            filtered_df["line_of_business"]
            .astype(str)
            .str.strip() == line_of_business
        ]

    with p2:
        programme_options = get_unique_values(
            filtered_df,
            "programme_name"
        )

        programme_name = st.selectbox(
            "Programme Name",
            programme_options
            if programme_options
            else ["Not Available"]
        )

    if "programme_name" in filtered_df.columns:
        filtered_df = filtered_df[
            filtered_df["programme_name"]
            .astype(str)
            .str.strip() == programme_name
        ]

    p3, p4, p5 = st.columns(3)

    with p3:
        job_code_options = get_unique_values(
            filtered_df,
            "job_code"
        )

        job_code = st.selectbox(
            "Job Code",
            job_code_options
            if job_code_options
            else ["Not Available"]
        )

    if "job_code" in filtered_df.columns:
        filtered_df = filtered_df[
            filtered_df["job_code"]
            .astype(str)
            .str.strip() == job_code
        ]

    with p4:
        batch_options = get_unique_values(
            filtered_df,
            "batch"
        )

        batch = st.selectbox(
            "Batch",
            batch_options
            if batch_options
            else ["Not Available"]
        )

    if "batch" in filtered_df.columns:
        filtered_df = filtered_df[
            filtered_df["batch"]
            .astype(str)
            .str.strip() == batch
        ]

    with p5:
        semester_options = get_unique_values(
            filtered_df,
            "semester"
        )

        semester = st.selectbox(
            "Semester",
            semester_options
            if semester_options
            else ["Not Available"]
        )

    if "semester" in filtered_df.columns:
        filtered_df = filtered_df[
            filtered_df["semester"]
            .astype(str)
            .str.strip() == semester
        ]

    selected_master = (
        filtered_df.iloc[0]
        if not filtered_df.empty
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
        else 0
    )

    paper_name = (
        str(
            selected_master.get(
                "paper_name",
                ""
            )
        )
        if len(selected_master)
        else ""
    )

    total_cost_from_master = (
        safe_number(
            selected_master.get(
                "total",
                0
            )
        )
        if len(selected_master)
        else 0
    )

    st.markdown(
        '<div class="section-title">Request Timeline</div>',
        unsafe_allow_html=True
    )

    t1, t2, t3, t4 = st.columns(4)

    with t1:
        st.text_input(
            "Request Date",
            value=str(current_date),
            disabled=True
        )

    with t2:
        start_date = st.date_input(
            "Training Start Date"
        )

    with t3:
        end_date = st.date_input(
            "Training End Date"
        )

    total_training_days = max(
        (end_date - start_date).days + 1,
        1
    )

    with t4:
        st.text_input(
            "Training Days",
            value=str(total_training_days),
            disabled=True
        )

    selected_month_col = MONTH_MAP.get(
        start_date.month,
        ""
    )

    selected_month_name = selected_month_col.upper()

    monthly_budget_from_master = (
        safe_number(
            selected_master.get(
                selected_month_col,
                0
            )
        )
        if len(selected_master)
        and selected_month_col
        else 0
    )

    st.markdown(
        """
        <div class="section-title">
            Auto-Fetched Training & Budget Details
        </div>
        """,
        unsafe_allow_html=True
    )

    m1, m2, m3, m4 = st.columns(4)

    with m1:
        st.metric(
            "Training Hours",
            f"{training_hours_from_master:,.0f}"
        )

    with m2:
        info_card(
            "Paper Name",
            paper_name
            if paper_name
            else "Not Available"
        )

    with m3:
        st.metric(
            f"{selected_month_name} Monthly Budget",
            f"₹{monthly_budget_from_master:,.0f}"
        )

    with m4:
        st.metric(
            "Annual Total",
            f"₹{total_cost_from_master:,.0f}"
        )

    st.markdown(
        '<div class="section-title">Trainer Details</div>',
        unsafe_allow_html=True
    )

    tr1, tr2 = st.columns(2)

    with tr1:
        trainer_name = st.text_input(
            "Trainer Name"
        )

    with tr2:
        trainer_type = st.selectbox(
            "Trainer Type",
            ["Full Time", "Freelancer"]
        )

    purpose = st.text_area(
        "Purpose / Remarks"
    )

    training_topic = programme_name

    st.markdown(
        """
        <div class="section-title">
            Training Budget Details
        </div>
        """,
        unsafe_allow_html=True
    )

    b1, b2, b3 = st.columns(3)

    with b1:
        total_hours = st.number_input(
            "Total Training Hours",
            min_value=1,
            value=(
                int(training_hours_from_master)
                if training_hours_from_master > 0
                else 8
            )
        )

    with b2:
        rate_per_hour = st.number_input(
            "Rate Per Hour (₹)",
            min_value=0,
            value=3000
        )

    training_cost = (
        total_hours * rate_per_hour
    )

    with b3:
        st.metric(
            "Calculated Training Cost",
            f"₹{training_cost:,.0f}"
        )

    st.markdown(
        """
        <div class="section-title">
            Travel Cost Details
        </div>
        """,
        unsafe_allow_html=True
    )

    travel1, travel2, travel3 = st.columns(3)

    with travel1:
        local_travel_per_day = st.number_input(
            "Local Taxi / Daily Travel Cost Per Day (₹)",
            min_value=0,
            value=0
        )

    local_travel_total = (
        local_travel_per_day
        * total_training_days
    )

    with travel2:
        outstation_travel_mode = st.selectbox(
            "Outstation Travel Mode",
            ["Flight", "Train", "Bus", "Car"]
        )

    with travel3:
        st.metric(
            "Local Travel Total",
            f"₹{local_travel_total:,.0f}"
        )

    travel4, travel5, travel6 = st.columns(3)

    with travel4:
        going_travel_cost = st.number_input(
            "Going Travel Cost (₹)",
            min_value=0,
            value=0
        )

    with travel5:
        return_travel_cost = st.number_input(
            "Return Travel Cost (₹)",
            min_value=0,
            value=0
        )

    outstation_travel_total = (
        going_travel_cost
        + return_travel_cost
    )

    total_travel_cost = (
        local_travel_total
        + outstation_travel_total
    )

    with travel6:
        st.metric(
            "Total Travel Cost",
            f"₹{total_travel_cost:,.0f}"
        )

    st.markdown(
        """
        <div class="section-title">
            Additional Requirements Cost
        </div>
        """,
        unsafe_allow_html=True
    )

    a1, a2 = st.columns(2)

    with a1:
        stay_cost = st.number_input(
            "Stay Cost (₹)",
            min_value=0,
            value=0
        )

    with a2:
        food_cost = st.number_input(
            "Food Cost (₹)",
            min_value=0,
            value=0
        )

    additional_cost = (
        stay_cost
        + total_travel_cost
        + food_cost
    )

    total_expected_budget = (
        training_cost
        + additional_cost
    )

    st.markdown(
        '<div class="section-title">Budget Summary</div>',
        unsafe_allow_html=True
    )

    s1, s2, s3, s4 = st.columns(4)

    with s1:
        st.metric(
            "Monthly Budget",
            f"₹{monthly_budget_from_master:,.0f}"
        )

    with s2:
        st.metric(
            "Training Cost",
            f"₹{training_cost:,.0f}"
        )

    with s3:
        st.metric(
            "Additional Cost",
            f"₹{additional_cost:,.0f}"
        )

    with s4:
        st.metric(
            "Total Expected Budget",
            f"₹{total_expected_budget:,.0f}"
        )

    if st.button(
        "Submit Request",
        use_container_width=True
    ):

        request_id = generate_request_id(
            college_name,
            business_type,
            requests_df
        )

        new_request = {
            "request_id": request_id,
            "created_by": username,
            "college_name": college_name,
            "request_date": str(current_date),
            "business_type": business_type,
            "line_of_business": line_of_business,
            "programme_name": programme_name,
            "job_code": job_code,
            "batch": batch,
            "semester": semester,
            "training_hours_from_master": training_hours_from_master,
            "paper_name": paper_name,
            "master_total_cost": total_cost_from_master,
            "monthly_budget": monthly_budget_from_master,
            "budget_month": selected_month_col,
            "start_date": str(start_date),
            "end_date": str(end_date),
            "training_days": total_training_days,
            "training_topic": training_topic,
            "trainer_name": trainer_name,
            "trainer_type": trainer_type,
            "total_hours": total_hours,
            "rate_per_hour": rate_per_hour,
            "training_cost": training_cost,
            "local_travel_per_day": local_travel_per_day,
            "local_travel_total": local_travel_total,
            "outstation_travel_mode": outstation_travel_mode,
            "going_travel_cost": going_travel_cost,
            "return_travel_cost": return_travel_cost,
            "outstation_travel_total": outstation_travel_total,
            "total_travel_cost": total_travel_cost,
            "stay_cost": stay_cost,
            "food_cost": food_cost,
            "additional_cost": additional_cost,
            "total_expected_budget": total_expected_budget,
            "purpose": purpose,
            "request_status": "Pending Mediator Review",
            "created_at": datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )
        }

        requests_df = pd.concat(
            [
                requests_df,
                pd.DataFrame([new_request])
            ],
            ignore_index=True
        )

        requests_df.to_csv(
            REQUESTS_FILE,
            index=False
        )

        email_sent = send_email(
            "Kapil.Arora@in.gt.com",
            "New Training Request Received",
            f"""
Request ID: {request_id}

College: {college_name}

Training Topic: {training_topic}

Please login to review the request.
"""
        )

        if email_sent:
            st.success(
                "Email notification sent to Approver."
            )

        else:
            st.warning(
                "Request saved but email notification failed."
            )

        save_request_to_mysql(
            new_request
        )

        st.success(
            f"Request {request_id} sent successfully!"
        )
