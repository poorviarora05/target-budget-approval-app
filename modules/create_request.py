import streamlit as st
import pandas as pd
from datetime import datetime

REQUESTS_FILE = "requests.csv"


def show_create_request(username):

    st.title("Create Training Request")
    st.caption("Submit training requirement with budget estimation for approval review.")

    try:
        requests_df = pd.read_csv(REQUESTS_FILE)
    except:
        requests_df = pd.DataFrame()

    current_date = datetime.now().date()
    st.write("Request Date:", current_date)

    st.subheader("Request Timeline")

    col1, col2, col3 = st.columns(3)

    with col1:
        start_date = st.date_input("Training Start Date")

    with col2:
        end_date = st.date_input("Training End Date")

    total_training_days = max((end_date - start_date).days + 1, 1)

    with col3:
        st.text_input(
            "Training Days",
            value=str(total_training_days),
            disabled=True
        )

    st.divider()

    st.subheader("College & Training Details")

    college_name = st.text_input("College / University Name")

    training_topic = st.selectbox(
        "Training Topic",
        [
            "Artificial Intelligence",
            "Machine Learning",
            "Generative AI",
            "Data Analytics",
            "Cyber Security",
            "Cloud Computing",
            "Python Programming",
            "Soft Skills",
            "Finance & Taxation",
            "Industry Expert Session"
        ]
    )

    trainer_name = st.text_input("Trainer Name")
    purpose = st.text_area("Purpose / Remarks")

    st.divider()

    st.subheader("Training Budget Details")

    col4, col5 = st.columns(2)

    with col4:
        total_hours = st.number_input(
            "Total Training Hours",
            min_value=1,
            value=8
        )

    with col5:
        rate_per_hour = st.number_input(
            "Rate Per Hour (₹)",
            min_value=0,
            value=3000
        )

    training_cost = total_hours * rate_per_hour
    st.info(f"Training Cost: ₹{training_cost:,.0f}")

    st.divider()

    st.subheader("Travel Cost Details")

    local_travel_per_day = st.number_input(
        "Local Taxi / Daily Travel Cost Per Day (₹)",
        min_value=0,
        value=0
    )

    local_travel_total = local_travel_per_day * total_training_days

    outstation_travel_mode = st.selectbox(
        "Outstation Travel Mode",
        ["Flight", "Train", "Bus", "Car"]
    )

    col6, col7 = st.columns(2)

    with col6:
        going_travel_cost = st.number_input(
            "Going Travel Cost (₹)",
            min_value=0,
            value=0
        )

    with col7:
        return_travel_cost = st.number_input(
            "Return Travel Cost (₹)",
            min_value=0,
            value=0
        )

    outstation_travel_total = going_travel_cost + return_travel_cost
    total_travel_cost = local_travel_total + outstation_travel_total

    col8, col9, col10 = st.columns(3)

    with col8:
        st.info(f"Local Travel: ₹{local_travel_total:,.0f}")

    with col9:
        st.info(
            f"Outstation Travel ({outstation_travel_mode}): ₹{outstation_travel_total:,.0f}"
        )

    with col10:
        st.success(f"Total Travel: ₹{total_travel_cost:,.0f}")

    st.divider()

    st.subheader("Additional Requirements Cost")

    col11, col12 = st.columns(2)

    with col11:
        stay_cost = st.number_input(
            "Stay Cost (₹)",
            min_value=0,
            value=0
        )

    with col12:
        food_cost = st.number_input(
            "Food Cost (₹)",
            min_value=0,
            value=0
        )

    additional_cost = stay_cost + total_travel_cost + food_cost
    total_expected_budget = training_cost + additional_cost

    st.divider()

    st.subheader("Budget Summary")

    col13, col14, col15 = st.columns(3)

    with col13:
        st.metric("Training Cost", f"₹{training_cost:,.0f}")

    with col14:
        st.metric("Additional Cost", f"₹{additional_cost:,.0f}")

    with col15:
        st.metric("Total Expected Budget", f"₹{total_expected_budget:,.0f}")

    st.divider()

    if st.button("Submit Request", use_container_width=True):

        new_request = {
            "request_id": f"REQ{len(requests_df) + 1:03d}",
            "created_by": username,
            "request_date": str(current_date),
            "start_date": str(start_date),
            "end_date": str(end_date),
            "training_days": total_training_days,
            "college_name": college_name,
            "training_topic": training_topic,
            "trainer_name": trainer_name,
            "total_hours": total_hours,
            "rate_per_hour": rate_per_hour,
            "training_cost": training_cost,
            "local_travel_per_day": local_travel_per_day,
            "local_travel_total": local_travel_total,
            "outstation_travel_mode": outstation_travel_mode,
            "going_travel_cost": going_travel_cost,
            "return_travel_cost": return_travel_cost,
            "outstation_travel_total": outstation_travel_total,
            "total_travel_cost": total_travel_cost,
            "stay_cost": stay_cost,
            "food_cost": food_cost,
            "additional_cost": additional_cost,
            "total_expected_budget": total_expected_budget,
            "purpose": purpose,
            "request_status": "Pending Mediator Review",
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        requests_df = pd.concat(
            [requests_df, pd.DataFrame([new_request])],
            ignore_index=True
        )

        requests_df.to_csv(REQUESTS_FILE, index=False)

        st.success("Request sent successfully!")