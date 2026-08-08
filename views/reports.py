import streamlit as st
import pandas as pd
import plotly.express as px

from database import (
    get_total_income,
    get_total_expense,
    get_income,
    get_expense
)


def reports_page():

    st.title("📊 Reports & Analytics")

    st.markdown(
        "### Analyze your income, expenses and overall financial health."
    )

    # =========================================================
    # FINANCIAL SUMMARY
    # =========================================================

    total_income = get_total_income()
    total_expense = get_total_expense()
    balance = total_income - total_expense

    if total_income > 0:
        savings_rate = (balance / total_income) * 100
    else:
        savings_rate = 0

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "💵 Total Income",
            f"₹ {total_income:,.2f}"
        )

    with col2:
        st.metric(
            "💸 Total Expense",
            f"₹ {total_expense:,.2f}"
        )

    with col3:
        st.metric(
            "💰 Balance",
            f"₹ {balance:,.2f}"
        )

    with col4:
        st.metric(
            "📈 Savings Rate",
            f"{savings_rate:.1f}%"
        )

    st.divider()

    # =========================================================
    # INCOME HISTORY
    # =========================================================

    st.subheader("💵 Income History")

    income = get_income()

    if income:

        income_df = pd.DataFrame(
            income,
            columns=[
                "ID",
                "Amount",
                "Source",
                "Date"
            ]
        )

        # -------------------------
        # Search Income
        # -------------------------

        income_search = st.text_input(
            "🔍 Search Income Source",
            placeholder="Example: Salary, Freelancing...",
            key="income_search"
        )

        filtered_income = income_df.copy()

        if income_search:

            filtered_income = filtered_income[
                filtered_income["Source"].str.contains(
                    income_search,
                    case=False,
                    na=False
                )
            ]

        # -------------------------
        # Income Date Filter
        # -------------------------

        if not filtered_income.empty:

            income_dates = pd.to_datetime(
                filtered_income["Date"]
            )

            min_income_date = income_dates.min().date()
            max_income_date = income_dates.max().date()

            income_date_range = st.date_input(
                "📅 Filter Income by Date",
                value=(
                    min_income_date,
                    max_income_date
                ),
                min_value=min_income_date,
                max_value=max_income_date,
                key="income_date_filter"
            )

            if len(income_date_range) == 2:

                start_date = pd.to_datetime(
                    income_date_range[0]
                )

                end_date = pd.to_datetime(
                    income_date_range[1]
                )

                filtered_income = filtered_income[
                    (
                        pd.to_datetime(
                            filtered_income["Date"]
                        ) >= start_date
                    )
                    &
                    (
                        pd.to_datetime(
                            filtered_income["Date"]
                        ) <= end_date
                    )
                ]

        # -------------------------
        # Income Table
        # -------------------------

        if not filtered_income.empty:

            st.dataframe(
                filtered_income,
                use_container_width=True,
                hide_index=True
            )

            income_csv = filtered_income.to_csv(
                index=False
            ).encode("utf-8")

            st.download_button(
                "📥 Download Income CSV",
                data=income_csv,
                file_name="income_report.csv",
                mime="text/csv",
                key="income_download"
            )

        else:

            st.warning(
                "No income records match your filter."
            )

    else:

        st.info("No income records available.")

    st.divider()

    # =========================================================
    # EXPENSE HISTORY
    # =========================================================

    st.subheader("💸 Expense History")

    expense = get_expense()

    if expense:

        expense_df = pd.DataFrame(
            expense,
            columns=[
                "ID",
                "Amount",
                "Category",
                "Date"
            ]
        )

        # -------------------------
        # Search Expense
        # -------------------------

        expense_search = st.text_input(
            "🔍 Search Expense Category",
            placeholder="Example: Food, Travel, Bills...",
            key="expense_search"
        )

        filtered_expense = expense_df.copy()

        if expense_search:

            filtered_expense = filtered_expense[
                filtered_expense["Category"].str.contains(
                    expense_search,
                    case=False,
                    na=False
                )
            ]

        # -------------------------
        # Expense Date Filter
        # -------------------------

        if not filtered_expense.empty:

            expense_dates = pd.to_datetime(
                filtered_expense["Date"]
            )

            min_expense_date = expense_dates.min().date()
            max_expense_date = expense_dates.max().date()

            expense_date_range = st.date_input(
                "📅 Filter Expense by Date",
                value=(
                    min_expense_date,
                    max_expense_date
                ),
                min_value=min_expense_date,
                max_value=max_expense_date,
                key="expense_date_filter"
            )

            if len(expense_date_range) == 2:

                start_date = pd.to_datetime(
                    expense_date_range[0]
                )

                end_date = pd.to_datetime(
                    expense_date_range[1]
                )

                filtered_expense = filtered_expense[
                    (
                        pd.to_datetime(
                            filtered_expense["Date"]
                        ) >= start_date
                    )
                    &
                    (
                        pd.to_datetime(
                            filtered_expense["Date"]
                        ) <= end_date
                    )
                ]

        # -------------------------
        # Expense Table
        # -------------------------

        if not filtered_expense.empty:

            st.dataframe(
                filtered_expense,
                use_container_width=True,
                hide_index=True
            )

            expense_csv = filtered_expense.to_csv(
                index=False
            ).encode("utf-8")

            st.download_button(
                "📥 Download Expense CSV",
                data=expense_csv,
                file_name="expense_report.csv",
                mime="text/csv",
                key="expense_download"
            )

        else:

            st.warning(
                "No expense records match your filter."
            )

    else:

        st.info("No expense records available.")

    st.divider()

    # =========================================================
    # VISUAL ANALYTICS
    # =========================================================

    st.subheader("📊 Visual Analytics")

    # =========================================================
    # INCOME VS EXPENSE
    # =========================================================

    comparison_df = pd.DataFrame(
        {
            "Type": [
                "Income",
                "Expense"
            ],
            "Amount": [
                total_income,
                total_expense
            ]
        }
    )

    fig_comparison = px.bar(
        comparison_df,
        x="Type",
        y="Amount",
        text="Amount",
        title="Income vs Expense",
        labels={
            "Amount": "Amount (₹)",
            "Type": "Financial Type"
        }
    )

    fig_comparison.update_traces(
        texttemplate="₹ %{text:,.0f}",
        textposition="outside"
    )

    st.plotly_chart(
        fig_comparison,
        use_container_width=True
    )

    # =========================================================
    # CATEGORY / SOURCE CHARTS
    # =========================================================

    chart_col1, chart_col2 = st.columns(2)

    # -------------------------
    # Expense Category Chart
    # -------------------------

    with chart_col1:

        st.subheader("💸 Expense by Category")

        if expense:

            expense_chart_df = pd.DataFrame(
                expense,
                columns=[
                    "ID",
                    "Amount",
                    "Category",
                    "Date"
                ]
            )

            expense_summary = (
                expense_chart_df
                .groupby("Category")["Amount"]
                .sum()
                .reset_index()
            )

            fig_expense = px.pie(
                expense_summary,
                names="Category",
                values="Amount",
                hole=0.4,
                title="Expense Distribution"
            )

            st.plotly_chart(
                fig_expense,
                use_container_width=True
            )

        else:

            st.info(
                "No expense data available."
            )

    # -------------------------
    # Income Source Chart
    # -------------------------

    with chart_col2:

        st.subheader("💵 Income by Source")

        if income:

            income_chart_df = pd.DataFrame(
                income,
                columns=[
                    "ID",
                    "Amount",
                    "Source",
                    "Date"
                ]
            )

            income_summary = (
                income_chart_df
                .groupby("Source")["Amount"]
                .sum()
                .reset_index()
            )

            fig_income = px.pie(
                income_summary,
                names="Source",
                values="Amount",
                hole=0.4,
                title="Income Distribution"
            )

            st.plotly_chart(
                fig_income,
                use_container_width=True
            )

        else:

            st.info(
                "No income data available."
            )

    st.divider()

    # =========================================================
    # FINANCIAL STATUS
    # =========================================================

    st.subheader("📈 Financial Status")

    if balance > 0:

        st.success(
            "🎉 Great! Your income is higher than your expenses."
        )

    elif balance == 0:

        st.warning(
            "Your income and expenses are currently equal."
        )

    else:

        st.error(
            "⚠️ Your expenses are greater than your income."
        )

    st.divider()

    st.caption("ExpenseIQ © 2026")