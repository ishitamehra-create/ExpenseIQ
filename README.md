# 💰 ExpenseIQ

> A Streamlit-based personal finance analytics application for tracking income, expenses, budgets, and spending patterns.

## 📌 Project Overview

ExpenseIQ is a personal finance management application built with Python and Streamlit.

The application helps users record and manage their income and expenses, monitor budgets, and analyze their financial performance through an interactive dashboard.

The goal of ExpenseIQ is to make personal financial tracking simple, organized, and data-driven.

---

## 🎯 Problem Statement

Managing personal finances using notebooks or spreadsheets can become difficult as the number of transactions increases.

ExpenseIQ provides a centralized application where users can:

- Track income and expenses
- Categorize spending
- Monitor budgets
- Review financial performance
- Generate reports
- Analyze spending patterns

---

## ✨ Features

- 💵 **Income Tracking**
- 💸 **Expense Tracking**
- ✏️ **Edit & Delete Records**
- 🎯 **Monthly Budget Management**
- 📊 **Financial Analytics Dashboard**
- 📈 **Expense & Income Analysis**
- 📥 **CSV Reports**
- 🗃️ **Local Database Storage**
- 🖥️ **Interactive Streamlit Interface**

---

## 🛠️ Tech Stack

| Technology | Purpose |
|------------|---------|
| Python | Application development |
| Streamlit | Web application interface |
| SQLite | Local database management |
| Pandas | Data processing and analysis |
| Plotly | Data visualization |
| Git & GitHub | Version control and project management |

---

## 📂 Project Structure

```text
ExpenseIQ/
│
├── assets/
│
├── utils/
│   └── helper.py
│
├── views/
│   ├── __init__.py
│   ├── dashboard.py
│   ├── expense.py
│   ├── income.py
│   └── reports.py
│
├── app.py
├── database.py
├── requirements.txt
├── README.md
├── LICENSE
└── .gitignore

---

## ⚙️ Installation & Setup

### 1. Clone the repository

```bash
git clone https://github.com/ishitamehra-create/ExpenseIQ.git
```

### 2. Navigate to the project directory

```bash
cd ExpenseIQ
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the application

```bash
streamlit run app.py
```

The application will open in your browser.

---

## 📊 Application Modules

### 🏠 Dashboard

Provides an overview of financial activity and helps users understand their income, expenses, and overall financial position.

### 💵 Income Management

Allows users to record and manage income transactions.

### 💸 Expense Management

Allows users to record, categorize, edit, and delete expense transactions.

### 🎯 Budget Management

Helps users define and monitor their monthly spending budget.

### 📈 Reports & Analytics

Provides financial reports and insights that help users understand their spending patterns.

---

## 🔐 Data & Privacy

ExpenseIQ uses a local SQLite database for storing application data.

Local database files and sensitive configuration files are excluded from version control using `.gitignore`.

---

## 🚀 Future Improvements

Planned improvements include:

- 📊 Advanced financial analytics
- 📅 Date-based filtering
- 📈 More interactive visualizations
- 📤 Improved report exporting
- ☁️ Cloud database integration
- 🔐 User authentication
- 📱 Responsive UI improvements
- 🤖 AI-powered spending insights

---

## 👩‍💻 Author

**Ishita Mehra**

B.Tech Data Science Student

**Areas of Interest:**
- Data Analytics
- Python
- SQL
- Power BI
- Machine Learning
- Data Visualization

---

## 📄 License

This project is licensed under the MIT License.