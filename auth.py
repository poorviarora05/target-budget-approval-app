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
            return pd.DataFrame(columns=["username", "password", "role", "email"])
    return pd.DataFrame(columns=["username", "password", "role", "email"])


def save_users(users_df):
    users_df.to_csv(USERS_FILE, index=False)


def login_page():
    st.markdown("""
    <style>
    .portal-title {
        font-size: 48px;
        font-weight: 800;
        text-align: center;
        color: #111827;
        margin-top: 20px;
    }
    .portal-subtitle {
        text-align: center;
        color: #6B7280;
        font-size: 17px;
        margin-bottom: 35px;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="portal-title">Trainer Budget Approval System</div>
    <div class="portal-subtitle">
        Enterprise workflow portal for requests, budget approvals and invoices.
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 1.5, 1])

    with col2:
        tab1, tab2 = st.tabs(["Sign In", "Sign Up"])

        with tab1:
            st.subheader("Sign In")

            role = st.selectbox(
                "Continue As",
                ["Requester", "Mediator", "Director", "Trainer"],
                key="signin_role"
            )

            username = st.text_input("Username", key="login_username")
            password = st.text_input("Password", type="password", key="login_password")

            if st.button("Login", use_container_width=True):
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
                    st.error("Invalid credentials or incorrect role.")

        with tab2:
            st.subheader("Sign Up")

            role = st.selectbox(
                "Register As",
                ["Requester", "Mediator", "Director", "Trainer"],
                key="signup_role"
            )

            new_username = st.text_input("Create Username")
            new_email = st.text_input("Email")
            new_password = st.text_input("Create Password", type="password")

            if st.button("Create Account", use_container_width=True):
                users_df = load_users()

                if new_username in users_df["username"].values:
                    st.error("Username already exists")
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
                    st.success(f"{role} account created successfully. Please sign in.")


def logout_button():
    st.sidebar.markdown("---")
    st.sidebar.write(f"Logged in as: {st.session_state.role}")

    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.username = None
        st.session_state.role = None
        st.rerun()