import streamlit as st
import pandas as pd

REQUESTS_FILE = "requests.csv"
INVOICES_FILE = "invoices.csv"


def status_badge(status):
    if status in ["Approved", "Director Approved", "Approve Payment"]:
        return "🟢 Approved"
    elif status in ["Rejected", "Director Rejected", "Reject Invoice"]:
        return "🔴 Rejected"
    elif status in ["Pending Director Approval", "Pending Mediator Review"]:
        return "🟡 Pending"
    else:
        return f"⚪ {status}"


def show_dashboard(role, username):

    st.markdown("## 📊 Dashboard Overview")

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

        if "created_by" in requests_df.columns:
            my_requests = requests_df[
                requests_df["created_by"] == username
            ]
        else:
            my_requests = requests_df

        approved_requests = my_requests[
            my_requests["request_status"].isin(
                ["Approved", "Director Approved"]
            )
        ]

        if not approved_requests.empty:
            st.success(
                "🔔 Notification: Your request has been approved by the Director."
            )
            st.balloons()

        total = len(my_requests)
        pending = len(
            my_requests[
                my_requests["request_status"].isin(
                    ["Pending Mediator Review", "Pending Director Approval"]
                )
            ]
        )
        approved = len(
            my_requests[
                my_requests["request_status"].isin(
                    ["Approved", "Director Approved"]
                )
            ]
        )

        col1, col2, col3 = st.columns(3)

        col1.metric("My Requests", total)
        col2.metric("Pending", pending)
        col3.metric("Approved", approved)

        st.markdown("### My Submitted Requests")

        requester_columns = [
            "request_id",
            "training_date",
            "college_name",
            "training_topic",
            "trainer_requirement",
            "hours",
            "training_days",
            "estimated_budget",
            "stay_required",
            "travel_required",
            "food_required",
            "training_material_required",
            "purpose",
            "request_status",
            "created_at"
        ]

        available_columns = [
            col for col in requester_columns
            if col in my_requests.columns
        ]

        display_df = my_requests[available_columns].copy()

        if "request_status" in display_df.columns:
            display_df["request_status"] = display_df["request_status"].apply(
                status_badge
            )

        st.dataframe(
            display_df,
            use_container_width=True,
            hide_index=True
        )

    # ---------------- OTHER USERS DASHBOARD ---------------- #

    else:

        total_requests = len(requests_df)

        pending_mediator = len(
            requests_df[
                requests_df["request_status"] == "Pending Mediator Review"
            ]
        )

        pending_director = len(
            requests_df[
                requests_df["request_status"] == "Pending Director Approval"
            ]
        )

        approved = len(
            requests_df[
                requests_df["request_status"].isin(
                    ["Approved", "Director Approved"]
                )
            ]
        )

        rejected = len(
            requests_df[
                requests_df["request_status"].isin(
                    ["Rejected", "Director Rejected"]
                )
            ]
        )

        col1, col2, col3, col4, col5 = st.columns(5)

        col1.metric("Total Requests", total_requests)
        col2.metric("Mediator Pending", pending_mediator)
        col3.metric("Director Pending", pending_director)
        col4.metric("Approved", approved)
        col5.metric("Rejected", rejected)

        st.markdown("### Training Requests")

        display_requests = requests_df.copy()

        if "request_status" in display_requests.columns:
            display_requests["request_status"] = display_requests[
                "request_status"
            ].apply(status_badge)

        st.dataframe(
            display_requests,
            use_container_width=True,
            hide_index=True
        )

        st.markdown("### Invoices")

        if invoices_df.empty:
            st.info("No invoices submitted yet.")
        else:
            st.dataframe(
                invoices_df,
                use_container_width=True,
                hide_index=True
            )