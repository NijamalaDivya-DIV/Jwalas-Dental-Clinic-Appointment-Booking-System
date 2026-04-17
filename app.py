import sqlite3
from flask import Flask, render_template, request

app = Flask(__name__)

# 🔹 Create table (only first time)
def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS appointments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            phone TEXT,
            date TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# 🔹 Home page
@app.route('/')
def home():
    return render_template('index.html')

# 🔹 Booking
@app.route('/booking', methods=['GET', 'POST'])
def booking():
    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        date = request.form['date']

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO appointments (name, phone, date) VALUES (?, ?, ?)",
            (name, phone, date)
        )
        conn.commit()
        conn.close()

        return render_template('success.html', name=name)

    return render_template('booking.html')


# 🔹 View all appointments (NEW)
@app.route('/appointments')
def appointments():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM appointments")
    data = cursor.fetchall()
    conn.close()

    return render_template('appointments.html', data=data)


if __name__ == "__main__":
    app.run(debug=True)