import streamlit as st
import pandas as pd

INVOICES_FILE = "invoices.csv"


def show_invoice_approval():
    st.header("Director Invoice Approval")

    try:
        invoices_df = pd.read_csv(INVOICES_FILE)
    except:
        st.error("No invoices found.")
        return

    pending_invoices = invoices_df[
        invoices_df["invoice_status"] == "Pending Director Invoice Approval"
    ]

    if pending_invoices.empty:
        st.info("No pending invoices.")
        return

    invoice_id = st.selectbox(
        "Select Invoice",
        pending_invoices["invoice_id"]
    )

    selected_invoice = pending_invoices[
        pending_invoices["invoice_id"] == invoice_id
    ].iloc[0]

    st.subheader("Invoice Details")
    st.write(selected_invoice)

    director_invoice_remarks = st.text_area("Director Invoice Remarks")

    decision = st.selectbox(
        "Decision",
        ["Approve Payment", "Reject Invoice"]
    )

    if st.button("Submit Invoice Decision"):
        index = invoices_df[
            invoices_df["invoice_id"] == invoice_id
        ].index[0]

        invoices_df.loc[index, "director_invoice_remarks"] = director_invoice_remarks
        invoices_df.loc[index, "invoice_status"] = decision

        invoices_df.to_csv(INVOICES_FILE, index=False)

        st.success("Invoice decision submitted successfully.")