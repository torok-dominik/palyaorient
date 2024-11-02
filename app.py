from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'
db = SQLAlchemy(app)

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    max_capacity = db.Column(db.Integer, nullable=False)
    current_enrollment = db.Column(db.Integer, default=0)

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    registered_course_id = db.Column(db.Integer, db.ForeignKey('course.id'))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    courses = Course.query.all()
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        selected_course_id = request.form['courses']

        selected_course = Course.query.get(selected_course_id)

        if selected_course.current_enrollment >= selected_course.max_capacity:
            flash('This course is full. Please choose another one.', 'error')
            return redirect(url_for('register'))

        new_student = Student(first_name=first_name, last_name=last_name, email=email, registered_course_id=selected_course_id)
        selected_course.current_enrollment += 1
        db.session.add(new_student)
        db.session.commit()
        return redirect(url_for('index'))

    return render_template('register.html', courses=courses)

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        password = request.form['password']
        if password == 'admin_password':  # Change this to a secure password check
            session['admin_logged_in'] = True
            return redirect(url_for('admin_dashboard'))
    
    return render_template('admin.html')

@app.route('/admin/dashboard')
def admin_dashboard():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin'))
    
    students = Student.query.all()
    courses = Course.query.all()
    return render_template('admin_dashboard.html', students=students, courses=courses)

@app.route('/logout')
def logout():
    session.pop('admin_logged_in', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
