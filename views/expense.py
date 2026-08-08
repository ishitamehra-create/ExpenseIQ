import streamlit as st
import pandas as pd

from database import (
    add_expense,
    get_expense,
    delete_expense,
    update_expense
)


def expense_page():

    st.title("💸 Add Expense")

    st.write("Add your expense details below.")

    st.divider()

    # =============================
    # Add Expense
    # =============================

    with st.form("expense_form"):

        amount = st.number_input(
            "Amount (₹)",
            min_value=0.0,
            step=100.0
        )

        category = st.selectbox(
            "Category",
            [
                "Food",
                "Travel",
                "Shopping",
                "Bills",
                "Entertainment",
                "Medical",
                "Education",
                "Other"
            ]
        )

        date = st.date_input("Date")

        submit = st.form_submit_button("Save Expense")

    if submit:

        if amount == 0:

            st.warning(
                "Please enter a valid amount."
            )

        else:

            add_expense(
                amount,
                category,
                str(date)
            )

            st.success(
                "✅ Expense added successfully!"
            )

            st.rerun()

    st.divider()

    # =============================
    # Expense History
    # =============================

    st.subheader("📋 Expense History")

    expense_data = get_expense()

    if expense_data:

        expense_df = pd.DataFrame(
            expense_data,
            columns=[
                "ID",
                "Amount",
                "Category",
                "Date"
            ]
        )

        st.dataframe(
            expense_df,
            use_container_width=True,
            hide_index=True
        )

        st.divider()

        # =============================
        # Edit Expense
        # =============================

        st.subheader("✏️ Edit Expense")

        expense_ids = expense_df["ID"].tolist()

        selected_edit_id = st.selectbox(
            "Select Expense ID to Edit",
            expense_ids,
            key="edit_expense_id"
        )

        selected_expense = expense_df[
            expense_df["ID"] == selected_edit_id
        ].iloc[0]

        with st.form("edit_expense_form"):

            edit_amount = st.number_input(
                "Amount (₹)",
                min_value=0.0,
                value=float(
                    selected_expense["Amount"]
                ),
                step=100.0
            )

            category_options = [
                "Food",
                "Travel",
                "Shopping",
                "Bills",
                "Entertainment",
                "Medical",
                "Education",
                "Other"
            ]

            current_category = selected_expense[
                "Category"
            ]

            if current_category in category_options:

                category_index = category_options.index(
                    current_category
                )

            else:

                category_index = 0

            edit_category = st.selectbox(
                "Category",
                category_options,
                index=category_index
            )

            edit_date = st.date_input(
                "Date",
                value=pd.to_datetime(
                    selected_expense["Date"]
                ).date()
            )

            update_button = st.form_submit_button(
                "✏️ Update Expense"
            )

        if update_button:

            if edit_amount == 0:

                st.warning(
                    "Please enter a valid amount."
                )

            else:

                update_expense(
                    selected_edit_id,
                    edit_amount,
                    edit_category,
                    str(edit_date)
                )

                st.success(
                    "✅ Expense updated successfully!"
                )

                st.rerun()

        st.divider()

        # =============================
        # Delete Expense
        # =============================

        st.subheader("🗑️ Delete Expense")

        selected_delete_id = st.selectbox(
            "Select Expense ID",
            expense_ids,
            key="delete_expense_id"
        )

        if st.button(
            "🗑️ Delete Expense"
        ):

            delete_expense(
                selected_delete_id
            )

            st.success(
                "✅ Expense deleted successfully!"
            )

            st.rerun()

    else:

        st.info(
            "No expense records found."
        )