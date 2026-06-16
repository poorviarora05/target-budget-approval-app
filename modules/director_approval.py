import streamlit as st
import pandas as pd

REQUESTS_FILE = "requests.csv"


def show_director_approval():

    st.header("Partner Approval & Budget Allocation")

    try:
        requests_df = pd.read_csv(REQUESTS_FILE)
    except:
        st.error("No requests found.")
        return

    pending_requests = requests_df[
        requests_df["request_status"] == "Pending Director Approval"
    ]

    if pending_requests.empty:
        st.info("No requests pending for Partner approval.")
        return

    request_id = st.selectbox(
        "Select Request",
        pending_requests["request_id"]
    )

    selected_request = pending_requests[
        pending_requests["request_id"] == request_id
    ].iloc[0]

    st.subheader("Request Details Received from Approver")

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
            "Estimated Request Budget",
            "Approver Remarks"
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
            selected_request.get("estimated_budget", 0),
            selected_request.get("approver_remarks", "")
        ]
    })

    st.table(request_table)

    st.subheader("Partner Budget Allocation")

    university_budget = st.number_input(
        "Total Budget Available for this University",
        min_value=0,
        value=100000
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

    estimated_budget = float(selected_request.get("estimated_budget", 0))

    budget_per_program = university_budget / number_of_programs
    budget_per_trainer = university_budget / number_of_trainers
    remaining_budget = university_budget - estimated_budget

    if remaining_budget >= 0:
        profitability_status = "Profitable / Within Budget"
    else:
        profitability_status = "Loss / Over Budget"

    st.subheader("Budget Comparison")

    comparison_table = pd.DataFrame({
        "Particulars": [
            "University Budget",
            "Number of Programs",
            "Number of Trainers",
            "Suggested Budget Per Program",
            "Suggested Budget Per Trainer",
            "Estimated Request Budget",
            "Remaining / Loss Amount",
            "Profitability Status"
        ],
        "Value": [
            f"₹{university_budget:,.0f}",
            number_of_programs,
            number_of_trainers,
            f"₹{budget_per_program:,.0f}",
            f"₹{budget_per_trainer:,.0f}",
            f"₹{estimated_budget:,.0f}",
            f"₹{remaining_budget:,.0f}",
            profitability_status
        ]
    })

    st.table(comparison_table)

    if remaining_budget >= 0:
        st.success(
            f"Within budget. Remaining budget: ₹{remaining_budget:,.0f}"
        )
    else:
        st.error(
            f"Budget exceeded. Loss amount: ₹{abs(remaining_budget):,.0f}"
        )

    st.subheader("Partner Decision")

    partner_remarks = st.text_area("Partner Remarks")

    decision = st.selectbox(
        "Decision",
        ["Approve", "Reject"]
    )

    if st.button("Submit Partner Decision"):

        index = requests_df[
            requests_df["request_id"] == request_id
        ].index[0]

        requests_df.loc[index, "university_budget"] = university_budget
        requests_df.loc[index, "number_of_programs"] = number_of_programs
        requests_df.loc[index, "number_of_trainers"] = number_of_trainers
        requests_df.loc[index, "budget_per_program"] = budget_per_program
        requests_df.loc[index, "budget_per_trainer"] = budget_per_trainer
        requests_df.loc[index, "remaining_budget"] = remaining_budget
        requests_df.loc[index, "profitability_status"] = profitability_status

        if "partner_remarks" not in requests_df.columns:
            requests_df["partner_remarks"] = ""

        requests_df["partner_remarks"] = requests_df["partner_remarks"].astype(str)
        requests_df.at[index, "partner_remarks"] = str(partner_remarks)

        if decision == "Approve":
            requests_df.loc[index, "request_status"] = "Approved"
            st.success("Partner approved the request successfully.")
        else:
            requests_df.loc[index, "request_status"] = "Rejected"
            st.error("Partner rejected the request.")

        requests_df.to_csv(
            REQUESTS_FILE,
            index=False
        )