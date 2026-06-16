import streamlit as st
import pandas as pd

REQUESTS_FILE = "requests.csv"


def show_mediator_budget_check():

    st.header("Approver Review")

    try:
        requests_df = pd.read_csv(REQUESTS_FILE)
    except:
        st.error("No requests found.")
        return

    pending_requests = requests_df[
        requests_df["request_status"] == "Pending Mediator Review"
    ]

    if pending_requests.empty:
        st.info("No requests pending for Approver.")
        return

    request_id = st.selectbox(
        "Select Request",
        pending_requests["request_id"]
    )

    selected_request = pending_requests[
        pending_requests["request_id"] == request_id
    ].iloc[0]

    st.subheader("Request Details")

    request_table = pd.DataFrame({
        "Field": [
            "Request Date",
            "Training Start Date",
            "Training End Date",
            "College / University",
            "Training Topic",
            "Trainer Name",
            "Total Hours",
            "Training Days",
            "Rate Per Hour",
            "Estimated Budget",
            "Purpose / Remarks"
        ],
        "Details": [
            selected_request.get("request_date", ""),
            selected_request.get("start_date", ""),
            selected_request.get("end_date", ""),
            selected_request.get("college_name", ""),
            selected_request.get("training_topic", ""),
            selected_request.get("trainer_name", ""),
            selected_request.get("total_hours", ""),
            selected_request.get("training_days", ""),
            selected_request.get("rate_per_hour", ""),
            selected_request.get("estimated_budget", ""),
            selected_request.get("purpose", "")
        ]
    })

    st.table(request_table)

    st.subheader("Approver Decision")

    approver_remarks = st.text_area("Approver Remarks")

    decision = st.selectbox(
        "Decision",
        [
            "Approve and Send to Director",
            "Send Back to Requester"
        ]
    )

    if st.button("Submit Decision"):

        index = requests_df[
            requests_df["request_id"] == request_id
        ].index[0]

        if "approver_remarks" not in requests_df.columns:
            requests_df["approver_remarks"] = ""

        requests_df["approver_remarks"] = (
            requests_df["approver_remarks"]
            .astype(str)
        )

        requests_df.at[index, "approver_remarks"] = str(approver_remarks)

        if decision == "Approve and Send to Director":
            requests_df.loc[index, "request_status"] = "Pending Director Approval"
        else:
            requests_df.loc[index, "request_status"] = "Sent Back to Requester"

        requests_df.to_csv(
            REQUESTS_FILE,
            index=False
        )

        st.success("Approver decision submitted successfully.")