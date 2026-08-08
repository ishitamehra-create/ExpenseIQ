import streamlit as st

# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="ExpenseIQ",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# IMPORT PAGES
# =========================================================

import views.dashboard as dashboard
from views.income import income_page
from views.expense import expense_page
from views.reports import reports_page


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.title("💰 ExpenseIQ")

    st.caption("Personal Finance Dashboard")

    st.divider()

    page = st.radio(
        "📍 Navigation",
        [
            "🏠 Dashboard",
            "💵 Income",
            "💸 Expense",
            "📊 Reports"
        ]
    )

    st.divider()

    # -------------------------
    # About ExpenseIQ
    # -------------------------

    st.markdown("### 💡 About")

    st.write(
        "ExpenseIQ helps you track income, "
        "expenses, budgets and financial performance "
        "in one place."
    )

    st.divider()

    st.markdown("### 🚀 Features")

    st.markdown(
        """
        - 💵 Income Tracking
        - 💸 Expense Tracking
        - ✏️ Edit & Delete Records
        - 🎯 Monthly Budget
        - 📊 Financial Analytics
        - 📥 CSV Reports
        """
    )

    st.divider()

    st.success("ExpenseIQ v1.0")

    st.caption("© 2026 ExpenseIQ")


# =========================================================
# PAGE NAVIGATION
# =========================================================

if page == "🏠 Dashboard":

    dashboard.dashboard_page()


elif page == "💵 Income":

    income_page()


elif page == "💸 Expense":

    expense_page()


elif page == "📊 Reports":

    reports_page()