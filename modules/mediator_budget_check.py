import streamlit as st
import pandas as pd

REQUESTS_FILE = "requests.csv"


def show_mediator_budget_check():

    st.header("Approver Cost Estimation")

    try:
        requests_df = pd.read_csv(REQUESTS_FILE)
    except:
        st.error("No requests found.")
        return

    pending_requests = requests_df[
        requests_df["request_status"] == "Pending Mediator Review"
    ]

    if pending_requests.empty:
        st.info("No requests pending for Approver.")
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
            "Purpose / Remarks"
        ],
        "Details": [
            selected_request.get("request_date", ""),
            selected_request.get("start_date", ""),
            selected_request.get("end_date", ""),
            selected_request.get("college_name", ""),
            selected_request.get("training_topic", ""),
            selected_request.get("trainer_name", ""),
            selected_request.get("purpose", "")
        ]
    })

    st.table(request_table)

    st.subheader("Training Duration")

    training_days = st.number_input(
        "Total Training Days",
        min_value=1,
        value=int(selected_request.get("training_days", 1))
    )

    hours_per_day = st.number_input(
        "Hours Per Day",
        min_value=1,
        value=6
    )

    total_hours = training_days * hours_per_day

    st.info(f"Total Program Hours: {total_hours}")

    st.subheader("Approver Cost Calculation")

    rate_per_hour = st.number_input(
        "Trainer Rate Per Hour",
        min_value=0,
        value=3000
    )

    trainer_cost = total_hours * rate_per_hour

    st.markdown("### Per Day Requirement Cost")

    stay_per_day = st.number_input("Stay Cost Per Day", min_value=0, value=0)
    travel_per_day = st.number_input("Travel Cost Per Day", min_value=0, value=0)
    food_per_day = st.number_input("Food Cost Per Day", min_value=0, value=0)
    material_per_day = st.number_input("Training Material Cost Per Day", min_value=0, value=0)
    other_per_day = st.number_input("Other Cost Per Day", min_value=0, value=0)

    stay_total = stay_per_day * training_days
    travel_total = travel_per_day * training_days
    food_total = food_per_day * training_days
    material_total = material_per_day * training_days
    other_total = other_per_day * training_days

    estimated_budget = (
        trainer_cost
        + stay_total
        + travel_total
        + food_total
        + material_total
        + other_total
    )

    st.subheader("Complete Cost Breakdown")

    cost_table = pd.DataFrame({
        "Cost Component": [
            "Trainer Fee",
            "Stay Cost",
            "Travel Cost",
            "Food Cost",
            "Training Material Cost",
            "Other Cost",
            "Total Estimated Budget"
        ],
        "Per Day / Rate": [
            f"₹{rate_per_hour:,.0f} per hour",
            f"₹{stay_per_day:,.0f}",
            f"₹{travel_per_day:,.0f}",
            f"₹{food_per_day:,.0f}",
            f"₹{material_per_day:,.0f}",
            f"₹{other_per_day:,.0f}",
            "-"
        ],
        "Days / Hours": [
            f"{total_hours} hours",
            f"{training_days} days",
            f"{training_days} days",
            f"{training_days} days",
            f"{training_days} days",
            f"{training_days} days",
            "-"
        ],
        "Total Amount": [
            f"₹{trainer_cost:,.0f}",
            f"₹{stay_total:,.0f}",
            f"₹{travel_total:,.0f}",
            f"₹{food_total:,.0f}",
            f"₹{material_total:,.0f}",
            f"₹{other_total:,.0f}",
            f"₹{estimated_budget:,.0f}"
        ]
    })

    st.table(cost_table)

    st.subheader("Approver Decision")

    approver_remarks = st.text_area("Approver Remarks")

    decision = st.selectbox(
        "Decision",
        [
            "Approve and Send to Partner",
            "Send Back to Requester"
        ]
    )

    if st.button("Submit Approver Decision"):

        index = requests_df[
            requests_df["request_id"] == request_id
        ].index[0]

        requests_df.loc[index, "training_days"] = training_days
        requests_df.loc[index, "hours_per_day"] = hours_per_day
        requests_df.loc[index, "total_hours"] = total_hours
        requests_df.loc[index, "rate_per_hour"] = rate_per_hour
        requests_df.loc[index, "trainer_cost"] = trainer_cost

        requests_df.loc[index, "stay_per_day"] = stay_per_day
        requests_df.loc[index, "travel_per_day"] = travel_per_day
        requests_df.loc[index, "food_per_day"] = food_per_day
        requests_df.loc[index, "material_per_day"] = material_per_day
        requests_df.loc[index, "other_per_day"] = other_per_day

        requests_df.loc[index, "stay_total"] = stay_total
        requests_df.loc[index, "travel_total"] = travel_total
        requests_df.loc[index, "food_total"] = food_total
        requests_df.loc[index, "material_total"] = material_total
        requests_df.loc[index, "other_total"] = other_total

        requests_df.loc[index, "estimated_budget"] = estimated_budget

        if "approver_remarks" not in requests_df.columns:
            requests_df["approver_remarks"] = ""

        requests_df["approver_remarks"] = requests_df["approver_remarks"].astype(str)
        requests_df.at[index, "approver_remarks"] = str(approver_remarks)

        if decision == "Approve and Send to Partner":
            requests_df.loc[index, "request_status"] = "Pending Director Approval"
            st.success("Complete estimation sent to Partner successfully.")
        else:
            requests_df.loc[index, "request_status"] = "Sent Back to Requester"
            st.warning("Request sent back to Requester.")

        requests_df.to_csv(REQUESTS_FILE, index=False)