import streamlit.components.v1 as components
import streamlit as st
import pandas as pd
from datetime import datetime

REQUESTS_FILE = "requests.csv"
INVOICES_FILE = "invoices.csv"


def show_submit_invoice():

    st.header("Generate Invoice")

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
        st.info("No approved requests available for invoice generation.")
        return

    request_id = st.selectbox(
        "Select Approved Request",
        approved_requests["request_id"]
    )

    selected_request = approved_requests[
        approved_requests["request_id"] == request_id
    ].iloc[0]

    st.subheader("Invoice Details")

    col1, col2 = st.columns(2)

    with col1:
        company_name = st.text_input("Company Name", "Trainer Services Pvt. Ltd.")
        company_address = st.text_area("Company Address", "New Delhi, India")
        bill_to = st.text_input(
            "Bill To",
            selected_request.get("college_name", "")
        )

    with col2:
        invoice_number = st.text_input(
            "Invoice Number",
            f"INV{len(invoices_df) + 1:03d}"
        )
        invoice_date = st.date_input("Invoice Date")
        due_date = st.date_input("Due Date")

    st.subheader("Expense Details")

    service_fee = st.number_input("Service / Trainer Fee", min_value=0, value=0)
    stay_expense = st.number_input("Stay Expense", min_value=0, value=0)
    travel_expense = st.number_input("Travel Expense", min_value=0, value=0)
    food_expense = st.number_input("Food Expense", min_value=0, value=0)
    material_expense = st.number_input("Training Material Expense", min_value=0, value=0)
    other_expense = st.number_input("Other Expense", min_value=0, value=0)

    tax_rate = st.number_input(
        "Tax Rate (%)",
        min_value=0.0,
        value=18.0
    )

    subtotal = (
        service_fee
        + stay_expense
        + travel_expense
        + food_expense
        + material_expense
        + other_expense
    )

    tax_amount = subtotal * tax_rate / 100
    total_amount = subtotal + tax_amount

    comments = st.text_area(
        "Other Comments",
        "Payment due within 30 days."
    )

    invoice_html = f"""
    <div style="background:white; padding:35px; border-radius:14px; border:1px solid #d1d5db; font-family:Arial; color:#111827;">

        <div style="display:flex; justify-content:space-between; align-items:flex-start;">
            <div>
                <h2 style="color:#1e3a8a; margin-bottom:4px;">{company_name}</h2>
                <p style="white-space:pre-line;">{company_address}</p>
            </div>

            <div style="text-align:right;">
                <h1 style="color:#64748b; letter-spacing:2px;">INVOICE</h1>
                <p><b>Date:</b> {invoice_date}</p>
                <p><b>Invoice #:</b> {invoice_number}</p>
                <p><b>Due Date:</b> {due_date}</p>
            </div>
        </div>

        <hr style="margin:25px 0;">

        <h3 style="background:#1e3a8a; color:white; padding:10px; border-radius:6px;">
            BILL TO
        </h3>

        <p>{bill_to}</p>

        <table style="width:100%; border-collapse:collapse; margin-top:22px;">
            <tr style="background:#1e3a8a; color:white;">
                <th style="padding:12px; text-align:left;">Description</th>
                <th style="padding:12px; text-align:right;">Amount</th>
            </tr>

            <tr>
                <td style="padding:10px; border-bottom:1px solid #e5e7eb;">Service / Trainer Fee</td>
                <td style="padding:10px; border-bottom:1px solid #e5e7eb; text-align:right;">₹{service_fee}</td>
            </tr>

            <tr>
                <td style="padding:10px; border-bottom:1px solid #e5e7eb;">Stay Expense</td>
                <td style="padding:10px; border-bottom:1px solid #e5e7eb; text-align:right;">₹{stay_expense}</td>
            </tr>

            <tr>
                <td style="padding:10px; border-bottom:1px solid #e5e7eb;">Travel Expense</td>
                <td style="padding:10px; border-bottom:1px solid #e5e7eb; text-align:right;">₹{travel_expense}</td>
            </tr>

            <tr>
                <td style="padding:10px; border-bottom:1px solid #e5e7eb;">Food Expense</td>
                <td style="padding:10px; border-bottom:1px solid #e5e7eb; text-align:right;">₹{food_expense}</td>
            </tr>

            <tr>
                <td style="padding:10px; border-bottom:1px solid #e5e7eb;">Training Material</td>
                <td style="padding:10px; border-bottom:1px solid #e5e7eb; text-align:right;">₹{material_expense}</td>
            </tr>

            <tr>
                <td style="padding:10px; border-bottom:1px solid #e5e7eb;">Other Expense</td>
                <td style="padding:10px; border-bottom:1px solid #e5e7eb; text-align:right;">₹{other_expense}</td>
            </tr>
        </table>

        <div style="text-align:right; margin-top:25px;">
            <p><b>Subtotal:</b> ₹{subtotal}</p>
            <p><b>Tax ({tax_rate}%):</b> ₹{tax_amount}</p>
            <h2 style="color:#1e3a8a;">TOTAL: ₹{total_amount}</h2>
        </div>

        <h3 style="background:#1e3a8a; color:white; padding:10px; border-radius:6px;">
            OTHER COMMENTS
        </h3>

        <p>{comments}</p>

        <p style="text-align:center; margin-top:30px;">
            <b>Thank You For Your Business!</b>
        </p>

    </div>
    """

    st.subheader("Invoice Preview")

    components.html(
    invoice_html,
    height=900,
    scrolling=True
)

    if st.button("Submit Invoice"):

        new_invoice = {
            "invoice_id": invoice_number,
            "request_id": request_id,
            "company_name": company_name,
            "bill_to": bill_to,
            "invoice_date": str(invoice_date),
            "due_date": str(due_date),
            "service_fee": service_fee,
            "stay_expense": stay_expense,
            "travel_expense": travel_expense,
            "food_expense": food_expense,
            "material_expense": material_expense,
            "other_expense": other_expense,
            "subtotal": subtotal,
            "tax_rate": tax_rate,
            "tax_amount": tax_amount,
            "total_amount": total_amount,
            "invoice_status": "Pending Director Invoice Approval",
            "submitted_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        invoices_df = pd.concat(
            [invoices_df, pd.DataFrame([new_invoice])],
            ignore_index=True
        )

        invoices_df.to_csv(
            INVOICES_FILE,
            index=False
        )

        st.success("Invoice generated and submitted successfully.")