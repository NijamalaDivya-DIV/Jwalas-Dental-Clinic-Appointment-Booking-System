import sqlite3
from twilio.rest import Client
from flask import Flask, render_template, request, redirect, url_for
import smtplib
from email.mime.text import MIMEText

app = Flask(__name__)

# 🔹 TWILIO CLIENT
try:
    from twilio.rest import Client
    twilio_client = Client("your_sid", "your_token")
except:
    print("Twilio not installed")
    twilio_client = None

# 🔹 SMS FUNCTION
def send_sms(name, phone, date):
    try:
        message = twilio_client.messages.create(
            body=f"New Appointment:\nName: {name}\nDate: {date}",
            from_="+1234567890",   # your Twilio number
            to="+91" + phone
        )
        print("✅ SMS sent:", message.sid)
    except Exception as e:
        print("❌ SMS Error:", e)


# 🔹 EMAIL FUNCTION
def send_email(name, phone, date):
    try:
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

        server = smtplib.SMTP('smtp.gmail.com', 587, timeout=10)
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(msg)
        server.quit()

        print("✅ Email sent")

    except Exception as e:
        print("❌ Email Error:", e)


# 🔹 HOME PAGE
@app.route('/')
def home():
    return render_template('index.html')


# 🔹 BOOKING
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

        # 📧 EMAIL
        send_email(name, phone, date)

        # 📱 SMS
        send_sms(name, phone, date)

        return render_template('success.html', name=name)

    return render_template('booking.html')


# 🔹 VIEW
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


# 🔹 RUN
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)    