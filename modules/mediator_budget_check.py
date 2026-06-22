import streamlit as st
import pandas as pd
from datetime import datetime

REQUESTS_FILE = "requests.csv"


AVAILABLE_BUDGET_MASTER = {
    "Chandigarh University": {
        "Apr-26": 0,
        "May-26": 388009,
        "Jun-26": 60000,
        "Jul-26": 60000,
        "Aug-26": 60000,
        "Sep-26": 60000,
        "Oct-26": 60000,
        "Nov-26": 0,
        "Dec-26": 75000,
        "Jan-27": 75000,
        "Feb-27": 75000,
        "Mar-27": 75000,
    }
}


def safe_int(value, default=0):
    try:
        if pd.isna(value):
            return default
        return int(float(value))
    except:
        return default


def get_month_key_from_date(date_value):
    try:
        parsed_date = pd.to_datetime(date_value)
        return parsed_date.strftime("%b-%y")
    except:
        return ""


def get_available_budget(college_name, month_key):
    college_name = str(college_name).lower()

    if "chandigarh" in college_name:
        return AVAILABLE_BUDGET_MASTER.get(
            "Chandigarh University", {}
        ).get(month_key, 0)

    return 0


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

    requester_total_budget = safe_int(
        selected_request.get("total_expected_budget", 0),
        0
    )

    st.subheader("Requester Budget Estimation")

    requester_table = pd.DataFrame({
        "Component": [
            "Training Days",
            "Total Hours",
            "Rate Per Hour",
            "Training Cost",
            "Local Travel",
            "Outstation Travel",
            "Total Travel Cost",
            "Stay Cost",
            "Food Cost",
            "Total Requester Budget"
        ],
        "Requester Value": [
            selected_request.get("training_days", 0),
            selected_request.get("total_hours", 0),
            f"₹{safe_int(selected_request.get('rate_per_hour', 0)):,.0f}",
            f"₹{safe_int(selected_request.get('training_cost', 0)):,.0f}",
            f"₹{safe_int(selected_request.get('local_travel_total', 0)):,.0f}",
            f"₹{safe_int(selected_request.get('outstation_travel_total', 0)):,.0f}",
            f"₹{safe_int(selected_request.get('total_travel_cost', 0)):,.0f}",
            f"₹{safe_int(selected_request.get('stay_cost', 0)):,.0f}",
            f"₹{safe_int(selected_request.get('food_cost', 0)):,.0f}",
            f"₹{requester_total_budget:,.0f}"
        ]
    })

    st.table(requester_table)

    st.subheader("Total Available Budget")

    college_name = selected_request.get("college_name", "")
    training_start_date = selected_request.get("start_date", "")
    month_key = get_month_key_from_date(training_start_date)

    total_available_budget = get_available_budget(
        college_name,
        month_key
    )

    b1, b2, b3 = st.columns(3)

    with b1:
        st.metric("College / University", college_name)

    with b2:
        st.metric("Budget Month", month_key if month_key else "Not Found")

    with b3:
        st.metric("Total Available Budget", f"₹{total_available_budget:,.0f}")

    if total_available_budget == 0:
        st.warning(
            "No available budget found for this university/month in the sample budget master."
        )

    st.subheader("Approver Budget Calculation")

    training_days = st.number_input(
        "Total Training Days",
        min_value=1,
        value=safe_int(selected_request.get("training_days", 1), 1)
    )

    hours_per_day = st.number_input(
        "Hours Per Day",
        min_value=1,
        value=6
    )

    total_hours = training_days * hours_per_day

    rate_per_hour = st.number_input(
        "Trainer Rate Per Hour",
        min_value=0,
        value=3000
    )

    trainer_cost = total_hours * rate_per_hour

    st.info(f"Total Program Hours: {total_hours}")
    st.info(f"Trainer Cost: ₹{trainer_cost:,.0f}")

    st.subheader("Additional Requirements Cost")

    stay_per_day = st.number_input(
        "Stay Cost Per Day",
        min_value=0,
        value=0
    )

    food_per_day = st.number_input(
        "Food Cost Per Day",
        min_value=0,
        value=0
    )

    st.subheader("Travel Cost Details")

    approver_local_travel_per_day = st.number_input(
        "Local Taxi / Daily Travel Cost Per Day (₹)",
        min_value=0,
        value=0
    )

    approver_local_travel_total = (
        approver_local_travel_per_day * training_days
    )

    approver_outstation_travel_mode = st.selectbox(
        "Outstation Travel Mode",
        ["Flight", "Train", "Bus", "Car"]
    )

    col1, col2 = st.columns(2)

    with col1:
        approver_going_travel_cost = st.number_input(
            "Going Travel Cost (₹)",
            min_value=0,
            value=0
        )

    with col2:
        approver_return_travel_cost = st.number_input(
            "Return Travel Cost (₹)",
            min_value=0,
            value=0
        )

    approver_outstation_travel_total = (
        approver_going_travel_cost + approver_return_travel_cost
    )

    approver_total_travel_cost = (
        approver_local_travel_total + approver_outstation_travel_total
    )

    st.info(f"Local Travel Total: ₹{approver_local_travel_total:,.0f}")
    st.info(
        f"Outstation Travel ({approver_outstation_travel_mode}): ₹{approver_outstation_travel_total:,.0f}"
    )
    st.success(f"Total Travel Cost: ₹{approver_total_travel_cost:,.0f}")

    stay_total = stay_per_day * training_days
    food_total = food_per_day * training_days

    approver_estimated_budget = (
        trainer_cost
        + approver_total_travel_cost
        + stay_total
        + food_total
    )

    remaining_after_approval = total_available_budget - approver_estimated_budget

    st.subheader("Available Budget vs Approver Estimate")

    a1, a2, a3 = st.columns(3)

    with a1:
        st.metric("Total Available Budget", f"₹{total_available_budget:,.0f}")

    with a2:
        st.metric("Approver Estimated Budget", f"₹{approver_estimated_budget:,.0f}")

    with a3:
        st.metric("Balance After Approval", f"₹{remaining_after_approval:,.0f}")

    if total_available_budget > 0 and approver_estimated_budget > total_available_budget:
        st.error("Approver estimated budget exceeds the available budget.")
    elif total_available_budget > 0:
        st.success("Approver estimated budget is within the available budget.")

    st.subheader("Approver Cost Breakdown")

    cost_table = pd.DataFrame({
        "Cost Component": [
            "Trainer Fee",
            "Stay Cost",
            "Food Cost",
            "Travel Cost",
            "Total Approver Budget"
        ],
        "Rate / Details": [
            f"₹{rate_per_hour:,.0f} per hour",
            f"₹{stay_per_day:,.0f} per day",
            f"₹{food_per_day:,.0f} per day",
            "Local + Outstation",
            "-"
        ],
        "Days / Hours": [
            f"{total_hours} hours",
            f"{training_days} days",
            f"{training_days} days",
            "Daily + Going/Return",
            "-"
        ],
        "Total Amount": [
            f"₹{trainer_cost:,.0f}",
            f"₹{stay_total:,.0f}",
            f"₹{food_total:,.0f}",
            f"₹{approver_total_travel_cost:,.0f}",
            f"₹{approver_estimated_budget:,.0f}"
        ]
    })

    st.table(cost_table)

    st.subheader("Requester vs Approver Budget Comparison")

    difference = approver_estimated_budget - requester_total_budget

    col3, col4, col5 = st.columns(3)

    with col3:
        st.metric("Requester Budget", f"₹{requester_total_budget:,.0f}")

    with col4:
        st.metric("Approver Budget", f"₹{approver_estimated_budget:,.0f}")

    with col5:
        st.metric("Difference", f"₹{difference:,.0f}")

    if difference > 0:
        st.warning(
            f"Approver budget is ₹{difference:,.0f} higher than requester budget."
        )
    elif difference < 0:
        st.success(
            f"Approver budget is ₹{abs(difference):,.0f} lower than requester budget."
        )
    else:
        st.success("Requester and Approver budgets match.")

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

        numeric_columns = [
            "training_days",
            "hours_per_day",
            "total_hours",
            "rate_per_hour",
            "trainer_cost",
            "stay_per_day",
            "food_per_day",
            "approver_local_travel_per_day",
            "approver_local_travel_total",
            "approver_going_travel_cost",
            "approver_return_travel_cost",
            "approver_outstation_travel_total",
            "approver_total_travel_cost",
            "stay_total",
            "food_total",
            "estimated_budget",
            "budget_difference",
            "total_available_budget",
            "remaining_after_approval"
        ]

        text_columns = [
            "approver_outstation_travel_mode",
            "approver_remarks",
            "budget_month"
        ]

        for col in numeric_columns:
            if col not in requests_df.columns:
                requests_df[col] = 0

        for col in text_columns:
            if col not in requests_df.columns:
                requests_df[col] = ""
            requests_df[col] = requests_df[col].astype(str)

        requests_df.loc[index, "training_days"] = training_days
        requests_df.loc[index, "hours_per_day"] = hours_per_day
        requests_df.loc[index, "total_hours"] = total_hours
        requests_df.loc[index, "rate_per_hour"] = rate_per_hour
        requests_df.loc[index, "trainer_cost"] = trainer_cost

        requests_df.loc[index, "stay_per_day"] = stay_per_day
        requests_df.loc[index, "food_per_day"] = food_per_day

        requests_df.loc[index, "approver_local_travel_per_day"] = approver_local_travel_per_day
        requests_df.loc[index, "approver_local_travel_total"] = approver_local_travel_total

        requests_df.loc[index, "approver_outstation_travel_mode"] = str(
            approver_outstation_travel_mode
        )

        requests_df.loc[index, "approver_going_travel_cost"] = approver_going_travel_cost
        requests_df.loc[index, "approver_return_travel_cost"] = approver_return_travel_cost
        requests_df.loc[index, "approver_outstation_travel_total"] = approver_outstation_travel_total
        requests_df.loc[index, "approver_total_travel_cost"] = approver_total_travel_cost

        requests_df.loc[index, "stay_total"] = stay_total
        requests_df.loc[index, "food_total"] = food_total
        requests_df.loc[index, "estimated_budget"] = approver_estimated_budget
        requests_df.loc[index, "budget_difference"] = difference

        requests_df.loc[index, "total_available_budget"] = total_available_budget
        requests_df.loc[index, "remaining_after_approval"] = remaining_after_approval
        requests_df.loc[index, "budget_month"] = str(month_key)

        requests_df.at[index, "approver_remarks"] = str(approver_remarks)

        if decision == "Approve and Send to Partner":
            requests_df.loc[index, "request_status"] = "Pending Director Approval"
            st.success("Complete estimation sent to Partner successfully.")
        else:
            requests_df.loc[index, "request_status"] = "Sent Back to Requester"
            st.warning("Request sent back to Requester.")

        requests_df.to_csv(
            REQUESTS_FILE,
            index=False
        )
