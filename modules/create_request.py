import streamlit as st
import pandas as pd
from datetime import datetime

REQUESTS_FILE = "requests.csv"


def show_create_request(username):

    st.header("Create Training Request")

    try:
        requests_df = pd.read_csv(REQUESTS_FILE)
    except:
        requests_df = pd.DataFrame()

    current_date = datetime.now().date()
    st.write("Request Date:", current_date)

    col1, col2, col3 = st.columns(3)

    with col1:
        start_date = st.date_input("Training Start Date")

    with col2:
        end_date = st.date_input("Training End Date")

    total_training_days = max(
        (end_date - start_date).days + 1,
        1
    )

    with col3:
        st.metric("Training Days", total_training_days)

    st.markdown("---")

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

    st.markdown("---")

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

    st.subheader("Additional Requirements Cost")

    col6, col7 = st.columns(2)

    with col6:
        stay_cost = st.number_input(
            "Stay Cost (₹)",
            min_value=0,
            value=0
        )

        travel_cost = st.number_input(
            "Travel Cost (₹)",
            min_value=0,
            value=0
        )

    with col7:
        food_cost = st.number_input(
            "Food Cost (₹)",
            min_value=0,
            value=0
        )

        material_cost = st.number_input(
            "Training Material Cost (₹)",
            min_value=0,
            value=0
        )

    additional_cost = (
        stay_cost
        + travel_cost
        + food_cost
        + material_cost
    )

    total_expected_budget = (
        training_cost
        + additional_cost
    )

    st.info(f"Additional Cost: ₹{additional_cost:,.0f}")
    st.success(f"Total Expected Budget: ₹{total_expected_budget:,.0f}")

    st.markdown("---")

    if st.button("Submit Request"):

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
            "stay_cost": stay_cost,
            "travel_cost": travel_cost,
            "food_cost": food_cost,
            "material_cost": material_cost,
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

        requests_df.to_csv(
            REQUESTS_FILE,
            index=False
        )

        st.success("Request sent successfully!")