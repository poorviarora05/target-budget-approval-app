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

        college_name = st.text_input("College Name")
        requester_email = st.text_input("Requester Email")
        training_topic = st.text_input("Training Topic")
        trainer_requirement = st.text_input("Trainer / Industrialist Requirement")

        hours = st.number_input(
            "Number of Hours Per Day",
            min_value=1,
            value=1
        )

        training_days = st.number_input(
            "Number of Training Days",
            min_value=1,
            value=1
        )

        rate_per_hour = st.number_input(
            "Rate Per Hour",
            min_value=0,
            value=1000
        )

        estimated_budget = hours * training_days * rate_per_hour

        st.info(f"Estimated Budget: ₹{estimated_budget}")

        stay_required = st.selectbox("Stay Required?", ["Yes", "No"])
        travel_required = st.selectbox("Travel Required?", ["Yes", "No"])
        food_required = st.selectbox("Food Required?", ["Yes", "No"])

        training_material_required = st.selectbox(
            "Training Material Required?",
            ["Yes", "No"]
        )

        other_requirements = st.text_area("Other Requirements")
        purpose = st.text_area("Purpose / Remarks")

        submit = st.form_submit_button("Submit Request")

        if submit:

            new_request = {
                "request_id": f"REQ{len(requests_df) + 1:03d}",
                "created_by": username,
                "requester_email": requester_email,
                "college_name": college_name,
                "training_topic": training_topic,
                "trainer_requirement": trainer_requirement,
                "hours": hours,
                "training_days": training_days,
                "rate_per_hour": rate_per_hour,
                "estimated_budget": estimated_budget,
                "stay_required": stay_required,
                "travel_required": travel_required,
                "food_required": food_required,
                "training_material_required": training_material_required,
                "other_requirements": other_requirements,
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

            st.session_state.request_submitted = True

    if st.session_state.get("request_submitted", False):
        st.success("Request submitted successfully.")
        st.session_state.request_submitted = False