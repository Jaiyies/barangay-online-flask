from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

# Ito yung instance ng database
db = SQLAlchemy()

# ===== USER TABLE =====
class User(UserMixin, db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    contact_number = db.Column(db.String(20))
    address = db.Column(db.String(200))
    role = db.Column(db.String(50), default='user') # 'user', 'head_admin', 'admin_permits', etc.
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Para makuha yung buong pangalan
    @property
    def fullname(self):
        return f"{self.first_name} {self.last_name}"

# ===== DOCUMENT REQUEST TABLE =====
class DocumentRequest(db.Model):
    __tablename__ = 'document_requests'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    document_type = db.Column(db.String(100), nullable=False) # 'clearance', 'indigency', 'proof_residency'
    status = db.Column(db.String(20), default='pending') # 'pending', 'approved', 'rejected', 'processing'
    reference_number = db.Column(db.String(50), unique=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Para makuha yung pangalan ng user na nag-request (para sa admin)
    @property
    def user_fullname(self):
        return f"{self.user.first_name} {self.user.last_name}" if self.user else "Unknown"

# ===== EVENT PERMIT TABLE =====
class EventPermit(db.Model):
    __tablename__ = 'event_permits'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    event_name = db.Column(db.String(200), nullable=False)
    event_date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(20), default='pending') # 'pending', 'approved', 'rejected'
    reference_number = db.Column(db.String(50), unique=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)