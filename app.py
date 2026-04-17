import sqlite3
from flask import Flask, render_template, request, redirect, url_for
import smtplib
from email.mime.text import MIMEText

app = Flask(__name__)

# 🔹 EMAIL FUNCTION
def send_email(name, phone, date):
    sender_email = "yourgmail@gmail.com"
    sender_password = "your_app_password"

    receiver_email = "yourgmail@gmail.com"

    subject = "New Dental Appointment"
    body = f"""
New appointment booked:

Name: {name}
Phone: {phone}
Date: {date}
"""

    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = receiver_email

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender_email, sender_password)
    server.send_message(msg)
    server.quit()


# 🔹 HOME PAGE
@app.route('/')
def home():
    return render_template('index.html')


# 🔹 BOOKING ROUTE (IMPORTANT - YOU MISSED THIS)
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

        # 📧 SEND EMAIL
        send_email(name, phone, date)

        return render_template('success.html', name=name)

    return render_template('booking.html')


# 🔹 VIEW APPOINTMENTS
@app.route('/appointments')
def appointments():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM appointments")
    data = cursor.fetchall()
    conn.close()

    return render_template('appointments.html', data=data)


# 🔹 DELETE
@app.route('/delete/<int:id>')
def delete(id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM appointments WHERE id=?", (id,))
    conn.commit()
    conn.close()

    return redirect(url_for('appointments'))


# 🔹 EDIT
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        date = request.form['date']

        cursor.execute("""
            UPDATE appointments
            SET name=?, phone=?, date=?
            WHERE id=?
        """, (name, phone, date, id))

        conn.commit()
        conn.close()

        return redirect(url_for('appointments'))

    cursor.execute("SELECT * FROM appointments WHERE id=?", (id,))
    data = cursor.fetchone()
    conn.close()

    return render_template('edit.html', data=data)


# 🔹 RUN APP
if __name__ == "__main__":
    app.run(debug=True)