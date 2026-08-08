import streamlit as st
import pandas as pd
import plotly.express as px

from database import (
    get_total_income,
    get_total_expense,
    get_income,
    get_expense,
    expense_category_summary,
    income_source_summary,
    get_budget,
    set_budget
)


def dashboard_page():

    st.title("💰 ExpenseIQ")

    st.markdown("### Track Smart. Spend Better.")

    st.write(
        "Welcome to ExpenseIQ! Manage your income, expenses and savings in one place."
    )

    st.divider()

    # =========================================================
    # GET DATA
    # =========================================================

    total_income = get_total_income()
    total_expense = get_total_expense()
    balance = total_income - total_expense

    income = get_income()
    expense = get_expense()

    # =========================================================
    # DASHBOARD CARDS
    # =========================================================

    col1, col2, col3 = st.columns(3)

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

    st.divider()

    # =========================================================
    # MONTHLY ANALYSIS
    # =========================================================

    st.subheader("📅 Monthly Analysis")

    if income or expense:

        # -------------------------
        # Prepare Income Data
        # -------------------------

        if income:

            monthly_income_df = pd.DataFrame(
                income,
                columns=[
                    "ID",
                    "Amount",
                    "Source",
                    "Date"
                ]
            )

            monthly_income_df["Date"] = pd.to_datetime(
                monthly_income_df["Date"]
            )

            monthly_income_df["Month"] = (
                monthly_income_df["Date"]
                .dt.to_period("M")
                .astype(str)
            )

            income_monthly = (
                monthly_income_df
                .groupby("Month")["Amount"]
                .sum()
                .reset_index()
            )

            income_monthly.rename(
                columns={"Amount": "Income"},
                inplace=True
            )

        else:

            income_monthly = pd.DataFrame(
                columns=["Month", "Income"]
            )

        # -------------------------
        # Prepare Expense Data
        # -------------------------

        if expense:

            monthly_expense_df = pd.DataFrame(
                expense,
                columns=[
                    "ID",
                    "Amount",
                    "Category",
                    "Date"
                ]
            )

            monthly_expense_df["Date"] = pd.to_datetime(
                monthly_expense_df["Date"]
            )

            monthly_expense_df["Month"] = (
                monthly_expense_df["Date"]
                .dt.to_period("M")
                .astype(str)
            )

            expense_monthly = (
                monthly_expense_df
                .groupby("Month")["Amount"]
                .sum()
                .reset_index()
            )

            expense_monthly.rename(
                columns={"Amount": "Expense"},
                inplace=True
            )

        else:

            expense_monthly = pd.DataFrame(
                columns=["Month", "Expense"]
            )

        # -------------------------
        # Combine Income + Expense
        # -------------------------

        monthly_df = pd.merge(
            income_monthly,
            expense_monthly,
            on="Month",
            how="outer"
        ).fillna(0)

        monthly_df["Balance"] = (
            monthly_df["Income"]
            - monthly_df["Expense"]
        )

        monthly_df = monthly_df.sort_values(
            "Month"
        )

        # -------------------------
        # Monthly Chart
        # -------------------------

        chart_df = monthly_df.melt(
            id_vars="Month",
            value_vars=[
                "Income",
                "Expense"
            ],
            var_name="Type",
            value_name="Amount"
        )

        fig_monthly = px.bar(
            chart_df,
            x="Month",
            y="Amount",
            color="Type",
            barmode="group",
            text="Amount",
            title="Monthly Income vs Expense"
        )

        fig_monthly.update_traces(
            texttemplate="₹ %{text:,.0f}",
            textposition="outside"
        )

        st.plotly_chart(
            fig_monthly,
            use_container_width=True
        )

        # -------------------------
        # Monthly Summary Table
        # -------------------------

        display_monthly = monthly_df.copy()

        display_monthly.columns = [
            "Month",
            "Income",
            "Expense",
            "Balance"
        ]

        st.dataframe(
            display_monthly,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info(
            "Add income or expense records to see monthly analysis."
        )

    st.divider()

    # =========================================================
    # RECENT INCOME
    # =========================================================

    st.subheader("💵 Recent Income")

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

        st.dataframe(
            income_df,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info(
            "No income records found."
        )

    st.divider()

    # =========================================================
    # RECENT EXPENSES
    # =========================================================

    st.subheader("💸 Recent Expenses")

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

        st.dataframe(
            expense_df,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info(
            "No expense records found."
        )

    st.divider()

    # =========================================================
    # EXPENSE & INCOME CHARTS
    # =========================================================

    st.subheader("📊 Spending & Income Overview")

    col1, col2 = st.columns(2)

    # -------------------------
    # Expense Chart
    # -------------------------

    with col1:

        st.markdown("#### 💸 Expense Analysis")

        expense_chart = expense_category_summary()

        if expense_chart:

            expense_chart_df = pd.DataFrame(
                expense_chart,
                columns=[
                    "Category",
                    "Amount"
                ]
            )

            fig_expense = px.pie(
                expense_chart_df,
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
    # Income Chart
    # -------------------------

    with col2:

        st.markdown("#### 💵 Income Analysis")

        income_chart = income_source_summary()

        if income_chart:

            income_chart_df = pd.DataFrame(
                income_chart,
                columns=[
                    "Source",
                    "Amount"
                ]
            )

            fig_income = px.pie(
                income_chart_df,
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
    # MONTHLY BUDGET
    # =========================================================

    st.subheader("🎯 Monthly Budget")

    budget = get_budget()

    new_budget = st.number_input(
        "Set Monthly Budget (₹)",
        min_value=0.0,
        value=float(budget),
        step=500.0
    )

    if st.button(
        "💾 Save Budget"
    ):

        set_budget(new_budget)

        st.success(
            "✅ Budget saved successfully!"
        )

        st.rerun()

    budget = get_budget()

    # =========================================================
    # CURRENT MONTH EXPENSE
    # =========================================================

    current_month_expense = 0

    if expense:

        current_date = pd.Timestamp.today()

        current_month = current_date.month
        current_year = current_date.year

        budget_expense_df = pd.DataFrame(
            expense,
            columns=[
                "ID",
                "Amount",
                "Category",
                "Date"
            ]
        )

        budget_expense_df["Date"] = pd.to_datetime(
            budget_expense_df["Date"]
        )

        current_month_expenses = budget_expense_df[
            (budget_expense_df["Date"].dt.month == current_month)
            &
            (budget_expense_df["Date"].dt.year == current_year)
        ]

        current_month_expense = (
            current_month_expenses["Amount"]
            .sum()
        )

    # =========================================================
    # BUDGET STATUS
    # =========================================================

    if budget > 0:

        remaining = (
            budget - current_month_expense
        )

        progress = min(
            current_month_expense / budget,
            1.0
        )

        st.progress(progress)

        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric(
                "🎯 Monthly Budget",
                f"₹ {budget:,.2f}"
            )

        with col2:

            st.metric(
                "💸 This Month Expense",
                f"₹ {current_month_expense:,.2f}"
            )

        with col3:

            st.metric(
                "💰 Remaining",
                f"₹ {remaining:,.2f}"
            )

        if remaining >= 0:

            st.success(
                "✅ You are within your monthly budget."
            )

        else:

            st.error(
                f"⚠️ Budget exceeded by ₹ {-remaining:,.2f}"
            )

    else:

        st.info(
            "Set your monthly budget to start tracking."
        )

    st.divider()

    st.caption(
        "ExpenseIQ © 2026"
    )