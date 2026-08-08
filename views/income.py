import streamlit as st
import pandas as pd

from database import (
    add_income,
    get_income,
    delete_income,
    update_income
)


def income_page():

    st.title("💵 Add Income")

    st.write("Add your income details below.")

    st.divider()

    # =============================
    # Add Income
    # =============================

    with st.form("income_form"):

        amount = st.number_input(
            "Amount (₹)",
            min_value=0.0,
            step=100.0
        )

        source = st.selectbox(
            "Income Source",
            [
                "Salary",
                "Freelancing",
                "Business",
                "Investment",
                "Gift",
                "Other"
            ]
        )

        date = st.date_input("Date")

        submit = st.form_submit_button("Save Income")

    if submit:

        if amount == 0:
            st.warning("Please enter a valid amount.")

        else:

            add_income(
                amount,
                source,
                str(date)
            )

            st.success("✅ Income added successfully!")

    st.divider()

    # =============================
    # Income History
    # =============================

    st.subheader("📋 Income History")

    income_data = get_income()

    if income_data:

        income_df = pd.DataFrame(
            income_data,
            columns=["ID", "Amount", "Source", "Date"]
        )

        st.dataframe(
            income_df,
            use_container_width=True,
            hide_index=True
        )

        st.divider()

        # =============================
        # Edit Income
        # =============================

        st.subheader("✏️ Edit Income")

        income_ids = income_df["ID"].tolist()

        selected_edit_id = st.selectbox(
            "Select Income ID to Edit",
            income_ids,
            key="edit_income_id"
        )

        selected_income = income_df[
            income_df["ID"] == selected_edit_id
        ].iloc[0]

        with st.form("edit_income_form"):

            edit_amount = st.number_input(
                "Amount (₹)",
                min_value=0.0,
                value=float(selected_income["Amount"]),
                step=100.0
            )

            source_options = [
                "Salary",
                "Freelancing",
                "Business",
                "Investment",
                "Gift",
                "Other"
            ]

            current_source = selected_income["Source"]

            if current_source in source_options:
                source_index = source_options.index(current_source)
            else:
                source_index = 0

            edit_source = st.selectbox(
                "Income Source",
                source_options,
                index=source_index
            )

            edit_date = st.date_input(
                "Date",
                value=pd.to_datetime(
                    selected_income["Date"]
                ).date()
            )

            update_button = st.form_submit_button(
                "✏️ Update Income"
            )

        if update_button:

            if edit_amount == 0:

                st.warning(
                    "Please enter a valid amount."
                )

            else:

                update_income(
                    selected_edit_id,
                    edit_amount,
                    edit_source,
                    str(edit_date)
                )

                st.success(
                    "✅ Income updated successfully!"
                )

                st.rerun()

        st.divider()

        # =============================
        # Delete Income
        # =============================

        st.subheader("🗑️ Delete Income")

        selected_delete_id = st.selectbox(
            "Select Income ID",
            income_ids,
            key="delete_income_id"
        )

        if st.button("🗑️ Delete Income"):

            delete_income(selected_delete_id)

            st.success(
                "✅ Income deleted successfully!"
            )

            st.rerun()

    else:

        st.info("No income records found.")