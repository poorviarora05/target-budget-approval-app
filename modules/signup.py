import streamlit as st
from db import get_connection


def show_signup():
    st.header("User Signup")

    name = st.text_input("Full Name")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    role = st.selectbox(
        "Select Role",
        ["Requester", "Approver", "Partner", "Trainer"]
    )

    if st.button("Create Account"):
        if not name or not email or not password:
            st.error("Please fill all fields.")
            return

        try:
            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute(
                """
                INSERT INTO users (name, email, password, role)
                VALUES (%s, %s, %s, %s)
                """,
                (name, email, password, role)
            )

            conn.commit()
            cursor.close()
            conn.close()

            st.success("Account created successfully.")

        except Exception as e:
            st.error(f"Signup failed: {e}")