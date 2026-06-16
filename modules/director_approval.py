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

    st.subheader("Partner Budget Setup")

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

    st.subheader("Smart Budget Optimizer")

    optimizer_table = pd.DataFrame({
        "Budget Parameter": [
            "Available University Budget",
            "Number of Programs",
            "Number of Trainers",
            "Suggested Budget Per Program",
            "Suggested Budget Per Trainer",
            "Estimated Request Budget"
        ],
        "Value": [
            f"₹{available_budget:,.0f}",
            number_of_programs,
            number_of_trainers,
            f"₹{budget_per_program:,.0f}",
            f"₹{budget_per_trainer:,.0f}",
            f"₹{estimated_budget:,.0f}"
        ]
    })

    st.table(optimizer_table)

    st.subheader("Program-wise Requirement & Budget Allocation")

    allocation_rows = []

    for i in range(1, int(number_of_programs) + 1):

        st.markdown(f"### Program {i}")

        col1, col2 = st.columns(2)

        with col1:
            program_name = st.text_input(
                f"Program {i} Name",
                key=f"program_name_{i}"
            )

            trainer_name = st.text_input(
                f"Trainer {i} Name",
                key=f"trainer_name_{i}"
            )

            trainer_fee = st.number_input(
                f"Trainer Fee - Program {i}",
                min_value=0,
                value=0,
                key=f"trainer_fee_{i}"
            )

        with col2:
            stay_budget = st.number_input(
                f"Stay Budget - Program {i}",
                min_value=0,
                value=0,
                key=f"stay_budget_{i}"
            )

            travel_budget = st.number_input(
                f"Travel Budget - Program {i}",
                min_value=0,
                value=0,
                key=f"travel_budget_{i}"
            )

            food_budget = st.number_input(
                f"Food Budget - Program {i}",
                min_value=0,
                value=0,
                key=f"food_budget_{i}"
            )

            material_budget = st.number_input(
                f"Material Budget - Program {i}",
                min_value=0,
                value=0,
                key=f"material_budget_{i}"
            )

            other_budget = st.number_input(
                f"Other Budget - Program {i}",
                min_value=0,
                value=0,
                key=f"other_budget_{i}"
            )

        program_total = (
            trainer_fee
            + stay_budget
            + travel_budget
            + food_budget
            + material_budget
            + other_budget
        )

        st.info(
            f"Total Budget for Program {i}: ₹{program_total:,.0f}"
        )

        allocation_rows.append({
            "Program": program_name,
            "Trainer": trainer_name,
            "Trainer Fee": trainer_fee,
            "Stay": stay_budget,
            "Travel": travel_budget,
            "Food": food_budget,
            "Material": material_budget,
            "Other": other_budget,
            "Program Total": program_total
        })

    allocation_df = pd.DataFrame(allocation_rows)

    total_allocated_budget = allocation_df["Program Total"].sum()

    st.subheader("Allocation Summary")

    st.table(allocation_df)

    st.write(
        f"Total Allocated Budget: ₹{total_allocated_budget:,.0f}"
    )

    final_remaining_budget = available_budget - total_allocated_budget

    if final_remaining_budget >= 0:
        st.success(
            f"Allocation is within budget. Remaining: ₹{final_remaining_budget:,.0f}"
        )
        allocation_status = "Profitable / Within Budget"
    else:
        st.error(
            f"Allocation exceeds budget. Loss: ₹{abs(final_remaining_budget):,.0f}"
        )
        allocation_status = "Loss / Over Budget"

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
        requests_df.loc[index, "total_allocated_budget"] = total_allocated_budget
        requests_df.loc[index, "final_remaining_budget"] = final_remaining_budget
        requests_df.loc[index, "allocation_status"] = allocation_status

        if "partner_remarks" not in requests_df.columns:
            requests_df["partner_remarks"] = ""

        requests_df["partner_remarks"] = requests_df[
            "partner_remarks"
        ].astype(str)

        requests_df.at[
            index,
            "partner_remarks"
        ] = str(partner_remarks)

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