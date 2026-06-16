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

    with st.form("create_request_form"):

        current_date = datetime.now().date()
        st.write("Request Date:", current_date)

        start_date = st.date_input("Training Start Date")
        end_date = st.date_input("Training End Date")

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

        total_hours = st.number_input(
            "Total Hours of Full Program",
            min_value=1,
            value=1
        )

        total_training_days = (end_date - start_date).days + 1

        if total_training_days < 1:
            st.error("End Date cannot be before Start Date.")
            total_training_days = 1

        st.info(f"Total Training Days: {total_training_days}")

        rate_per_hour = st.number_input(
            "Trainer Rate Per Hour",
            min_value=0,
            value=3000
        )

        st.subheader("Per Day Service Budget")

        stay_per_day = st.number_input("Stay Budget Per Day", min_value=0, value=0)
        travel_per_day = st.number_input("Travel Budget Per Day", min_value=0, value=0)
        food_per_day = st.number_input("Food Budget Per Day", min_value=0, value=0)
        material_per_day = st.number_input("Training Material Budget Per Day", min_value=0, value=0)
        other_per_day = st.number_input("Other Budget Per Day", min_value=0, value=0)

        trainer_cost = total_hours * rate_per_hour

        stay_total = stay_per_day * total_training_days
        travel_total = travel_per_day * total_training_days
        food_total = food_per_day * total_training_days
        material_total = material_per_day * total_training_days
        other_total = other_per_day * total_training_days

        estimated_budget = (
            trainer_cost
            + stay_total
            + travel_total
            + food_total
            + material_total
            + other_total
        )

        st.info(f"Estimated Total Budget: ₹{estimated_budget}")

        purpose = st.text_area("Purpose / Remarks")

        submit = st.form_submit_button("Submit Request")

        if submit:

            new_request = {
                "request_id": f"REQ{len(requests_df) + 1:03d}",
                "created_by": username,
                "request_date": str(current_date),
                "start_date": str(start_date),
                "end_date": str(end_date),
                "college_name": college_name,
                "training_topic": training_topic,
                "trainer_name": trainer_name,
                "total_hours": total_hours,
                "training_days": total_training_days,
                "rate_per_hour": rate_per_hour,
                "trainer_cost": trainer_cost,
                "stay_per_day": stay_per_day,
                "travel_per_day": travel_per_day,
                "food_per_day": food_per_day,
                "material_per_day": material_per_day,
                "other_per_day": other_per_day,
                "stay_total": stay_total,
                "travel_total": travel_total,
                "food_total": food_total,
                "material_total": material_total,
                "other_total": other_total,
                "estimated_budget": estimated_budget,
                "purpose": purpose,
                "request_status": "Pending Mediator Review",
                "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }

            requests_df = pd.concat(
                [requests_df, pd.DataFrame([new_request])],
                ignore_index=True
            )

            requests_df.to_csv(REQUESTS_FILE, index=False)

            st.toast("Request sent successfully!")