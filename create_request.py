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
        requester_phone = st.text_input(
        "Requester WhatsApp Number with country code",
         placeholder="+919999999999"
)
        training_topic = st.text_input("Training Topic")
        trainer_requirement = st.text_input("Trainer / Industrialist Requirement")
        hours = st.number_input(
       "Number of Hours",
        min_value=1,
        value=1
)
        requester_budget = st.number_input(
       "Your Available Budget",
       min_value=0,
       value=0
)

        st.subheader("Service Requirements")

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
                "college_name": college_name,
                "training_topic": training_topic,
                "trainer_requirement": trainer_requirement,
                "hours": hours,
                "requester_budget": requester_budget,
                "stay_required": stay_required,
                "travel_required": travel_required,
                "food_required": food_required,
                "training_material_required": training_material_required,
                "other_requirements": other_requirements,
                "purpose": purpose,
                "request_status": "Pending Mediator Review",
                "requester_phone": requester_phone,
                "requester_email": requester_email,
                "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }

            requests_df = pd.concat(
                [requests_df, pd.DataFrame([new_request])],
                ignore_index=True
            )

            requests_df.to_csv(REQUESTS_FILE, index=False)

            st.success("Request submitted successfully.")