import streamlit as st
import pandas as pd

REQUESTS_FILE = "requests.csv"


def show_mediator_budget_check():

    st.header("Approver Budget Allocation")

    try:
        requests_df = pd.read_csv(REQUESTS_FILE)

    except:
        st.error("No requests found.")
        return

    pending_requests = requests_df[
        requests_df["request_status"] == "Pending Mediator Review"
    ]

    if pending_requests.empty:
        st.info("No pending requests.")
        return

    request_id = st.selectbox(
        "Select Request",
        pending_requests["request_id"]
    )

    selected_request = pending_requests[
        pending_requests["request_id"] == request_id
    ].iloc[0]

    # ---------------- REQUEST DETAILS ---------------- #

    st.subheader("Training Request Details")

    details_table = pd.DataFrame({

        "Field": [
            "Request Date",
            "Training Start Date",
            "Training End Date",
            "College Name",
            "Training Topic",
            "Trainer Name",
            "Total Hours",
            "Training Days",
            "Estimated Budget"
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
            selected_request.get("estimated_budget", 0)
        ]
    })

    st.table(details_table)

    # ---------------- UNIVERSITY BUDGET ---------------- #

    st.subheader("University Budget Allocation")

    university_budget = st.number_input(
        "Enter Total Budget Available for this University/College",
        min_value=0,
        value=200000
    )

    number_of_programs = st.number_input(
        "Total Number of Programs",
        min_value=1,
        value=1
    )

    number_of_trainers = st.number_input(
        "Total Number of Trainers",
        min_value=1,
        value=1
    )

    suggested_budget_per_program = (
        university_budget / number_of_programs
    )

    suggested_budget_per_trainer = (
        university_budget / number_of_trainers
    )

    st.info(
        f"Suggested Budget Per Program: ₹{suggested_budget_per_program:,.0f}"
    )

    st.info(
        f"Suggested Budget Per Trainer: ₹{suggested_budget_per_trainer:,.0f}"
    )

    estimated_budget = selected_request.get(
        "estimated_budget",
        0
    )

    remaining_budget = (
        university_budget - estimated_budget
    )

    st.subheader("Budget Analysis")

    st.write(
        f"Estimated Request Budget: ₹{estimated_budget:,.0f}"
    )

    st.write(
        f"Remaining Budget After Allocation: ₹{remaining_budget:,.0f}"
    )

    if estimated_budget <= suggested_budget_per_program:

        st.success(
            "Budget allocation is balanced."
        )

        fairness_status = "Balanced Allocation"

    else:

        st.warning(
            "Budget exceeds suggested allocation."
        )

        fairness_status = "Over Allocation"

    # ---------------- APPROVER REMARKS ---------------- #

    approver_remarks = st.text_area(
        "Approver Remarks"
    )

    decision = st.selectbox(
        "Decision",
        [
            "Approve and Send to Director",
            "Send Back for Revision"
        ]
    )

    # ---------------- SUBMIT ---------------- #

    if st.button("Submit Decision"):

        index = requests_df[
            requests_df["request_id"] == request_id
        ].index[0]

        requests_df.loc[
            index,
            "university_budget"
        ] = university_budget

        requests_df.loc[
            index,
            "number_of_programs"
        ] = number_of_programs

        requests_df.loc[
            index,
            "number_of_trainers"
        ] = number_of_trainers

        requests_df.loc[
            index,
            "suggested_budget_per_program"
        ] = suggested_budget_per_program

        requests_df.loc[
            index,
            "suggested_budget_per_trainer"
        ] = suggested_budget_per_trainer

        requests_df.loc[
            index,
            "remaining_budget"
        ] = remaining_budget

        requests_df.loc[
            index,
            "fairness_status"
        ] = fairness_status

        if "approver_remarks" not in requests_df.columns:
            requests_df["approver_remarks"] = ""

        requests_df["approver_remarks"] = (
            requests_df["approver_remarks"]
            .astype(str)
        )

        requests_df.at[
            index,
            "approver_remarks"
        ] = str(approver_remarks)

        if decision == "Approve and Send to Director":

            requests_df.loc[
                index,
                "request_status"
            ] = "Pending Director Approval"

        else:

            requests_df.loc[
                index,
                "request_status"
            ] = "Sent Back for Revision"

        requests_df.to_csv(
            REQUESTS_FILE,
            index=False
        )

        st.success(
            "Budget allocation submitted successfully."
        )