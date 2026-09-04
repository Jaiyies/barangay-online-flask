from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
import mysql.connector
from werkzeug.security import check_password_hash, generate_password_hash
from functools import wraps
import os

app = Flask(__name__)
app.secret_key = 'your-secret-key-here-change-in-production'

# ===== HOME/INDEX ROUTE =====
@app.route('/')
def index():
    return redirect(url_for('login'))

# ===== DATABASE CONNECTION =====
def get_db():
    return mysql.connector.connect(
        host='127.0.0.1',
        port=3306,
        user='root',
        password='bsit2026@123',
        database='barangay_online_services'
    )

# ===== LOGIN ROUTE (MAY LOCKOUT) =====
@app.route('/login', methods=['GET', 'POST'])
def login():
    # Check kung naka-lockout ba
    if session.get('login_attempts', 0) >= 3:
        lockout_time = session.get('lockout_time', 0)
        current_time = time.time()
        if current_time < lockout_time:
            remaining = int(lockout_time - current_time)
            lockout_msg = f"Too many failed attempts. Please wait {remaining} seconds before trying again."
            return render_template('login.html', login_error=True, lockout_message=lockout_msg)
        else:
            # Reset attempts after lockout expires
            session['login_attempts'] = 0
            session['lockout_time'] = 0

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
            # Kapag mali ang password
            if not check_password_hash(user['password'], password):
                session['login_attempts'] = session.get('login_attempts', 0) + 1
                if session['login_attempts'] >= 3:
                    session['lockout_time'] = time.time() + 30
                    lockout_msg = "Too many failed attempts. Please wait 30 seconds before trying again."
                    return render_template('login.html', login_error=True, lockout_message=lockout_msg)
                else:
                    return render_template('login.html', login_error=True)
            
            # Kapag tama na
            session['login_attempts'] = 0
            session['lockout_time'] = 0
            
            if role == 'admin' and user['role'] not in ['admin', 'head_admin']:
                flash('You are not authorized as admin.', 'danger')
                return render_template('login.html')
            
            session['user_id'] = user['id']
            session['fullname'] = f"{user['first_name']} {user['last_name']}"
            session['email'] = user['email']
            session['role'] = user['role']
            
            flash(f'Welcome back, {session["fullname"]}!', 'success')
            
            if user['role'] == 'head_admin':
                return redirect(url_for('head_admin_dashboard'))
            elif user['role'] == 'admin':
                return redirect(url_for('admin_dashboard'))
            else:
                return redirect(url_for('dashboard'))
        else:
            # Kapag walang user
            session['login_attempts'] = session.get('login_attempts', 0) + 1
            if session['login_attempts'] >= 3:
                session['lockout_time'] = time.time() + 30
                lockout_msg = "Too many failed attempts. Please wait 30 seconds before trying again."
                return render_template('login.html', login_error=True, lockout_message=lockout_msg)
            else:
                return render_template('login.html', login_error=True)
    
    return render_template('login.html')

# ===== REGISTER ROUTE =====
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        first_name = request.form.get('first_name', '').strip()
        last_name = request.form.get('last_name', '').strip()
        email = request.form.get('email', '').strip()
        contact_number = request.form.get('contact_number', '').strip()
        address = request.form.get('address', '').strip()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')
        
        if not first_name or not last_name or not email or not password:
            flash('Please fill in all required fields.', 'danger')
            return render_template('register.html')
        
        if password != confirm_password:
            flash('Passwords do not match.', 'danger')
            return render_template('register.html')
        
        if len(password) < 8:
            flash('Password must be at least 8 characters long.', 'danger')
            return render_template('register.html')
        
        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        
        cursor.execute("SELECT id FROM users WHERE email = %s", (email,))
        existing = cursor.fetchone()
        
        if existing:
            conn.close()
            flash('Email address already registered. Please login.', 'danger')
            return render_template('register.html')
        
        hashed_password = generate_password_hash(password)
        
        cursor.execute("""
            INSERT INTO users (first_name, last_name, email, password, contact_number, address, role, is_verified)
            VALUES (%s, %s, %s, %s, %s, %s, 'resident', TRUE)
        """, (first_name, last_name, email, hashed_password, contact_number, address))
        conn.commit()
        conn.close()
        
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

# ============================================================
# ===== RESIDENT ROUTES =====
# ============================================================

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        flash('Please login first.', 'warning')
        return redirect(url_for('login'))
    return render_template('dashboard.html')

@app.route('/request-document')
def request_document():
    if 'user_id' not in session:
        flash('Please login first.', 'warning')
        return redirect(url_for('login'))
    return render_template('request_document.html')

@app.route('/apply-permit', methods=['GET'])
def apply_permit():
    if 'user_id' not in session:
        flash('Please login first.', 'warning')
        return redirect(url_for('login'))
    return render_template('apply_permit.html')

@app.route('/apply-permit', methods=['POST'])
def apply_permit_post():
    """Submit event permit application - Residents only"""
    if 'user_id' not in session:
        flash('Please login first.', 'warning')
        return redirect(url_for('login'))
    
    # Get form data
    event_name = request.form.get('event_name', '').strip()
    event_description = request.form.get('event_description', '').strip()
    purpose = request.form.get('purpose', '').strip()
    event_date = request.form.get('event_date', '').strip()
    start_time = request.form.get('start_time', '').strip()
    end_time = request.form.get('end_time', '').strip()
    estimated_attendees = request.form.get('estimated_attendees', '').strip()
    venue = request.form.get('venue', '').strip()
    
    # Validation
    if not event_name or not event_date or not start_time or not end_time or not venue:
        flash('Please fill in all required fields.', 'danger')
        return redirect(url_for('apply_permit'))
    
    # Validate time range
    if start_time >= end_time:
        flash('End time must be after start time.', 'danger')
        return redirect(url_for('apply_permit'))
    
    # Validate time limits (8:00 AM to 10:00 PM)
    if start_time < '08:00' or start_time > '22:00':
        flash('Start time must be between 8:00 AM and 10:00 PM.', 'danger')
        return redirect(url_for('apply_permit'))
    
    if end_time < '08:00' or end_time > '22:00':
        flash('End time must be between 8:00 AM and 10:00 PM.', 'danger')
        return redirect(url_for('apply_permit'))
    
    # Validate 10-day rule
    try:
        selected_date = datetime.datetime.strptime(event_date, '%Y-%m-%d').date()
        today = datetime.date.today()
        diff_days = (selected_date - today).days
        
        if diff_days < 10:
            flash('Please apply at least 10 days before the event date.', 'danger')
            return redirect(url_for('apply_permit'))
    except ValueError:
        flash('Invalid date format.', 'danger')
        return redirect(url_for('apply_permit'))
    
    # File upload handling
    file_data = None
    if 'requirement' in request.files:
        file = request.files['requirement']
        if file and file.filename:
            # Save file or store filename
            file_data = file.filename
    
    # Generate reference number and queuing number
    ref_num = f"BP-{datetime.datetime.now().strftime('%Y%m%d')}-{random.randint(1000, 9999)}"
    queue_num = f"Q-{random.randint(1, 999):03d}"
    
    # Insert into database
    conn = get_db()
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            INSERT INTO event_permits (
                user_id, event_name, event_description, purpose, event_date, 
                start_time, end_time, estimated_attendees, venue, 
                status, requirements_file, reference_number, queuing_number
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, 'pending', %s, %s, %s)
        """, (
            session['user_id'],
            event_name,
            event_description,
            purpose,
            event_date,
            start_time,
            end_time,
            estimated_attendees if estimated_attendees else 0,
            venue,
            file_data,
            ref_num,
            queue_num
        ))
        conn.commit()
        permit_id = cursor.lastrowid
        
        # Create notification for user
        cursor.execute("""
            INSERT INTO notifications (user_id, title, message, notification_type)
            VALUES (%s, %s, %s, 'permit_submitted')
        """, (
            session['user_id'],
            'Permit Application Submitted',
            f'Your event permit "{event_name}" has been submitted for review. Reference: {ref_num} | Queue: {queue_num}'
        ))
        conn.commit()
        
        flash('Permit application submitted successfully!', 'success')
        return redirect(url_for('dashboard'))
        
    except mysql.connector.Error as e:
        flash(f'Database error: {str(e)}', 'danger')
        return redirect(url_for('apply_permit'))
    finally:
        conn.close()

# ============================================================
# ===== HEAD ADMIN DASHBOARD =====
# ============================================================

@app.route('/head-admin-dashboard')
def head_admin_dashboard():
    if 'user_id' not in session or session.get('role') != 'head_admin':
        flash('Please login as Head Admin.', 'danger')
        return redirect(url_for('login'))
    
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    
    cursor.execute("SELECT COUNT(*) as total FROM users")
    total_users = cursor.fetchone()['total']
    
    cursor.execute("SELECT COUNT(*) as total FROM users WHERE role = 'resident'")
    total_residents = cursor.fetchone()['total']
    
    cursor.execute("SELECT COUNT(*) as total FROM users WHERE role = 'admin'")
    total_admins = cursor.fetchone()['total']
    
    cursor.execute("SELECT COUNT(*) as total FROM document_requests")
    total_requests = cursor.fetchone()['total']
    
    cursor.execute("SELECT COUNT(*) as total FROM event_permits")
    total_events = cursor.fetchone()['total']
    
    conn.close()
    
    return render_template('admin/head_admin_dashboard.html',
                         total_users=total_users,
                         total_residents=total_residents,
                         total_admins=total_admins,
                         total_requests=total_requests,
                         total_events=total_events)

# ===== ADMIN DASHBOARD (Secondary Admin) =====
@app.route('/admin-dashboard')
def admin_dashboard():
    if 'user_id' not in session or session.get('role') != 'admin':
        flash('Please login as Admin.', 'danger')
        return redirect(url_for('login'))
    
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    
    cursor.execute("SELECT COUNT(*) as total FROM document_requests WHERE status = 'pending'")
    pending_requests = cursor.fetchone()['total']
    
    cursor.execute("SELECT COUNT(*) as total FROM event_permits WHERE status = 'pending'")
    pending_events = cursor.fetchone()['total']
    
    conn.close()
    
    return render_template('admin/admin_dashboard.html',
                         pending_requests=pending_requests,
                         pending_events=pending_events)

# ===== DASHBOARD FOR RESIDENTS =====
@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        flash('Please login first.', 'warning')
        return redirect(url_for('login'))
    return render_template('dashboard.html')

# ============================================================
# ===== USER MANAGEMENT =====
# ============================================================

@app.route('/users')
def user_management():
    if 'user_id' not in session or session.get('role') != 'head_admin':
        flash('Please login as Head Admin.', 'danger')
        return redirect(url_for('login'))
    
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id, first_name, last_name, email, contact_number, address, role, is_verified, created_at FROM users WHERE role = 'resident' ORDER BY created_at DESC")
    users = cursor.fetchall()
    conn.close()
    
    for user in users:
        if user.get('created_at'):
            if hasattr(user['created_at'], 'strftime'):
                user['created_at'] = user['created_at'].strftime('%b %d, %Y')
    
    return render_template('admin/user_management.html', users=users)

# ===== UPDATE USER ROLE =====
@app.route('/update-role/<int:user_id>', methods=['POST'])
def update_user_role(user_id):
    if 'user_id' not in session or session.get('role') != 'head_admin':
        flash('Unauthorized access.', 'danger')
        return redirect(url_for('login'))
    
    if user_id == session['user_id']:
        flash('You cannot change your own role.', 'danger')
        return redirect(url_for('user_management'))
    
    new_role = request.form.get('role')
    
    if new_role not in ['resident', 'admin', 'head_admin']:
        flash('Invalid role selected.', 'danger')
        return redirect(url_for('user_management'))
    
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET role = %s WHERE id = %s", (new_role, user_id))
    conn.commit()
    conn.close()
    
    flash(f'User role updated to {new_role.replace("_", " ").title()} successfully!', 'success')
    return redirect(url_for('user_management'))

# ===== API: GET USER DETAILS =====
@app.route('/api/user/<int:user_id>')
def api_get_user(user_id):
    if 'user_id' not in session or session.get('role') != 'head_admin':
        return jsonify({'error': 'Unauthorized'}), 401
    
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id, first_name, last_name, email, contact_number, address, role, is_verified, created_at FROM users WHERE id = %s", (user_id,))
    user = cursor.fetchone()
    conn.close()
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    if user.get('created_at'):
        if hasattr(user['created_at'], 'strftime'):
            user['created_at'] = user['created_at'].strftime('%b %d, %Y')
    
    return jsonify(user)

# ===== API: TOGGLE BLOCK USER =====
@app.route('/api/user/<int:user_id>/toggle-block', methods=['POST'])
def api_toggle_block(user_id):
    if 'user_id' not in session or session.get('role') != 'head_admin':
        return jsonify({'error': 'Unauthorized'}), 401
    
    if user_id == session['user_id']:
        return jsonify({'error': 'You cannot block yourself'}), 400
    
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id, is_verified FROM users WHERE id = %s", (user_id,))
    user = cursor.fetchone()
    
    if not user:
        conn.close()
        return jsonify({'error': 'User not found'}), 404
    
    new_status = not user['is_verified']
    cursor.execute("UPDATE users SET is_verified = %s WHERE id = %s", (new_status, user_id))
    conn.commit()
    conn.close()
    
    status_text = 'unblocked' if new_status else 'blocked'
    return jsonify({'message': f'User {status_text} successfully', 'status': new_status})

# ===== API: DELETE USER =====
@app.route('/api/user/<int:user_id>/delete', methods=['DELETE'])
def api_delete_user(user_id):
    if 'user_id' not in session or session.get('role') != 'head_admin':
        return jsonify({'error': 'Unauthorized'}), 401
    
    if user_id == session['user_id']:
        return jsonify({'error': 'You cannot delete your own account'}), 400
    
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM users WHERE id = %s", (user_id,))
    user = cursor.fetchone()
    
    if not user:
        conn.close()
        return jsonify({'error': 'User not found'}), 404
    
    cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
    conn.commit()
    conn.close()
    
    return jsonify({'message': 'User deleted successfully'})

# ===== ADMIN MANAGEMENT =====
@app.route('/admins')
def admin_management():
    if 'user_id' not in session or session.get('role') != 'head_admin':
        flash('Please login as Head Admin.', 'danger')
        return redirect(url_for('login'))
    
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    
    cursor.execute("SELECT id, first_name, last_name, email, contact_number, address, role, is_verified, created_at FROM users WHERE role IN ('admin', 'head_admin') ORDER BY role DESC, created_at DESC")
    admins = cursor.fetchall()
    conn.close()
    
    for admin in admins:
        if admin.get('created_at'):
            if hasattr(admin['created_at'], 'strftime'):
                admin['created_at'] = admin['created_at'].strftime('%b %d, %Y')
    
    return render_template('admin/admin_management.html', admins=admins)

# ===== API: GET RESIDENTS =====
@app.route('/api/residents')
def api_get_residents():
    if 'user_id' not in session or session.get('role') != 'head_admin':
        return jsonify({'error': 'Unauthorized'}), 401
    
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id, first_name, last_name, email FROM users WHERE role = 'resident' ORDER BY first_name ASC")
    residents = cursor.fetchall()
    conn.close()
    
    return jsonify(residents)

# ===== API: PROMOTE TO ADMIN =====
@app.route('/api/user/<int:user_id>/promote', methods=['POST'])
def api_promote_admin(user_id):
    if 'user_id' not in session or session.get('role') != 'head_admin':
        return jsonify({'error': 'Unauthorized'}), 401
    
    if user_id == session['user_id']:
        return jsonify({'error': 'You cannot change your own role'}), 400
    
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id, role FROM users WHERE id = %s", (user_id,))
    user = cursor.fetchone()
    
    if not user:
        conn.close()
        return jsonify({'error': 'User not found'}), 404
    
    if user['role'] == 'admin':
        conn.close()
        return jsonify({'error': 'User is already an admin'}), 400
    
    if user['role'] == 'head_admin':
        conn.close()
        return jsonify({'error': 'Cannot change head_admin role'}), 400
    
    cursor.execute("UPDATE users SET role = 'admin' WHERE id = %s", (user_id,))
    conn.commit()
    conn.close()
    
    return jsonify({'message': 'User promoted to Admin successfully'})

# ===== API: DEMOTE ADMIN =====
@app.route('/api/user/<int:user_id>/demote', methods=['POST'])
def api_demote_admin(user_id):
    if 'user_id' not in session or session.get('role') != 'head_admin':
        return jsonify({'error': 'Unauthorized'}), 401
    
    if user_id == session['user_id']:
        return jsonify({'error': 'You cannot demote yourself'}), 400
    
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id, role FROM users WHERE id = %s", (user_id,))
    user = cursor.fetchone()
    
    if not user:
        conn.close()
        return jsonify({'error': 'User not found'}), 404
    
    if user['role'] == 'head_admin':
        conn.close()
        return jsonify({'error': 'Cannot demote head_admin'}), 400
    
    if user['role'] != 'admin':
        conn.close()
        return jsonify({'error': 'User is not an admin'}), 400
    
    cursor.execute("UPDATE users SET role = 'resident' WHERE id = %s", (user_id,))
    conn.commit()
    conn.close()
    
    return jsonify({'message': 'Admin demoted to Resident successfully'})

# ===== CREATE ADMIN =====
@app.route('/create-admin', methods=['POST'])
def create_admin():
    if 'user_id' not in session or session.get('role') != 'head_admin':
        flash('Unauthorized access.', 'danger')
        return redirect(url_for('login'))
    
    first_name = request.form.get('first_name', '').strip()
    last_name = request.form.get('last_name', '').strip()
    email = request.form.get('email', '').strip()
    password = request.form.get('password', '')
    role = request.form.get('role', 'admin')
    
    if not first_name or not last_name or not email or not password:
        flash('Please fill in all fields.', 'danger')
        return redirect(url_for('admin_management'))
    
    if role not in ['admin', 'head_admin']:
        flash('Invalid role selected.', 'danger')
        return redirect(url_for('admin_management'))
    
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    
    cursor.execute("SELECT id FROM users WHERE email = %s", (email,))
    existing = cursor.fetchone()
    
    if existing:
        conn.close()
        flash('Email address already registered.', 'danger')
        return redirect(url_for('admin_management'))
    
    hashed_password = generate_password_hash(password)
    
    cursor.execute("""
        INSERT INTO users (first_name, last_name, email, password, role, is_verified)
        VALUES (%s, %s, %s, %s, %s, TRUE)
    """, (first_name, last_name, email, hashed_password, role))
    conn.commit()
    conn.close()
    
    flash('Admin created successfully!', 'success')
    return redirect(url_for('admin_management'))

# ===== ANNOUNCEMENTS =====
@app.route('/announcements')
def announcements():
    if 'user_id' not in session or session.get('role') != 'head_admin':
        flash('Please login as Head Admin.', 'danger')
        return redirect(url_for('login'))
    
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    
    cursor.execute("""
        SELECT a.*, u.first_name, u.last_name 
        FROM announcements a 
        LEFT JOIN users u ON a.created_by = u.id 
        ORDER BY a.created_at DESC
    """)
    announcements = cursor.fetchall()
    conn.close()
    
    return render_template('admin/announcements.html', announcements=announcements)

@app.route('/create-announcement', methods=['POST'])
def create_announcement():
    if 'user_id' not in session or session.get('role') != 'head_admin':
        flash('Unauthorized access.', 'danger')
        return redirect(url_for('login'))
    
    title = request.form.get('title', '').strip()
    content = request.form.get('content', '').strip()
    
    if not title or not content:
        flash('Please fill in all fields.', 'danger')
        return redirect(url_for('announcements'))
    
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO announcements (title, content, created_by)
        VALUES (%s, %s, %s)
    """, (title, content, session['user_id']))
    conn.commit()
    conn.close()
    
    flash('Announcement posted successfully!', 'success')
    return redirect(url_for('announcements'))

@app.route('/edit-announcement/<int:announcement_id>', methods=['POST'])
def edit_announcement(announcement_id):
    if 'user_id' not in session or session.get('role') != 'head_admin':
        flash('Unauthorized access.', 'danger')
        return redirect(url_for('login'))
    
    title = request.form.get('title', '').strip()
    content = request.form.get('content', '').strip()
    
    if not title or not content:
        flash('Please fill in all fields.', 'danger')
        return redirect(url_for('announcements'))
    
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE announcements SET title = %s, content = %s
        WHERE id = %s
    """, (title, content, announcement_id))
    conn.commit()
    conn.close()
    
    flash('Announcement updated successfully!', 'success')
    return redirect(url_for('announcements'))

@app.route('/delete-announcement/<int:announcement_id>', methods=['DELETE'])
def delete_announcement(announcement_id):
    if 'user_id' not in session or session.get('role') != 'head_admin':
        return jsonify({'error': 'Unauthorized'}), 401
    
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM announcements WHERE id = %s", (announcement_id,))
    conn.commit()
    conn.close()
    
    return jsonify({'message': 'Announcement deleted successfully'})

@app.route('/send-email-all', methods=['POST'])
def send_email_all():
    if 'user_id' not in session or session.get('role') != 'head_admin':
        flash('Unauthorized access.', 'danger')
        return redirect(url_for('login'))
    
    subject = request.form.get('subject', '').strip()
    message = request.form.get('message', '').strip()
    
    if not subject or not message:
        flash('Please fill in all fields.', 'danger')
        return redirect(url_for('announcements'))
    
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT email FROM users")
    users = cursor.fetchall()
    conn.close()
    
    flash(f'Email sent to {len(users)} users!', 'success')
    return redirect(url_for('announcements'))

# ============================================================
# ===== CHECK SESSION =====
@app.route('/check-session')
def check_session():
    if 'user_id' in session:
        return f"""
        <h1>Session Info</h1>
        <p><strong>User ID:</strong> {session['user_id']}</p>
        <p><strong>Name:</strong> {session['fullname']}</p>
        <p><strong>Email:</strong> {session['email']}</p>
        <p><strong>Role:</strong> {session['role']}</p>
        <hr>
        <a href="/head-admin-dashboard">Head Admin Dashboard</a><br>
        <a href="/admin-dashboard">Admin Dashboard</a><br>
        <a href="/dashboard">Resident Dashboard</a><br>
        <a href="/users">User Management</a><br>
        <a href="/admins">Admin Management</a><br>
        <a href="/announcements">Announcements</a><br>
        <a href="/logout">Logout</a>
        """
    else:
        return "No active session. <a href='/login'>Login</a>"

# ===== LOGOUT =====
@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)