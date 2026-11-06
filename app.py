from flask import Flask, abort, render_template, request, redirect, url_for, session, flash, jsonify, send_file, send_from_directory
import mysql.connector
from werkzeug.security import check_password_hash, generate_password_hash
from functools import wraps
import os
import subprocess
import time
import datetime
import random
import glob
import secrets
import qrcode
import io
import base64
import uuid
from flask_mail import Mail, Message
from authlib.integrations.flask_client import OAuth
from dotenv import load_dotenv

# ============ LOAD ENVIRONMENT VARIABLES ============
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'fallback-secret-key-if-env-fails')

# ============================================================
# EMAIL CONFIGURATION - BARANGAY STO. NINO
# ============================================================
app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT', 587))
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = ('Barangay Sto. Nino', os.getenv('MAIL_USERNAME'))

mail = Mail(app)

# ============ GOOGLE OAUTH SETUP ============
oauth = OAuth(app)

google = oauth.register(
    name='google',
    client_id=os.getenv('GOOGLE_CLIENT_ID'),
    client_secret=os.getenv('GOOGLE_CLIENT_SECRET'),
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={'scope': 'openid email profile'}
)

# ============================================================
# EMAIL HELPER FUNCTION
# ============================================================
def send_email(to_email, subject, body_html):
    """Send email helper. Returns True if success, False if failed."""
    try:
        msg = Message(
            subject=subject,
            recipients=[to_email],
            html=body_html
        )
        mail.send(msg)
        print(f"Email sent to {to_email}: {subject}")
        return True
    except Exception as e:
        print(f"Email failed to {to_email}: {str(e)}")
        return False

# ============================================================
# RBAC DECORATORS
# ============================================================
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please login first.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def role_required(*allowed_roles):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'user_id' not in session:
                flash('Please login first.', 'warning')
                return redirect(url_for('login'))
            if session.get('role') not in allowed_roles:
                flash('Unauthorized access.', 'danger')
                role = session.get('role')
                if role == 'head_admin':
                    return redirect(url_for('head_admin_dashboard'))
                elif role == 'admin_documents':
                    return redirect(url_for('sec_admin_dashboard'))
                elif role == 'admin_court_1':
                    return redirect(url_for('court1_dashboard'))
                elif role == 'admin_court_2':
                    return redirect(url_for('court2_dashboard'))
                elif role == 'admin_court_3':
                    return redirect(url_for('court3_dashboard'))
                elif role == 'admin_court_4':
                    return redirect(url_for('court4_dashboard'))
                return redirect(url_for('login'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator

# ============================================================
# ROLE DEFINITIONS
# ============================================================
ADMIN_ROLES = ['head_admin', 'admin_court_1', 'admin_court_2', 'admin_court_3', 'admin_court_4', 'admin_documents']
COURT_ROLES = ['admin_court_1', 'admin_court_2', 'admin_court_3', 'admin_court_4']
ALL_ROLES = ['resident', 'head_admin', 'admin_court_1', 'admin_court_2', 'admin_court_3', 'admin_court_4', 'admin_documents']

# ============================================================
# COURT CONFIGURATION
# ============================================================
COURT_CONFIG = {
    'admin_court_1': {
        'venue': 'Sto. Nino Sports Complex',
        'dashboard_template': 'admin/admin_court1_dashboard.html',
        'calendar_template': 'admin/admin_court1_calendar.html',
        'pending_template': 'admin/admin_court1_pending.html',
        'reviewed_template': 'admin/admin_court1_reviewed.html',
        'label': 'Court 1',
        'icon': 'fa-building',
        'subtitle': 'Sto. Nino Sports Complex'
    },
    'admin_court_2': {
        'venue': 'Sto. Nino Basketball Court',
        'dashboard_template': 'admin/admin_court2_dashboard.html',
        'calendar_template': 'admin/admin_court2_calendar.html',
        'pending_template': 'admin/admin_court2_pending.html',
        'reviewed_template': 'admin/admin_court2_reviewed.html',
        'label': 'Court 2',
        'icon': 'fa-basketball-ball',
        'subtitle': 'Sto. Nino Basketball Court'
    },
    'admin_court_3': {
        'venue': 'Sampaguita Covered Court',
        'dashboard_template': 'admin/admin_court3_dashboard.html',
        'calendar_template': 'admin/admin_court3_calendar.html',
        'pending_template': 'admin/admin_court3_pending.html',
        'reviewed_template': 'admin/admin_court3_reviewed.html',
        'label': 'Court 3',
        'icon': 'fa-tree',
        'subtitle': 'Sampaguita Covered Court'
    },
    'admin_court_4': {
        'venue': '2nd Street Covered Court',
        'dashboard_template': 'admin/admin_court4_dashboard.html',
        'calendar_template': 'admin/admin_court4_calendar.html',
        'pending_template': 'admin/admin_court4_pending.html',
        'reviewed_template': 'admin/admin_court4_reviewed.html',
        'label': 'Court 4',
        'icon': 'fa-road',
        'subtitle': '2nd Street Covered Court'
    }
}

# ============================================================
# FILE UPLOAD CONFIGURATION
# ============================================================
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'pdf', 'doc', 'docx'}

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def save_uploaded_file(file):
    if file and file.filename:
        if not allowed_file(file.filename):
            return None
        ext = file.filename.rsplit('.', 1)[1].lower()
        new_filename = f"{uuid.uuid4().hex}.{ext}"
        filepath = os.path.join(UPLOAD_FOLDER, new_filename)
        file.save(filepath)
        return new_filename
    return None

@app.route('/uploads/<filename>')
@login_required
def uploaded_file(filename):
    if '..' in filename or filename.startswith('/'):
        abort(404)
    return send_from_directory('uploads', filename)

# ============================================================
# HOME/INDEX ROUTE
# ============================================================
@app.route('/')
def index():
    return redirect(url_for('login'))

# ============================================================
# DATABASE CONNECTION
# ============================================================
def get_db():
    return mysql.connector.connect(
        host=os.getenv('DB_HOST', '127.0.0.1'),
        port=int(os.getenv('DB_PORT', 3306)),
        user=os.getenv('DB_USER', 'root'),
        password=os.getenv('DB_PASSWORD', ''),
        database=os.getenv('DB_NAME', 'barangay_online_services')
    )

def generate_qr_token():
    return secrets.token_urlsafe(32)

def generate_qr_base64(data_text):
    qr = qrcode.QRCode(version=1, box_size=10, border=4)
    qr.add_data(data_text)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    buffered = io.BytesIO()
    img.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()

def is_maintenance_mode():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT maintenance_mode FROM system_config WHERE id = 1")
        config = cursor.fetchone()
        return bool(config['maintenance_mode']) if config else False
    except:
        return False
    finally:
        conn.close()

# ============================================================
# QR CODE IMAGE ROUTE
# ============================================================
@app.route('/generate-qr/<string:token>')
def generate_qr_image(token):
    qr = qrcode.QRCode(version=1, box_size=10, border=4)
    qr.add_data(token)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    buffered = io.BytesIO()
    img.save(buffered, format="PNG")
    buffered.seek(0)
    return send_file(buffered, mimetype='image/png')

# ============================================================
# NOTIFICATION HELPER FUNCTIONS
# ============================================================
def create_notification(user_id, title, message, notif_type, link=None):
    conn = get_db()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO notifications (user_id, title, message, notification_type, link)
            VALUES (%s, %s, %s, %s, %s)
        """, (user_id, title, message, notif_type, link))
        conn.commit()
        return True
    except Exception as e:
        print(f"Notification error: {e}")
        return False
    finally:
        conn.close()

def notify_role(roles, title, message, notif_type, link=None):
    if not roles:
        return []
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    try:
        placeholders = ','.join(['%s'] * len(roles))
        cursor.execute(
            f"SELECT id, email, first_name FROM users WHERE role IN ({placeholders})",
            tuple(roles)
        )
        admins = cursor.fetchall()
    finally:
        conn.close()
    for admin in admins:
        create_notification(admin['id'], title, message, notif_type, link)
    return admins

def get_court_role_by_venue(venue):
    venue_mapping = {
        'Sto. Nino Sports Complex': 'admin_court_1',
        'Sto. Nino Basketball Court': 'admin_court_2',
        'Sampaguita Covered Court': 'admin_court_3',
        '2nd Street Covered Court': 'admin_court_4',
    }
    return venue_mapping.get(venue)

def send_admin_notification_email(recipient_email, subject, title, message,
                                   reference_no=None, applicant_name=None,
                                   action_type='new'):
    if action_type == 'new':
        icon = '🔔'
        header_text = 'New Request Received'
    elif action_type == 'approved':
        icon = '✅'
        header_text = 'Request Approved'
    else:
        icon = '❌'
        header_text = 'Request Rejected'

    body_html = f"""
    <!DOCTYPE html>
    <html>
    <body style="margin:0;padding:0;background:#f4f8f5;font-family:'Segoe UI',Tahoma,sans-serif;">
        <table width="100%" style="background:#f4f8f5;padding:40px 15px;">
            <tr><td align="center">
                <table width="600" style="max-width:600px;background:#fff;border-radius:16px;overflow:hidden;box-shadow:0 8px 30px rgba(0,0,0,0.08);">
                    <tr>
                        <td style="background:linear-gradient(135deg,#0f3d2a,#228b54);padding:35px;text-align:center;">
                            <div style="width:70px;height:70px;background:#fff;border-radius:50%;line-height:70px;font-size:32px;margin:0 auto 12px;">{icon}</div>
                            <h1 style="margin:0;color:#fff;font-size:22px;">{header_text}</h1>
                            <p style="margin:6px 0 0;color:#c9d6f0;font-size:11px;letter-spacing:2px;text-transform:uppercase;">Barangay Sto. Nino Admin</p>
                        </td>
                    </tr>
                    <tr>
                        <td style="padding:35px 40px;">
                            <h2 style="margin:0 0 15px;color:#0f3d2a;font-size:20px;">{title}</h2>
                            <p style="margin:0 0 20px;color:#64748b;font-size:14px;line-height:1.7;">{message}</p>
                            {f'<p style="margin:0 0 10px;color:#334155;font-size:14px;"><strong>Reference:</strong> {reference_no}</p>' if reference_no else ''}
                            {f'<p style="margin:0 0 10px;color:#334155;font-size:14px;"><strong>Applicant:</strong> {applicant_name}</p>' if applicant_name else ''}
                            <table width="100%" style="margin:25px 0 10px;">
                                <tr><td align="center">
                                    <a href="http://127.0.0.1:5000/login" style="display:inline-block;background:linear-gradient(135deg,#0f3d2a,#228b54);color:#fff;padding:14px 40px;text-decoration:none;border-radius:10px;font-weight:700;font-size:14px;">
                                        Login to Admin Panel
                                    </a>
                                </td></tr>
                            </table>
                        </td>
                    </tr>
                    <tr>
                        <td style="background:linear-gradient(135deg,#0f3d2a,#228b54);padding:20px;text-align:center;">
                            <p style="margin:0;color:#c9d6f0;font-size:11px;">© 2026 Barangay Sto. Nino. Automated message.</p>
                        </td>
                    </tr>
                </table>
            </td></tr>
        </table>
    </body>
    </html>
    """
    return send_email(recipient_email, subject, body_html)

# ============================================================
# QUEUE NUMBER GENERATOR
# ============================================================
def get_next_queue_number(table_name, venue=None):
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    today = datetime.date.today()
    try:
        if table_name == 'event_permits':
            if venue:
                cursor.execute("""
                    SELECT COALESCE(MAX(CAST(SUBSTRING(queuing_number, LOCATE('-Q', queuing_number) + 2) AS UNSIGNED)), 0) as max_num
                    FROM event_permits
                    WHERE DATE(requested_at) = %s AND venue = %s
                """, (today, venue))
                count = int(cursor.fetchone()['max_num'] or 0) + 1
                court_role = get_court_role_by_venue(venue)
                court_num = court_role.replace('admin_court_', '') if court_role else '0'
                return f"C{court_num}-Q{count:03d}"
            else:
                cursor.execute("""
                    SELECT COUNT(*) as total FROM event_permits
                    WHERE DATE(requested_at) = %s
                """, (today,))
                count = (cursor.fetchone()['total'] or 0) + 1
                return f"Q-{count:03d}"
        else:
            cursor.execute("""
                SELECT COUNT(*) as total FROM document_requests
                WHERE DATE(created_at) = %s
            """, (today,))
            count = (cursor.fetchone()['total'] or 0) + 1
            return f"Q-{count:03d}"
    finally:
        conn.close()

# ============================================================
# MAINTENANCE MODE CHECKER
# ============================================================
@app.before_request
def check_maintenance():
    allowed_endpoints = ['login', 'static', 'login_google', 'authorize_google', 'forgot_password', 'show_reset_page', 'verify_reset_code']
    if request.endpoint in allowed_endpoints:
        return
    if session.get('role') in ADMIN_ROLES:
        return
    if is_maintenance_mode():
        session.clear()
        flash('The system is currently under maintenance. Please try again later.', 'warning')
        return redirect(url_for('login'))

# ============================================================
# LOGIN ROUTE
# ============================================================
@app.route('/login', methods=['GET', 'POST'])
def login():
    if session.get('login_attempts', 0) >= 3:
        lockout_time = session.get('lockout_time', 0)
        current_time = time.time()
        if current_time < lockout_time:
            remaining = int(lockout_time - current_time)
            lockout_msg = f"Too many failed attempts. Please wait {remaining} seconds before trying again."
            return render_template('login.html', login_error=True, lockout_message=lockout_msg)
        else:
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
            if not user['is_verified']:
                flash('Your account has been deactivated. Please contact the administrator.', 'danger')
                return render_template('login.html')

            if not check_password_hash(user['password'], password):
                session['login_attempts'] = session.get('login_attempts', 0) + 1
                if session['login_attempts'] >= 3:
                    session['lockout_time'] = time.time() + 30
                    lockout_msg = "Too many failed attempts. Please wait 30 seconds before trying again."
                    return render_template('login.html', login_error=True, lockout_message=lockout_msg)
                return render_template('login.html', login_error=True)

            if role == 'admin' and user['role'] not in ADMIN_ROLES:
                flash('You are not authorized as admin.', 'danger')
                return render_template('login.html')

            if role == 'resident' and user['role'] in ADMIN_ROLES:
                flash('This is an Admin account. Please select "Admin" in the dropdown to login.', 'danger')
                return render_template('login.html')

            session['user_id'] = user['id']
            session['fullname'] = f"{user['first_name']} {user['last_name']}"
            session['email'] = user['email']
            session['role'] = user['role']

            flash(f'Welcome back, {session["fullname"]}!', 'success')

            try:
                log_conn = get_db()
                log_cursor = log_conn.cursor()
                log_cursor.execute("""
                    INSERT INTO admin_activity_logs (admin_id, action, document_id, details)
                    VALUES (%s, %s, %s, %s)
                """, (user['id'], 'login', None, f'{user["role"]} logged in from {request.remote_addr}'))
                log_conn.commit()
                log_conn.close()
            except Exception as e:
                print(f"Login log error: {e}")

            if user['role'] == 'head_admin':
                return redirect(url_for('head_admin_dashboard'))
            elif user['role'] == 'admin_documents':
                return redirect(url_for('sec_admin_dashboard'))
            elif user['role'] == 'admin_court_1':
                return redirect(url_for('court1_dashboard'))
            elif user['role'] == 'admin_court_2':
                return redirect(url_for('court2_dashboard'))
            elif user['role'] == 'admin_court_3':
                return redirect(url_for('court3_dashboard'))
            elif user['role'] == 'admin_court_4':
                return redirect(url_for('court4_dashboard'))
            return redirect(url_for('dashboard'))
        else:
            session['login_attempts'] = session.get('login_attempts', 0) + 1
            if session['login_attempts'] >= 3:
                session['lockout_time'] = time.time() + 30
                lockout_msg = "Too many failed attempts. Please wait 30 seconds before trying again."
                return render_template('login.html', login_error=True, lockout_message=lockout_msg)
            return render_template('login.html', login_error=True)

    return render_template('login.html')

# ============================================================
# GOOGLE LOGIN ROUTES
# ============================================================
@app.route('/login/google')
def login_google():
    redirect_uri = url_for('authorize_google', _external=True)
    return google.authorize_redirect(redirect_uri)

@app.route('/login/google/authorized')
def authorize_google():
    try:
        token = google.authorize_access_token()
        user_info = token.get('userinfo')
        if not user_info:
            flash('Hindi makuha ang Google user info. Please try again.', 'danger')
            return redirect(url_for('login'))
        google_id = user_info['sub']
        email = user_info['email']
        name = user_info.get('name', email.split('@')[0])
        name_parts = name.split(' ', 1)
        first_name = name_parts[0]
        last_name = name_parts[1] if len(name_parts) > 1 else ''

        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()
        if user:
            if not user.get('google_id'):
                cursor.execute("UPDATE users SET google_id = %s WHERE id = %s", (google_id, user['id']))
                conn.commit()
            if not user['is_verified']:
                conn.close()
                flash('Your account has been deactivated. Please contact the administrator.', 'danger')
                return redirect(url_for('login'))
        else:
            cursor.execute("""
                INSERT INTO users (first_name, last_name, email, password, google_id, role, is_verified)
                VALUES (%s, %s, %s, NULL, %s, 'resident', TRUE)
            """, (first_name, last_name, email, google_id))
            conn.commit()
            cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
            user = cursor.fetchone()
        conn.close()

        session['user_id'] = user['id']
        session['fullname'] = f"{user['first_name']} {user['last_name']}"
        session['email'] = user['email']
        session['role'] = user['role']
        flash(f'Welcome back, {session["fullname"]}!', 'success')

        if user['role'] == 'resident':
            return redirect(url_for('dashboard'))
        role = user['role']
        if role == 'head_admin':
            return redirect(url_for('head_admin_dashboard'))
        elif role == 'admin_documents':
            return redirect(url_for('sec_admin_dashboard'))
        elif role == 'admin_court_1':
            return redirect(url_for('court1_dashboard'))
        elif role == 'admin_court_2':
            return redirect(url_for('court2_dashboard'))
        elif role == 'admin_court_3':
            return redirect(url_for('court3_dashboard'))
        elif role == 'admin_court_4':
            return redirect(url_for('court4_dashboard'))
        return redirect(url_for('dashboard'))

    except Exception as e:
        print(f"Google login error: {e}")
        import traceback
        traceback.print_exc()
        flash('Google login failed. Please try again.', 'danger')
        return redirect(url_for('login'))

# ============================================================
# REGISTER ROUTE
# ============================================================
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

        subject = "Welcome to Barangay Sto. Nino Online Services!"
        body_html = f"""
        <!DOCTYPE html>
        <html><body style="margin:0;padding:0;background:#eef2f7;font-family:'Segoe UI',Tahoma,sans-serif;">
        <table width="100%" style="background:#eef2f7;padding:40px 15px;">
        <tr><td align="center">
        <table width="600" style="max-width:600px;background:#fff;border-radius:16px;overflow:hidden;box-shadow:0 8px 30px rgba(0,0,0,0.08);">
            <tr><td style="background:linear-gradient(135deg,#0f3d2a 0%,#145233 60%,#3b7dd8 100%);padding:45px 30px 35px;text-align:center;">
                <div style="width:80px;height:80px;background:#fff;border-radius:50%;margin:0 auto 18px;line-height:80px;font-size:38px;">🏛️</div>
                <h1 style="margin:0;color:#fff;font-size:24px;">Barangay Sto. Nino</h1>
                <p style="margin:8px 0 0;color:#c9d6f0;font-size:12px;letter-spacing:2px;text-transform:uppercase;">Online Services Portal</p>
            </td></tr>
            <tr><td style="padding:40px;">
                <h2 style="margin:0 0 12px;color:#0f3d2a;font-size:26px;text-align:center;">Welcome, {first_name}!</h2>
                <p style="margin:0 0 30px;color:#64748b;font-size:15px;line-height:1.7;text-align:center;">Your account has been successfully created.</p>
                <p style="margin:0 0 15px;color:#0f3d2a;font-size:12px;font-weight:700;text-transform:uppercase;letter-spacing:1.5px;">Account Details</p>
                <table width="100%" style="background:#f8fafc;border-radius:12px;padding:20px;border:1px solid #e2e8f0;">
                    <tr><td style="padding:8px 0;color:#94a3b8;font-size:13px;width:130px;">Email</td><td style="padding:8px 0;color:#1e293b;font-size:14px;font-weight:600;">{email}</td></tr>
                    <tr><td style="padding:8px 0;color:#94a3b8;font-size:13px;">Account Type</td><td style="padding:8px 0;color:#1e293b;font-size:14px;font-weight:600;">Resident</td></tr>
                    <tr><td style="padding:8px 0;color:#94a3b8;font-size:13px;">Date Registered</td><td style="padding:8px 0;color:#1e293b;font-size:14px;font-weight:600;">{datetime.datetime.now().strftime('%B %d, %Y')}</td></tr>
                </table>
                <table width="100%" style="margin:30px 0 10px;"><tr><td align="center">
                    <a href="http://127.0.0.1:5000/login" style="display:inline-block;background:linear-gradient(135deg,#0f3d2a 0%,#2a5298 100%);color:#fff;padding:16px 50px;text-decoration:none;border-radius:10px;font-weight:700;font-size:15px;">Login to Your Account</a>
                </td></tr></table>
            </td></tr>
            <tr><td style="background:linear-gradient(135deg,#0f3d2a 0%,#2a5298 100%);padding:30px 40px;text-align:center;">
                <p style="margin:0 0 8px;color:#fff;font-size:14px;font-weight:700;">Barangay Sto. Nino</p>
                <p style="margin:0;color:#c9d6f0;font-size:12px;">Parañaque City, Metro Manila</p>
            </td></tr>
        </table>
        </td></tr></table>
        </body></html>
        """
        send_email(email, subject, body_html)

        flash('Registration successful! Please check your email. You can now login.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')

# ============================================================
# RESIDENT ROUTES
# ============================================================
@app.route('/dashboard')
@role_required('resident')
def dashboard():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM users WHERE id = %s", (session['user_id'],))
    user = cursor.fetchone()

    cursor.execute("SELECT COUNT(*) as total FROM document_requests WHERE user_id = %s", (session['user_id'],))
    total_docs = cursor.fetchone()['total']

    cursor.execute("SELECT COUNT(*) as pending FROM document_requests WHERE user_id = %s AND status = 'pending'", (session['user_id'],))
    pending_docs = cursor.fetchone()['pending']

    cursor.execute("SELECT COUNT(*) as processing FROM document_requests WHERE user_id = %s AND status = 'processing'", (session['user_id'],))
    processing_docs = cursor.fetchone()['processing']

    cursor.execute("SELECT COUNT(*) as ready FROM document_requests WHERE user_id = %s AND status = 'ready_for_pickup'", (session['user_id'],))
    ready_docs = cursor.fetchone()['ready']

    cursor.execute("SELECT COUNT(*) as rejected FROM document_requests WHERE user_id = %s AND status = 'rejected'", (session['user_id'],))
    rejected_docs = cursor.fetchone()['rejected']

    cursor.execute("SELECT COUNT(*) as total FROM event_permits WHERE user_id = %s", (session['user_id'],))
    total_events = cursor.fetchone()['total']

    cursor.execute("SELECT COUNT(*) as pending FROM event_permits WHERE user_id = %s AND status = 'pending'", (session['user_id'],))
    pending_events = cursor.fetchone()['pending']

    cursor.execute("SELECT COUNT(*) as approved FROM event_permits WHERE user_id = %s AND status = 'approved'", (session['user_id'],))
    approved_events = cursor.fetchone()['approved']

    cursor.execute("SELECT COUNT(*) as rejected FROM event_permits WHERE user_id = %s AND status = 'rejected'", (session['user_id'],))
    rejected_events = cursor.fetchone()['rejected']

    cursor.execute("""
        SELECT * FROM announcements
        WHERE is_draft = FALSE
        ORDER BY is_pinned DESC, created_at DESC
        LIMIT 5
    """)
    announcements = cursor.fetchall()

    cursor.execute("SELECT * FROM document_requests WHERE user_id = %s ORDER BY created_at DESC LIMIT 5", (session['user_id'],))
    recent_docs = cursor.fetchall()

    cursor.execute("""
        SELECT id, event_name, event_date, start_time, end_time, venue,
               status, reference_number, queuing_number, requested_at
        FROM event_permits
        WHERE user_id = %s
        ORDER BY requested_at DESC
        LIMIT 5
    """, (session['user_id'],))
    recent_events = cursor.fetchall()
    conn.close()

    return render_template('dashboard.html',
                         user=user,
                         total_docs=total_docs,
                         pending_docs=pending_docs,
                         processing_docs=processing_docs,
                         ready_docs=ready_docs,
                         rejected_docs=rejected_docs,
                         total_events=total_events,
                         pending_events=pending_events,
                         approved_events=approved_events,
                         rejected_events=rejected_events,
                         announcements=announcements,
                         recent_docs=recent_docs,
                         recent_events=recent_events)

@app.route('/faqs')
def faqs():
    return render_template('faqs.html')

@app.route('/profile')
@role_required('resident')
def profile():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE id = %s", (session['user_id'],))
    user = cursor.fetchone()
    conn.close()
    return render_template('profile.html', user=user)

@app.route('/user-update-profile', methods=['POST'])
@role_required('resident')
def user_update_profile():
    first_name = request.form.get('first_name', '').strip()
    last_name = request.form.get('last_name', '').strip()
    email = request.form.get('email', '').strip()
    contact_number = request.form.get('contact_number', '').strip()
    address = request.form.get('address', '').strip()

    if not first_name or not last_name or not email:
        flash('Please fill in all required fields.', 'danger')
        return redirect(url_for('user_settings'))

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE users SET
            first_name = %s,
            last_name = %s,
            email = %s,
            contact_number = %s,
            address = %s
        WHERE id = %s
    """, (first_name, last_name, email, contact_number, address, session['user_id']))
    conn.commit()
    conn.close()

    session['fullname'] = f"{first_name} {last_name}"
    session['email'] = email

    subject = "Profile Update Confirmation - Barangay Sto. Nino"
    body_html = f"""
    <!DOCTYPE html>
    <html>
    <body style="margin:0;padding:0;background:#f4f8f5;font-family:'Segoe UI',Tahoma,sans-serif;">
        <table width="100%" style="background:#f4f8f5;padding:40px 15px;">
            <tr><td align="center">
                <table width="600" style="max-width:600px;background:#fff;border-radius:16px;overflow:hidden;box-shadow:0 8px 30px rgba(0,0,0,0.08);">
                    <tr>
                        <td style="background:linear-gradient(135deg,#0f3d2a,#228b54);padding:35px;text-align:center;">
                            <div style="width:70px;height:70px;background:#fff;border-radius:50%;line-height:70px;font-size:32px;margin:0 auto 12px;">✅</div>
                            <h1 style="margin:0;color:#fff;font-size:22px;">Profile Updated Successfully</h1>
                        </td>
                    </tr>
                    <tr>
                        <td style="padding:35px 40px;">
                            <h2 style="margin:0 0 15px;color:#0f3d2a;font-size:20px;">Hello, {first_name}!</h2>
                            <p style="margin:0 0 20px;color:#64748b;font-size:14px;line-height:1.7;">
                                Your profile details have been successfully updated. Here are your current information:
                            </p>
                            <table style="background:#f4f8f5;padding:15px;border-radius:10px;margin:20px 0;width:100%;">
                                <tr><td style="padding:6px 0;"><strong>Full Name:</strong> {first_name} {last_name}</td></tr>
                                <tr><td style="padding:6px 0;"><strong>Email:</strong> {email}</td></tr>
                                <tr><td style="padding:6px 0;"><strong>Contact No:</strong> {contact_number if contact_number else 'N/A'}</td></tr>
                                <tr><td style="padding:6px 0;"><strong>Address:</strong> {address if address else 'N/A'}</td></tr>
                            </table>
                        </td>
                    </tr>
                </table>
            </td></tr>
        </table>
    </body>
    </html>
    """
    send_email(email, subject, body_html)

    flash('Profile updated successfully! A confirmation email has been sent.', 'success')
    return redirect(url_for('user_settings'))

@app.route('/user-change-password', methods=['POST'])
@role_required('resident')
def user_change_password():
    current_password = request.form.get('current_password', '')
    new_password = request.form.get('new_password', '')
    confirm_password = request.form.get('confirm_password', '')

    if not current_password or not new_password or not confirm_password:
        flash('Please fill in all fields.', 'danger')
        return redirect(url_for('user_settings'))

    if new_password != confirm_password:
        flash('New passwords do not match.', 'danger')
        return redirect(url_for('user_settings'))

    if len(new_password) < 8:
        flash('New password must be at least 8 characters.', 'danger')
        return redirect(url_for('user_settings'))

    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT password, email, first_name FROM users WHERE id = %s", (session['user_id'],))
    user = cursor.fetchone()

    if not user or not check_password_hash(user['password'], current_password):
        conn.close()
        flash('Current password is incorrect.', 'danger')
        return redirect(url_for('user_settings'))

    hashed_password = generate_password_hash(new_password)
    cursor.execute("UPDATE users SET password = %s WHERE id = %s", (hashed_password, session['user_id']))
    conn.commit()
    conn.close()

    subject = "Password Changed Successfully - Barangay Sto. Nino"
    body_html = f"""
    <!DOCTYPE html>
    <html>
    <body style="margin:0;padding:0;background:#f4f8f5;font-family:'Segoe UI',Tahoma,sans-serif;">
        <table width="100%" style="background:#f4f8f5;padding:40px 15px;">
            <tr><td align="center">
                <table width="600" style="max-width:600px;background:#fff;border-radius:16px;overflow:hidden;box-shadow:0 8px 30px rgba(0,0,0,0.08);">
                    <tr>
                        <td style="background:linear-gradient(135deg,#0f3d2a,#2a5298);padding:35px;text-align:center;">
                            <div style="width:70px;height:70px;background:#fff;border-radius:50%;line-height:70px;font-size:32px;margin:0 auto 12px;">🔒</div>
                            <h1 style="margin:0;color:#fff;font-size:22px;">Password Changed</h1>
                        </td>
                    </tr>
                    <tr>
                        <td style="padding:35px 40px;">
                            <h2 style="margin:0 0 15px;color:#0f3d2a;font-size:20px;">Hello, {user['first_name']}!</h2>
                            <p style="margin:0 0 20px;color:#64748b;font-size:14px;line-height:1.7;">
                                Your password has been successfully changed.
                            </p>
                            <table style="background:#fef2f2;border-left:4px solid #ef4444;padding:15px;border-radius:10px;margin:20px 0;width:100%;">
                                <tr><td style="color:#991b1b;font-size:13px;">
                                    ⚠️ <strong>If you did not make this change,</strong> please contact the Barangay Office immediately.
                                </td></tr>
                            </table>
                        </td>
                    </tr>
                </table>
            </td></tr>
        </table>
    </body>
    </html>
    """
    send_email(user['email'], subject, body_html)

    flash('Password changed successfully! A confirmation email has been sent.', 'success')
    return redirect(url_for('user_settings'))

# ============================================================
# EVENTS CALENDAR (RESIDENT)
# ============================================================
@app.route('/events-calendar')
def events_calendar():
    if 'user_id' not in session:
        flash('Please login first.', 'warning')
        return redirect(url_for('login'))
    return render_template('events_calendar.html')

@app.route('/events')
def events():
    return redirect(url_for('events_calendar'))

@app.route('/barangay-map')
def barangay_map():
    return render_template('barangay_map.html')

# ============================================================
# EVENT CRUD API
# ============================================================
@app.route('/api/events', methods=['GET'])
def api_get_events():
    if 'user_id' not in session:
        return jsonify({'error': 'Please login first.'}), 401

    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT e.*, u.first_name, u.last_name
        FROM event_permits e
        JOIN users u ON e.user_id = u.id
        WHERE e.status = 'approved'
        ORDER BY e.event_date DESC
    """)
    events = cursor.fetchall()
    conn.close()

    for event in events:
        if event.get('event_date') and hasattr(event['event_date'], 'strftime'):
            event['event_date'] = event['event_date'].strftime('%Y-%m-%d')
        if event.get('requested_at') and hasattr(event['requested_at'], 'strftime'):
            event['requested_at'] = event['requested_at'].strftime('%Y-%m-%d %H:%M:%S')
        if event.get('start_time'):
            event['start_time'] = str(event['start_time'])
        if event.get('end_time'):
            event['end_time'] = str(event['end_time'])
    return jsonify({'success': True, 'events': events})

@app.route('/api/events/<int:event_id>', methods=['GET'])
def api_get_event(event_id):
    if 'user_id' not in session:
        return jsonify({'error': 'Please login first.'}), 401

    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT e.*, u.first_name, u.last_name, u.email
        FROM event_permits e
        JOIN users u ON e.user_id = u.id
        WHERE e.id = %s
    """, (event_id,))
    event = cursor.fetchone()
    conn.close()

    if not event:
        return jsonify({'error': 'Event not found'}), 404

    if event.get('event_date') and hasattr(event['event_date'], 'strftime'):
        event['event_date'] = event['event_date'].strftime('%Y-%m-%d')
    if event.get('requested_at') and hasattr(event['requested_at'], 'strftime'):
        event['requested_at'] = event['requested_at'].strftime('%Y-%m-%d %H:%M:%S')
    if event.get('start_time'):
        event['start_time'] = str(event['start_time'])
    if event.get('end_time'):
        event['end_time'] = str(event['end_time'])
    return jsonify({'success': True, 'event': event})

@app.route('/api/events/<int:event_id>', methods=['PUT'])
def api_update_event(event_id):
    if 'user_id' not in session:
        return jsonify({'error': 'Please login first.'}), 401

    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM event_permits WHERE id = %s AND user_id = %s", (event_id, session['user_id']))
    event = cursor.fetchone()

    if not event:
        conn.close()
        return jsonify({'error': 'Event not found or you do not have permission'}), 404

    if event['status'] != 'pending':
        conn.close()
        return jsonify({'error': 'Only pending events can be edited'}), 400

    data = request.get_json()
    event_name = data.get('event_name', event['event_name']).strip()
    event_description = data.get('event_description', event['event_description']).strip()
    purpose = data.get('purpose', event.get('purpose', '')).strip()
    contact_person = data.get('contact_person', event.get('contact_person', '')).strip()
    contact_phone = data.get('contact_phone', event.get('contact_phone', '')).strip()
    event_date = data.get('event_date', str(event['event_date'])).strip()
    start_time = data.get('start_time', str(event['start_time'])).strip()[:5]
    end_time = data.get('end_time', str(event['end_time'])).strip()[:5]
    estimated_attendees = data.get('estimated_attendees', event['estimated_attendees'])
    venue = data.get('venue', event['venue']).strip()

    if not event_name or not event_date or not start_time or not end_time or not venue:
        conn.close()
        return jsonify({'error': 'Please fill in all required fields.'}), 400
    if not purpose:
        conn.close()
        return jsonify({'error': 'Purpose is required.'}), 400
    if not contact_person:
        conn.close()
        return jsonify({'error': 'Contact person is required.'}), 400
    if not contact_phone:
        conn.close()
        return jsonify({'error': 'Contact phone is required.'}), 400
    if start_time >= end_time:
        conn.close()
        return jsonify({'error': 'End time must be after start time.'}), 400

    cursor.execute("""
        UPDATE event_permits SET
            event_name = %s,
            event_description = %s,
            purpose = %s,
            contact_person = %s,
            contact_phone = %s,
            event_date = %s,
            start_time = %s,
            end_time = %s,
            estimated_attendees = %s,
            venue = %s
        WHERE id = %s
    """, (event_name, event_description, purpose, contact_person, contact_phone,
          event_date, start_time, end_time, estimated_attendees, venue, event_id))
    conn.commit()
    conn.close()
    return jsonify({'success': True, 'message': 'Event updated successfully'})

@app.route('/api/events/<int:event_id>', methods=['DELETE'])
def api_delete_event(event_id):
    if 'user_id' not in session:
        return jsonify({'error': 'Please login first.'}), 401

    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM event_permits WHERE id = %s AND user_id = %s", (event_id, session['user_id']))
    event = cursor.fetchone()

    if not event:
        conn.close()
        return jsonify({'error': 'Event not found or you do not have permission'}), 404
    if event['status'] != 'pending':
        conn.close()
        return jsonify({'error': 'Only pending events can be deleted'}), 400

    cursor.execute("DELETE FROM event_permits WHERE id = %s", (event_id,))
    conn.commit()
    conn.close()
    return jsonify({'success': True, 'message': 'Event deleted successfully'})

@app.route('/my-requests')
@role_required('resident')
def my_requests():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM document_requests WHERE user_id = %s ORDER BY created_at DESC", (session['user_id'],))
    document_requests = cursor.fetchall()

    cursor.execute("SELECT * FROM event_permits WHERE user_id = %s ORDER BY requested_at DESC", (session['user_id'],))
    event_permits = cursor.fetchall()

    cursor.execute("SELECT COUNT(*) as total FROM document_requests WHERE user_id = %s", (session['user_id'],))
    total_docs = cursor.fetchone()['total']
    cursor.execute("SELECT COUNT(*) as pending FROM document_requests WHERE user_id = %s AND status = 'pending'", (session['user_id'],))
    pending_docs = cursor.fetchone()['pending']
    cursor.execute("SELECT COUNT(*) as processing FROM document_requests WHERE user_id = %s AND status = 'processing'", (session['user_id'],))
    processing_docs = cursor.fetchone()['processing']
    cursor.execute("SELECT COUNT(*) as ready FROM document_requests WHERE user_id = %s AND status = 'ready_for_pickup'", (session['user_id'],))
    ready_docs = cursor.fetchone()['ready']
    cursor.execute("SELECT COUNT(*) as rejected FROM document_requests WHERE user_id = %s AND status = 'rejected'", (session['user_id'],))
    rejected_docs = cursor.fetchone()['rejected']

    cursor.execute("SELECT COUNT(*) as total FROM event_permits WHERE user_id = %s", (session['user_id'],))
    total_events = cursor.fetchone()['total']
    cursor.execute("SELECT COUNT(*) as pending FROM event_permits WHERE user_id = %s AND status = 'pending'", (session['user_id'],))
    pending_events = cursor.fetchone()['pending']
    cursor.execute("SELECT COUNT(*) as approved FROM event_permits WHERE user_id = %s AND status = 'approved'", (session['user_id'],))
    approved_events = cursor.fetchone()['approved']
    cursor.execute("SELECT COUNT(*) as rejected FROM event_permits WHERE user_id = %s AND status = 'rejected'", (session['user_id'],))
    rejected_events = cursor.fetchone()['rejected']
    conn.close()

    return render_template('my_requests.html',
                         document_requests=document_requests,
                         event_permits=event_permits,
                         total_docs=total_docs,
                         pending_docs=pending_docs,
                         processing_docs=processing_docs,
                         ready_docs=ready_docs,
                         rejected_docs=rejected_docs,
                         total_events=total_events,
                         pending_events=pending_events,
                         approved_events=approved_events,
                         rejected_events=rejected_events)

@app.route('/my_request')
@role_required('resident')
def my_request():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM document_requests WHERE user_id = %s ORDER BY created_at DESC", (session['user_id'],))
    document_requests = cursor.fetchall()
    cursor.execute("SELECT * FROM event_permits WHERE user_id = %s ORDER BY requested_at DESC", (session['user_id'],))
    event_permits = cursor.fetchall()
    conn.close()
    return render_template('my_request.html',
                         document_requests=document_requests,
                         event_permits=event_permits)

@app.route('/about_us')
def about_us():
    return render_template('about_us.html')

@app.route('/request-document', methods=['GET'])
@role_required('resident')
def request_document():
    return render_template('request_document.html')

@app.route('/request-document', methods=['POST'])
@role_required('resident')
def request_document_post():
    document_type = request.form.get('document_type', '').strip()
    surname = request.form.get('surname', '').strip()
    given_name = request.form.get('given_name', '').strip()
    middle_name = request.form.get('middle_name', '').strip()
    address = request.form.get('address', '').strip()
    contact_no = request.form.get('contact_no', '').strip()
    civil_status = request.form.get('civil_status', '').strip()
    age = request.form.get('age', 0)
    dob = request.form.get('dob', '').strip()
    precinct_no = request.form.get('precinct_no', '').strip()
    place_of_birth = request.form.get('place_of_birth', '').strip()
    length_of_stay = request.form.get('length_of_stay', '').strip()
    residency_type = request.form.get('residency_type', '').strip()
    lessor_name = request.form.get('lessor_name', '').strip()
    lessor_address = request.form.get('lessor_address', '').strip()
    rep_position = request.form.get('rep_position', '').strip()
    father_name = request.form.get('father_name', '').strip()
    mother_name = request.form.get('mother_name', '').strip()
    spouse_name = request.form.get('spouse_name', '').strip()
    occupation = request.form.get('occupation', '').strip()
    emergency_name = request.form.get('emergency_name', '').strip()
    emergency_number = request.form.get('emergency_number', '').strip()
    ref1_name = request.form.get('ref1_name', '').strip()
    ref1_address = request.form.get('ref1_address', '').strip()
    ref2_name = request.form.get('ref2_name', '').strip()
    ref2_address = request.form.get('ref2_address', '').strip()
    purpose = request.form.get('purpose', '').strip()
    printed_name = request.form.get('printed_name', '').strip()
    signature_date = request.form.get('signature_date', '').strip()

    if not document_type or not surname or not given_name or not address:
        flash('Please fill in all required fields.', 'danger')
        return redirect(url_for('request_document'))

    file_data = None
    if 'fileInput' in request.files:
        file_data = save_uploaded_file(request.files['fileInput'])

    ref_num = f"DOC-{datetime.datetime.now().strftime('%Y%m%d')}-{random.randint(1000, 9999)}"
    queue_num = get_next_queue_number('document_requests')

    conn = get_db()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO document_requests (
                user_id, document_type, surname, given_name, middle_name,
                address, contact_no, civil_status, age, dob,
                precinct_no, place_of_birth, length_of_stay, residency_type,
                lessor_name, lessor_address, rep_position,
                father_name, mother_name, spouse_name, occupation,
                emergency_name, emergency_number,
                ref1_name, ref1_address, ref2_name, ref2_address,
                purpose, printed_name, signature_date,
                reference_number, queuing_number, status,
                document_path
            ) VALUES (
                %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s,
                %s, %s, %s, %s,
                %s, %s, %s,
                %s, %s, %s, %s,
                %s, %s,
                %s, %s, %s, %s,
                %s, %s, %s,
                %s, %s, 'pending',
                %s
            )
        """, (
            session['user_id'], document_type, surname, given_name, middle_name,
            address, contact_no, civil_status, age, dob,
            precinct_no, place_of_birth, length_of_stay, residency_type,
            lessor_name, lessor_address, rep_position,
            father_name, mother_name, spouse_name, occupation,
            emergency_name, emergency_number,
            ref1_name, ref1_address, ref2_name, ref2_address,
            purpose, printed_name, signature_date,
            ref_num, queue_num, file_data
        ))
        conn.commit()

        create_notification(
            session['user_id'],
            '📄 Document Request Submitted',
            f'Your {document_type.replace("_", " ").title()} request is now pending. Reference: {ref_num} | Queue: {queue_num}',
            'document_submitted',
            link='/my-requests'
        )

        admin_users = notify_role(
            ['admin_documents', 'head_admin'],
            '🔔 New Document Request',
            f'{session["fullname"]} requested {document_type.replace("_", " ").title()}. Reference: {ref_num}',
            'document_new_request',
            link='/admin/documents'
        )

        cursor2 = conn.cursor(dictionary=True)
        cursor2.execute("SELECT first_name, email FROM users WHERE id = %s", (session['user_id'],))
        resident_info = cursor2.fetchone()

        if resident_info:
            subject = f"Document Request Received - {ref_num}"
            body_html = f"""
            <html><body style="font-family:Arial,sans-serif;padding:20px;">
                <h2 style="color:#0f3d2a;">📄 Document Request Received</h2>
                <p>Hello <strong>{resident_info['first_name']}</strong>,</p>
                <p>Natanggap na namin ang iyong request para sa <strong>{document_type.replace('_', ' ').title()}</strong>.</p>
                <table style="background:#f4f8f5;padding:15px;border-radius:10px;margin:20px 0;">
                    <tr><td><strong>Reference No:</strong> {ref_num}</td></tr>
                    <tr><td><strong>Queue No:</strong> {queue_num}</td></tr>
                    <tr><td><strong>Status:</strong> <span style="color:#d97706;">PENDING</span></td></tr>
                </table>
                <a href="http://127.0.0.1:5000/login" style="display:inline-block;background:#0f3d2a;color:#fff;padding:12px 30px;text-decoration:none;border-radius:8px;margin-top:15px;">Login to Track</a>
            </body></html>
            """
            send_email(resident_info['email'], subject, body_html)

        for admin in admin_users:
            send_admin_notification_email(
                admin['email'],
                f'New Document Request - {ref_num}',
                f'New {document_type.replace("_", " ").title()} Request',
                f'A resident has submitted a new document request.',
                reference_no=ref_num,
                applicant_name=session['fullname'],
                action_type='new'
            )

        flash('Document request submitted successfully! Reference: ' + ref_num, 'success')
        return redirect(url_for('my_requests'))
    except mysql.connector.Error as e:
        flash(f'Database error: {str(e)}', 'danger')
        return redirect(url_for('request_document'))
    finally:
        conn.close()

@app.route('/submit-document-request', methods=['POST'])
@role_required('resident')
def submit_document_request():
    conn = None
    try:
        data = request.form.to_dict()
        file_data = None
        if 'fileInput' in request.files:
            uploaded = request.files['fileInput']
            if uploaded and uploaded.filename:
                file_data = save_uploaded_file(uploaded)

        conn = get_db()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("DESCRIBE document_requests")
        col_names = [col['Field'] for col in cursor.fetchall()]
        required_columns = ['user_id', 'document_type', 'reference_number', 'status']
        missing_columns = [col for col in required_columns if col not in col_names]
        if missing_columns:
            conn.close()
            return jsonify({'error': f"MISSING COLUMNS SA DATABASE: {', '.join(missing_columns)}. Idagdag mo muna ito sa MySQL!"}), 500

        doc_type = data.get('document_type', 'clearance')
        ref_num = f"DOC-{datetime.datetime.now().strftime('%Y%m%d')}-{random.randint(1000, 9999)}"
        queue_num = get_next_queue_number('document_requests')
        qr_token = generate_qr_token()

        insert_cols = ['user_id', 'document_type', 'reference_number', 'status', 'qr_token']
        insert_vals = [session['user_id'], doc_type, ref_num, 'pending', qr_token]

        if 'queuing_number' in col_names:
            insert_cols.append('queuing_number')
            insert_vals.append(queue_num)
        if file_data and 'document_path' in col_names:
            insert_cols.append('document_path')
            insert_vals.append(file_data)

        ALLOWED_COLS = {
            'surname', 'given_name', 'middle_name', 'address', 'contact_no',
            'civil_status', 'age', 'dob', 'precinct_no', 'place_of_birth',
            'length_of_stay', 'residency_type', 'lessor_name', 'lessor_address',
            'rep_position', 'father_name', 'mother_name', 'spouse_name',
            'occupation', 'emergency_name', 'emergency_number',
            'ref1_name', 'ref1_address', 'ref2_name', 'ref2_address',
            'purpose', 'printed_name', 'signature_date'
        }
        for key, value in data.items():
            if key in ALLOWED_COLS and key in col_names and key not in insert_cols:
                insert_cols.append(key)
                insert_vals.append(value)

        placeholders = ', '.join(['%s'] * len(insert_cols))
        columns_str = ', '.join(insert_cols)
        sql = f"INSERT INTO document_requests ({columns_str}) VALUES ({placeholders})"
        cursor.execute(sql, tuple(insert_vals))
        conn.commit()

        cursor.execute("SELECT first_name, email FROM users WHERE id = %s", (session['user_id'],))
        resident_info = cursor.fetchone()

        if resident_info:
            create_notification(
                session['user_id'],
                '📄 Document Request Submitted',
                f'Your {doc_type.replace("_", " ").title()} request is now pending. Reference: {ref_num} | Queue: {queue_num}',
                'document_submitted',
                link='/my-requests'
            )

            subject = f"Document Request Received - {ref_num}"
            body_html = f"""
            <html><body style="font-family:Arial,sans-serif;padding:20px;">
                <h2 style="color:#0f3d2a;">📄 Document Request Received</h2>
                <p>Hello <strong>{resident_info['first_name']}</strong>,</p>
                <p>Natanggap na namin ang iyong request para sa <strong>{doc_type.replace('_', ' ').title()}</strong>.</p>
                <table style="background:#f4f8f5;padding:15px;border-radius:10px;margin:20px 0;">
                    <tr><td><strong>Reference No:</strong> {ref_num}</td></tr>
                    <tr><td><strong>Queue No:</strong> {queue_num}</td></tr>
                    <tr><td><strong>Status:</strong> <span style="color:#d97706;">PENDING</span></td></tr>
                </table>
            </body></html>
            """
            send_email(resident_info['email'], subject, body_html)

            admin_users = notify_role(
                ['admin_documents', 'head_admin'],
                '🔔 New Document Request',
                f'{session["fullname"]} requested {doc_type.replace("_", " ").title()}. Reference: {ref_num}',
                'document_new_request',
                link='/admin/documents'
            )
            for admin in admin_users:
                send_admin_notification_email(
                    admin['email'],
                    f'New Document Request - {ref_num}',
                    f'New {doc_type.replace("_", " ").title()} Request',
                    f'A resident has submitted a new document request.',
                    reference_no=ref_num,
                    applicant_name=session['fullname'],
                    action_type='new'
                )

        return jsonify({
            'success': True,
            'message': 'Document request submitted successfully',
            'reference_number': ref_num,
            'queuing_number': queue_num if 'queuing_number' in col_names else 'N/A',
            'qr_token': qr_token
        })
    except Exception as e:
        if conn:
            try:
                conn.close()
            except:
                pass
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500
    finally:
        if conn:
            try:
                conn.close()
            except:
                pass

@app.route('/apply-permit', methods=['GET'])
@role_required('resident')
def apply_permit():
    return render_template('apply_permit.html')

@app.route('/apply-permit', methods=['POST'])
@role_required('resident')
def apply_permit_post():
    event_name = request.form.get('event_name', '').strip()
    event_description = request.form.get('event_description', '').strip()
    purpose = request.form.get('purpose', '').strip()
    contact_person = request.form.get('contact_person', '').strip()
    contact_phone = request.form.get('contact_phone', '').strip()
    event_date = request.form.get('event_date', '').strip()
    start_time = request.form.get('start_time', '').strip()[:5]
    end_time = request.form.get('end_time', '').strip()[:5]
    estimated_attendees = request.form.get('estimated_attendees', '').strip()
    venue = request.form.get('venue', '').strip()

    if not event_name or not event_date or not start_time or not end_time or not venue:
        return jsonify({'success': False, 'error': 'Please fill in all required fields.'}), 400
    if not purpose:
        return jsonify({'success': False, 'error': 'Purpose is required.'}), 400
    if not contact_person:
        return jsonify({'success': False, 'error': 'Contact person name is required.'}), 400
    if not contact_phone:
        return jsonify({'success': False, 'error': 'Contact phone number is required.'}), 400
    if start_time >= end_time:
        return jsonify({'success': False, 'error': 'End time must be after start time.'}), 400
    if start_time < '08:00' or start_time > '22:00':
        return jsonify({'success': False, 'error': 'Start time must be between 8:00 AM and 10:00 PM.'}), 400
    if end_time < '08:00' or end_time > '22:00':
        return jsonify({'success': False, 'error': 'End time must be between 8:00 AM and 10:00 PM.'}), 400

    try:
        selected_date = datetime.datetime.strptime(event_date, '%Y-%m-%d').date()
        diff_days = (selected_date - datetime.date.today()).days
        if diff_days < 10:
            return jsonify({'success': False, 'error': 'Please apply at least 10 days before the event date.'}), 400
    except ValueError:
        return jsonify({'success': False, 'error': 'Invalid date format.'}), 400

    file_data = None
    if 'requirement' in request.files:
        file_data = save_uploaded_file(request.files['requirement'])

    ref_num = f"BP-{datetime.datetime.now().strftime('%Y%m%d')}-{random.randint(1000, 9999)}"
    queue_num = get_next_queue_number('event_permits', venue)

    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("""
            SELECT id FROM event_permits
            WHERE venue = %s AND event_date = %s AND status = 'approved'
              AND start_time < %s AND end_time > %s
            LIMIT 1
        """, (venue, event_date, end_time, start_time))
        if cursor.fetchone():
            return jsonify({'success': False, 'error': 'This time slot is already taken by an approved event at this venue.'}), 409

        pending_warning = None
        cursor.execute("""
            SELECT id, start_time, end_time FROM event_permits
            WHERE venue = %s AND event_date = %s AND status = 'pending'
              AND start_time < %s AND end_time > %s
            LIMIT 1
        """, (venue, event_date, end_time, start_time))
        pending_conflict = cursor.fetchone()
        if pending_conflict:
            cs = str(pending_conflict['start_time'])[:5]
            ce = str(pending_conflict['end_time'])[:5]
            pending_warning = f'There is a pending permit for this slot ({cs} - {ce}). You may still apply, but it could conflict if approved.'

        cursor.execute("""
            INSERT INTO event_permits (
                user_id, event_name, event_description, purpose,
                contact_person, contact_phone,
                event_date, start_time, end_time, estimated_attendees, venue,
                status, requirements_file, reference_number, queuing_number
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 'pending', %s, %s, %s)
        """, (
            session['user_id'], event_name, event_description, purpose,
            contact_person, contact_phone,
            event_date, start_time, end_time,
            estimated_attendees if estimated_attendees else 0,
            venue, file_data, ref_num, queue_num
        ))
        conn.commit()

        create_notification(
            session['user_id'],
            '🎉 Permit Application Submitted',
            f'Your event permit "{event_name}" has been submitted for review. Reference: {ref_num} | Queue: {queue_num}',
            'permit_submitted',
            link='/my-requests'
        )

        court_role = get_court_role_by_venue(venue)
        admin_roles = ['head_admin']
        if court_role:
            admin_roles.append(court_role)

        admin_users = notify_role(
            admin_roles,
            '🔔 New Permit Request',
            f'{session["fullname"]} submitted a permit for "{event_name}" at {venue}. Reference: {ref_num}',
            'permit_new_request',
            link='/admin/events'
        )

        cursor.execute("SELECT first_name, email FROM users WHERE id = %s", (session['user_id'],))
        resident = cursor.fetchone()

        if resident:
            subject = f"Event Permit Application Received - {ref_num}"
            body_html = f"""
            <html><body style="font-family:Arial,sans-serif;padding:20px;">
                <h2 style="color:#0f3d2a;">🎉 Event Permit Application Received</h2>
                <p>Hello <strong>{resident['first_name']}</strong>,</p>
                <p>Natanggap na namin ang iyong event permit application. Ipro-process na ito ng aming Court Admin.</p>
                <table style="background:#f4f8f5;padding:15px;border-radius:10px;margin:20px 0;">
                    <tr><td><strong>Event:</strong> {event_name}</td></tr>
                    <tr><td><strong>Date:</strong> {event_date}</td></tr>
                    <tr><td><strong>Time:</strong> {start_time} - {end_time}</td></tr>
                    <tr><td><strong>Venue:</strong> {venue}</td></tr>
                    <tr><td><strong>Reference No:</strong> {ref_num}</td></tr>
                    <tr><td><strong>Queue No:</strong> {queue_num}</td></tr>
                    <tr><td><strong>Status:</strong> <span style="color:#d97706;">PENDING</span></td></tr>
                </table>
            </body></html>
            """
            send_email(resident['email'], subject, body_html)

        return jsonify({
            'success': True,
            'message': 'Permit application submitted successfully',
            'reference_number': ref_num,
            'queuing_number': queue_num,
            'event_name': event_name,
            'event_date': event_date,
            'start_time': start_time,
            'end_time': end_time,
            'venue': venue,
            'warning': pending_warning
        }), 201
    except mysql.connector.Error as e:
        return jsonify({'success': False, 'error': f'Database error: {str(e)}'}), 500
    finally:
        conn.close()

@app.route('/api/permits/check-availability', methods=['GET'])
def check_permit_availability():
    if 'user_id' not in session:
        return jsonify({'status': 'error', 'message': 'Please login first.'}), 401
    try:
        date_str = request.args.get('date')
        start_str = request.args.get('start_time')
        end_str = request.args.get('end_time')
        venue = request.args.get('venue')

        if not all([date_str, start_str, end_str, venue]):
            return jsonify({'status': 'error', 'message': 'Missing parameters.'})

        start_time = start_str[:5]
        end_time = end_str[:5]

        if start_time >= end_time:
            return jsonify({'status': 'error', 'message': 'End time must be after start time.'})
        if start_time < '08:00' or start_time > '22:00':
            return jsonify({'status': 'error', 'message': 'Start time must be between 8:00 AM and 10:00 PM.'})
        if end_time < '08:00' or end_time > '22:00':
            return jsonify({'status': 'error', 'message': 'End time must be between 8:00 AM and 10:00 PM.'})

        conn = get_db()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT id, start_time, end_time FROM event_permits
            WHERE venue = %s AND event_date = %s AND status = 'approved'
              AND start_time < %s AND end_time > %s
            LIMIT 1
        """, (venue, date_str, end_time, start_time))
        approved_conflict = cursor.fetchone()
        if approved_conflict:
            cs = str(approved_conflict['start_time'])[:5]
            ce = str(approved_conflict['end_time'])[:5]
            conn.close()
            return jsonify({'status': 'blocked', 'message': f'This slot is already taken by an approved event ({cs} - {ce}).'})

        cursor.execute("""
            SELECT id, start_time, end_time FROM event_permits
            WHERE venue = %s AND event_date = %s AND status = 'pending'
              AND start_time < %s AND end_time > %s
            LIMIT 1
        """, (venue, date_str, end_time, start_time))
        pending_conflict = cursor.fetchone()
        conn.close()

        if pending_conflict:
            cs = str(pending_conflict['start_time'])[:5]
            ce = str(pending_conflict['end_time'])[:5]
            return jsonify({'status': 'pending_conflict', 'message': f'There is a pending permit for this slot ({cs} - {ce}). You may still apply, but it could conflict if approved.'})

        return jsonify({'status': 'available'})
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'status': 'error', 'message': f'Server error: {str(e)}'}), 500

# ============================================================
# HEAD ADMIN DASHBOARD
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
    cursor.execute("SELECT COUNT(*) as total FROM users WHERE role IN ('head_admin', 'admin_court_1', 'admin_court_2', 'admin_court_3', 'admin_court_4', 'admin_documents')")
    total_admins = cursor.fetchone()['total']

    cursor.execute("SELECT COUNT(*) as total FROM document_requests")
    total_requests = cursor.fetchone()['total']
    cursor.execute("SELECT COUNT(*) as total FROM document_requests WHERE status = 'pending'")
    docs_pending = cursor.fetchone()['total']
    cursor.execute("SELECT COUNT(*) as total FROM document_requests WHERE status = 'processing'")
    docs_processing = cursor.fetchone()['total']
    cursor.execute("SELECT COUNT(*) as total FROM document_requests WHERE status = 'ready_for_pickup'")
    docs_ready = cursor.fetchone()['total']
    cursor.execute("SELECT COUNT(*) as total FROM document_requests WHERE status = 'rejected'")
    docs_rejected = cursor.fetchone()['total']

    cursor.execute("SELECT COUNT(*) as total FROM event_permits")
    total_events = cursor.fetchone()['total']
    cursor.execute("SELECT COUNT(*) as total FROM event_permits WHERE status = 'pending'")
    events_pending = cursor.fetchone()['total']
    cursor.execute("SELECT COUNT(*) as total FROM event_permits WHERE status = 'approved'")
    events_approved = cursor.fetchone()['total']
    cursor.execute("SELECT COUNT(*) as total FROM event_permits WHERE status = 'rejected'")
    events_rejected = cursor.fetchone()['total']

    cursor.execute("""
        SELECT d.*, u.first_name, u.last_name, u.email
        FROM document_requests d
        JOIN users u ON d.user_id = u.id
        WHERE d.status = 'pending'
        ORDER BY d.created_at DESC
        LIMIT 5
    """)
    pending_documents = cursor.fetchall()

    cursor.execute("""
        SELECT e.*, u.first_name, u.last_name, u.email
        FROM event_permits e
        JOIN users u ON e.user_id = u.id
        WHERE e.status = 'pending'
        ORDER BY e.requested_at DESC
        LIMIT 5
    """)
    pending_events_list = cursor.fetchall()

    monthly_docs_data = []
    monthly_events_data = []
    current_year = datetime.date.today().year
    for month in range(1, 13):
        cursor.execute("""
            SELECT COUNT(*) as total FROM document_requests
            WHERE MONTH(created_at) = %s AND YEAR(created_at) = %s
        """, (month, current_year))
        monthly_docs_data.append(cursor.fetchone()['total'])
        cursor.execute("""
            SELECT COUNT(*) as total FROM event_permits
            WHERE MONTH(requested_at) = %s AND YEAR(requested_at) = %s
        """, (month, current_year))
        monthly_events_data.append(cursor.fetchone()['total'])

    conn.close()

    return render_template('admin/head_admin_dashboard.html',
                         total_users=total_users,
                         total_residents=total_residents,
                         total_admins=total_admins,
                         total_requests=total_requests,
                         total_events=total_events,
                         docs_pending=docs_pending,
                         docs_processing=docs_processing,
                         docs_ready=docs_ready,
                         docs_rejected=docs_rejected,
                         events_pending=events_pending,
                         events_approved=events_approved,
                         events_rejected=events_rejected,
                         pending_documents=pending_documents,
                         pending_events_list=pending_events_list,
                         monthly_docs_data=monthly_docs_data,
                         monthly_events_data=monthly_events_data)

@app.route('/head-admin/all-documents')
def head_admin_all_documents():
    if 'user_id' not in session or session.get('role') != 'head_admin':
        flash('Unauthorized access. Head Admin only.', 'danger')
        return redirect(url_for('login'))

    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT d.*, u.first_name, u.last_name, u.email, u.contact_number
        FROM document_requests d
        JOIN users u ON d.user_id = u.id
        ORDER BY d.created_at DESC
    """)
    documents = cursor.fetchall()
    cursor.execute("SELECT COUNT(*) as total FROM document_requests")
    total_documents = cursor.fetchone()['total']
    cursor.execute("SELECT COUNT(*) as total FROM document_requests WHERE status = 'pending'")
    pending_count = cursor.fetchone()['total']
    cursor.execute("SELECT COUNT(*) as total FROM document_requests WHERE status = 'processing'")
    processing_count = cursor.fetchone()['total']
    cursor.execute("SELECT COUNT(*) as total FROM document_requests WHERE status = 'ready_for_pickup'")
    ready_count = cursor.fetchone()['total']
    cursor.execute("SELECT COUNT(*) as total FROM document_requests WHERE status = 'rejected'")
    rejected_count = cursor.fetchone()['total']
    conn.close()

    return render_template('admin/head_admin_all_documents.html',
                         documents=documents,
                         total_documents=total_documents,
                         pending_count=pending_count,
                         processing_count=processing_count,
                         ready_count=ready_count,
                         rejected_count=rejected_count)

@app.route('/head-admin/events')
def head_admin_events():
    if 'user_id' not in session or session.get('role') != 'head_admin':
        flash('Unauthorized access. Head Admin only.', 'danger')
        return redirect(url_for('login'))

    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT e.*, u.first_name, u.last_name, u.email, u.contact_number
        FROM event_permits e
        JOIN users u ON e.user_id = u.id
        ORDER BY e.id DESC
    """)
    events = cursor.fetchall()
    cursor.execute("SELECT COUNT(*) as total FROM event_permits")
    total_events = cursor.fetchone()['total']
    cursor.execute("SELECT COUNT(*) as total FROM event_permits WHERE status = 'pending'")
    pending_count = cursor.fetchone()['total']
    cursor.execute("SELECT COUNT(*) as total FROM event_permits WHERE status = 'approved'")
    approved_count = cursor.fetchone()['total']
    cursor.execute("SELECT COUNT(*) as total FROM event_permits WHERE status = 'rejected'")
    rejected_count = cursor.fetchone()['total']
    conn.close()

    return render_template('admin/head_admin_events.html',
                         events=events,
                         total_events=total_events,
                         pending_count=pending_count,
                         approved_count=approved_count,
                         rejected_count=rejected_count)

@app.route('/head-admin/events/calendar')
def head_admin_events_calendar():
    if 'user_id' not in session or session.get('role') != 'head_admin':
        flash('Unauthorized access. Head Admin only.', 'danger')
        return redirect(url_for('login'))
    return render_template('admin/head_admin_events_calendar.html')

@app.route('/api/events/all-approved')
@login_required
def api_all_approved_events():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT e.*, u.first_name, u.last_name
        FROM event_permits e
        JOIN users u ON e.user_id = u.id
        WHERE e.status = 'approved'
        ORDER BY e.requested_at DESC
    """)
    events = cursor.fetchall()
    conn.close()

    result = []
    for event in events:
        result.append({
            'id': event['id'],
            'title': event['event_name'],
            'start': event['event_date'].strftime('%Y-%m-%d') if event['event_date'] else None,
            'extendedProps': {
                'status': event['status'],
                'reference': event['reference_number'] or 'N/A',
                'organizer': f"{event['first_name']} {event['last_name']}",
                'venue': event['venue'] or 'N/A',
                'attendees': event['estimated_attendees'] or 0,
                'start_time': str(event['start_time']) if event['start_time'] else '',
                'end_time': str(event['end_time']) if event['end_time'] else '',
                'purpose': event['purpose'] or 'N/A',
                'description': event['event_description'] or 'N/A',
                'remarks': event.get('admin_remarks', '') or ''
            }
        })
    return jsonify(result)

@app.route('/api/events/court/<court_role>')
@login_required
def api_events_by_court(court_role):
    if court_role not in COURT_CONFIG:
        return jsonify({'error': 'Invalid court'}), 400
    VENUE = COURT_CONFIG[court_role]['venue']

    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT e.*, u.first_name, u.last_name
        FROM event_permits e
        JOIN users u ON e.user_id = u.id
        WHERE e.venue = %s AND e.status = 'approved' AND e.event_date >= CURDATE()
        ORDER BY e.requested_at DESC
    """, (VENUE,))
    events = cursor.fetchall()
    conn.close()

    result = []
    for event in events:
        result.append({
            'id': event['id'],
            'title': event['event_name'],
            'start': event['event_date'].strftime('%Y-%m-%d') if event['event_date'] else None,
            'extendedProps': {
                'status': event['status'],
                'reference': event['reference_number'] or 'N/A',
                'organizer': f"{event['first_name']} {event['last_name']}",
                'venue': event['venue'] or 'N/A',
                'attendees': event['estimated_attendees'] or 0,
                'start_time': str(event['start_time']) if event['start_time'] else '',
                'end_time': str(event['end_time']) if event['end_time'] else '',
                'purpose': event['purpose'] or 'N/A',
                'remarks': event.get('admin_remarks', '') or ''
            }
        })
    return jsonify(result)

@app.route('/api/events/approved')
def api_approved_events():
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401

    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT e.*, u.first_name, u.last_name
        FROM event_permits e
        JOIN users u ON e.user_id = u.id
        WHERE e.status = 'approved'
        ORDER BY e.requested_at DESC
    """)
    events = cursor.fetchall()
    conn.close()

    result = []
    for event in events:
        result.append({
            'id': event['id'],
            'title': event['event_name'],
            'date': event['event_date'].strftime('%Y-%m-%d') if event['event_date'] else None,
            'start_time': str(event['start_time']) if event['start_time'] else '',
            'end_time': str(event['end_time']) if event['end_time'] else '',
            'venue': event['venue'] or 'N/A',
            'attendees': event['estimated_attendees'] or 0,
            'organizer': f"{event['first_name']} {event['last_name']}",
            'reference': event['reference_number'] or 'N/A',
            'description': event['event_description'] or 'N/A'
        })
    return jsonify(result)

@app.route('/sec-admin-dashboard')
def sec_admin_dashboard():
    if 'user_id' not in session or session.get('role') != 'admin_documents':
        flash('Please login as Documents Admin.', 'danger')
        return redirect(url_for('login'))

    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT COUNT(*) as total FROM document_requests")
    total_documents = cursor.fetchone()['total']
    cursor.execute("SELECT COUNT(*) as total FROM document_requests WHERE status = 'pending'")
    pending_documents = cursor.fetchone()['total']
    cursor.execute("SELECT COUNT(*) as total FROM document_requests WHERE status = 'processing'")
    processing_documents = cursor.fetchone()['total']
    cursor.execute("SELECT COUNT(*) as total FROM document_requests WHERE status = 'ready_for_pickup'")
    ready_documents = cursor.fetchone()['total']
    cursor.execute("SELECT COUNT(*) as total FROM document_requests WHERE status = 'rejected'")
    rejected_documents = cursor.fetchone()['total']

    weekly_data = []
    for i in range(6, -1, -1):
        date = datetime.date.today() - datetime.timedelta(days=i)
        cursor.execute("SELECT COUNT(*) as total FROM document_requests WHERE DATE(created_at) = %s", (date,))
        weekly_data.append(cursor.fetchone()['total'])

    cursor.execute("""
        SELECT d.*, u.first_name, u.last_name
        FROM document_requests d
        JOIN users u ON d.user_id = u.id
        WHERE d.status = 'pending'
        ORDER BY d.created_at DESC
        LIMIT 5
    """)
    recent_pending = cursor.fetchall()
    conn.close()

    return render_template('admin/sec_admin_dashboard.html',
                         total_documents=total_documents,
                         pending_documents=pending_documents,
                         processing_documents=processing_documents,
                         ready_documents=ready_documents,
                         rejected_documents=rejected_documents,
                         weekly_data=weekly_data,
                         recent_pending=recent_pending)

@app.route('/admin/documents')
def admin_documents():
    if 'user_id' not in session or session.get('role') not in ['head_admin', 'admin_documents']:
        flash('Unauthorized access.', 'danger')
        return redirect(url_for('login'))

    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT d.*, u.first_name, u.last_name, u.email, u.contact_number
        FROM document_requests d
        JOIN users u ON d.user_id = u.id
        ORDER BY d.created_at DESC
    """)
    documents = cursor.fetchall()
    conn.close()
    return render_template('admin/sec_admin_documents.html', documents=documents)

@app.route('/admin/documents/clearance')
def admin_documents_clearance():
    if 'user_id' not in session or session.get('role') not in ['head_admin', 'admin_documents']:
        flash('Unauthorized access.', 'danger')
        return redirect(url_for('login'))
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT d.*, u.first_name, u.last_name, u.email, u.contact_number
        FROM document_requests d
        JOIN users u ON d.user_id = u.id
        WHERE d.document_type = 'clearance'
        ORDER BY d.created_at DESC
    """)
    documents = cursor.fetchall()
    conn.close()
    return render_template('admin/sec_admin_documents_clearance.html', documents=documents)

@app.route('/admin/documents/ready-for-pickup')
def admin_documents_ready():
    if 'user_id' not in session or session.get('role') not in ['head_admin', 'admin_documents']:
        flash('Unauthorized access.', 'danger')
        return redirect(url_for('login'))
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT d.*, u.first_name, u.last_name, u.email, u.contact_number
        FROM document_requests d
        JOIN users u ON d.user_id = u.id
        WHERE d.status IN ('processing', 'ready_for_pickup')
        ORDER BY d.created_at DESC
    """)
    documents = cursor.fetchall()
    conn.close()
    return render_template('admin/sec_admin_ready_pickup.html', documents=documents)

@app.route('/admin/upload-final-document', methods=['POST'])
def upload_final_document():
    if 'user_id' not in session or session.get('role') not in ['head_admin', 'admin_documents']:
        return jsonify({'error': 'Unauthorized'}), 401

    doc_id = request.form.get('doc_id')
    if not doc_id:
        return jsonify({'error': 'Document ID missing'}), 400
    if 'completed_file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    file = request.files['completed_file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    filename = save_uploaded_file(file)
    if not filename:
        return jsonify({'error': 'Invalid file type'}), 400

    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        UPDATE document_requests
        SET status = 'ready_for_pickup', completed_file = %s, completed_at = NOW()
        WHERE id = %s
    """, (filename, doc_id))
    conn.commit()

    cursor.execute("""
        SELECT u.email, u.first_name, d.document_type, d.reference_number, d.user_id
        FROM document_requests d
        JOIN users u ON d.user_id = u.id
        WHERE d.id = %s
    """, (doc_id,))
    user_info = cursor.fetchone()
    conn.close()

    if user_info:
        subject = f"Your Document is Ready for Pickup! - {user_info['reference_number']}"
        body_html = f"""
        <html><body style="font-family:Arial; padding:20px;">
            <h2 style="color:#0f3d2a;">✅ Ready for Pickup!</h2>
            <p>Hello <strong>{user_info['first_name']}</strong>,</p>
            <p>Ang iyong <strong>{user_info['document_type'].replace('_', ' ').title()}</strong> ay ready na for pickup sa Barangay Hall.</p>
            <p><strong>Reference:</strong> {user_info['reference_number']}</p>
            <p>Paki-bring ang iyong QR Code o Reference Number para ma-verify.</p>
        </body></html>
        """
        send_email(user_info['email'], subject, body_html)

        create_notification(
            user_info['user_id'],
            '✅ Ready for Pickup',
            f'Your {user_info["document_type"].replace("_", " ").title()} is now ready for pickup. Reference: {user_info["reference_number"]}',
            'document_ready',
            link='/my-requests'
        )

    return jsonify({'success': True, 'message': 'Document uploaded and user notified.'})

@app.route('/admin/documents/indigency')
def admin_documents_indigency():
    if 'user_id' not in session or session.get('role') not in ['head_admin', 'admin_documents']:
        flash('Unauthorized access.', 'danger')
        return redirect(url_for('login'))
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT d.*, u.first_name, u.last_name, u.email, u.contact_number
        FROM document_requests d
        JOIN users u ON d.user_id = u.id
        WHERE d.document_type = 'indigency'
        ORDER BY d.created_at DESC
    """)
    documents = cursor.fetchall()
    conn.close()
    return render_template('admin/sec_admin_documents_indigency.html', documents=documents)

@app.route('/admin/documents/residency')
def admin_documents_residency():
    if 'user_id' not in session or session.get('role') not in ['head_admin', 'admin_documents']:
        flash('Unauthorized access.', 'danger')
        return redirect(url_for('login'))
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT d.*, u.first_name, u.last_name, u.email, u.contact_number
        FROM document_requests d
        JOIN users u ON d.user_id = u.id
        WHERE d.document_type = 'proof_residency'
        ORDER BY d.created_at DESC
    """)
    documents = cursor.fetchall()
    conn.close()
    return render_template('admin/sec_admin_documents_residency.html', documents=documents)

# ============================================================
# COURT DASHBOARDS (HELPER)
# ============================================================
def _format_event_times(events):
    for event in events:
        if event.get('start_time') and hasattr(event['start_time'], 'total_seconds'):
            total_seconds = int(event['start_time'].total_seconds())
            event['start_time'] = f"{total_seconds // 3600:02d}:{(total_seconds % 3600) // 60:02d}"
        if event.get('end_time') and hasattr(event['end_time'], 'total_seconds'):
            total_seconds = int(event['end_time'].total_seconds())
            event['end_time'] = f"{total_seconds // 3600:02d}:{(total_seconds % 3600) // 60:02d}"
        if event.get('event_date') and hasattr(event['event_date'], 'strftime'):
            event['event_date'] = event['event_date'].strftime('%Y-%m-%d')
    return events

def _render_court_dashboard(role):
    if 'user_id' not in session or session.get('role') != role:
        flash('Unauthorized access.', 'danger')
        return redirect(url_for('login'))
    config = COURT_CONFIG.get(role)
    if not config:
        flash('Invalid court role.', 'danger')
        return redirect(url_for('login'))
    VENUE = config['venue']

    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT COUNT(*) as total FROM event_permits WHERE venue = %s", (VENUE,))
    total_events = cursor.fetchone()['total']
    cursor.execute("SELECT COUNT(*) as total FROM event_permits WHERE venue = %s AND status = 'pending'", (VENUE,))
    pending_events = cursor.fetchone()['total']
    cursor.execute("SELECT COUNT(*) as total FROM event_permits WHERE venue = %s AND status = 'approved'", (VENUE,))
    approved_events = cursor.fetchone()['total']
    cursor.execute("SELECT COUNT(*) as total FROM event_permits WHERE venue = %s AND status = 'rejected'", (VENUE,))
    rejected_events = cursor.fetchone()['total']

    monthly_data = []
    current_year = datetime.date.today().year
    for month in range(1, 13):
        cursor.execute("""
            SELECT COUNT(*) as total FROM event_permits
            WHERE venue = %s AND MONTH(event_date) = %s AND YEAR(event_date) = %s
        """, (VENUE, month, current_year))
        monthly_data.append(cursor.fetchone()['total'])

    cursor.execute("""
        SELECT e.*, u.first_name, u.last_name
        FROM event_permits e
        JOIN users u ON e.user_id = u.id
        WHERE e.venue = %s AND e.status = 'pending'
        ORDER BY e.id DESC
    """, (VENUE,))
    pending_events_list = cursor.fetchall()
    conn.close()

    return render_template(config['dashboard_template'],
                         total_events=total_events,
                         pending_events=pending_events,
                         approved_events=approved_events,
                         rejected_events=rejected_events,
                         monthly_data=monthly_data,
                         pending_events_list=pending_events_list,
                         court_config=config)

def _render_court_pending(role):
    if 'user_id' not in session or session.get('role') != role:
        flash('Unauthorized access.', 'danger')
        return redirect(url_for('login'))
    config = COURT_CONFIG.get(role)
    if not config:
        flash('Invalid court role.', 'danger')
        return redirect(url_for('login'))
    VENUE = config['venue']

    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT e.*, u.first_name, u.last_name, u.email, u.contact_number
        FROM event_permits e
        JOIN users u ON e.user_id = u.id
        WHERE e.venue = %s AND e.status = 'pending'
        ORDER BY e.requested_at DESC
    """, (VENUE,))
    pending_events = cursor.fetchall()
    conn.close()
    pending_events = _format_event_times(pending_events)
    return render_template(config['pending_template'],
                         pending_events=pending_events,
                         court_config=config)

def _render_court_reviewed(role):
    if 'user_id' not in session or session.get('role') != role:
        flash('Unauthorized access.', 'danger')
        return redirect(url_for('login'))
    config = COURT_CONFIG.get(role)
    if not config:
        flash('Invalid court role.', 'danger')
        return redirect(url_for('login'))
    VENUE = config['venue']

    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT e.*, u.first_name, u.last_name, u.email, u.contact_number
        FROM event_permits e
        JOIN users u ON e.user_id = u.id
        WHERE e.venue = %s AND e.status = 'approved'
        ORDER BY e.event_date DESC
    """, (VENUE,))
    approved_events = cursor.fetchall()
    cursor.execute("""
        SELECT e.*, u.first_name, u.last_name, u.email, u.contact_number
        FROM event_permits e
        JOIN users u ON e.user_id = u.id
        WHERE e.venue = %s AND e.status = 'rejected'
        ORDER BY e.event_date DESC
    """, (VENUE,))
    rejected_events = cursor.fetchall()
    conn.close()
    _format_event_times(approved_events)
    _format_event_times(rejected_events)
    return render_template(config['reviewed_template'],
                         approved_events=approved_events,
                         rejected_events=rejected_events,
                         court_config=config)

# ============================================================
# COURT ROUTES (1-4)
# ============================================================
@app.route('/court1/dashboard')
def court1_dashboard():
    return _render_court_dashboard('admin_court_1')

@app.route('/court1/pending')
def court1_pending():
    return _render_court_pending('admin_court_1')

@app.route('/court1/reviewed')
def court1_reviewed():
    return _render_court_reviewed('admin_court_1')

@app.route('/court1/calendar')
def court1_calendar():
    if 'user_id' not in session or session.get('role') != 'admin_court_1':
        flash('Unauthorized access.', 'danger')
        return redirect(url_for('login'))
    return render_template('admin/admin_court1_calendar.html')

@app.route('/court1/activity-logs')
def court1_activity_logs():
    if 'user_id' not in session or session.get('role') != 'admin_court_1':
        flash('Unauthorized access.', 'danger')
        return redirect(url_for('login'))
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT l.*, u.first_name, u.last_name
        FROM admin_activity_logs l
        JOIN users u ON l.admin_id = u.id
        WHERE l.admin_id = %s
        ORDER BY l.created_at DESC
        LIMIT 50
    """, (session['user_id'],))
    logs = cursor.fetchall()
    conn.close()
    return render_template('admin/admin_court1_activity_logs.html', logs=logs)

@app.route('/court2/dashboard')
def court2_dashboard():
    return _render_court_dashboard('admin_court_2')

@app.route('/court2/pending')
def court2_pending():
    return _render_court_pending('admin_court_2')

@app.route('/court2/reviewed')
def court2_reviewed():
    return _render_court_reviewed('admin_court_2')

@app.route('/court2/calendar')
def court2_calendar():
    if 'user_id' not in session or session.get('role') != 'admin_court_2':
        flash('Unauthorized access.', 'danger')
        return redirect(url_for('login'))
    return render_template('admin/admin_court2_calendar.html')

@app.route('/court2/activity-logs')
def court2_activity_logs():
    if 'user_id' not in session or session.get('role') != 'admin_court_2':
        flash('Unauthorized access.', 'danger')
        return redirect(url_for('login'))
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT l.*, u.first_name, u.last_name
        FROM admin_activity_logs l
        JOIN users u ON l.admin_id = u.id
        WHERE l.admin_id = %s
        ORDER BY l.created_at DESC
        LIMIT 50
    """, (session['user_id'],))
    logs = cursor.fetchall()
    conn.close()
    return render_template('admin/admin_court2_activity_logs.html', logs=logs)

@app.route('/court3/dashboard')
def court3_dashboard():
    return _render_court_dashboard('admin_court_3')

@app.route('/court3/pending')
def court3_pending():
    return _render_court_pending('admin_court_3')

@app.route('/court3/reviewed')
def court3_reviewed():
    return _render_court_reviewed('admin_court_3')

@app.route('/court3/calendar')
def court3_calendar():
    if 'user_id' not in session or session.get('role') != 'admin_court_3':
        flash('Unauthorized access.', 'danger')
        return redirect(url_for('login'))
    return render_template('admin/admin_court3_calendar.html')

@app.route('/court3/activity-logs')
def court3_activity_logs():
    if 'user_id' not in session or session.get('role') != 'admin_court_3':
        flash('Unauthorized access.', 'danger')
        return redirect(url_for('login'))
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT l.*, u.first_name, u.last_name
        FROM admin_activity_logs l
        JOIN users u ON l.admin_id = u.id
        WHERE l.admin_id = %s
        ORDER BY l.created_at DESC
        LIMIT 50
    """, (session['user_id'],))
    logs = cursor.fetchall()
    conn.close()
    return render_template('admin/admin_court3_activity_logs.html', logs=logs)

@app.route('/court4/dashboard')
def court4_dashboard():
    return _render_court_dashboard('admin_court_4')

@app.route('/court4/pending')
def court4_pending():
    return _render_court_pending('admin_court_4')

@app.route('/court4/reviewed')
def court4_reviewed():
    return _render_court_reviewed('admin_court_4')

@app.route('/court4/calendar')
def court4_calendar():
    if 'user_id' not in session or session.get('role') != 'admin_court_4':
        flash('Unauthorized access.', 'danger')
        return redirect(url_for('login'))
    return render_template('admin/admin_court4_calendar.html')

@app.route('/court4/activity-logs')
def court4_activity_logs():
    if 'user_id' not in session or session.get('role') != 'admin_court_4':
        flash('Unauthorized access.', 'danger')
        return redirect(url_for('login'))
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT l.*, u.first_name, u.last_name
        FROM admin_activity_logs l
        JOIN users u ON l.admin_id = u.id
        WHERE l.admin_id = %s
        ORDER BY l.created_at DESC
        LIMIT 50
    """, (session['user_id'],))
    logs = cursor.fetchall()
    conn.close()
    return render_template('admin/admin_court4_activity_logs.html', logs=logs)

# ============================================================
# API: COURT EVENTS
# ============================================================
@app.route('/api/court1/events')
def api_court1_events():
    if 'user_id' not in session or session.get('role') != 'admin_court_1':
        return jsonify({'error': 'Unauthorized'}), 401
    return _get_court_events('admin_court_1')

@app.route('/api/court2/events')
def api_court2_events():
    if 'user_id' not in session or session.get('role') != 'admin_court_2':
        return jsonify({'error': 'Unauthorized'}), 401
    return _get_court_events('admin_court_2')

@app.route('/api/court3/events')
def api_court3_events():
    if 'user_id' not in session or session.get('role') != 'admin_court_3':
        return jsonify({'error': 'Unauthorized'}), 401
    return _get_court_events('admin_court_3')

@app.route('/api/court4/events')
def api_court4_events():
    if 'user_id' not in session or session.get('role') != 'admin_court_4':
        return jsonify({'error': 'Unauthorized'}), 401
    return _get_court_events('admin_court_4')

def _get_court_events(role):
    config = COURT_CONFIG.get(role)
    if not config:
        return jsonify({'error': 'Invalid court'}), 400
    VENUE = config['venue']

    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT e.*, u.first_name, u.last_name
        FROM event_permits e
        JOIN users u ON e.user_id = u.id
        WHERE e.venue = %s AND e.status = 'approved' AND e.event_date >= CURDATE()
        ORDER BY e.requested_at DESC
    """, (VENUE,))
    events = cursor.fetchall()
    conn.close()

    result = []
    for event in events:
        result.append({
            'id': event['id'],
            'title': event['event_name'],
            'start': event['event_date'].strftime('%Y-%m-%d') if event['event_date'] else None,
            'extendedProps': {
                'status': event['status'],
                'reference': event['reference_number'] or 'N/A',
                'organizer': f"{event['first_name']} {event['last_name']}",
                'venue': event['venue'] or 'N/A',
                'attendees': event['estimated_attendees'] or 0,
                'start_time': str(event['start_time']) if event['start_time'] else '',
                'end_time': str(event['end_time']) if event['end_time'] else '',
                'purpose': event['purpose'] or 'N/A',
                'remarks': event.get('admin_remarks', '') or ''
            }
        })
    return jsonify(result)

# ============================================================
# API: UPDATE EVENT STATUS
# ============================================================
@app.route('/api/court1/event/<int:event_id>/update-status', methods=['POST'])
def court1_update_event_status(event_id):
    if 'user_id' not in session or session.get('role') != 'admin_court_1':
        return jsonify({'error': 'Unauthorized'}), 401
    return _update_event_status(event_id)

@app.route('/api/court2/event/<int:event_id>/update-status', methods=['POST'])
def court2_update_event_status(event_id):
    if 'user_id' not in session or session.get('role') != 'admin_court_2':
        return jsonify({'error': 'Unauthorized'}), 401
    return _update_event_status(event_id)

@app.route('/api/court3/event/<int:event_id>/update-status', methods=['POST'])
def court3_update_event_status(event_id):
    if 'user_id' not in session or session.get('role') != 'admin_court_3':
        return jsonify({'error': 'Unauthorized'}), 401
    return _update_event_status(event_id)

@app.route('/api/court4/event/<int:event_id>/update-status', methods=['POST'])
def court4_update_event_status(event_id):
    if 'user_id' not in session or session.get('role') != 'admin_court_4':
        return jsonify({'error': 'Unauthorized'}), 401
    return _update_event_status(event_id)

def _update_event_status(event_id):
    data = request.json
    status = data.get('status')
    remarks = data.get('remarks', '').strip()

    if status not in ['approved', 'rejected']:
        return jsonify({'error': 'Invalid status'}), 400

    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT e.event_name, e.event_date, e.start_time, e.end_time, e.venue,
               u.email, u.first_name, u.last_name
        FROM event_permits e
        JOIN users u ON e.user_id = u.id
        WHERE e.id = %s
    """, (event_id,))
    event_data = cursor.fetchone()

    cursor.execute("""
        UPDATE event_permits SET status = %s, admin_remarks = %s WHERE id = %s
    """, (status, remarks, event_id))
    conn.commit()

    if event_data:
        event_name = event_data["event_name"]
        safe_remarks = remarks or "N/A"
        details = f'Event permit "{event_name}" {status} - Remarks: {safe_remarks}'
        cursor.execute("""
            INSERT INTO admin_activity_logs (admin_id, action, document_id, details)
            VALUES (%s, %s, %s, %s)
        """, (session['user_id'], status, event_id, details))
        conn.commit()

    if event_data:
        status_text = "APPROVED ✅" if status == 'approved' else "REJECTED ❌"
        color = "#059669" if status == 'approved' else "#dc2626"
        bg_color = "#ecfdf5" if status == 'approved' else "#fef2f2"
        icon = "✅" if status == 'approved' else "❌"

        subject = f"Event Permit {status.upper()} - Barangay Sto. Nino"
        body_html = f"""
        <html><body style="font-family:Arial,sans-serif;padding:20px;background:#ecfdf5;">
        <div style="max-width:600px;margin:0 auto;background:#fff;border-radius:16px;padding:30px;">
            <h2 style="color:{color};">Event Permit {status_text}</h2>
            <p>Hello <strong>{event_data['first_name']}</strong>,</p>
            <p>Your event permit application has been processed.</p>
            <table style="background:{bg_color};border-left:4px solid {color};padding:15px;border-radius:10px;margin:20px 0;width:100%;">
                <tr><td style="color:#334155;font-size:14px;line-height:1.7;">
                    <strong>Event:</strong> {event_data['event_name']}<br>
                    <strong>Date:</strong> {event_data['event_date']}<br>
                    <strong>Time:</strong> {event_data['start_time']} - {event_data['end_time']}<br>
                    <strong>Venue:</strong> {event_data['venue']}<br>
                    <strong>Remarks:</strong> {remarks or 'N/A'}
                </td></tr>
            </table>
        </div>
        </body></html>
        """
        send_email(event_data['email'], subject, body_html)

        cursor.execute("SELECT user_id FROM event_permits WHERE id = %s", (event_id,))
        permit_owner = cursor.fetchone()
        if permit_owner:
            create_notification(
                permit_owner['user_id'],
                f'{icon} Permit {status.title()}',
                f'Your permit for "{event_data["event_name"]}" has been {status}. {("Remarks: " + remarks) if remarks else ""}',
                f'permit_{status}',
                link='/my-requests'
            )

    conn.close()
    return jsonify({'success': True, 'message': f'Event {status} successfully'})

@app.route('/api/event/<int:event_id>/update-status', methods=['POST'])
def update_event_status(event_id):
    if 'user_id' not in session or session.get('role') not in ADMIN_ROLES:
        return jsonify({'error': 'Unauthorized'}), 401

    data = request.json
    status = data.get('status')
    remarks = data.get('remarks', '').strip()

    if status not in ['approved', 'rejected']:
        return jsonify({'error': 'Invalid status'}), 400

    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT e.event_name, e.event_date, e.start_time, e.end_time, e.venue,
               u.email, u.first_name, u.last_name
        FROM event_permits e
        JOIN users u ON e.user_id = u.id
        WHERE e.id = %s
    """, (event_id,))
    event_data = cursor.fetchone()

    if event_data:
        current_role = session.get('role')
        if current_role in COURT_CONFIG:
            if COURT_CONFIG[current_role]['venue'] != event_data['venue']:
                conn.close()
                return jsonify({'error': 'Unauthorized. This event belongs to another court.'}), 403

    cursor.execute("""
        UPDATE event_permits SET status = %s, admin_remarks = %s WHERE id = %s
    """, (status, remarks, event_id))
    conn.commit()
    conn.close()

    if event_data:
        status_text = "APPROVED ✅" if status == 'approved' else "REJECTED ❌"
        color = "#059669" if status == 'approved' else "#dc2626"
        bg_color = "#ecfdf5" if status == 'approved' else "#fef2f2"
        icon = "✅" if status == 'approved' else "❌"

        subject = f"Event Permit {status.upper()} - Barangay Sto. Nino"
        body_html = f"""
        <html><body style="font-family:Arial,sans-serif;padding:20px;background:#ecfdf5;">
        <div style="max-width:600px;margin:0 auto;background:#fff;border-radius:16px;padding:30px;">
            <h2 style="color:{color};">Event Permit {status_text}</h2>
            <p>Hello <strong>{event_data['first_name']}</strong>,</p>
            <p>Your event permit application has been processed.</p>
            <table style="background:{bg_color};border-left:4px solid {color};padding:15px;border-radius:10px;margin:20px 0;width:100%;">
                <tr><td style="color:#334155;font-size:14px;line-height:1.7;">
                    <strong>Event:</strong> {event_data['event_name']}<br>
                    <strong>Date:</strong> {event_data['event_date']}<br>
                    <strong>Time:</strong> {event_data['start_time']} - {event_data['end_time']}<br>
                    <strong>Venue:</strong> {event_data['venue']}<br>
                    <strong>Remarks:</strong> {remarks or 'N/A'}
                </td></tr>
            </table>
        </div>
        </body></html>
        """
        send_email(event_data['email'], subject, body_html)

    return jsonify({'success': True, 'message': f'Event permit {status} successfully'})

# ============================================================
# ACTIVITY LOGS
# ============================================================
@app.route('/admin/activity-logs')
def admin_activity_logs():
    if 'user_id' not in session or session.get('role') not in ADMIN_ROLES:
        flash('Unauthorized access.', 'danger')
        return redirect(url_for('login'))
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    role = session.get('role')
    if role == 'head_admin':
        cursor.execute("""
            SELECT l.*, u.first_name, u.last_name, u.role
            FROM admin_activity_logs l
            LEFT JOIN users u ON l.admin_id = u.id
            ORDER BY l.created_at DESC
            LIMIT 100
        """)
        logs = cursor.fetchall()
        conn.close()
        return render_template('admin/head_admin_activity_logs.html', logs=logs)
    cursor.execute("""
        SELECT l.*, u.first_name, u.last_name
        FROM admin_activity_logs l
        LEFT JOIN users u ON l.admin_id = u.id
        WHERE l.admin_id = %s
        ORDER BY l.created_at DESC
        LIMIT 50
    """, (session['user_id'],))
    logs = cursor.fetchall()
    conn.close()
    return render_template('admin/sec_admin_activity_logs.html', logs=logs)

@app.route('/admin/update-document-status/<int:doc_id>', methods=['POST'])
def update_document_status(doc_id):
    if 'user_id' not in session or session.get('role') not in ['head_admin', 'admin_documents']:
        return jsonify({'error': 'Unauthorized'}), 401

    data = request.json
    status = data.get('status')
    remarks = data.get('remarks', '').strip()

    if status not in ['processing', 'rejected']:
        return jsonify({'error': 'Invalid status'}), 400

    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        UPDATE document_requests SET status = %s, admin_remarks = %s WHERE id = %s
    """, (status, remarks, doc_id))
    conn.commit()

    cursor.execute("""
        INSERT INTO admin_activity_logs (admin_id, action, document_id, details)
        VALUES (%s, %s, %s, %s)
    """, (session['user_id'], status, doc_id, f'Document {status} - Remarks: {remarks}'))
    conn.commit()

    cursor.execute("""
        SELECT u.email, u.first_name, u.last_name, d.document_type, d.user_id, d.reference_number
        FROM document_requests d
        JOIN users u ON d.user_id = u.id
        WHERE d.id = %s
    """, (doc_id,))
    user_data = cursor.fetchone()
    conn.close()

    if user_data:
        if status == 'processing':
            status_text = "PROCESSING ⏳"
            color = "#d97706"
            bg_color = "#fffbeb"
            icon = "⏳"
            main_message = "Your request is currently being processed. Please wait for the final document to be ready for pickup."
            subject = f"Document Request is Now Processing - Barangay Sto. Nino"
        else:
            status_text = "REJECTED ❌"
            color = "#dc2626"
            bg_color = "#fef2f2"
            icon = "❌"
            main_message = "Your request has been rejected."
            subject = f"Document Request REJECTED - Barangay Sto. Nino"

        body_html = f"""
        <html><body style="font-family:Arial,sans-serif;padding:20px;background:#ecfdf5;">
        <div style="max-width:600px;margin:0 auto;background:#fff;border-radius:16px;padding:30px;">
            <h2 style="color:{color};">{icon} Document {status_text}</h2>
            <p>Hello <strong>{user_data['first_name']}</strong>,</p>
            <p>{main_message}</p>
            <table style="background:{bg_color};border-left:4px solid {color};padding:15px;border-radius:10px;margin:20px 0;width:100%;">
                <tr><td style="color:#334155;font-size:14px;line-height:1.7;">
                    <strong>Document:</strong> {user_data['document_type'].replace('_', ' ').title()}<br>
                    <strong>Reference:</strong> {user_data['reference_number'] or 'N/A'}<br>
                    <strong>Remarks:</strong> {remarks or 'N/A'}<br>
                    <strong>Date:</strong> {datetime.datetime.now().strftime('%B %d, %Y %I:%M %p')}
                </td></tr>
            </table>
        </div>
        </body></html>
        """
        send_email(user_data['email'], subject, body_html)

        if status == 'processing':
            status_emoji = '⏳'
        elif status == 'rejected':
            status_emoji = '❌'
        else:
            status_emoji = '✅'

        create_notification(
            user_data['user_id'],
            f'{status_emoji} Document {status.title()}',
            f'Your {user_data["document_type"].replace("_", " ").title()} request is now {status}. {("Remarks: " + remarks) if remarks else ""}',
            f'document_{status}',
            link='/my-requests'
        )

    return jsonify({
        'success': True,
        'message': f'Document {status} successfully',
        'user_data': user_data
    })

@app.route('/api/admin/my-activity-logs')
def api_my_activity_logs():
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized', 'logs': []}), 401
    if session.get('role') not in ADMIN_ROLES:
        return jsonify({'error': 'Unauthorized', 'logs': []}), 401
    try:
        limit = int(request.args.get('limit', 10))
        if limit > 50:
            limit = 50
        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT action, details, created_at
            FROM admin_activity_logs
            WHERE admin_id = %s
            ORDER BY created_at DESC
            LIMIT %s
        """, (session['user_id'], limit))
        logs = cursor.fetchall()
        conn.close()
        for log in logs:
            if log.get('created_at'):
                log['created_at'] = log['created_at'].strftime('%Y-%m-%d %H:%M:%S')
        return jsonify({'success': True, 'logs': logs})
    except Exception as e:
        print(f"Activity logs error: {e}")
        return jsonify({'error': str(e), 'logs': []}), 500

@app.route('/admin/document-details/<int:doc_id>')
def admin_document_details(doc_id):
    if 'user_id' not in session or session.get('role') not in ['head_admin', 'admin_documents']:
        return jsonify({'error': 'Unauthorized'}), 401

    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT d.*, u.first_name, u.last_name, u.email, u.contact_number, u.address
        FROM document_requests d
        JOIN users u ON d.user_id = u.id
        WHERE d.id = %s
    """, (doc_id,))
    document = cursor.fetchone()
    conn.close()

    if not document:
        return jsonify({'error': 'Document not found'}), 404

    if document.get('created_at') and hasattr(document['created_at'], 'strftime'):
        document['created_at_formatted'] = document['created_at'].strftime('%b %d, %Y')
    elif document.get('created_at'):
        document['created_at_formatted'] = str(document['created_at'])

    if document.get('dob') and hasattr(document['dob'], 'strftime'):
        document['dob'] = document['dob'].strftime('%Y-%m-%d')
    if document.get('signature_date') and hasattr(document['signature_date'], 'strftime'):
        document['signature_date'] = document['signature_date'].strftime('%Y-%m-%d')

    return jsonify(document)

@app.route('/verify/<string:token>')
@login_required
def verify_document(token):
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT d.*, u.first_name, u.last_name, u.email, u.contact_number
        FROM document_requests d
        JOIN users u ON d.user_id = u.id
        WHERE d.qr_token = %s
    """, (token,))
    doc = cursor.fetchone()
    conn.close()

    if not doc:
        flash('Invalid or Expired QR Code.', 'danger')
        return redirect(url_for('admin_documents'))
    if session.get('role') not in ['head_admin', 'admin_documents']:
        flash('Unauthorized access.', 'danger')
        return redirect(url_for('login'))
    return render_template('admin/verify_document.html', doc=doc)

@app.route('/admin/events')
def admin_events():
    if 'user_id' not in session or session.get('role') not in ['head_admin', 'admin_court_1', 'admin_court_2', 'admin_court_3', 'admin_court_4']:
        flash('Unauthorized access.', 'danger')
        return redirect(url_for('login'))
    role = session.get('role')
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    if role in COURT_CONFIG:
        VENUE = COURT_CONFIG[role]['venue']
        cursor.execute("""
            SELECT e.*, u.first_name, u.last_name, u.email, u.contact_number
            FROM event_permits e
            JOIN users u ON e.user_id = u.id
            WHERE e.venue = %s
            ORDER BY e.id DESC
        """, (VENUE,))
    else:
        cursor.execute("""
            SELECT e.*, u.first_name, u.last_name, u.email, u.contact_number
            FROM event_permits e
            JOIN users u ON e.user_id = u.id
            ORDER BY e.id DESC
        """)
    events = cursor.fetchall()
    conn.close()
    return render_template('admin/sec_admin_events.html', events=events)

@app.route('/user-settings')
@role_required('resident')
def user_settings():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE id = %s", (session['user_id'],))
    user = cursor.fetchone()
    conn.close()
    return render_template('settings.html', user=user)

@app.route('/user-delete-account', methods=['POST'])
@role_required('resident')
def user_delete_account():
    confirm_text = request.form.get('confirm_text', '').strip()
    password = request.form.get('password', '')

    if confirm_text != 'DELETE':
        flash('Please type DELETE to confirm.', 'danger')
        return redirect(url_for('user_settings'))
    if not password:
        flash('Please enter your password.', 'danger')
        return redirect(url_for('user_settings'))

    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT password FROM users WHERE id = %s", (session['user_id'],))
    user = cursor.fetchone()

    if not user or not check_password_hash(user['password'], password):
        conn.close()
        flash('Password is incorrect.', 'danger')
        return redirect(url_for('user_settings'))

    user_id = session['user_id']
    try:
        cursor.execute("DELETE FROM document_requests WHERE user_id = %s", (user_id,))
        cursor.execute("DELETE FROM event_permits WHERE user_id = %s", (user_id,))
        cursor.execute("DELETE FROM notifications WHERE user_id = %s", (user_id,))
        cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
        conn.commit()
        conn.close()
        session.clear()
        flash('Your account has been permanently deleted.', 'info')
        return redirect(url_for('login'))
    except Exception as e:
        conn.rollback()
        conn.close()
        flash(f'Error deleting account: {str(e)}', 'danger')
        return redirect(url_for('user_settings'))

@app.route('/sec-admin-settings')
def sec_admin_settings():
    if 'user_id' not in session or session.get('role') not in ADMIN_ROLES:
        flash('Unauthorized access.', 'danger')
        return redirect(url_for('login'))
    return render_template('admin/sec_admin_settings.html')

@app.route('/admin-update-profile', methods=['POST'])
def admin_update_profile():
    if 'user_id' not in session or session.get('role') not in ADMIN_ROLES:
        flash('Unauthorized access.', 'danger')
        return redirect(url_for('login'))
    first_name = request.form.get('first_name', '').strip()
    last_name = request.form.get('last_name', '').strip()
    email = request.form.get('email', '').strip()
    if not first_name or not last_name or not email:
        flash('Please fill in all fields.', 'danger')
        return redirect(url_for('sec_admin_settings'))
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET first_name = %s, last_name = %s, email = %s WHERE id = %s",
                   (first_name, last_name, email, session['user_id']))
    conn.commit()
    conn.close()
    session['fullname'] = f"{first_name} {last_name}"
    session['email'] = email
    flash('Profile updated successfully!', 'success')
    return redirect(url_for('sec_admin_settings'))

@app.route('/admin-change-password', methods=['POST'])
def admin_change_password():
    if 'user_id' not in session or session.get('role') not in ADMIN_ROLES:
        flash('Unauthorized access.', 'danger')
        return redirect(url_for('login'))
    current_password = request.form.get('current_password', '')
    new_password = request.form.get('new_password', '')
    confirm_password = request.form.get('confirm_password', '')
    if not current_password or not new_password or not confirm_password:
        flash('Please fill in all fields.', 'danger')
        return redirect(url_for('sec_admin_settings'))
    if new_password != confirm_password:
        flash('New passwords do not match.', 'danger')
        return redirect(url_for('sec_admin_settings'))
    if len(new_password) < 8:
        flash('New password must be at least 8 characters.', 'danger')
        return redirect(url_for('sec_admin_settings'))
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT password FROM users WHERE id = %s", (session['user_id'],))
    user = cursor.fetchone()
    if not user or not check_password_hash(user['password'], current_password):
        conn.close()
        flash('Current password is incorrect.', 'danger')
        return redirect(url_for('sec_admin_settings'))
    hashed_password = generate_password_hash(new_password)
    cursor.execute("UPDATE users SET password = %s WHERE id = %s", (hashed_password, session['user_id']))
    conn.commit()
    conn.close()
    flash('Password changed successfully!', 'success')
    return redirect(url_for('sec_admin_settings'))

@app.route('/secondary-admin-settings')
def secondary_admin_settings():
    if 'user_id' not in session or session.get('role') not in ADMIN_ROLES:
        flash('Unauthorized access.', 'danger')
        return redirect(url_for('login'))
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE id = %s", (session['user_id'],))
    user = cursor.fetchone()
    conn.close()
    return render_template('admin/secondary_admin_settings.html', user=user)

@app.route('/secondary-admin-update-profile', methods=['POST'])
def secondary_admin_update_profile():
    if 'user_id' not in session or session.get('role') not in ADMIN_ROLES:
        flash('Unauthorized access.', 'danger')
        return redirect(url_for('login'))
    first_name = request.form.get('first_name', '').strip()
    last_name = request.form.get('last_name', '').strip()
    email = request.form.get('email', '').strip()
    if not first_name or not last_name or not email:
        flash('Please fill in all fields.', 'danger')
        return redirect(url_for('secondary_admin_settings'))
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET first_name = %s, last_name = %s, email = %s WHERE id = %s",
                   (first_name, last_name, email, session['user_id']))
    conn.commit()
    conn.close()
    session['fullname'] = f"{first_name} {last_name}"
    session['email'] = email
    flash('Profile updated successfully!', 'success')
    return redirect(url_for('secondary_admin_settings'))

@app.route('/secondary-admin-change-password', methods=['POST'])
def secondary_admin_change_password():
    if 'user_id' not in session or session.get('role') not in ADMIN_ROLES:
        flash('Unauthorized access.', 'danger')
        return redirect(url_for('login'))
    current_password = request.form.get('current_password', '')
    new_password = request.form.get('new_password', '')
    confirm_password = request.form.get('confirm_password', '')
    if not current_password or not new_password or not confirm_password:
        flash('Please fill in all fields.', 'danger')
        return redirect(url_for('secondary_admin_settings'))
    if new_password != confirm_password:
        flash('New passwords do not match.', 'danger')
        return redirect(url_for('secondary_admin_settings'))
    if len(new_password) < 8:
        flash('New password must be at least 8 characters.', 'danger')
        return redirect(url_for('secondary_admin_settings'))
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT password FROM users WHERE id = %s", (session['user_id'],))
    user = cursor.fetchone()
    if not user or not check_password_hash(user['password'], current_password):
        conn.close()
        flash('Current password is incorrect.', 'danger')
        return redirect(url_for('secondary_admin_settings'))
    hashed_password = generate_password_hash(new_password)
    cursor.execute("UPDATE users SET password = %s WHERE id = %s", (hashed_password, session['user_id']))
    conn.commit()
    conn.close()
    flash('Password changed successfully!', 'success')
    return redirect(url_for('secondary_admin_settings'))

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
        if user.get('created_at') and hasattr(user['created_at'], 'strftime'):
            user['created_at'] = user['created_at'].strftime('%b %d, %Y')
    return render_template('admin/user_management.html', users=users)

@app.route('/update-role/<int:user_id>', methods=['POST'])
def update_user_role(user_id):
    if 'user_id' not in session or session.get('role') != 'head_admin':
        flash('Unauthorized access.', 'danger')
        return redirect(url_for('login'))
    if user_id == session['user_id']:
        flash('You cannot change your own role.', 'danger')
        return redirect(url_for('user_management'))
    new_role = request.form.get('role')
    if new_role not in ADMIN_ROLES:
        flash('Invalid role selected.', 'danger')
        return redirect(url_for('user_management'))
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id, role FROM users WHERE id = %s", (user_id,))
    user = cursor.fetchone()
    if not user:
        conn.close()
        flash('User not found.', 'danger')
        return redirect(url_for('user_management'))
    if user['role'] not in ADMIN_ROLES:
        conn.close()
        flash('Resident accounts cannot be promoted.', 'danger')
        return redirect(url_for('user_management'))
    if user['role'] == 'head_admin':
        conn.close()
        flash('Cannot change Head Admin role.', 'danger')
        return redirect(url_for('user_management'))
    cursor.execute("UPDATE users SET role = %s WHERE id = %s", (new_role, user_id))
    conn.commit()
    conn.close()
    flash('Admin role updated successfully!', 'success')
    return redirect(url_for('user_management'))

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
    if user.get('created_at') and hasattr(user['created_at'], 'strftime'):
        user['created_at'] = user['created_at'].strftime('%b %d, %Y')
    return jsonify(user)

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

@app.route('/api/user/<int:user_id>/toggle-active', methods=['POST'])
def api_toggle_admin_active(user_id):
    if 'user_id' not in session or session.get('role') != 'head_admin':
        return jsonify({'error': 'Unauthorized'}), 401
    if user_id == session['user_id']:
        return jsonify({'error': 'You cannot deactivate your own account'}), 400
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id, role, is_verified FROM users WHERE id = %s", (user_id,))
    user = cursor.fetchone()
    if not user:
        conn.close()
        return jsonify({'error': 'Admin not found'}), 404
    if user['role'] == 'head_admin':
        conn.close()
        return jsonify({'error': 'Cannot deactivate another Head Admin'}), 400
    new_status = not user['is_verified']
    cursor.execute("UPDATE users SET is_verified = %s WHERE id = %s", (new_status, user_id))
    conn.commit()
    conn.close()
    status_text = 'activated' if new_status else 'deactivated'
    return jsonify({'success': True, 'message': f'Admin {status_text} successfully', 'status': new_status})

@app.route('/api/user/<int:user_id>/delete-admin', methods=['DELETE'])
def api_delete_admin(user_id):
    if 'user_id' not in session or session.get('role') != 'head_admin':
        return jsonify({'error': 'Unauthorized'}), 401
    if user_id == session['user_id']:
        return jsonify({'error': 'You cannot delete your own account'}), 400
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id, role, email FROM users WHERE id = %s", (user_id,))
    user = cursor.fetchone()
    if not user:
        conn.close()
        return jsonify({'error': 'Admin not found'}), 404
    if user['role'] == 'head_admin':
        conn.close()
        return jsonify({'error': 'Cannot delete another Head Admin'}), 400
    try:
        cursor.execute("UPDATE admin_activity_logs SET admin_id = NULL WHERE admin_id = %s", (user_id,))
        cursor.execute("UPDATE announcements SET created_by = NULL WHERE created_by = %s", (user_id,))
        cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
        conn.commit()
        conn.close()
        return jsonify({'success': True, 'message': 'Admin deleted successfully'})
    except mysql.connector.Error as e:
        conn.rollback()
        conn.close()
        return jsonify({'error': f'Database error: {str(e)}'}), 500

@app.route('/admins')
def admin_management():
    if 'user_id' not in session or session.get('role') != 'head_admin':
        flash('Please login as Head Admin.', 'danger')
        return redirect(url_for('login'))
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT id, first_name, last_name, email, contact_number, address, role, is_verified, created_at
        FROM users
        WHERE role IN ('head_admin', 'admin_court_1', 'admin_court_2', 'admin_court_3', 'admin_court_4', 'admin_documents')
        ORDER BY role DESC, created_at DESC
    """)
    admins = cursor.fetchall()
    conn.close()
    for admin in admins:
        if admin.get('created_at') and hasattr(admin['created_at'], 'strftime'):
            admin['created_at'] = admin['created_at'].strftime('%b %d, %Y')
    return render_template('admin/admin_management.html', admins=admins)

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

@app.route('/create-admin', methods=['POST'])
def create_admin():
    if 'user_id' not in session or session.get('role') != 'head_admin':
        flash('Unauthorized access.', 'danger')
        return redirect(url_for('login'))
    first_name = request.form.get('first_name', '').strip()
    last_name = request.form.get('last_name', '').strip()
    email = request.form.get('email', '').strip()
    password = request.form.get('password', '')
    role = request.form.get('role', 'admin_court_1')

    if not first_name or not last_name or not email or not password:
        flash('Please fill in all fields.', 'danger')
        return redirect(url_for('admin_management'))
    if role not in ADMIN_ROLES:
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

@app.route('/api/user/<int:user_id>/update-role', methods=['POST'])
def api_update_user_role(user_id):
    if 'user_id' not in session or session.get('role') != 'head_admin':
        return jsonify({'error': 'Unauthorized'}), 401
    if user_id == session['user_id']:
        return jsonify({'error': 'You cannot change your own role'}), 400
    data = request.get_json(silent=True) or {}
    new_role = data.get('role')
    if new_role not in ADMIN_ROLES:
        return jsonify({'error': 'Invalid role'}), 400
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id, role FROM users WHERE id = %s", (user_id,))
    user = cursor.fetchone()
    if not user:
        conn.close()
        return jsonify({'error': 'User not found'}), 404
    if user['role'] not in ADMIN_ROLES:
        conn.close()
        return jsonify({'error': 'Resident accounts cannot be promoted.'}), 403
    if user['role'] == 'head_admin':
        conn.close()
        return jsonify({'error': 'Cannot change Head Admin role.'}), 403
    cursor.execute("UPDATE users SET role = %s WHERE id = %s", (new_role, user_id))
    conn.commit()
    conn.close()
    return jsonify({'success': True, 'message': 'Admin role updated successfully'})

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
    if user['role'] == 'resident':
        conn.close()
        return jsonify({'error': 'Resident accounts cannot be promoted to Admin.'}), 403
    if user['role'] in ADMIN_ROLES:
        conn.close()
        return jsonify({'error': 'User is already an admin'}), 400
    conn.close()
    return jsonify({'error': 'Invalid account role'}), 400

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
        return jsonify({'error': 'Cannot demote Head Admin'}), 403
    if user['role'] in ADMIN_ROLES:
        conn.close()
        return jsonify({'error': 'Admin accounts cannot be demoted to Resident.'}), 403
    conn.close()
    return jsonify({'error': 'User is not an admin'}), 400

# ============================================================
# ANNOUNCEMENTS
# ============================================================
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
        ORDER BY a.is_pinned DESC, a.created_at DESC
    """)
    announcements = cursor.fetchall()

    cursor.execute("SELECT COUNT(*) as total FROM announcements")
    total_announcements = cursor.fetchone()['total']
    cursor.execute("""
        SELECT COUNT(*) as total FROM announcements
        WHERE MONTH(created_at) = MONTH(CURRENT_DATE()) AND YEAR(created_at) = YEAR(CURRENT_DATE())
    """)
    this_month = cursor.fetchone()['total']
    cursor.execute("""
        SELECT COUNT(*) as total FROM announcements
        WHERE YEARWEEK(created_at, 1) = YEARWEEK(CURRENT_DATE(), 1)
    """)
    this_week = cursor.fetchone()['total']
    conn.close()

    return render_template('admin/announcements.html',
                         announcements=announcements,
                         total_announcements=total_announcements,
                         this_month=this_month,
                         this_week=this_week)

@app.route('/create-announcement', methods=['POST'])
def create_announcement():
    if 'user_id' not in session or session.get('role') != 'head_admin':
        flash('Unauthorized access.', 'danger')
        return redirect(url_for('login'))
    title = request.form.get('title', '').strip()
    content = request.form.get('content', '').strip()
    is_draft = request.form.get('is_draft', '0') == '1'
    if not title or not content:
        flash('Please fill in all fields.', 'danger')
        return redirect(url_for('announcements'))
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO announcements (title, content, created_by, is_draft)
        VALUES (%s, %s, %s, %s)
    """, (title, content, session['user_id'], is_draft))
    conn.commit()
    conn.close()
    if is_draft:
        flash('Announcement saved as draft!', 'info')
    else:
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
    cursor.execute("UPDATE announcements SET title = %s, content = %s WHERE id = %s", (title, content, announcement_id))
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

@app.route('/api/announcement/<int:announcement_id>/view', methods=['POST'])
def increment_announcement_view(announcement_id):
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE announcements SET view_count = COALESCE(view_count, 0) + 1 WHERE id = %s
        """, (announcement_id,))
        conn.commit()
        cursor.execute("SELECT view_count FROM announcements WHERE id = %s", (announcement_id,))
        result = cursor.fetchone()
        conn.close()
        return jsonify({'success': True, 'view_count': result[0] if result else 0})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/announcement/<int:announcement_id>/toggle-pin', methods=['POST'])
def toggle_announcement_pin(announcement_id):
    if 'user_id' not in session or session.get('role') != 'head_admin':
        return jsonify({'error': 'Unauthorized'}), 401
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id, is_pinned, title FROM announcements WHERE id = %s", (announcement_id,))
    ann = cursor.fetchone()
    if not ann:
        conn.close()
        return jsonify({'error': 'Announcement not found'}), 404
    new_status = not ann['is_pinned']
    cursor.execute("UPDATE announcements SET is_pinned = %s WHERE id = %s", (new_status, announcement_id))
    conn.commit()
    conn.close()
    status_text = 'pinned' if new_status else 'unpinned'
    return jsonify({'success': True, 'message': f'Announcement {status_text} successfully', 'is_pinned': new_status})

@app.route('/api/announcement/<int:announcement_id>/toggle-draft', methods=['POST'])
def toggle_announcement_draft(announcement_id):
    if 'user_id' not in session or session.get('role') != 'head_admin':
        return jsonify({'error': 'Unauthorized'}), 401
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id, is_draft FROM announcements WHERE id = %s", (announcement_id,))
    ann = cursor.fetchone()
    if not ann:
        conn.close()
        return jsonify({'error': 'Announcement not found'}), 404
    new_status = not ann['is_draft']
    cursor.execute("UPDATE announcements SET is_draft = %s WHERE id = %s", (new_status, announcement_id))
    conn.commit()
    conn.close()
    status_text = 'saved as draft' if new_status else 'published'
    return jsonify({'success': True, 'message': f'Announcement {status_text} successfully', 'is_draft': new_status})

@app.route('/api/announcement/<int:announcement_id>/mark-read', methods=['POST'])
def mark_announcement_read(announcement_id):
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    try:
        user_id = session['user_id']
        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT id FROM announcements WHERE id = %s", (announcement_id,))
        if not cursor.fetchone():
            conn.close()
            return jsonify({'error': 'Announcement not found'}), 404
        cursor.execute("""
            INSERT IGNORE INTO announcement_reads (user_id, announcement_id) VALUES (%s, %s)
        """, (user_id, announcement_id))
        conn.commit()
        conn.close()
        return jsonify({'success': True, 'message': 'Marked as read'})
    except Exception as e:
        print(f"Error marking as read: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/announcements/mark-all-read', methods=['POST'])
def mark_all_announcements_read():
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    try:
        user_id = session['user_id']
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT IGNORE INTO announcement_reads (user_id, announcement_id)
            SELECT %s, id FROM announcements WHERE is_draft = FALSE
        """, (user_id,))
        conn.commit()
        conn.close()
        return jsonify({'success': True, 'message': 'All marked as read'})
    except Exception as e:
        print(f"Error marking all as read: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/admin/announcements')
def admin_view_announcements():
    if 'user_id' not in session:
        flash('Please login first.', 'warning')
        return redirect(url_for('login'))
    allowed_roles = ['head_admin', 'admin_documents', 'admin_court_1', 'admin_court_2', 'admin_court_3', 'admin_court_4']
    if session.get('role') not in allowed_roles:
        flash('Unauthorized access.', 'danger')
        return redirect(url_for('login'))
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT a.*, u.first_name, u.last_name
        FROM announcements a
        LEFT JOIN users u ON a.created_by = u.id
        WHERE a.is_draft = FALSE
        ORDER BY a.is_pinned DESC, a.created_at DESC
    """)
    announcements = cursor.fetchall()
    cursor.execute("SELECT COUNT(*) as total FROM announcements WHERE is_draft = FALSE")
    total_announcements = cursor.fetchone()['total']
    cursor.execute("SELECT COUNT(*) as total FROM announcements WHERE is_draft = FALSE AND is_pinned = TRUE")
    pinned_count = cursor.fetchone()['total']
    conn.close()
    return render_template('admin/admin_view_announcements.html',
                         announcements=announcements,
                         total_announcements=total_announcements,
                         pinned_count=pinned_count)

@app.route('/user-announcements')
@role_required('resident')
def user_announcements():
    if 'user_id' not in session:
        flash('Please login first.', 'warning')
        return redirect(url_for('login'))
    user_id = session['user_id']
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT a.*, u.first_name, u.last_name,
               CASE WHEN ar.id IS NOT NULL THEN 1 ELSE 0 END as is_read
        FROM announcements a
        LEFT JOIN users u ON a.created_by = u.id
        LEFT JOIN announcement_reads ar ON ar.announcement_id = a.id AND ar.user_id = %s
        WHERE a.is_draft = FALSE
        ORDER BY a.is_pinned DESC, a.created_at DESC
    """, (user_id,))
    announcements = cursor.fetchall()
    conn.close()
    notifications = announcements[:5]
    return render_template('user_announcements.html', announcements=announcements, notifications=notifications)

@app.route('/api/announcements/unread_count', methods=['GET'])
def api_unread_announcements_count():
    if 'user_id' not in session:
        return jsonify({'unread_count': 0})
    try:
        user_id = session['user_id']
        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT COUNT(*) as unread_count
            FROM announcements a
            LEFT JOIN announcement_reads ar ON ar.announcement_id = a.id AND ar.user_id = %s
            WHERE a.is_draft = FALSE AND ar.id IS NULL
        """, (user_id,))
        result = cursor.fetchone()
        unread = result['unread_count'] if result else 0
        conn.close()
        return jsonify({'unread_count': unread})
    except Exception as e:
        print(f"Error fetching unread count: {e}")
        return jsonify({'unread_count': 0})

@app.route('/api/announcements/recent', methods=['GET'])
def api_recent_announcements():
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized', 'announcements': []}), 401
    try:
        limit = int(request.args.get('limit', 5))
        if limit > 20:
            limit = 20
        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        user_id = session['user_id']
        cursor.execute("""
            SELECT a.id, a.title, a.content, a.created_at,
                   CASE WHEN ar.id IS NOT NULL THEN 1 ELSE 0 END as is_read
            FROM announcements a
            LEFT JOIN announcement_reads ar ON ar.announcement_id = a.id AND ar.user_id = %s
            WHERE a.is_draft = FALSE
            ORDER BY a.is_pinned DESC, a.created_at DESC
            LIMIT %s
        """, (user_id, limit))
        announcements = cursor.fetchall()
        conn.close()
        for a in announcements:
            if a.get('created_at') and hasattr(a['created_at'], 'strftime'):
                a['created_at'] = a['created_at'].strftime('%Y-%m-%d %H:%M:%S')
        return jsonify({'success': True, 'announcements': announcements})
    except Exception as e:
        print(f"Recent announcements error: {e}")
        return jsonify({'error': str(e), 'announcements': []}), 500

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
    cursor.execute("SELECT email, first_name FROM users WHERE role = 'resident'")
    users = cursor.fetchall()
    conn.close()
    if not users:
        flash('Walang residents na pwedeng padalhan.', 'warning')
        return redirect(url_for('announcements'))
    body_template = """
    <html><body style="margin:0;padding:0;background:#f4f8f5;font-family:'Segoe UI',Tahoma,sans-serif;">
        <table width="100%" style="background:#f4f8f5;padding:40px 15px;">
            <tr><td align="center">
                <table width="600" style="max-width:600px;background:#fff;border-radius:16px;overflow:hidden;box-shadow:0 8px 30px rgba(0,0,0,0.08);">
                    <tr><td style="background:linear-gradient(135deg,#0f3d2a,#228b54);padding:35px;text-align:center;">
                        <div style="width:70px;height:70px;background:#fff;border-radius:50%;line-height:70px;font-size:32px;margin:0 auto 12px;">📢</div>
                        <h1 style="margin:0;color:#fff;font-size:22px;">Barangay Announcement</h1>
                    </td></tr>
                    <tr><td style="padding:35px 40px;">
                        <h2 style="margin:0 0 15px;color:#0f3d2a;font-size:20px;">__SUBJECT__</h2>
                        <p style="margin:0 0 20px;color:#64748b;font-size:14px;line-height:1.7;">__MESSAGE__</p>
                        <table width="100%" style="margin:25px 0 10px;"><tr><td align="center">
                            <a href="http://127.0.0.1:5000/login" style="display:inline-block;background:linear-gradient(135deg,#0f3d2a,#228b54);color:#fff;padding:14px 40px;text-decoration:none;border-radius:10px;font-weight:700;font-size:14px;">Login to Portal</a>
                        </td></tr></table>
                    </td></tr>
                    <tr><td style="background:#0f3d2a;padding:20px;text-align:center;">
                        <p style="margin:0;color:#c9d6f0;font-size:11px;">© 2026 Barangay Sto. Nino. Automated message.</p>
                    </td></tr>
                </table>
            </td></tr>
        </table>
    </body></html>
    """
    sent_count = 0
    failed_count = 0
    for user in users:
        body_html = body_template.replace('__SUBJECT__', subject).replace('__MESSAGE__', message)
        if send_email(user['email'], subject, body_html):
            sent_count += 1
        else:
            failed_count += 1
    if failed_count > 0:
        flash(f'Email sent to {sent_count} users. {failed_count} failed.', 'warning')
    else:
        flash(f'Email sent to {sent_count} users successfully!', 'success')
    return redirect(url_for('announcements'))

@app.route('/api/permits', methods=['GET', 'POST'])
@role_required('resident')
def api_permits():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    if request.method == 'GET':
        cursor.execute("SELECT * FROM event_permits WHERE user_id = %s ORDER BY requested_at DESC", (session['user_id'],))
        permits = cursor.fetchall()
        conn.close()
        return jsonify(permits)

    if request.method == 'POST':
        data = request.json
        event_name = data.get('event_name', '').strip()
        event_date = data.get('event_date', '').strip()
        start_time = data.get('start_time', '').strip()[:5]
        end_time = data.get('end_time', '').strip()[:5]
        venue = data.get('venue', '').strip()
        if not event_name or not event_date or not start_time or not end_time or not venue:
            conn.close()
            return jsonify({'error': 'Please fill in all required fields.'}), 400
        cursor.execute("""
            SELECT id FROM event_permits
            WHERE venue = %s AND event_date = %s AND status = 'approved'
              AND start_time < %s AND end_time > %s LIMIT 1
        """, (venue, event_date, end_time, start_time))
        if cursor.fetchone():
            conn.close()
            return jsonify({'error': 'This time slot is already taken by an approved event at this venue.'}), 409
        ref_num = f"BP-{datetime.datetime.now().strftime('%Y%m%d')}-{random.randint(1000, 9999)}"
        queue_num = get_next_queue_number('event_permits', venue)
        cursor.execute("""
            INSERT INTO event_permits (
                user_id, event_name, event_description, purpose, event_date,
                start_time, end_time, estimated_attendees, venue,
                status, requirements_file, reference_number, queuing_number
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, 'pending', %s, %s, %s)
        """, (
            session['user_id'], event_name, data.get('event_description', ''),
            data.get('purpose', ''), event_date, start_time, end_time,
            data.get('estimated_attendees', 0), venue, data.get('requirement', None),
            ref_num, queue_num
        ))
        conn.commit()
        permit_id = cursor.lastrowid
        create_notification(
            session['user_id'],
            '🎉 Permit Application Submitted',
            f'Your event permit "{event_name}" has been submitted for review. Reference: {ref_num} | Queue: {queue_num}',
            'permit_submitted',
            link='/my-requests'
        )
        conn.close()
        return jsonify({
            'message': 'Permit submitted successfully',
            'id': permit_id,
            'reference_number': ref_num,
            'queuing_number': queue_num
        }), 201

@app.route('/api/permits/notifications', methods=['GET'])
def api_notifications():
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT * FROM notifications WHERE user_id = %s ORDER BY created_at DESC LIMIT 50
    """, (session['user_id'],))
    notifications = cursor.fetchall()
    conn.close()
    return jsonify(notifications)

@app.route('/api/permits/notifications/unread_count', methods=['GET'])
def api_unread_count():
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT COUNT(*) as unread_count FROM notifications WHERE user_id = %s AND is_read = FALSE", (session['user_id'],))
    result = cursor.fetchone()
    conn.close()
    return jsonify({'unread_count': result['unread_count']})

@app.route('/api/permits/notifications/<int:notif_id>/mark_read', methods=['POST'])
def api_mark_read(notif_id):
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE notifications SET is_read = TRUE WHERE id = %s AND user_id = %s", (notif_id, session['user_id']))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Marked as read'})

@app.route('/api/permits/notifications/mark_all_read', methods=['POST'])
def api_mark_all_read():
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE notifications SET is_read = TRUE WHERE user_id = %s", (session['user_id'],))
    conn.commit()
    conn.close()
    return jsonify({'message': 'All notifications marked as read'})

@app.route('/api/document-requests')
def api_document_requests():
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM document_requests WHERE user_id = %s ORDER BY created_at DESC", (session['user_id'],))
    requests = cursor.fetchall()
    conn.close()
    return jsonify(requests)

# ============================================================
# SETTINGS (DUAL PURPOSE: HEAD ADMIN + RESIDENT)
# ============================================================
@app.route('/settings')
def settings():
    if 'user_id' not in session:
        flash('Please login first.', 'warning')
        return redirect(url_for('login'))
    role = session.get('role')
    if role == 'head_admin':
        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS system_config (
                id INT PRIMARY KEY AUTO_INCREMENT,
                barangay_name VARCHAR(255),
                barangay_address VARCHAR(255),
                contact_number VARCHAR(50),
                email_notifications VARCHAR(20) DEFAULT 'enabled',
                maintenance_mode BOOLEAN DEFAULT FALSE,
                maintenance_message TEXT,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
            )
        """)
        conn.commit()
        cursor.execute("SELECT * FROM system_config LIMIT 1")
        config = cursor.fetchone()
        if not config:
            cursor.execute("""
                INSERT INTO system_config (barangay_name, barangay_address, contact_number, email_notifications, maintenance_mode)
                VALUES ('Barangay Sto. Nino', 'Paranaque City', 'N/A', 'enabled', FALSE)
            """)
            conn.commit()
            cursor.execute("SELECT * FROM system_config LIMIT 1")
            config = cursor.fetchone()
        conn.close()
        maintenance_mode = config.get('maintenance_mode', False) if config else False
        return render_template('admin/settings.html', config=config, maintenance_mode=maintenance_mode)

    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE id = %s", (session['user_id'],))
    user = cursor.fetchone()
    conn.close()
    return render_template('settings.html', user=user)

@app.route('/update-profile', methods=['POST'])
def update_profile():
    if 'user_id' not in session or session.get('role') != 'head_admin':
        flash('Unauthorized access.', 'danger')
        return redirect(url_for('login'))
    first_name = request.form.get('first_name', '').strip()
    last_name = request.form.get('last_name', '').strip()
    email = request.form.get('email', '').strip()
    if not first_name or not last_name or not email:
        flash('Please fill in all fields.', 'danger')
        return redirect(url_for('settings'))
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET first_name = %s, last_name = %s, email = %s WHERE id = %s",
                   (first_name, last_name, email, session['user_id']))
    conn.commit()
    conn.close()
    session['fullname'] = f"{first_name} {last_name}"
    session['email'] = email
    flash('Profile updated successfully!', 'success')
    return redirect(url_for('settings'))

@app.route('/change-password', methods=['POST'])
def change_password():
    if 'user_id' not in session or session.get('role') != 'head_admin':
        flash('Unauthorized access.', 'danger')
        return redirect(url_for('login'))
    current_password = request.form.get('current_password', '')
    new_password = request.form.get('new_password', '')
    confirm_password = request.form.get('confirm_password', '')
    if not current_password or not new_password or not confirm_password:
        flash('Please fill in all fields.', 'danger')
        return redirect(url_for('settings'))
    if new_password != confirm_password:
        flash('New passwords do not match.', 'danger')
        return redirect(url_for('settings'))
    if len(new_password) < 8:
        flash('New password must be at least 8 characters.', 'danger')
        return redirect(url_for('settings'))
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT password FROM users WHERE id = %s", (session['user_id'],))
    user = cursor.fetchone()
    if not user or not check_password_hash(user['password'], current_password):
        conn.close()
        flash('Current password is incorrect.', 'danger')
        return redirect(url_for('settings'))
    hashed_password = generate_password_hash(new_password)
    cursor.execute("UPDATE users SET password = %s WHERE id = %s", (hashed_password, session['user_id']))
    conn.commit()
    conn.close()
    flash('Password changed successfully!', 'success')
    return redirect(url_for('settings'))

@app.route('/system-config', methods=['POST'])
def system_config():
    if 'user_id' not in session or session.get('role') != 'head_admin':
        flash('Unauthorized access.', 'danger')
        return redirect(url_for('login'))
    barangay_name = request.form.get('barangay_name', '').strip()
    barangay_address = request.form.get('barangay_address', '').strip()
    contact_number = request.form.get('contact_number', '').strip()
    email_notifications = request.form.get('email_notifications', 'enabled')
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM system_config LIMIT 1")
    config_exists = cursor.fetchone()
    if config_exists:
        cursor.execute("""
            UPDATE system_config SET barangay_name = %s, barangay_address = %s, contact_number = %s, email_notifications = %s
            WHERE id = 1
        """, (barangay_name, barangay_address, contact_number, email_notifications))
    else:
        cursor.execute("""
            INSERT INTO system_config (barangay_name, barangay_address, contact_number, email_notifications)
            VALUES (%s, %s, %s, %s)
        """, (barangay_name, barangay_address, contact_number, email_notifications))
    conn.commit()
    conn.close()
    flash('System configuration updated successfully!', 'success')
    return redirect(url_for('settings'))

@app.route('/toggle-maintenance', methods=['POST'])
def toggle_maintenance():
    if 'user_id' not in session or session.get('role') != 'head_admin':
        flash('Unauthorized access.', 'danger')
        return redirect(url_for('login'))
    maintenance_message = request.form.get('maintenance_message', 'System is currently under maintenance. Please check back later.')
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT maintenance_mode FROM system_config WHERE id = 1")
    config = cursor.fetchone()
    if config:
        new_mode = not config['maintenance_mode']
        cursor.execute("""
            UPDATE system_config SET maintenance_mode = %s, maintenance_message = %s WHERE id = 1
        """, (new_mode, maintenance_message))
    else:
        new_mode = True
        cursor.execute("""
            INSERT INTO system_config (maintenance_mode, maintenance_message) VALUES (TRUE, %s)
        """, (maintenance_message,))
    conn.commit()
    conn.close()
    status = 'ON' if new_mode else 'OFF'
    flash(f'Maintenance mode turned {status}!', 'success')
    return redirect(url_for('settings'))

# ============================================================
# DATABASE BACKUP API
# ============================================================
@app.route('/api/backup-database', methods=['POST'])
def backup_database():
    if 'user_id' not in session or session.get('role') != 'head_admin':
        return jsonify({'error': 'Unauthorized'}), 401
    try:
        backup_dir = 'backups'
        if not os.path.exists(backup_dir):
            os.makedirs(backup_dir)
        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{backup_dir}/barangay_backup_{timestamp}.sql"
        db_user = os.getenv('DB_USER', 'root')
        db_pass = os.getenv('DB_PASSWORD', '')
        db_name = os.getenv('DB_NAME', 'barangay_online_services')
        mysqldump_path = r"C:\Program Files\MySQL\MySQL Server 8.0\bin\mysqldump.exe"
        with open(filename, 'w') as f:
            result = subprocess.run(
                [mysqldump_path, f'-u{db_user}', f'-p{db_pass}', db_name],
                stdout=f, stderr=subprocess.PIPE, text=True
            )
        if result.returncode != 0:
            return jsonify({'error': 'Backup failed. Please check your DB credentials in .env', 'details': result.stderr}), 500
        return jsonify({'success': True, 'message': 'Database backup created successfully', 'filename': filename})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/download-backup')
def download_backup():
    if 'user_id' not in session or session.get('role') != 'head_admin':
        flash('Unauthorized access.', 'danger')
        return redirect(url_for('login'))
    backup_files = glob.glob('backups/barangay_backup_*.sql')
    if not backup_files:
        flash('No backup files found.', 'danger')
        return redirect(url_for('settings'))
    latest_backup = max(backup_files, key=os.path.getctime)
    return send_file(latest_backup, as_attachment=True, download_name=f"barangay_backup_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.sql")

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
        <a href="/sec-admin-dashboard">Documents Admin Dashboard</a><br>
        <a href="/court1/dashboard">Court 1 Dashboard</a><br>
        <a href="/court2/dashboard">Court 2 Dashboard</a><br>
        <a href="/court3/dashboard">Court 3 Dashboard</a><br>
        <a href="/court4/dashboard">Court 4 Dashboard</a><br>
        <a href="/dashboard">Resident Dashboard</a><br>
        <a href="/events-calendar">Events Calendar</a><br>
        <a href="/logout">Logout</a>
        """
    return "No active session. <a href='/login'>Login</a>"

@app.route('/logout')
def logout():
    if 'user_id' in session:
        try:
            log_conn = get_db()
            log_cursor = log_conn.cursor()
            log_cursor.execute("""
                INSERT INTO admin_activity_logs (admin_id, action, document_id, details)
                VALUES (%s, %s, %s, %s)
            """, (session['user_id'], 'logout', None, f'{session.get("role", "user")} logged out from {request.remote_addr}'))
            log_conn.commit()
            log_conn.close()
        except Exception as e:
            print(f"Logout log error: {e}")
    session.clear()
    return redirect(url_for('login'))

# ============================================================
# FORGOT PASSWORD ROUTES
# ============================================================
@app.route('/forgot-password', methods=['POST'])
def forgot_password():
    email = request.form.get('email', '').strip()
    if not email:
        flash('Please enter your email address.', 'danger')
        return redirect(url_for('login'))
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id, first_name, email FROM users WHERE email = %s", (email,))
    user = cursor.fetchone()
    if not user:
        conn.close()
        flash('If that email is registered, a reset code has been sent. Please check your inbox.', 'info')
        return redirect(url_for('login'))
    reset_code = f"{random.randint(0, 999999):06d}"
    expires_at = datetime.datetime.now() + datetime.timedelta(minutes=15)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS password_resets (
            id INT PRIMARY KEY AUTO_INCREMENT,
            user_id INT NOT NULL,
            code VARCHAR(6) NOT NULL,
            expires_at DATETIME NOT NULL,
            used BOOLEAN DEFAULT FALSE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        )
    """)
    conn.commit()
    cursor.execute("UPDATE password_resets SET used = TRUE WHERE user_id = %s AND used = FALSE", (user['id'],))
    cursor.execute("""
        INSERT INTO password_resets (user_id, code, expires_at) VALUES (%s, %s, %s)
    """, (user['id'], reset_code, expires_at))
    conn.commit()
    conn.close()
    session['reset_email'] = user['email']

    subject = "Your Password Reset Code - Barangay Sto. Nino"
    body_html = f"""
    <html><body style="font-family:Arial,sans-serif;padding:20px;">
        <h2>Password Reset Code</h2>
        <p>Hello {user['first_name']},</p>
        <p>Your reset code is:</p>
        <h1 style="font-size:42px;letter-spacing:12px;font-family:'Courier New',monospace;color:#0f3d2a;">{reset_code}</h1>
        <p>This code expires in 15 minutes.</p>
    </body></html>
    """
    send_email(user['email'], subject, body_html)
    flash('A 6-digit reset code has been sent to your email. Check your inbox (and spam folder).', 'info')
    return redirect(url_for('show_reset_page'))

@app.route('/reset-password', methods=['GET'])
def show_reset_page():
    return render_template('reset_password.html')

@app.route('/reset-password', methods=['POST'])
def verify_reset_code():
    email = session.get('reset_email', '').strip()
    code = request.form.get('code', '').strip()
    new_password = request.form.get('new_password', '')
    confirm_password = request.form.get('confirm_password', '')

    if not email:
        flash('Session expired. Please enter your email again.', 'danger')
        return redirect(url_for('login'))
    if not code or not new_password or not confirm_password:
        flash('Please fill in all fields.', 'danger')
        return redirect(url_for('show_reset_page'))
    if new_password != confirm_password:
        flash('Passwords do not match.', 'danger')
        return redirect(url_for('show_reset_page'))
    if len(new_password) < 8:
        flash('Password must be at least 8 characters long.', 'danger')
        return redirect(url_for('show_reset_page'))

    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT pr.*, u.email, u.first_name, u.id as uid
        FROM password_resets pr
        JOIN users u ON pr.user_id = u.id
        WHERE u.email = %s AND pr.code = %s AND pr.used = FALSE AND pr.expires_at > NOW()
        ORDER BY pr.created_at DESC
        LIMIT 1
    """, (email, code))
    reset_record = cursor.fetchone()
    if not reset_record:
        conn.close()
        flash('Invalid or expired code. Please try again or request a new code.', 'danger')
        return redirect(url_for('show_reset_page'))

    hashed_password = generate_password_hash(new_password)
    cursor.execute("UPDATE users SET password = %s WHERE id = %s", (hashed_password, reset_record['uid']))
    cursor.execute("UPDATE password_resets SET used = TRUE WHERE id = %s", (reset_record['id'],))
    conn.commit()
    conn.close()
    session.pop('reset_email', None)

    subject = "Password Changed Successfully - Barangay Sto. Nino"
    body_html = f"""
    <html><body style="font-family:Arial,sans-serif;padding:20px;">
        <h2>Password Changed</h2>
        <p>Hello {reset_record['first_name']},</p>
        <p>Your password has been successfully changed.</p>
        <p>Date: {datetime.datetime.now().strftime('%B %d, %Y %I:%M %p')}</p>
        <p style="color:#ef4444;">If you did not make this change, please contact the Barangay Office immediately.</p>
    </body></html>
    """
    send_email(reset_record['email'], subject, body_html)
    flash('Password reset successfully! You can now login with your new password.', 'success')
    return redirect(url_for('login'))

# ============================================================
# MAIN
# ============================================================
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True, use_reloader=False)