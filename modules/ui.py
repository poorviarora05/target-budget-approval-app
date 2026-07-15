import streamlit as st
from textwrap import dedent


def apply_global_ui():
    st.markdown(
        dedent(
            """
            <style>
            :root {
                --primary: #4f46e5;
                --primary-dark: #4338ca;
                --secondary: #7c3aed;
                --background: #f6f7fb;
                --surface: #ffffff;
                --surface-soft: #f8fafc;
                --text-main: #0f172a;
                --text-secondary: #64748b;
                --border: #e2e8f0;
                --success: #15803d;
                --warning: #b45309;
                --danger: #b91c1c;
            }

            /* =========================================
               GLOBAL APP
            ========================================= */

            html,
            body,
            [class*="css"] {
                font-family:
                    Inter,
                    -apple-system,
                    BlinkMacSystemFont,
                    "Segoe UI",
                    sans-serif;
            }

            .stApp {
                background:
                    radial-gradient(
                        circle at top right,
                        rgba(79, 70, 229, 0.06),
                        transparent 24%
                    ),
                    var(--background);
                color: var(--text-main);
            }

            [data-testid="stAppViewContainer"] {
                background: transparent;
            }

            [data-testid="stHeader"] {
                background: transparent;
            }

            .block-container {
                max-width: 1450px;
                padding-top: 2rem;
                padding-bottom: 3rem;
                padding-left: 2.2rem;
                padding-right: 2.2rem;
            }

            h1 {
                color: var(--text-main);
                font-size: 32px !important;
                line-height: 1.2;
                font-weight: 900 !important;
                letter-spacing: -0.035em;
            }

            h2 {
                color: var(--text-main);
                font-size: 24px !important;
                font-weight: 850 !important;
                letter-spacing: -0.025em;
            }

            h3 {
                color: var(--text-main);
                font-size: 19px !important;
                font-weight: 800 !important;
            }

            h4 {
                color: #1e293b;
                font-weight: 800 !important;
            }

            p {
                color: #475569;
            }

            hr {
                border: none;
                border-top: 1px solid var(--border);
                margin: 18px 0;
            }

            /* =========================================
               SIDEBAR
            ========================================= */

            section[data-testid="stSidebar"] {
                background:
                    linear-gradient(
                        180deg,
                        #111827 0%,
                        #1e1b4b 52%,
                        #312e81 100%
                    );
                border-right: none;
                box-shadow: 8px 0 28px rgba(15, 23, 42, 0.12);
            }

            section[data-testid="stSidebar"] > div {
                padding-top: 1rem;
            }

            section[data-testid="stSidebar"] h1,
            section[data-testid="stSidebar"] h2,
            section[data-testid="stSidebar"] h3,
            section[data-testid="stSidebar"] h4,
            section[data-testid="stSidebar"] p,
            section[data-testid="stSidebar"] label {
                color: #f8fafc !important;
            }

            section[data-testid="stSidebar"] hr {
                border-color: rgba(255, 255, 255, 0.15);
                margin: 16px 0;
            }

            section[data-testid="stSidebar"] div[role="radiogroup"] {
                gap: 7px;
            }

            section[data-testid="stSidebar"]
            div[role="radiogroup"] label {
                background: transparent;
                border: 1px solid transparent;
                border-radius: 13px;
                padding: 10px 12px;
                transition: all 0.18s ease;
            }

            section[data-testid="stSidebar"]
            div[role="radiogroup"] label:hover {
                background: rgba(255, 255, 255, 0.10);
                border-color: rgba(255, 255, 255, 0.12);
            }

            section[data-testid="stSidebar"]
            div[role="radiogroup"] label:has(input:checked) {
                background: rgba(255, 255, 255, 0.16);
                border-color: rgba(255, 255, 255, 0.18);
                box-shadow: 0 8px 20px rgba(15, 23, 42, 0.18);
            }

            section[data-testid="stSidebar"]
            div[role="radiogroup"] label p {
                color: #f8fafc !important;
                font-weight: 750 !important;
                font-size: 14px !important;
            }

            /* =========================================
               BUTTONS
            ========================================= */

            div[data-testid="stButton"] button {
                width: 100%;
                min-height: 44px;
                border: none !important;
                border-radius: 12px !important;
                background:
                    linear-gradient(
                        135deg,
                        var(--primary),
                        var(--secondary)
                    ) !important;
                color: #ffffff !important;
                font-size: 14px !important;
                font-weight: 800 !important;
                box-shadow: 0 8px 20px rgba(79, 70, 229, 0.20);
                transition:
                    transform 0.16s ease,
                    box-shadow 0.16s ease,
                    background 0.16s ease;
                opacity: 1 !important;
            }

            div[data-testid="stButton"] button:hover {
                background:
                    linear-gradient(
                        135deg,
                        var(--primary-dark),
                        #6d28d9
                    ) !important;
                color: #ffffff !important;
                transform: translateY(-1px);
                box-shadow: 0 12px 25px rgba(79, 70, 229, 0.28);
            }

            div[data-testid="stButton"] button:active {
                transform: translateY(0);
            }

            div[data-testid="stButton"] button p,
            div[data-testid="stButton"] button span {
                color: #ffffff !important;
                font-weight: 800 !important;
                opacity: 1 !important;
                visibility: visible !important;
                margin: 0 !important;
            }

            section[data-testid="stSidebar"]
            div[data-testid="stButton"] button {
                background:
                    linear-gradient(
                        135deg,
                        #4f46e5,
                        #7c3aed
                    ) !important;
                color: #ffffff !important;
                min-height: 46px;
                border: 1px solid rgba(255, 255, 255, 0.16) !important;
                box-shadow: 0 10px 22px rgba(15, 23, 42, 0.25);
            }

            section[data-testid="stSidebar"]
            div[data-testid="stButton"] button:hover {
                background:
                    linear-gradient(
                        135deg,
                        #4338ca,
                        #6d28d9
                    ) !important;
            }

            section[data-testid="stSidebar"]
            div[data-testid="stButton"] button p,
            section[data-testid="stSidebar"]
            div[data-testid="stButton"] button span {
                color: #ffffff !important;
                opacity: 1 !important;
                visibility: visible !important;
            }

            /* =========================================
               FORM INPUTS
            ========================================= */

            label {
                color: #334155 !important;
                font-size: 13px !important;
                font-weight: 750 !important;
            }

            div[data-testid="stTextInput"] input,
            div[data-testid="stNumberInput"] input,
            div[data-testid="stDateInput"] input,
            div[data-testid="stTextArea"] textarea {
                background: #ffffff !important;
                color: #0f172a !important;
                border: 1px solid #dbe3ef !important;
                border-radius: 12px !important;
                min-height: 44px;
                box-shadow: 0 4px 12px rgba(15, 23, 42, 0.035);
                font-size: 14px;
            }

            div[data-testid="stTextInput"] input:focus,
            div[data-testid="stNumberInput"] input:focus,
            div[data-testid="stDateInput"] input:focus,
            div[data-testid="stTextArea"] textarea:focus {
                border-color: #818cf8 !important;
                box-shadow:
                    0 0 0 3px rgba(99, 102, 241, 0.13) !important;
            }

            div[data-baseweb="select"] > div {
                background: #ffffff !important;
                color: #0f172a !important;
                border: 1px solid #dbe3ef !important;
                border-radius: 12px !important;
                min-height: 44px;
                box-shadow: 0 4px 12px rgba(15, 23, 42, 0.035);
            }

            div[data-baseweb="select"] > div:hover {
                border-color: #a5b4fc !important;
            }

            div[data-testid="stCheckbox"] label,
            div[data-testid="stRadio"] label {
                font-weight: 650 !important;
            }

            /* =========================================
               METRICS
            ========================================= */

            div[data-testid="stMetric"] {
                background:
                    linear-gradient(
                        180deg,
                        #ffffff 0%,
                        #fbfcff 100%
                    );
                border: 1px solid var(--border);
                padding: 16px 17px;
                border-radius: 16px;
                box-shadow: 0 8px 22px rgba(15, 23, 42, 0.055);
                min-height: 110px;
            }

            div[data-testid="stMetricLabel"] {
                color: var(--text-secondary) !important;
                font-size: 12px !important;
                font-weight: 750 !important;
            }

            div[data-testid="stMetricValue"] {
                color: var(--text-main) !important;
                font-size: 23px !important;
                font-weight: 900 !important;
                letter-spacing: -0.025em;
            }

            div[data-testid="stMetricDelta"] {
                font-weight: 700 !important;
            }

            /* =========================================
               TABS
            ========================================= */

            div[data-testid="stTabs"] {
                background: #ffffff;
                border: 1px solid var(--border);
                border-radius: 16px;
                padding: 8px 12px 14px;
                box-shadow: 0 8px 22px rgba(15, 23, 42, 0.045);
            }

            div[data-testid="stTabs"] [data-baseweb="tab-list"] {
                gap: 4px;
                border-bottom: 1px solid #e2e8f0;
            }

            div[data-testid="stTabs"] button {
                color: #64748b;
                font-size: 13px;
                font-weight: 750;
                padding-left: 13px;
                padding-right: 13px;
            }

            div[data-testid="stTabs"]
            button[aria-selected="true"] {
                color: var(--primary) !important;
                font-weight: 850 !important;
            }

            div[data-testid="stTabs"]
            [data-baseweb="tab-highlight"] {
                background-color: var(--primary) !important;
                height: 3px;
                border-radius: 999px;
            }

            /* =========================================
               EXPANDERS
            ========================================= */

            div[data-testid="stExpander"] {
                background: #ffffff;
                border: 1px solid var(--border);
                border-radius: 14px;
                box-shadow: 0 7px 20px rgba(15, 23, 42, 0.04);
                overflow: hidden;
            }

            div[data-testid="stExpander"] details summary {
                font-weight: 800;
                color: #1e293b;
                padding-top: 4px;
                padding-bottom: 4px;
            }

            /* =========================================
               TABLES
            ========================================= */

            div[data-testid="stDataFrame"],
            div[data-testid="stTable"],
            .stTable {
                background: #ffffff;
                border: 1px solid var(--border);
                border-radius: 14px;
                overflow: hidden;
                box-shadow: 0 7px 20px rgba(15, 23, 42, 0.04);
            }

            div[data-testid="stDataFrame"] {
                padding: 2px;
            }

            /* =========================================
               ALERTS
            ========================================= */

            div[data-testid="stAlert"] {
                border-radius: 13px;
                border-width: 1px;
                padding: 12px 14px;
            }

            div[data-testid="stAlert"] p {
                font-weight: 650;
            }

            /* =========================================
               PROGRESS BAR
            ========================================= */

            div[data-testid="stProgress"] > div {
                background: #e2e8f0;
                border-radius: 999px;
            }

            div[data-testid="stProgress"] > div > div {
                border-radius: 999px;
                height: 10px;
            }

            /* =========================================
               CUSTOM CLASSES
            ========================================= */

            .professional-card {
                background: #ffffff;
                border: 1px solid var(--border);
                border-radius: 17px;
                padding: 20px;
                box-shadow: 0 8px 22px rgba(15, 23, 42, 0.05);
                margin-bottom: 16px;
            }

            .page-title {
                color: var(--text-main);
                font-size: 31px;
                font-weight: 900;
                letter-spacing: -0.035em;
                margin-bottom: 4px;
            }

            .page-subtitle {
                color: var(--text-secondary);
                font-size: 14px;
                font-weight: 550;
                margin-top: 0;
                margin-bottom: 20px;
            }

            .section-card {
                background: #ffffff;
                border: 1px solid var(--border);
                border-radius: 16px;
                padding: 18px;
                box-shadow: 0 8px 22px rgba(15, 23, 42, 0.045);
                margin-bottom: 16px;
            }

            .muted-text {
                color: var(--text-secondary);
                font-size: 13px;
            }

            /* =========================================
               RESPONSIVE
            ========================================= */

            @media (max-width: 900px) {
                .block-container {
                    padding-left: 1rem;
                    padding-right: 1rem;
                    padding-top: 1.2rem;
                }

                h1 {
                    font-size: 27px !important;
                }

                div[data-testid="stMetric"] {
                    min-height: 96px;
                }
            }
            </style>
            """
        ),
        unsafe_allow_html=True
    )