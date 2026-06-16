import streamlit as st
import pandas as pd

REQUESTS_FILE = "requests.csv"


def safe_number(value):
    try:
        if pd.isna(value):
            return 0
        return float(value)
    except:
        return 0


def show_director_approval():

    st.header("Partner Approval & Budget Review")

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
            selected_request.get("approver_remarks", "")
        ]
    })

    st.table(request_table)

    st.subheader("Cost Estimate Received from Approver")

    trainer_cost = safe_number(selected_request.get("trainer_cost", 0))
    stay_total = safe_number(selected_request.get("stay_total", 0))
    travel_total = safe_number(selected_request.get("travel_total", 0))
    food_total = safe_number(selected_request.get("food_total", 0))
    material_total = safe_number(selected_request.get("material_total", 0))
    other_total = safe_number(selected_request.get("other_total", 0))
    estimated_budget = safe_number(selected_request.get("estimated_budget", 0))

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
        "Estimated Amount": [
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

    st.subheader("Partner Budget Decision")

    available_budget = st.number_input(
        "Available Budget for this University",
        min_value=0,
        value=100000
    )

    remaining_budget = available_budget - estimated_budget

    if available_budget > 0:
        utilization_percentage = (estimated_budget / available_budget) * 100
    else:
        utilization_percentage = 0

    budget_health_score = max(
        0,
        round(100 - abs(100 - utilization_percentage))
    )

    col1, col2, col3 = st.columns(3)

    col1.metric("Available Budget", f"₹{available_budget:,.0f}")
    col2.metric("Estimated Cost", f"₹{estimated_budget:,.0f}")
    col3.metric("Remaining / Loss", f"₹{remaining_budget:,.0f}")

    st.subheader("Smart Budget Insights")

    col1, col2, col3 = st.columns(3)

    col1.metric("Budget Health Score", f"{budget_health_score}/100")

    if utilization_percentage <= 80:
        risk_level = "Low Risk"
        recommendation = "Recommended for Approval"
    elif utilization_percentage <= 100:
        risk_level = "Medium Risk"
        recommendation = "Review Before Approval"
    else:
        risk_level = "High Risk"
        recommendation = "Budget Exceeded"

    col2.metric("Risk Level", risk_level)
    col3.metric("Budget Utilization", f"{utilization_percentage:.1f}%")

    if risk_level == "Low Risk":
        st.success("System Recommendation: Budget is healthy and can be approved.")
    elif risk_level == "Medium Risk":
        st.warning("System Recommendation: Budget is close to limit. Review carefully.")
    else:
        st.error("System Recommendation: Budget exceeded. Reallocation required.")

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

        requests_df.loc[index, "available_budget"] = available_budget
        requests_df.loc[index, "remaining_budget"] = remaining_budget
        requests_df.loc[index, "budget_health_score"] = budget_health_score
        requests_df.loc[index, "risk_level"] = risk_level
        requests_df.loc[index, "budget_utilization"] = utilization_percentage
        requests_df.loc[index, "partner_recommendation"] = recommendation

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

        st.rerun()