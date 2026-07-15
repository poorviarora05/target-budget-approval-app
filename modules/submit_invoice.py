import streamlit as st
import pandas as pd
from datetime import datetime
import os

REQUESTS_FILE = "requests.csv"
INVOICES_FILE = "invoices.csv"


def show_submit_invoice():
    st.header("Submit Invoice")

    try:
        requests_df = pd.read_csv(REQUESTS_FILE)
    except:
        st.error("No approved requests found.")
        return

    try:
        invoices_df = pd.read_csv(INVOICES_FILE)
    except:
        invoices_df = pd.DataFrame()

    approved_requests = requests_df[
        requests_df["request_status"] == "Director Approved"
    ]

    if approved_requests.empty:
        st.info("No director-approved requests available.")
        return

    request_id = st.selectbox(
        "Select Approved Request",
        approved_requests["request_id"]
    )

    selected_request = approved_requests[
        approved_requests["request_id"] == request_id
    ].iloc[0]

    st.subheader("Approved Request Details")
    st.write(selected_request)

    st.subheader("Actual Expense Details")

    trainer_fee = st.number_input("Actual Trainer Fee", min_value=0, value=0)
    stay_expense = st.number_input("Actual Stay Expense", min_value=0, value=0)
    travel_expense = st.number_input("Actual Travel Expense", min_value=0, value=0)
    food_expense = st.number_input("Actual Food Expense", min_value=0, value=0)
    training_material_expense = st.number_input("Actual Training Material Expense", min_value=0, value=0)
    other_expense = st.number_input("Actual Other Expense", min_value=0, value=0)

    invoice_file = st.file_uploader(
        "Upload Invoice / Bill",
        type=["pdf", "png", "jpg", "jpeg"]
    )

    total_actual_expense = (
        trainer_fee
        + stay_expense
        + travel_expense
        + food_expense
        + training_material_expense
        + other_expense
    )

    st.write("Total Actual Expense:", total_actual_expense)

    if st.button("Submit Invoice"):
        invoice_id = f"INV{len(invoices_df) + 1:03d}"

        file_path = ""

        if invoice_file is not None:
            os.makedirs("uploaded_invoices", exist_ok=True)
            file_path = f"uploaded_invoices/{invoice_id}_{invoice_file.name}"

            with open(file_path, "wb") as f:
                f.write(invoice_file.getbuffer())

        new_invoice = {
            "invoice_id": invoice_id,
            "request_id": request_id,
            "trainer_fee": trainer_fee,
            "stay_expense": stay_expense,
            "travel_expense": travel_expense,
            "food_expense": food_expense,
            "training_material_expense": training_material_expense,
            "other_expense": other_expense,
            "total_actual_expense": total_actual_expense,
            "invoice_file": file_path,
            "invoice_status": "Pending Director Invoice Approval",
            "submitted_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        invoices_df = pd.concat(
            [invoices_df, pd.DataFrame([new_invoice])],
            ignore_index=True
        )

        invoices_df.to_csv(INVOICES_FILE, index=False)

        st.success("Invoice submitted successfully.")