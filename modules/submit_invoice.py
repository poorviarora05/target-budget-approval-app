import streamlit as st
import pandas as pd
from datetime import datetime
import os

REQUESTS_FILE = "requests.csv"
INVOICES_FILE = "invoices.csv"
UPLOAD_FOLDER = "onedrive_invoices"


def safe_number(value):
    try:
        if pd.isna(value):
            return 0
        return float(value)
    except:
        return 0


def save_uploaded_file(uploaded_file, request_id, invoice_type):
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_name = uploaded_file.name.replace(" ", "_")
    file_name = f"{request_id}_{invoice_type}_{timestamp}_{safe_name}"
    file_path = os.path.join(UPLOAD_FOLDER, file_name)

    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    return file_name, file_path


def get_approved_budget(selected_request):
    budget = safe_number(selected_request.get("partner_final_available_budget", 0))

    if budget == 0:
        budget = safe_number(selected_request.get("available_budget", 0))

    if budget == 0:
        budget = safe_number(selected_request.get("total_available_budget", 0))

    if budget == 0:
        budget = safe_number(selected_request.get("estimated_budget", 0))

    return budget


def show_submit_invoice():

    st.header("Trainer Invoice Submission")

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
        requests_df["request_status"].isin(["Approved", "Director Approved"])
    ]

    if approved_requests.empty:
        st.info("No approved requests available for invoice submission.")
        return

    request_id = st.selectbox(
        "Select Approved Request",
        approved_requests["request_id"]
    )

    selected_request = approved_requests[
        approved_requests["request_id"] == request_id
    ].iloc[0]

    approved_budget = get_approved_budget(selected_request)

    st.subheader("Approved Request Summary")

    summary_df = pd.DataFrame({
        "Field": [
            "College / University",
            "Training Topic",
            "Trainer Name",
            "Training Start Date",
            "Training End Date",
            "Approved Budget"
        ],
        "Details": [
            selected_request.get("college_name", ""),
            selected_request.get("training_topic", ""),
            selected_request.get("trainer_name", ""),
            selected_request.get("start_date", ""),
            selected_request.get("end_date", ""),
            f"₹{approved_budget:,.0f}"
        ]
    })

    st.table(summary_df)

    st.subheader("Section 1: Training Invoice")

    training_invoice_file = st.file_uploader(
        "Upload Training Invoice",
        type=["pdf", "png", "jpg", "jpeg", "xlsx", "xls"],
        key="training_invoice_file"
    )

    training_invoice_amount = st.number_input(
        "Training Invoice Amount",
        min_value=0,
        value=0,
        step=500
    )

    training_invoice_remarks = st.text_area(
        "Training Invoice Remarks",
        key="training_invoice_remarks"
    )

    st.subheader("Section 2: Stay / Travel / Food / Other Bills")

    expense_files = st.file_uploader(
        "Upload Stay, Travel, Food, Swiggy, Restaurant, Taxi or Other Bills",
        type=["pdf", "png", "jpg", "jpeg", "xlsx", "xls"],
        accept_multiple_files=True,
        key="expense_bill_files"
    )

    stay_amount = st.number_input("Stay Bills Amount", min_value=0, value=0, step=500)
    travel_amount = st.number_input("Travel Bills Amount", min_value=0, value=0, step=500)
    food_amount = st.number_input("Food / Restaurant / Swiggy Bills Amount", min_value=0, value=0, step=500)
    other_amount = st.number_input("Other Bills Amount", min_value=0, value=0, step=500)

    expense_remarks = st.text_area(
        "Expense Bills Remarks",
        key="expense_remarks"
    )

    total_expense_amount = (
        training_invoice_amount
        + stay_amount
        + travel_amount
        + food_amount
        + other_amount
    )

    remaining_budget = approved_budget - total_expense_amount

    st.subheader("Budget Validation")

    c1, c2, c3 = st.columns(3)

    c1.metric("Approved Budget", f"₹{approved_budget:,.0f}")
    c2.metric("Total Invoice Amount", f"₹{total_expense_amount:,.0f}")
    c3.metric("Balance / Excess", f"₹{remaining_budget:,.0f}")

    if approved_budget == 0:
        invoice_status = "Under Consideration"
        st.warning("Approved budget not found. Invoice will be marked under consideration.")
    elif total_expense_amount <= approved_budget:
        invoice_status = "Approved for Payment"
        st.success("Invoice amount is within the approved budget. It can be approved for payment.")
    else:
        invoice_status = "Under Consideration"
        st.warning("Invoice amount exceeds the approved budget. It will be taken under consideration.")

    if st.button("Submit Invoices"):

        if training_invoice_file is None and not expense_files:
            st.error("Please upload at least one invoice or bill.")
            return

        saved_files = []

        if training_invoice_file is not None:
            file_name, file_path = save_uploaded_file(
                training_invoice_file,
                request_id,
                "training_invoice"
            )

            saved_files.append({
                "invoice_id": f"INV{len(invoices_df) + len(saved_files) + 1:03d}",
                "request_id": request_id,
                "invoice_type": "Training Invoice",
                "file_name": file_name,
                "file_path": file_path,
                "amount": training_invoice_amount,
                "approved_budget": approved_budget,
                "total_invoice_amount": total_expense_amount,
                "remaining_budget": remaining_budget,
                "invoice_status": invoice_status,
                "remarks": training_invoice_remarks,
                "submitted_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })

        for uploaded_file in expense_files:
            file_name, file_path = save_uploaded_file(
                uploaded_file,
                request_id,
                "expense_bill"
            )

            saved_files.append({
                "invoice_id": f"INV{len(invoices_df) + len(saved_files) + 1:03d}",
                "request_id": request_id,
                "invoice_type": "Expense Bill",
                "file_name": file_name,
                "file_path": file_path,
                "amount": stay_amount + travel_amount + food_amount + other_amount,
                "approved_budget": approved_budget,
                "total_invoice_amount": total_expense_amount,
                "remaining_budget": remaining_budget,
                "invoice_status": invoice_status,
                "remarks": expense_remarks,
                "submitted_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })

        invoices_df = pd.concat(
            [invoices_df, pd.DataFrame(saved_files)],
            ignore_index=True
        )

        invoices_df.to_csv(INVOICES_FILE, index=False)

        st.success("Invoices uploaded and saved successfully.")
        st.info(f"Files saved in folder: {UPLOAD_FOLDER}")
        st.info(f"Invoice records saved in: {INVOICES_FILE}")
