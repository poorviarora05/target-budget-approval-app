import streamlit as st
import pandas as pd

REQUESTS_FILE = "requests.csv"


def show_director_approval():
    st.header("Director Approval")
    try:
    requests_df = pd.read_csv("requests.csv")

    pending_director = requests_df[
        requests_df["request_status"]
        == "Pending Director Approval"
    ]

    if len(pending_director) > 0:

        st.warning(
            f"🔔 {len(pending_director)} request(s) waiting for Director approval!"
        )

        st.balloons()

except:
    pass

    try:
        requests_df = pd.read_csv(REQUESTS_FILE)
    except:
        st.error("No requests found.")
        return

    pending_requests = requests_df[
        requests_df["request_status"] == "Pending Director Approval"
    ]
    if not pending_requests.empty:
    st.toast("New request received from mediator for approval!")
    st.success(
        f"🔔 {len(pending_requests)} new request(s) pending for Director approval."
    )

    if pending_requests.empty:
        st.info("No requests pending for director approval.")
        return

    request_id = st.selectbox("Select Request", pending_requests["request_id"])

    selected_request = pending_requests[
        pending_requests["request_id"] == request_id
    ].iloc[0]

    st.subheader("Request Details")
    st.write(selected_request)

    director_remarks = st.text_area("Director Remarks")

    decision = st.selectbox("Decision", ["Approve", "Reject"])

    if st.button("Submit Director Decision"):

        index = requests_df[
            requests_df["request_id"] == request_id
        ].index[0]

        requests_df.loc[index, "director_remarks"] = director_remarks

        if decision == "Approve":
            requests_df.loc[index, "request_status"] = "Director Approved"
            requester_email = selected_request["requester_email"]

            send_approval_email(
            requester_email,
            selected_request["request_id"],
            selected_request["college_name"],
            selected_request["training_topic"]
)

        else:
            requests_df.loc[index, "request_status"] = "Director Rejected"

        requests_df.to_csv(REQUESTS_FILE, index=False)

        st.success("Director decision submitted successfully.")