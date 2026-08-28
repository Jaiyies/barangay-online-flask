from flask import Flask, render_template, request, redirect, url_for, session, flash
import mysql.connector
from werkzeug.security import check_password_hash, generate_password_hash
from functools import wraps
import os

app = Flask(__name__)
app.secret_key = 'your-secret-key-here-change-in-production'

# ===== DATABASE CONNECTION =====
def get_db():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='bsit2026@123',
        database='barangay_online_services'
    )

# ===== LOGIN ROUTE =====
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        role = request.form.get('role', 'resident')
        
        if not email or not password:
            flash('Please fill in all fields.', 'warning')
            return render_template('login.html')
        
        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()
        conn.close()
        
        if user:
            # Check if password matches (hashed)
            if check_password_hash(user['password'], password):
                # Check role access
                if role == 'admin' and user['role'] not in ['admin', 'barangay_staff']:
                    flash('You are not authorized as admin.', 'danger')
                    return render_template('login.html')
                
                # Set session
                session['user_id'] = user['id']
                session['fullname'] = f"{user['first_name']} {user['last_name']}"
                session['email'] = user['email']
                session['role'] = user['role']
                
                flash(f'Welcome back, {session["fullname"]}!', 'success')
                
                # Redirect based on role
                if user['role'] in ['admin', 'barangay_staff']:
                    return redirect(url_for('admin_dashboard'))
                return redirect(url_for('dashboard'))
            else:
                flash('Invalid email or password.', 'danger')
        else:
            flash('Invalid email or password.', 'danger')
        
        return render_template('login.html')
    
    return render_template('login.html')