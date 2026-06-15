import streamlit as st
import pandas as pd

REQUESTS_FILE = "requests.csv"


def show_mediator_budget_check():

    st.header("Mediator Budget Check")

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

    # ---------------- REQUESTER DETAILS TABLE ---------------- #

    st.subheader("Requester Details")

    requester_data = pd.DataFrame({

        "Field": [
            "Training Date",
            "College Name",
            "Training Topic",
            "Trainer Requirement",
            "Hours Per Day",
            "Training Days",
            "Estimated Budget",
            "Stay Required",
            "Travel Required",
            "Food Required",
            "Training Material Required",
            "Other Requirements",
            "Purpose"
        ],

        "Details": [
            selected_request.get("training_date", ""),
            selected_request.get("college_name", ""),
            selected_request.get("training_topic", ""),
            selected_request.get("trainer_requirement", ""),
            selected_request.get("hours", ""),
            selected_request.get("training_days", 1),
            selected_request.get("estimated_budget", 0),
            selected_request.get("stay_required", ""),
            selected_request.get("travel_required", ""),
            selected_request.get("food_required", ""),
            selected_request.get("training_material_required", ""),
            selected_request.get("other_requirements", ""),
            selected_request.get("purpose", "")
        ]
    })

    st.table(requester_data)

    # ---------------- UNIVERSITY BUDGET ---------------- #

    st.subheader("University / College Budget")

    university_budget = st.number_input(
        "Enter Budget Available for this University/College",
        min_value=0,
        value=25000
    )

    # ---------------- COST DETAILS ---------------- #

    st.subheader("Expense Calculation")

    rate_per_hour = st.number_input(
        "Rate Per Hour",
        min_value=0,
        value=3000
    )

    stay_cost = st.number_input(
        "Stay Cost",
        min_value=0,
        value=0
    )

    travel_cost = st.number_input(
        "Travel Cost",
        min_value=0,
        value=0
    )

    food_cost = st.number_input(
        "Food Cost",
        min_value=0,
        value=0
    )

    training_material_cost = st.number_input(
        "Training Material Cost",
        min_value=0,
        value=0
    )

    other_cost = st.number_input(
        "Other Expense Cost",
        min_value=0,
        value=0
    )

    training_days_value = selected_request.get(
        "training_days",
        1
    )

    if pd.isna(training_days_value):
        training_days_value = 1

    training_days_value = int(training_days_value)

    trainer_cost = (
        rate_per_hour
        * int(selected_request["hours"])
        * training_days_value
    )

    total_estimated_cost = (
        trainer_cost
        + stay_cost
        + travel_cost
        + food_cost
        + training_material_cost
        + other_cost
    )

    # ---------------- BUDGET COMPARISON ---------------- #

    st.subheader("Budget Comparison")

    comparison_df = pd.DataFrame({

        "Category": [
            "University Budget",
            "Trainer Cost",
            "Total Estimated Cost",
            "Remaining Budget"
        ],

        "Amount": [
            university_budget,
            trainer_cost,
            total_estimated_cost,
            university_budget - total_estimated_cost
        ]
    })

    st.table(comparison_df)

    difference = (
        university_budget
        - total_estimated_cost
    )

    if difference >= 0:

        st.success(
            f"Within budget. Remaining budget: ₹{difference}"
        )

        budget_status = "Budget Approved"

    else:

        st.error(
            f"Budget exceeded by ₹{abs(difference)}"
        )

        budget_status = "Budget Problem"

    # ---------------- DECISION ---------------- #

    mediator_remarks = st.text_area(
        "Mediator Remarks"
    )

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

        requests_df.loc[
            index,
            "university_budget"
        ] = university_budget

        requests_df.loc[
            index,
            "rate_per_hour"
        ] = rate_per_hour

        requests_df.loc[
            index,
            "trainer_cost"
        ] = trainer_cost

        requests_df.loc[
            index,
            "stay_cost"
        ] = stay_cost

        requests_df.loc[
            index,
            "travel_cost"
        ] = travel_cost

        requests_df.loc[
            index,
            "food_cost"
        ] = food_cost

        requests_df.loc[
            index,
            "training_material_cost"
        ] = training_material_cost

        requests_df.loc[
            index,
            "other_cost"
        ] = other_cost

        requests_df.loc[
            index,
            "budget_status"
        ] = budget_status

        requests_df.loc[
            index,
            "total_estimated_cost"
        ] = total_estimated_cost

        if "mediator_remarks" not in requests_df.columns:

            requests_df["mediator_remarks"] = ""

        requests_df["mediator_remarks"] = (
            requests_df["mediator_remarks"]
            .astype(str)
        )

        requests_df.at[
            index,
            "mediator_remarks"
        ] = str(mediator_remarks)

        if decision == "Approve and Send to Director":

            requests_df.loc[
                index,
                "request_status"
            ] = "Pending Director Approval"

        else:

            requests_df.loc[
                index,
                "request_status"
            ] = "Sent Back to Requester"

        requests_df.to_csv(
            REQUESTS_FILE,
            index=False
        )

        st.success(
            "Decision submitted successfully."
        )