from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# ------------------ DATABASE SETUP ------------------
def init_db():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            amount INTEGER,
            category TEXT,
            date TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# ------------------ HOME ROUTE ------------------
@app.route("/")
def home():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("SELECT * FROM expenses")
    expenses = c.fetchall()
    conn.close()

    total = sum(e[2] for e in expenses) if expenses else 0

    # Category-wise data for charts
    category_data = {}
    for e in expenses:
        cat = e[3] if e[3] else "Other"
        category_data[cat] = category_data.get(cat, 0) + int(e[2])

    labels = list(category_data.keys())
    values = list(category_data.values())

    return render_template(
        "index.html",
        expenses=expenses,
        total=total,
        labels=labels,
        values=values
    )

# ------------------ ADD EXPENSE ------------------
@app.route("/add", methods=["POST"])
def add():
    title = request.form.get("title", "")
    amount = request.form.get("amount", "0")
    category = request.form.get("category", "General")
    date = request.form.get("date", "N/A")

    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute(
        "INSERT INTO expenses (title, amount, category, date) VALUES (?, ?, ?, ?)",
        (title, amount, category, date)
    )
    conn.commit()
    conn.close()

    return redirect(url_for("home"))

# ------------------ DELETE EXPENSE ------------------
@app.route("/delete/<int:id>")
def delete(id):
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("DELETE FROM expenses WHERE id=?", (id,))
    conn.commit()
    conn.close()

    return redirect(url_for("home"))

# ------------------ RUN APP ------------------
if __name__ == "__main__":
    app.run(debug=True)