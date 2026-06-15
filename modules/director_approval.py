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
        requests_df["request_status"] == "Pending Director Approval"
    ]

    # ---------------- POPUP NOTIFICATION ---------------- #

    if not pending_requests.empty:

        @st.dialog("🔔 New Approval Request")
        def show_notification():

            st.write(
                f"{len(pending_requests)} request(s) received from Mediator for approval."
            )

        show_notification()

    if pending_requests.empty:
        st.info("No requests pending for Director.")
        return

    # ---------------- SELECT REQUEST ---------------- #

    request_id = st.selectbox(
        "Select Request",
        pending_requests["request_id"]
    )

    selected_request = pending_requests[
        pending_requests["request_id"] == request_id
    ].iloc[0]

    # ---------------- TABLE VIEW ---------------- #

    st.subheader(
        "Request Details Received from Mediator"
    )

    director_table = pd.DataFrame({

        "Field": [
            "Training Date",
            "College Name",
            "Training Topic",
            "Trainer Requirement",
            "Hours Per Day",
            "Training Days",
            "Estimated Budget by Requester",
            "University Budget",
            "Trainer Cost",
            "Stay Cost",
            "Travel Cost",
            "Food Cost",
            "Training Material Cost",
            "Other Cost",
            "Total Estimated Cost",
            "Budget Status",
            "Mediator Remarks"
        ],

        "Details": [
            selected_request.get("training_date", ""),
            selected_request.get("college_name", ""),
            selected_request.get("training_topic", ""),
            selected_request.get("trainer_requirement", ""),
            selected_request.get("hours", ""),
            selected_request.get("training_days", 1),
            selected_request.get("estimated_budget", 0),
            selected_request.get("university_budget", 0),
            selected_request.get("trainer_cost", 0),
            selected_request.get("stay_cost", 0),
            selected_request.get("travel_cost", 0),
            selected_request.get("food_cost", 0),
            selected_request.get("training_material_cost", 0),
            selected_request.get("other_cost", 0),
            selected_request.get("total_estimated_cost", 0),
            selected_request.get("budget_status", ""),
            selected_request.get("mediator_remarks", "")
        ]
    })

    st.table(director_table)

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

    # ---------------- SUBMIT ---------------- #

    if st.button("Submit Director Decision"):

        index = requests_df[
            requests_df["request_id"] == request_id
        ].index[0]

        # FIX DATATYPE ISSUE

        if "director_remarks" not in requests_df.columns:

            requests_df["director_remarks"] = ""

        requests_df["director_remarks"] = (
            requests_df["director_remarks"]
            .astype(str)
        )

        requests_df.at[
            index,
            "director_remarks"
        ] = str(director_remarks)

        # STATUS UPDATE

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

        # SAVE

        requests_df.to_csv(
            REQUESTS_FILE,
            index=False
        )