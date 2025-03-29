import os

def create_project_structure():
    # Create main project directory
    project_dir = 'PythonProject'
    os.makedirs(project_dir, exist_ok=True)

    # Create subdirectories for templates and static files
    os.makedirs(os.path.join(project_dir, 'templates'), exist_ok=True)
    os.makedirs(os.path.join(project_dir, 'static'), exist_ok=True)

    # Create main Python file
    with open(os.path.join(project_dir, 'app.py'), 'w') as f:
        f.write("# Main application file\n")

    # Create database file
    with open(os.path.join(project_dir, 'database.db'), 'w') as f:
        pass  # Empty database file

    print(f"Project structure created at: {project_dir}")

create_project_structure()

#2nd code

from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Database connection function
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_id = request.form['user_id']
        password = request.form['password']
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE email = ? AND password = ?', (user_id, password)).fetchone()
        conn.close()
        if user:
            return redirect(url_for('home'))
        else:
            return "Invalid credentials!"
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        new_password = request.form['new_password']
        confirm_password = request.form['confirm_password']
        if new_password == confirm_password:
            conn = get_db_connection()
            conn.execute('INSERT INTO users (email, password) VALUES (?, ?)', (email, new_password))
            conn.commit()
            conn.close()
            return redirect(url_for('login'))
        else:
            return "Passwords do not match!"
    return render_template('signup.html')

if __name__ == '__main__':
    app.run(debug=True)

#3rd code

@app.route('/home')
def home():
    classes = [
        {'name': 'BCA 1st Year', 'batch': 2023},
        {'name': 'BCA 2nd Year', 'batch': 2022},
        {'name': 'BCA 3rd Year', 'batch': 2021}
    ]
    return render_template('home.html', classes=classes)


#4th code

@app.route('/batch/<batch_name>')
def batch_students(batch_name):
    # Example student data
    students = {
        'BCA 1st Year': ['Alice', 'Bob', 'Charlie'],
        'BCA 2nd Year': ['David', 'Eve', 'Frank'],
        'BCA 3rd Year': ['Grace', 'Heidi', 'Ivan']
    }
    student_list = students.get(batch_name, [])
    return render_template('batch_students.html', batch_name=batch_name, students=student_list)


#code 5

import sqlite3
import os

def setup_database():
    db_path = 'PythonProject/database.db'

    # Remove existing file if not valid
    if os.path.exists(db_path):
        os.remove(db_path)

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Create users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT NOT NULL,
            password TEXT NOT NULL
        )
    ''')

    # Create students table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            batch_name TEXT NOT NULL
        )
    ''')

    conn.commit()
    conn.close()
setup_database()
