import streamlit as st
import pandas as pd

REQUESTS_FILE = "requests.csv"
INVOICES_FILE = "invoices.csv"


def show_dashboard(role, username):

    st.header("Dashboard")

    try:
        requests_df = pd.read_csv(REQUESTS_FILE)

    except:
        requests_df = pd.DataFrame()

    try:
        invoices_df = pd.read_csv(INVOICES_FILE)

    except:
        invoices_df = pd.DataFrame()

    if requests_df.empty:
        st.info("No requests found yet.")
        return

    # ---------------- REQUESTER DASHBOARD ---------------- #

    if role == "Requester":

        st.subheader("My Submitted Requests")

        if "created_by" in requests_df.columns:
            my_requests = requests_df[
                requests_df["created_by"] == username
            ]

        else:
            my_requests = requests_df

        approved_requests = my_requests[
            my_requests["request_status"] == "Director Approved"
        ]

        if not approved_requests.empty:

            st.success(
                "Notification: Your request has been approved by the Director."
            )

            st.balloons()

        requester_columns = [
            "request_id",
            "college_name",
            "training_topic",
            "trainer_requirement",
            "hours",
            "stay_required",
            "travel_required",
            "food_required",
            "training_material_required",
            "other_requirements",
            "purpose",
            "request_status",
            "created_at"
        ]

        available_columns = [
            col for col in requester_columns
            if col in my_requests.columns
        ]

        st.dataframe(
            my_requests[available_columns],
            use_container_width=True
        )

    # ---------------- OTHER USERS DASHBOARD ---------------- #

    else:

        st.subheader("All Training Requests")

        st.dataframe(
            requests_df,
            use_container_width=True
        )

        st.subheader("All Invoices")

        st.dataframe(
            invoices_df,
            use_container_width=True
        )

        st.metric(
            "Total Requests",
            len(requests_df)
        )