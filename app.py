from flask import Flask, render_template, request

app = Flask(__name__)

appointments = []

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/booking', methods=['GET', 'POST'])
def booking():
    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        date = request.form['date']

        appointments.append({
            "name": name,
            "phone": phone,
            "date": date
        })

        return render_template('success.html', name=name)

    return render_template('booking.html')

if __name__ == "__main__":
    app.run(debug=True)