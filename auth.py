import streamlit as st
from textwrap import dedent

from db import get_connection


def init_session():
    default_values = {
        "logged_in": False,
        "username": None,
        "email": None,
        "role": None
    }

    for key, value in default_values.items():
        if key not in st.session_state:
            st.session_state[key] = value


def apply_auth_ui():
    st.markdown(
        dedent(
            """
            <style>
            [data-testid="stAppViewContainer"] {
                background:
                    radial-gradient(
                        circle at top left,
                        rgba(99, 102, 241, 0.18),
                        transparent 32%
                    ),
                    radial-gradient(
                        circle at bottom right,
                        rgba(168, 85, 247, 0.18),
                        transparent 32%
                    ),
                    linear-gradient(
                        135deg,
                        #f8fafc 0%,
                        #eef2ff 50%,
                        #fdf2f8 100%
                    );
            }

            [data-testid="stHeader"] {
                background: transparent;
            }

            .block-container {
                padding-top: 4rem;
                padding-bottom: 3rem;
                max-width: 620px;
            }

            .portal-card {
                background: rgba(255, 255, 255, 0.90);
                backdrop-filter: blur(18px);
                border: 1px solid rgba(226, 232, 240, 0.95);
                border-radius: 28px;
                padding: 30px 34px;
                box-shadow: 0 30px 80px rgba(15, 23, 42, 0.14);
                margin-bottom: 18px;
            }

            .auth-logo {
                width: 66px;
                height: 66px;
                border-radius: 22px;
                background: linear-gradient(135deg, #4f46e5, #9333ea);
                display: flex;
                align-items: center;
                justify-content: center;
                color: #ffffff;
                font-size: 32px;
                font-weight: 900;
                margin: 0 auto 17px auto;
                box-shadow: 0 18px 38px rgba(79, 70, 229, 0.32);
            }

            .auth-title {
                text-align: center;
                font-size: 32px;
                line-height: 1.2;
                font-weight: 900;
                color: #0f172a;
                margin-bottom: 8px;
                letter-spacing: -0.04em;
            }

            .auth-subtitle {
                text-align: center;
                font-size: 14px;
                line-height: 1.6;
                color: #64748b;
                font-weight: 600;
                margin-bottom: 0;
            }

            div[data-testid="stTabs"] {
                background: rgba(255, 255, 255, 0.86);
                border: 1px solid rgba(226, 232, 240, 0.95);
                border-radius: 20px;
                padding: 10px 16px 18px;
                box-shadow: 0 18px 45px rgba(15, 23, 42, 0.08);
            }

            div[data-testid="stTabs"] [data-baseweb="tab-list"] {
                border-bottom: 1px solid #e2e8f0;
                gap: 6px;
            }

            div[data-testid="stTabs"] button {
                color: #64748b;
                font-weight: 800;
                font-size: 14px;
            }

            div[data-testid="stTabs"] button[aria-selected="true"] {
                color: #4f46e5 !important;
                font-weight: 900;
            }

            div[data-testid="stTabs"] [data-baseweb="tab-highlight"] {
                background-color: #4f46e5 !important;
                height: 3px;
                border-radius: 999px;
            }

            label {
                color: #334155 !important;
                font-weight: 800 !important;
                font-size: 13px !important;
            }

            div[data-testid="stTextInput"] input {
                min-height: 50px;
                border-radius: 15px !important;
                border: 1px solid #dbe3ef !important;
                background: #ffffff !important;
                color: #111827 !important;
                font-size: 14px;
                font-weight: 650;
                box-shadow: 0 8px 20px rgba(15, 23, 42, 0.04);
            }

            div[data-testid="stTextInput"] input:focus {
                border-color: #818cf8 !important;
                box-shadow:
                    0 0 0 3px rgba(99, 102, 241, 0.13) !important;
            }

            div[data-baseweb="select"] > div {
                min-height: 50px;
                border-radius: 15px;
                border: 1px solid #dbe3ef;
                background: #ffffff;
                color: #111827;
                box-shadow: 0 8px 20px rgba(15, 23, 42, 0.04);
            }

            div[data-testid="stButton"] button {
                width: 100%;
                min-height: 50px;
                margin-top: 8px;
                border: none !important;
                border-radius: 15px !important;
                background:
                    linear-gradient(
                        135deg,
                        #4f46e5,
                        #9333ea
                    ) !important;
                color: #ffffff !important;
                font-size: 15px;
                font-weight: 900 !important;
                box-shadow: 0 18px 38px rgba(79, 70, 229, 0.30);
                transition:
                    transform 0.16s ease,
                    box-shadow 0.16s ease;
            }

            div[data-testid="stButton"] button:hover {
                background:
                    linear-gradient(
                        135deg,
                        #4338ca,
                        #7e22ce
                    ) !important;
                color: #ffffff !important;
                transform: translateY(-1px);
                box-shadow: 0 22px 44px rgba(79, 70, 229, 0.38);
            }

            div[data-testid="stButton"] button p,
            div[data-testid="stButton"] button span {
                color: #ffffff !important;
                font-weight: 900 !important;
                opacity: 1 !important;
                visibility: visible !important;
                margin: 0 !important;
            }

            div[data-testid="stAlert"] {
                border-radius: 15px;
            }

            @media (max-width: 700px) {
                .block-container {
                    padding-top: 2rem;
                    padding-left: 1rem;
                    padding-right: 1rem;
                }

                .portal-card {
                    padding: 25px 20px;
                    border-radius: 23px;
                }

                .auth-title {
                    font-size: 27px;
                }
            }
            </style>
            """
        ),
        unsafe_allow_html=True
    )


def signup_form():
    name = st.text_input(
        "Full Name",
        key="signup_name"
    )

    email = st.text_input(
        "Email",
        key="signup_email"
    )

    password = st.text_input(
        "Password",
        type="password",
        key="signup_password"
    )

    role = st.selectbox(
        "Select Role",
        [
            "Requester",
            "Approver",
            "Partner",
            "Trainer"
        ],
        key="signup_role"
    )

    if st.button(
        "Create Account",
        key="create_account_btn",
        use_container_width=True
    ):
        name = name.strip()
        email = email.strip()
        password = password.strip()

        if not name or not email or not password:
            st.error("Please fill all fields.")
            return

        conn = None
        cursor = None

        try:
            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute(
                """
                SELECT email
                FROM users
                WHERE email = %s
                """,
                (email,)
            )

            existing_user = cursor.fetchone()

            if existing_user:
                st.warning("An account with this email already exists.")
                return

            cursor.execute(
                """
                INSERT INTO users (
                    name,
                    email,
                    password,
                    role
                )
                VALUES (%s, %s, %s, %s)
                """,
                (
                    name,
                    email,
                    password,
                    role
                )
            )

            conn.commit()

            st.success(
                "Account created successfully. Please sign in now."
            )

        except Exception as e:
            if conn:
                conn.rollback()

            st.error(f"Signup failed: {e}")

        finally:
            if cursor:
                cursor.close()

            if conn:
                conn.close()


def login_page():
    apply_auth_ui()

    # IMPORTANT:
    # No blank lines or indentation inside this HTML string.
    # Otherwise Streamlit may display nested HTML as a code block.
    login_header_html = (
        '<div class="portal-card">'
        '<div class="auth-logo">₹</div>'
        '<div class="auth-title">Trainer Budget Portal</div>'
        '<div class="auth-subtitle">'
        'Manage training requests, approvals, budgets and invoices '
        'through one secure workspace.'
        '</div>'
        '</div>'
    )

    st.markdown(
        login_header_html,
        unsafe_allow_html=True
    )

    sign_in_tab, sign_up_tab = st.tabs(
        [
            "Sign In",
            "Sign Up"
        ]
    )

    with sign_in_tab:
        email = st.text_input(
            "Email",
            key="login_email"
        )

        password = st.text_input(
            "Password",
            type="password",
            key="login_password"
        )

        if st.button(
            "Sign In",
            key="sign_in_btn",
            use_container_width=True
        ):
            email = email.strip()
            password = password.strip()

            if not email or not password:
                st.error("Please enter your email and password.")
                return

            conn = None
            cursor = None

            try:
                conn = get_connection()
                cursor = conn.cursor()

                cursor.execute(
                    """
                    SELECT name, email, role
                    FROM users
                    WHERE email = %s
                    AND password = %s
                    """,
                    (
                        email,
                        password
                    )
                )

                user = cursor.fetchone()

                if user:
                    user_name = user[0]
                    user_email = user[1]
                    user_role = user[2]

                    st.session_state.logged_in = True
                    st.session_state.username = user_name or user_email
                    st.session_state.email = user_email
                    st.session_state.role = user_role

                    st.rerun()

                else:
                    st.error("Invalid email or password.")

            except Exception as e:
                st.error(f"Login failed: {e}")

            finally:
                if cursor:
                    cursor.close()

                if conn:
                    conn.close()

    with sign_up_tab:
        signup_form()


def logout_button():
    st.sidebar.markdown("---")

    if st.sidebar.button(
        "Logout",
        key="logout_btn",
        use_container_width=True
    ):
        st.session_state.logged_in = False
        st.session_state.username = None
        st.session_state.email = None
        st.session_state.role = None

        st.rerun()