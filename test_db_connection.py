import mysql.connector

try:
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='bsit2026@123',
        database='barangay_online_services'
    )
    print("✅ Connected to MySQL successfully!")
    conn.close()
except Exception as e:
    print(f"❌ Connection failed: {e}")