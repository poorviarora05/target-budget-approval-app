import streamlit as st
import pandas as pd

REQUESTS_FILE = "requests.csv"


def show_director_approval():

    st.header("Director Approval")

    try:

        requests_df = pd.read_csv(REQUESTS_FILE)

    except:

        st.error("No requests found.")
        return

    pending_requests = requests_df[
        requests_df["request_status"]
        == "Pending Director Approval"
    ]

    # ---------------- DIALOG NOTIFICATION ---------------- #

    if not pending_requests.empty:

        @st.dialog("🔔 New Approval Request")
        def show_notification():

            st.write(
                f"{len(pending_requests)} request(s) received from Mediator for approval."
            )

        show_notification()

    # ---------------- NO REQUESTS ---------------- #

    if pending_requests.empty:

        st.info("No requests pending for Director.")
        return

    # ---------------- REQUEST SELECTION ---------------- #

    request_id = st.selectbox(
        "Select Request",
        pending_requests["request_id"]
    )

    selected_request = pending_requests[
        pending_requests["request_id"] == request_id
    ].iloc[0]

    # ---------------- REQUEST DETAILS ---------------- #

    st.subheader("Request Details")

    st.write(
        "College Name:",
        selected_request["college_name"]
    )

    st.write(
        "Training Topic:",
        selected_request["training_topic"]
    )

    st.write(
        "Trainer Requirement:",
        selected_request["trainer_requirement"]
    )

    st.write(
        "Hours:",
        selected_request.get("hours", 0)
    )

    st.write(
        "Training Days:",
        selected_request.get("training_days", 1)
    )

    st.write(
        "Estimated Budget:",
        selected_request.get(
            "estimated_budget",
            0
        )
    )

    st.write(
        "Total Estimated Cost:",
        selected_request.get(
            "total_estimated_cost",
            0
        )
    )

    st.write(
        "Mediator Remarks:",
        selected_request.get(
            "mediator_remarks",
            ""
        )
    )

    # ---------------- DECISION ---------------- #

    decision = st.selectbox(
        "Director Decision",
        [
            "Approve",
            "Reject"
        ]
    )

    director_remarks = st.text_area(
        "Director Remarks"
    )

    if st.button("Submit Director Decision"):

        index = requests_df[
            requests_df["request_id"] == request_id
        ].index[0]

        requests_df.loc[
            index,
            "director_remarks"
        ] = director_remarks

        if decision == "Approve":

            requests_df.loc[
                index,
                "request_status"
            ] = "Approved"

            st.success(
                "Request approved successfully."
            )

        else:

            requests_df.loc[
                index,
                "request_status"
            ] = "Rejected"

            st.error(
                "Request rejected."
            )

        requests_df.to_csv(
            REQUESTS_FILE,
            index=False
        )