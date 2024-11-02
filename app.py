from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Cseréld le a titkos kulcsot!

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Itt ellenőrizd a felhasználónevet és a jelszót
        # Példa: if username == "admin" and password == "password":
        flash('Sikeres bejelentkezés!')
        return redirect(url_for('index'))
    return render_template('admin.html')

@app.route('/student')
def student():
    return 'Diák regisztrációs oldal'  # Később bővítheted

if __name__ == '__main__':
    app.run(debug=True)
