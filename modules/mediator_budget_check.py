import streamlit as st
import pandas as pd

REQUESTS_FILE = "requests.csv"
INTERNAL_APP_BUDGET = 25000


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

    st.subheader("Requester Details")

    st.write("College Name:", selected_request["college_name"])

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
        selected_request["hours"]
    )

    st.write(
        "Training Days:",
        selected_request.get("training_days", 1)
    )

    st.write(
        "Estimated Budget:",
        selected_request.get("estimated_budget", 0)
    )

    st.subheader("Internal Budget")

    st.write(
        "Available Internal Budget:",
        INTERNAL_APP_BUDGET
    )

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

    st.subheader("Budget Comparison")

    st.write(
        "Trainer Cost:",
        trainer_cost
    )

    st.write(
        "Total Estimated Cost:",
        total_estimated_cost
    )

    difference = (
        INTERNAL_APP_BUDGET
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