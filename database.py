

import sqlite3

# Database Connection
conn = sqlite3.connect("expense.db", check_same_thread=False)
cursor = conn.cursor()

# -------------------------
# Create Income Table
# -------------------------
cursor.execute("""
CREATE TABLE IF NOT EXISTS income(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    amount REAL NOT NULL,
    source TEXT NOT NULL,
    date TEXT NOT NULL
)
""")

# -------------------------
# Create Expense Table
# -------------------------
cursor.execute("""
CREATE TABLE IF NOT EXISTS expense(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    amount REAL NOT NULL,
    category TEXT NOT NULL,
    date TEXT NOT NULL
)
""")

conn.commit()

# =========================
# Income Functions
# =========================

def add_income(amount, source, date):
    cursor.execute(
        "INSERT INTO income(amount,source,date) VALUES(?,?,?)",
        (amount, source, date)
    )
    conn.commit()


def get_income():
    cursor.execute("SELECT * FROM income ORDER BY id DESC")
    return cursor.fetchall()


def get_total_income():
    cursor.execute("SELECT SUM(amount) FROM income")
    result = cursor.fetchone()[0]
    return result if result else 0


# =========================
# Expense Functions
# =========================

def add_expense(amount, category, date):
    cursor.execute(
        "INSERT INTO expense(amount,category,date) VALUES(?,?,?)",
        (amount, category, date)
    )
    conn.commit()


def get_expense():
    cursor.execute("SELECT * FROM expense ORDER BY id DESC")
    return cursor.fetchall()


def get_total_expense():
    cursor.execute("SELECT SUM(amount) FROM expense")
    result = cursor.fetchone()[0]
    return result if result else 0


# =========================
# Expense Chart Data
# =========================

def expense_category_summary():

    cursor.execute("""
        SELECT category, SUM(amount)
        FROM expense
        GROUP BY category
    """)

    return cursor.fetchall()


# =========================
# Income Chart Data
# =========================

def income_source_summary():

    cursor.execute("""
        SELECT source, SUM(amount)
        FROM income
        GROUP BY source
    """)

    return cursor.fetchall()


# =========================
# Budget Table
# =========================

cursor.execute("""
CREATE TABLE IF NOT EXISTS budget(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    amount REAL
)
""")

conn.commit()


# =========================
# Budget Functions
# =========================

def set_budget(amount):

    cursor.execute("DELETE FROM budget")

    cursor.execute(
        "INSERT INTO budget(amount) VALUES(?)",
        (amount,)
    )

    conn.commit()


def get_budget():

    cursor.execute("SELECT amount FROM budget LIMIT 1")

    result = cursor.fetchone()

    if result:
        return result[0]

    return 0

# =========================
# Delete Functions
# =========================

def delete_income(record_id):

    cursor.execute(
        "DELETE FROM income WHERE id=?",
        (record_id,)
    )

    conn.commit()


def delete_expense(record_id):

    cursor.execute(
        "DELETE FROM expense WHERE id=?",
        (record_id,)
    )

    conn.commit()

# =========================
# Edit Income
# =========================

def update_income(record_id, amount, source, date):

    cursor.execute(
        """
        UPDATE income
        SET amount = ?, source = ?, date = ?
        WHERE id = ?
        """,
        (amount, source, date, record_id)
    )

    conn.commit()


# =========================
# Edit Expense
# =========================

def update_expense(record_id, amount, category, date):

    cursor.execute(
        """
        UPDATE expense
        SET amount = ?, category = ?, date = ?
        WHERE id = ?
        """,
        (amount, category, date, record_id)
    )

    conn.commit()