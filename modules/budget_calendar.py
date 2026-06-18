import streamlit as st
import pandas as pd

REQUESTS_FILE = "requests.csv"


def show_budget_calendar():

    st.header("Budget Calendar")

    try:
        requests_df = pd.read_csv(REQUESTS_FILE)
    except:
        st.error("No request data found.")
        return

    st.write("Budget calendar file is connected successfully.")

    st.dataframe(
        requests_df,
        use_container_width=True
    )
