import streamlit as st
import pandas as pd

REQUESTS_FILE = "requests.csv"
INVOICES_FILE = "invoices.csv"


def status_badge(status):

    if status in ["Approved", "Partner Approved"]:
        return "🟢 Approved"

    elif status in ["Rejected", "Partner Rejected"]:
        return "🔴 Rejected"

    elif status == "Pending Mediator Review":
        return "🟡 Pending Approver"

    elif status == "Pending Director Approval":
        return "🟠 Pending Partner"

    elif status == "Sent Back to Requester":
        return "🔵 Sent Back"

    else:
        return f"⚪ {status}"


def show_timeline(status):

    steps = [
        "Requester",
        "Approver",
        "Partner",
        "Invoice"
    ]

    if status == "Pending Mediator Review":
        completed = 1

    elif status == "Pending Director Approval":
        completed = 2

    elif status in ["Approved", "Partner Approved"]:
        completed = 3

    elif status in ["Invoice Submitted", "Pending Director Invoice Approval"]:
        completed = 4

    elif status in ["Rejected", "Partner Rejected"]:
        completed = 0

    else:
        completed = 1

    timeline_text = ""

    for i, step in enumerate(steps, start=1):

        if i <= completed:
            timeline_text += f"✅ {step}"

        else:
            timeline_text += f"⏳ {step}"

        if i != len(steps):
            timeline_text += "  →  "

    st.write(timeline_text)


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

    if role == "Requester":

        if "created_by" in requests_df.columns:
            my_requests = requests_df[
                requests_df["created_by"] == username
            ]
        else:
            my_requests = requests_df

        total = len(my_requests)

        pending = len(
            my_requests[
                my_requests["request_status"].isin(
                    [
                        "Pending Mediator Review",
                        "Pending Director Approval"
                    ]
                )
            ]
        )

        approved = len(
            my_requests[
                my_requests["request_status"].isin(
                    [
                        "Approved",
                        "Partner Approved"
                    ]
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
            "request_date",
            "start_date",
            "end_date",
            "college_name",
            "training_topic",
            "trainer_name",
            "total_hours",
            "training_days",
            "estimated_budget",
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

        st.markdown("### Approval Timeline")

        for _, row in my_requests.iterrows():
            st.write(f"**Request ID:** {row.get('request_id', '')}")
            show_timeline(row.get("request_status", ""))

    else:

        total_requests = len(requests_df)

        pending_approver = len(
            requests_df[
                requests_df["request_status"] == "Pending Mediator Review"
            ]
        )

        pending_partner = len(
            requests_df[
                requests_df["request_status"] == "Pending Director Approval"
            ]
        )

        approved = len(
            requests_df[
                requests_df["request_status"].isin(
                    [
                        "Approved",
                        "Partner Approved"
                    ]
                )
            ]
        )

        rejected = len(
            requests_df[
                requests_df["request_status"].isin(
                    [
                        "Rejected",
                        "Partner Rejected"
                    ]
                )
            ]
        )

        col1, col2, col3, col4, col5 = st.columns(5)

        col1.metric("Total Requests", total_requests)
        col2.metric("Pending Approver", pending_approver)
        col3.metric("Pending Partner", pending_partner)
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

        st.markdown("### Approval Timeline")

        for _, row in requests_df.iterrows():
            st.write(f"**Request ID:** {row.get('request_id', '')}")
            show_timeline(row.get("request_status", ""))

        st.markdown("### Invoices")

        if invoices_df.empty:
            st.info("No invoices submitted yet.")
        else:
            st.dataframe(
                invoices_df,
                use_container_width=True,
                hide_index=True
            )