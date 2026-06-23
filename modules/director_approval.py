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


def clean_text(value):
    if pd.isna(value):
        return ""
    return str(value).strip().title()


def get_budget_values(selected_request):
    total_available_budget = safe_number(
        selected_request.get("total_available_budget", 0)
    )

    if total_available_budget == 0:
        total_available_budget = safe_number(
            selected_request.get("available_budget", 0)
        )

    trainer_cost = safe_number(selected_request.get("trainer_cost", 0))
    stay_total = safe_number(selected_request.get("stay_total", 0))

    travel_total = safe_number(
        selected_request.get(
            "approver_total_travel_cost",
            selected_request.get("travel_total", 0)
        )
    )

    food_total = safe_number(selected_request.get("food_total", 0))
    material_total = safe_number(selected_request.get("material_total", 0))
    other_total = safe_number(selected_request.get("other_total", 0))
    estimated_budget = safe_number(selected_request.get("estimated_budget", 0))

    remaining_after_approval = total_available_budget - estimated_budget

    if total_available_budget > 0:
        utilization_percentage = (estimated_budget / total_available_budget) * 100
    else:
        utilization_percentage = 0

    if utilization_percentage <= 80:
        risk_level = "Low Risk"
        recommendation = "Recommended for Approval"
    elif utilization_percentage <= 100:
        risk_level = "Medium Risk"
        recommendation = "Review Before Approval"
    else:
        risk_level = "High Risk"
        recommendation = "Budget Exceeded"

    return {
        "total_available_budget": total_available_budget,
        "trainer_cost": trainer_cost,
        "stay_total": stay_total,
        "travel_total": travel_total,
        "food_total": food_total,
        "material_total": material_total,
        "other_total": other_total,
        "estimated_budget": estimated_budget,
        "remaining_after_approval": remaining_after_approval,
        "utilization_percentage": utilization_percentage,
        "risk_level": risk_level,
        "recommendation": recommendation,
    }


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

    st.subheader("Pending Requests")

    h1, h2, h3, h4, h5, h6 = st.columns([0.7, 1.2, 2.3, 2.3, 1.5, 1.5])
    h1.write("**Select**")
    h2.write("**Request ID**")
    h3.write("**University**")
    h4.write("**Topic**")
    h5.write("**Budget**")
    h6.write("**Risk**")

    selected_ids = []

    for _, row in pending_requests.iterrows():
        request_id = row.get("request_id", "")
        values = get_budget_values(row)

        c1, c2, c3, c4, c5, c6 = st.columns([0.7, 1.2, 2.3, 2.3, 1.5, 1.5])

        with c1:
            selected = st.checkbox(
                "",
                key=f"partner_select_{request_id}",
                label_visibility="collapsed"
            )

        with c2:
            st.write(f"**{request_id}**")

        with c3:
            st.write(clean_text(row.get("college_name", "")))

        with c4:
            st.write(clean_text(row.get("training_topic", "")))

        with c5:
            st.write(f"₹{values['estimated_budget']:,.0f}")

        with c6:
            st.write(values["risk_level"])

        if selected:
            selected_ids.append(request_id)

    if not selected_ids:
        st.info("Tick one or more requests to view details and take action.")
        return

    st.markdown("---")

    st.subheader("Selected Request Details")

    for selected_id in selected_ids:
        selected_request = pending_requests[
            pending_requests["request_id"] == selected_id
        ].iloc[0]

        values = get_budget_values(selected_request)

        with st.expander(f"Details for Request {selected_id}", expanded=True):

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
                    clean_text(selected_request.get("college_name", "")),
                    clean_text(selected_request.get("training_topic", "")),
                    clean_text(selected_request.get("trainer_name", "")),
                    selected_request.get("total_hours", ""),
                    selected_request.get("training_days", ""),
                    selected_request.get("approver_remarks", "")
                ]
            })

            st.table(request_table)

            cost_table = pd.DataFrame({
                "Cost Component": [
                    "Total Available Budget",
                    "Trainer Fee",
                    "Stay Cost",
                    "Travel Cost",
                    "Food Cost",
                    "Training Material Cost",
                    "Other Cost",
                    "Total Estimated Budget",
                    "Balance After Approver Estimate"
                ],
                "Estimated Amount": [
                    f"₹{values['total_available_budget']:,.0f}",
                    f"₹{values['trainer_cost']:,.0f}",
                    f"₹{values['stay_total']:,.0f}",
                    f"₹{values['travel_total']:,.0f}",
                    f"₹{values['food_total']:,.0f}",
                    f"₹{values['material_total']:,.0f}",
                    f"₹{values['other_total']:,.0f}",
                    f"₹{values['estimated_budget']:,.0f}",
                    f"₹{values['remaining_after_approval']:,.0f}"
                ]
            })

            st.table(cost_table)

            editable_budget = st.number_input(
                f"Total Available Budget for {selected_id}",
                min_value=0,
                value=int(values["total_available_budget"])
                if values["total_available_budget"] > 0
                else 100000,
                step=1000,
                key=f"partner_budget_{selected_id}"
            )

            final_remaining = editable_budget - values["estimated_budget"]

            if editable_budget > 0:
                final_utilization = (values["estimated_budget"] / editable_budget) * 100
            else:
                final_utilization = 0

            m1, m2, m3 = st.columns(3)
            m1.metric("Final Available Budget", f"₹{editable_budget:,.0f}")
            m2.metric("Estimated Cost", f"₹{values['estimated_budget']:,.0f}")
            m3.metric("Remaining / Loss", f"₹{final_remaining:,.0f}")

            if final_utilization <= 80:
                final_risk_level = "Low Risk"
                final_recommendation = "Recommended for Approval"
            elif final_utilization <= 100:
                final_risk_level = "Medium Risk"
                final_recommendation = "Review Before Approval"
            else:
                final_risk_level = "High Risk"
                final_recommendation = "Budget Exceeded"

            m4, m5 = st.columns(2)
            m4.metric("Risk Level", final_risk_level)
            m5.metric("Budget Utilization", f"{final_utilization:.1f}%")

            if final_risk_level == "Low Risk":
                st.success("System Recommendation: Budget is healthy and can be approved.")
            elif final_risk_level == "Medium Risk":
                st.warning("System Recommendation: Budget is close to limit. Review carefully.")
            else:
                st.error("System Recommendation: Budget exceeded. Reallocation required.")

    st.markdown("---")

    st.subheader("Partner Bulk Decision")

    partner_remarks = st.text_area("Partner Remarks")

    decision = st.selectbox(
        "Decision for Selected Requests",
        ["Approve Selected", "Reject Selected"]
    )

    if st.button("Submit Partner Decision"):

        for selected_id in selected_ids:
            index = requests_df[
                requests_df["request_id"] == selected_id
            ].index[0]

            selected_request = requests_df.loc[index]
            values = get_budget_values(selected_request)

            available_budget = st.session_state.get(
                f"partner_budget_{selected_id}",
                int(values["total_available_budget"])
                if values["total_available_budget"] > 0
                else 100000
            )

            estimated_budget = values["estimated_budget"]
            remaining_budget = available_budget - estimated_budget

            if available_budget > 0:
                utilization_percentage = (estimated_budget / available_budget) * 100
            else:
                utilization_percentage = 0

            if utilization_percentage <= 80:
                risk_level = "Low Risk"
                recommendation = "Recommended for Approval"
            elif utilization_percentage <= 100:
                risk_level = "Medium Risk"
                recommendation = "Review Before Approval"
            else:
                risk_level = "High Risk"
                recommendation = "Budget Exceeded"

            budget_health_score = max(
                0,
                round(100 - abs(100 - utilization_percentage))
            )

            requests_df.loc[index, "total_available_budget"] = available_budget
            requests_df.loc[index, "available_budget"] = available_budget
            requests_df.loc[index, "partner_final_available_budget"] = available_budget
            requests_df.loc[index, "remaining_budget"] = remaining_budget
            requests_df.loc[index, "budget_health_score"] = budget_health_score
            requests_df.loc[index, "risk_level"] = risk_level
            requests_df.loc[index, "budget_utilization"] = utilization_percentage
            requests_df.loc[index, "partner_recommendation"] = recommendation

            if "partner_remarks" not in requests_df.columns:
                requests_df["partner_remarks"] = ""

            requests_df["partner_remarks"] = requests_df["partner_remarks"].astype(str)
            requests_df.at[index, "partner_remarks"] = str(partner_remarks)

            if decision == "Approve Selected":
                requests_df.loc[index, "request_status"] = "Approved"
            else:
                requests_df.loc[index, "request_status"] = "Rejected"

        requests_df.to_csv(
            REQUESTS_FILE,
            index=False
        )

        if decision == "Approve Selected":
            st.success("Selected request(s) approved successfully.")
        else:
            st.error("Selected request(s) rejected.")

        st.rerun()
