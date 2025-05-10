from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_mysqldb import MySQL
from config import Config
import MySQLdb.cursors
import re
from datetime import datetime

app = Flask(__name__)
app.config.from_object(Config)

# Initialize MySQL
mysql = MySQL(app)

# Routes
@app.route('/')
def home():
    if 'loggedin' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE username = %s AND password = %s', (username, password))
        account = cursor.fetchone()
        
        if account:
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            return redirect(url_for('dashboard'))
        else:
            flash('Incorrect username/password!', 'danger')
    
    return render_template('login.html')

@app.route('/signup/', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE username = %s', (username,))
        account = cursor.fetchone()
        
        if account:
            flash('Account already exists!', 'danger')
        elif not re.match(r'^[A-Za-z0-9]+$', username):
            flash('Username must contain only characters and numbers!', 'danger')
        elif not username or not password:
            flash('Please fill out the form!', 'danger')
        else:
            cursor.execute('INSERT INTO users (username, password) VALUES (%s, %s)', (username, password))
            mysql.connection.commit()
            flash('You have successfully registered!', 'success')
            return redirect(url_for('login'))
    
    return render_template('signup.html')

@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/dashboard')
def dashboard():
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM students WHERE user_id = %s', (session['id'],))
        students = cursor.fetchall()
        return render_template('dashboard.html', username=session['username'], students=students)
    return redirect(url_for('login'))

@app.route('/add_student', methods=['GET', 'POST'])
def add_student():
    if 'loggedin' in session:
        if request.method == 'POST':
            first_name = request.form['first_name']
            last_name = request.form['last_name']
            email = request.form['email']
            course = request.form['course']
            year_level = request.form['year_level']
            gender = request.form['gender']
            
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('INSERT INTO students (first_name, last_name, email, course, year_level, gender, user_id) VALUES (%s, %s, %s, %s, %s, %s, %s)',
                          (first_name, last_name, email, course, year_level, gender, session['id']))
            mysql.connection.commit()
            flash('Student added successfully!', 'success')
            return redirect(url_for('dashboard'))
        
        return render_template('add_student.html')
    return redirect(url_for('login'))

@app.route('/edit_student/<int:id>', methods=['GET', 'POST'])
def edit_student(id):
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        
        if request.method == 'POST':
            first_name = request.form['first_name']
            last_name = request.form['last_name']
            email = request.form['email']
            course = request.form['course']
            year_level = request.form['year_level']
            gender = request.form['gender']
            
            cursor.execute('UPDATE students SET first_name = %s, last_name = %s, email = %s, course = %s, year_level = %s, gender = %s WHERE id = %s AND user_id = %s',
                          (first_name, last_name, email, course, year_level, gender, id, session['id']))
            mysql.connection.commit()
            flash('Student updated successfully!', 'success')
            return redirect(url_for('dashboard'))
        
        cursor.execute('SELECT * FROM students WHERE id = %s AND user_id = %s', (id, session['id']))
        student = cursor.fetchone()
        
        if student:
            return render_template('edit_student.html', student=student)
        else:
            flash('Student not found or you dont have permission to edit!', 'danger')
            return redirect(url_for('dashboard'))
    
    return redirect(url_for('login'))

@app.route('/delete_student/<int:id>')
def delete_student(id):
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('DELETE FROM students WHERE id = %s AND user_id = %s', (id, session['id']))
        mysql.connection.commit()
        flash('Student deleted successfully!', 'success')
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    app.run(debug=True)