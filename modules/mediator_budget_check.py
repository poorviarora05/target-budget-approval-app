import streamlit as st
import pandas as pd

REQUESTS_FILE = "requests.csv"

# Internal company/app budget
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

    # ---------------- REQUEST DETAILS ---------------- #

    st.subheader("Requester Details")

    st.write("College Name:", selected_request["college_name"])
    st.write("Training Topic:", selected_request["training_topic"])
    st.write("Trainer Requirement:", selected_request["trainer_requirement"])
    st.write("Hours:", selected_request["hours"])

    st.write("Stay Required:", selected_request["stay_required"])
    st.write("Travel Required:", selected_request["travel_required"])
    st.write("Food Required:", selected_request["food_required"])

    st.write(
        "Training Material Required:",
        selected_request["training_material_required"]
    )

    st.write("Other Requirements:", selected_request["other_requirements"])
    st.write("Purpose:", selected_request["purpose"])

    # ---------------- BUDGET COMPARISON ---------------- #

    requester_budget = selected_request["requester_budget"]

    st.subheader("Budget Comparison")

    st.write("Requester Estimated Budget:", requester_budget)

    st.write(
        "Available Internal Budget:",
        INTERNAL_APP_BUDGET
    )

    if requester_budget <= INTERNAL_APP_BUDGET:

        st.success(
            "Requester budget is within our available budget."
        )

        budget_comparison_status = "Requester Budget Accepted"

    else:

        st.error(
            "Requester budget is higher than our available budget."
        )

        budget_comparison_status = "Requester Budget Exceeded"

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

    trainer_cost = rate_per_hour * int(selected_request["hours"])

    total_estimated_cost = (
        trainer_cost
        + stay_cost
        + travel_cost
        + food_cost
        + training_material_cost
        + other_cost
    )

    st.subheader("Calculated Cost")

    st.write("Trainer Cost:", trainer_cost)

    st.write(
        "Total Estimated Cost:",
        total_estimated_cost
    )

    # ---------------- FINAL BUDGET CHECK ---------------- #

    if (
        requester_budget <= INTERNAL_APP_BUDGET
        and total_estimated_cost <= INTERNAL_APP_BUDGET
    ):

        st.success(
            "Final budget approved."
        )

        budget_status = "Budget Approved"

    else:

        st.error(
            "Budget problem detected."
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

        requests_df.loc[index, "rate_per_hour"] = rate_per_hour

        requests_df.loc[index, "trainer_cost"] = trainer_cost

        requests_df.loc[index, "stay_cost"] = stay_cost

        requests_df.loc[index, "travel_cost"] = travel_cost

        requests_df.loc[index, "food_cost"] = food_cost

        requests_df.loc[
            index,
            "training_material_cost"
        ] = training_material_cost

        requests_df.loc[index, "other_cost"] = other_cost

        requests_df.loc[
            index,
            "internal_app_budget"
        ] = INTERNAL_APP_BUDGET

        requests_df.loc[
            index,
            "budget_status"
        ] = budget_status

        requests_df.loc[
            index,
            "budget_comparison_status"
        ] = budget_comparison_status

        requests_df.loc[
            index,
            "total_estimated_cost"
        ] = total_estimated_cost

                requests_df["mediator_remarks"] = requests_df[
            "mediator_remarks"
        ].astype("object")

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