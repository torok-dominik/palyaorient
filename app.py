from flask import Flask, render_template, request, redirect, url_for, session, flash

app = Flask(__name__)
app.secret_key = 'my_secret_key'

# Dummy data for lectures
lectures = {
    '1': [('1.1', 'Előadás 1.1 (100 fő)'), ('1.2', 'Előadás 1.2 (28 fő)'), ('1.3', 'Előadás 1.3 (26 fő)')],
    '2': [('2.1', 'Előadás 2.1 (50 fő)'), ('2.2', 'Előadás 2.2 (25 fő)'), ('2.3', 'Előadás 2.3 (30 fő)')],
    '3': [('3.1', 'Előadás 3.1 (50 fő)'), ('3.2', 'Előadás 3.2 (40 fő)'), ('3.3', 'Előadás 3.3 (50 fő)')]
}

students = []  # Store student registration details

# Admin credentials
admin_credentials = {
    'username': 'admin',
    'password': 'admin123'
}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/admin', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == admin_credentials['username'] and password == admin_credentials['password']:
            session['admin_logged_in'] = True
            return redirect(url_for('admin_panel'))
        else:
            flash("Hibás felhasználónév vagy jelszó!")
    return render_template('admin_login.html')

@app.route('/admin_panel')
def admin_panel():
    if 'admin_logged_in' in session:
        return render_template('admin.html', students=students)
    else:
        return redirect(url_for('admin_login'))

@app.route('/student', methods=['GET', 'POST'])
def student():
    if request.method == 'POST':
        # Collect form data
        name = request.form['name']
        email = request.form['email']
        slot_1 = request.form.get('slot_1')
        slot_2 = request.form.get('slot_2')
        slot_3 = request.form.get('slot_3')

        # Save student data
        students.append({
            'name': name,
            'email': email,
            'slot_1': slot_1,
            'slot_2': slot_2,
            'slot_3': slot_3
        })

        return redirect(url_for('home'))
    return render_template('student.html', lectures=lectures)

if __name__ == '__main__':
    app.run(debug=True)
