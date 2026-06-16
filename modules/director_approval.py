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
            "Start Date",
            "End Date",
            "University",
            "Training Topic",
            "Trainer Name",
            "Total Hours",
            "Training Days",
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

    suggested_budget_per_program = available_budget / number_of_programs

    st.info(
        f"Suggested Budget Per Program: ₹{suggested_budget_per_program:,.0f}"
    )

    st.subheader("Program-wise Budget Allocation")

    program_tabs = st.tabs(
        [
            f"Program {i}"
            for i in range(1, int(number_of_programs) + 1)
        ]
    )

    allocation_rows = []

    for i, tab in enumerate(program_tabs, start=1):

        with tab:

            st.markdown(f"### Program {i} Allocation")

            col1, col2 = st.columns(2)

            with col1:

                program_name = st.text_input(
                    "Program Name",
                    key=f"program_name_{i}"
                )

                trainer_name = st.text_input(
                    "Trainer Name",
                    key=f"trainer_name_{i}"
                )

                trainer_fee = st.number_input(
                    "Trainer Fee",
                    min_value=0,
                    value=0,
                    key=f"trainer_fee_{i}"
                )

            with col2:

                stay_budget = st.number_input(
                    "Stay Budget",
                    min_value=0,
                    value=0,
                    key=f"stay_budget_{i}"
                )

                travel_budget = st.number_input(
                    "Travel Budget",
                    min_value=0,
                    value=0,
                    key=f"travel_budget_{i}"
                )

                food_budget = st.number_input(
                    "Food Budget",
                    min_value=0,
                    value=0,
                    key=f"food_budget_{i}"
                )

                material_budget = st.number_input(
                    "Training Material Budget",
                    min_value=0,
                    value=0,
                    key=f"material_budget_{i}"
                )

                other_budget = st.number_input(
                    "Other Budget",
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

            variance = suggested_budget_per_program - program_total

            if variance >= 0:
                program_status = "Within Suggested Budget"
                st.success(
                    f"Program {i} is within suggested budget. Remaining: ₹{variance:,.0f}"
                )
            else:
                program_status = "Over Suggested Budget"
                st.error(
                    f"Program {i} exceeds suggested budget by ₹{abs(variance):,.0f}"
                )

            allocation_rows.append({
                "Program No.": i,
                "Program Name": program_name,
                "Trainer Name": trainer_name,
                "Trainer Fee": trainer_fee,
                "Stay": stay_budget,
                "Travel": travel_budget,
                "Food": food_budget,
                "Material": material_budget,
                "Other": other_budget,
                "Program Total": program_total,
                "Suggested Budget": suggested_budget_per_program,
                "Variance": variance,
                "Status": program_status
            })

    allocation_df = pd.DataFrame(allocation_rows)

    total_allocated_budget = allocation_df["Program Total"].sum()

    remaining_budget = available_budget - total_allocated_budget

    st.subheader("Final Allocation Summary")

    st.dataframe(
        allocation_df,
        use_container_width=True,
        hide_index=True
    )

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Available Budget",
        f"₹{available_budget:,.0f}"
    )

    col2.metric(
        "Total Allocated",
        f"₹{total_allocated_budget:,.0f}"
    )

    col3.metric(
        "Remaining / Loss",
        f"₹{remaining_budget:,.0f}"
    )

    if remaining_budget >= 0:
        allocation_status = "Profitable / Within Budget"
        st.success(
            f"Overall allocation is profitable. Remaining budget: ₹{remaining_budget:,.0f}"
        )
    else:
        allocation_status = "Loss / Over Budget"
        st.error(
            f"Overall allocation exceeds budget. Loss: ₹{abs(remaining_budget):,.0f}"
        )

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
        requests_df.loc[index, "suggested_budget_per_program"] = suggested_budget_per_program
        requests_df.loc[index, "total_allocated_budget"] = total_allocated_budget
        requests_df.loc[index, "remaining_budget"] = remaining_budget
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