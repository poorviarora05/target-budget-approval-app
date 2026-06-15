import streamlit as st
import pandas as pd
import os

USERS_FILE = "users_data.csv"


def init_session():

    if "logged_in" not in st.session_state:

        st.session_state.logged_in = False
        st.session_state.username = None
        st.session_state.role = None


def load_users():

    if os.path.exists(USERS_FILE):

        try:
            return pd.read_csv(USERS_FILE)

        except:
            return pd.DataFrame(
                columns=[
                    "username",
                    "password",
                    "role",
                    "email"
                ]
            )

    else:

        return pd.DataFrame(
            columns=[
                "username",
                "password",
                "role",
                "email"
            ]
        )


def save_users(users_df):

    users_df.to_csv(
        USERS_FILE,
        index=False
    )


def login_page():

    st.markdown(
        """
        <style>

        .portal-title {
            font-size: 52px;
            font-weight: 800;
            text-align: center;
            color: #111827;
            margin-top: 20px;
        }

        .portal-subtitle {
            text-align: center;
            color: #6B7280;
            font-size: 18px;
            margin-bottom: 40px;
        }

        .login-card {
            background: white;
            padding: 28px;
            border-radius: 22px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.08);
            margin-top: 20px;
        }

        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="portal-title">
            Trainer Budget Approval System
        </div>

        <div class="portal-subtitle">
            Enterprise workflow portal for training requests,
            budget approvals and invoice management.
        </div>
        """,
        unsafe_allow_html=True
    )

    # ---------------- CENTER ROLE SELECT ---------------- #

    col1, col2, col3 = st.columns([1,2,1])

    with col2:

        role = st.selectbox(
            "Continue As",
            [
                "Requester",
                "Mediator",
                "Director",
                "Trainer"
            ]
        )

    tab1, tab2 = st.tabs(
        [
            "Sign In",
            "Sign Up"
        ]
    )

    # ---------------- SIGN IN ---------------- #

    with tab1:

        col1, col2, col3 = st.columns([1,2,1])

        with col2:

            st.markdown(
                f"""
                <div class="login-card">
                <h3>{role} Login</h3>
                </div>
                """,
                unsafe_allow_html=True
            )

            username = st.text_input(
                "Username",
                key="login_username"
            )

            password = st.text_input(
                "Password",
                type="password",
                key="login_password"
            )

            if st.button("Login"):

                users_df = load_users()

                user = users_df[
                    (users_df["username"] == username)
                    & (users_df["password"] == password)
                    & (users_df["role"] == role)
                ]

                if not user.empty:

                    st.session_state.logged_in = True
                    st.session_state.username = username
                    st.session_state.role = role

                    st.rerun()

                else:

                    st.error(
                        "Invalid credentials or incorrect role."
                    )

    # ---------------- SIGN UP ---------------- #

    with tab2:

        col1, col2, col3 = st.columns([1,2,1])

        with col2:

            st.markdown(
                f"""
                <div class="login-card">
                <h3>{role} Registration</h3>
                </div>
                """,
                unsafe_allow_html=True
            )

            new_username = st.text_input(
                "Create Username"
            )

            new_email = st.text_input(
                "Email"
            )

            new_password = st.text_input(
                "Create Password",
                type="password"
            )

            if st.button("Create Account"):

                users_df = load_users()

                if new_username in users_df["username"].values:

                    st.error(
                        "Username already exists"
                    )

                else:

                    new_user = {
                        "username": new_username,
                        "password": new_password,
                        "role": role,
                        "email": new_email
                    }

                    users_df = pd.concat(
                        [users_df, pd.DataFrame([new_user])],
                        ignore_index=True
                    )

                    save_users(users_df)

                    st.success(
                        f"{role} account created successfully."
                    )


def logout_button():

    st.sidebar.markdown("---")

    st.sidebar.write(
        f"Logged in as: {st.session_state.role}"
    )

    if st.sidebar.button("Logout"):

        st.session_state.logged_in = False
        st.session_state.username = None
        st.session_state.role = None

        st.rerun()