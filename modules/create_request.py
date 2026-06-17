import streamlit as st
import pandas as pd
from datetime import datetime

REQUESTS_FILE = "requests.csv"


def show_create_request(username):

    st.markdown("""
        <style>
        .main-title {
            font-size: 30px;
            font-weight: 700;
            color: #1f2937;
            margin-bottom: 5px;
        }

        .sub-title {
            font-size: 15px;
            color: #6b7280;
            margin-bottom: 25px;
        }

        .section-card {
            background-color: #ffffff;
            padding: 24px;
            border-radius: 14px;
            border: 1px solid #e5e7eb;
            box-shadow: 0px 4px 14px rgba(0,0,0,0.04);
            margin-bottom: 22px;
        }

        .section-heading {
            font-size: 19px;
            font-weight: 650;
            color: #111827;
            margin-bottom: 18px;
        }

        .summary-box {
            background-color: #f9fafb;
            padding: 18px;
            border-radius: 12px;
            border: 1px solid #e5e7eb;
            text-align: center;
        }

        .summary-label {
            font-size: 13px;
            color: #6b7280;
        }

        .summary-value {
            font-size: 22px;
            font-weight: 700;
            color: #111827;
        }

        div.stButton > button {
            background-color: #111827;
            color: white;
            border-radius: 10px;
            padding: 0.65rem 1.4rem;
            font-weight: 600;
            border: none;
            width: 100%;
        }

        div.stButton > button:hover {
            background-color: #374151;
            color: white;
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="main-title">Create Training Request</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Submit training requirement with budget estimation for approval review.</div>', unsafe_allow_html=True)

    try:
        requests_df = pd.read_csv(REQUESTS_FILE)
    except:
        requests_df = pd.DataFrame()

    current_date = datetime.now().date()

    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-heading">Request Timeline</div>', unsafe_allow_html=True)

    st.write("Request Date:", current_date)

    col1, col2, col3 = st.columns(3)

    with col1:
        start_date = st.date_input("Training Start Date")

    with col2:
        end_date = st.date_input("Training End Date")

    total_training_days = max((end_date - start_date).days + 1, 1)

    with col3:
        st.metric("Training Days", total_training_days)

    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-heading">College & Training Details</div>', unsafe_allow_html=True)

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

    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-heading">Training Budget Details</div>', unsafe_allow_html=True)

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

    st.metric("Training Cost", f"₹{training_cost:,.0f}")

    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-heading">Travel Cost Details</div>', unsafe_allow_html=True)

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

    col_a, col_b, col_c = st.columns(3)

    with col_a:
        st.metric("Local Travel", f"₹{local_travel_total:,.0f}")

    with col_b:
        st.metric(
            f"Outstation Travel ({outstation_travel_mode})",
            f"₹{outstation_travel_total:,.0f}"
        )

    with col_c:
        st.metric("Total Travel Cost", f"₹{total_travel_cost:,.0f}")

    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-heading">Additional Requirements Cost</div>', unsafe_allow_html=True)

    col8, col9 = st.columns(2)

    with col8:
        stay_cost = st.number_input(
            "Stay Cost (₹)",
            min_value=0,
            value=0
        )

    with col9:
        food_cost = st.number_input(
            "Food Cost (₹)",
            min_value=0,
            value=0
        )

    material_cost = 0

    additional_cost = (
        stay_cost
        + total_travel_cost
        + food_cost
        + material_cost
    )

    total_expected_budget = training_cost + additional_cost

    col10, col11, col12 = st.columns(3)

    with col10:
        st.metric("Additional Cost", f"₹{additional_cost:,.0f}")

    with col11:
        st.metric("Training Cost", f"₹{training_cost:,.0f}")

    with col12:
        st.metric("Total Expected Budget", f"₹{total_expected_budget:,.0f}")

    st.markdown('</div>', unsafe_allow_html=True)

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
            "local_travel_per_day": local_travel_per_day,
            "local_travel_total": local_travel_total,
            "outstation_travel_mode": outstation_travel_mode,
            "going_travel_cost": going_travel_cost,
            "return_travel_cost": return_travel_cost,
            "outstation_travel_total": outstation_travel_total,
            "total_travel_cost": total_travel_cost,
            "stay_cost": stay_cost,
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

        requests_df.to_csv(REQUESTS_FILE, index=False)

        st.success("Request sent successfully!")