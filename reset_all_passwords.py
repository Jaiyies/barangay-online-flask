import mysql.connector
from werkzeug.security import generate_password_hash

def reset_all_passwords():
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='bsit2026@123',
        database='barangay_online_services'
    )
    cursor = conn.cursor()
    
    # Reset password for admin@barangay.com
    admin_password = generate_password_hash('admin123')
    cursor.execute("UPDATE users SET password = %s WHERE email = %s", 
                   (admin_password, 'admin@barangay.com'))
    
    # Reset password for headadmin@barangay.com
    head_password = generate_password_hash('admin123')
    cursor.execute("UPDATE users SET password = %s WHERE email = %s", 
                   (head_password, 'headadmin@barangay.com'))
    
    conn.commit()
    
    print("✅ Passwords reset successfully!")
    print("🔑 admin@barangay.com / admin123")
    print("🔑 headadmin@barangay.com / admin123")
    
    # Verify the updates
    cursor.execute("SELECT id, email, role FROM users WHERE email IN ('admin@barangay.com', 'headadmin@barangay.com')")
    users = cursor.fetchall()
    for user in users:
        print(f"✅ {user[1]} - Role: {user[2]}")
    
    conn.close()

if __name__ == "__main__":
    reset_all_passwords()