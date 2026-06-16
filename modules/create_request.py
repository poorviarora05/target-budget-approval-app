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

        col1, col2, col3 = st.columns(3)

        with col1:
            start_date = st.date_input("Training Start Date")

        with col2:
            end_date = st.date_input("Training End Date")

        total_training_days = (end_date - start_date).days + 1

        if total_training_days < 1:
            total_training_days = 1

        with col3:
            st.metric("Total Training Days", total_training_days)

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

        st.subheader("Additional Requirements")

        col4, col5 = st.columns(2)

        with col4:
            stay_required = st.checkbox("Stay Required")
            travel_required = st.checkbox("Travel Required")

        with col5:
            food_required = st.checkbox("Food Required")
            training_material_required = st.checkbox(
                "Training Material Required"
            )

        purpose = st.text_area("Purpose / Remarks")

        submit = st.form_submit_button("Submit Request")

        if submit:

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
                "stay_required": stay_required,
                "travel_required": travel_required,
                "food_required": food_required,
                "training_material_required": training_material_required,
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