import streamlit as st
import pandas as pd

REQUESTS_FILE = "requests.csv"


def show_director_approval():

    st.header("Partner Approval & Smart Budget Allocation")

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

    available_budget = st.number_input(
        "Available Budget for this University",
        min_value=0,
        value=100000
    )

    number_of_programs = st.number_input(
        "Number of Programs",
        min_value=1,
        value=1
    )

    number_of_trainers = st.number_input(
        "Number of Trainers",
        min_value=1,
        value=1
    )

    estimated_budget = float(
        selected_request.get("estimated_budget", 0)
    )

    budget_per_program = available_budget / number_of_programs
    budget_per_trainer = available_budget / number_of_trainers
    remaining_budget = available_budget - estimated_budget

    if remaining_budget >= 0:
        profitability_status = "Profitable / Within Budget"
    else:
        profitability_status = "Loss / Over Budget"

    st.subheader("Smart Budget Optimizer")

    optimizer_table = pd.DataFrame({
        "Budget Parameter": [
            "Available University Budget",
            "Number of Programs",
            "Number of Trainers",
            "Suggested Budget Per Program",
            "Suggested Budget Per Trainer",
            "Estimated Request Budget",
            "Remaining / Loss Amount",
            "Profitability Status"
        ],
        "Value": [
            f"₹{available_budget:,.0f}",
            number_of_programs,
            number_of_trainers,
            f"₹{budget_per_program:,.0f}",
            f"₹{budget_per_trainer:,.0f}",
            f"₹{estimated_budget:,.0f}",
            f"₹{remaining_budget:,.0f}",
            profitability_status
        ]
    })

    st.table(optimizer_table)

    if remaining_budget >= 0:
        st.success(
            f"Within budget. Remaining amount: ₹{remaining_budget:,.0f}"
        )
    else:
        st.error(
            f"Budget exceeded. Loss amount: ₹{abs(remaining_budget):,.0f}"
        )

    st.subheader("Program-wise Allocation")

    allocation_rows = []

    for i in range(1, int(number_of_programs) + 1):

        st.markdown(f"### Program {i}")

        program_name = st.text_input(
            f"Program {i} Name",
            key=f"program_name_{i}"
        )

        trainer_name = st.text_input(
            f"Trainer {i} Name",
            key=f"trainer_name_{i}"
        )

        allocated_budget = st.number_input(
            f"Allocated Budget for Program {i}",
            min_value=0,
            value=int(budget_per_program),
            key=f"allocated_budget_{i}"
        )

        allocation_rows.append({
            "Program": program_name,
            "Trainer": trainer_name,
            "Allocated Budget": allocated_budget
        })

    allocation_df = pd.DataFrame(allocation_rows)

    total_allocated_budget = allocation_df["Allocated Budget"].sum()

    st.subheader("Allocation Summary")

    st.table(allocation_df)

    st.write(
        f"Total Allocated Budget: ₹{total_allocated_budget:,.0f}"
    )

    if total_allocated_budget <= available_budget:
        st.success("Allocation is within available budget.")
        allocation_status = "Balanced Allocation"
    else:
        st.error("Allocation exceeds available budget.")
        allocation_status = "Over Allocation"

    st.subheader("Partner Decision")

    partner_remarks = st.text_area("Partner Remarks")

    decision = st.selectbox(
        "Decision",
        [
            "Approve",
            "Reject"
        ]
    )

    if st.button("Submit Partner Decision"):

        index = requests_df[
            requests_df["request_id"] == request_id
        ].index[0]

        requests_df.loc[index, "available_budget"] = available_budget
        requests_df.loc[index, "number_of_programs"] = number_of_programs
        requests_df.loc[index, "number_of_trainers"] = number_of_trainers
        requests_df.loc[index, "budget_per_program"] = budget_per_program
        requests_df.loc[index, "budget_per_trainer"] = budget_per_trainer
        requests_df.loc[index, "remaining_budget"] = remaining_budget
        requests_df.loc[index, "profitability_status"] = profitability_status
        requests_df.loc[index, "total_allocated_budget"] = total_allocated_budget
        requests_df.loc[index, "allocation_status"] = allocation_status

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