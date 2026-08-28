import mysql.connector

try:
    conn = mysql.connector.connect(
        host='localhost',
        port=3306,
        user='root',
        password='bsit2026@123',  # ✅ TAMA YAN! Yan ang root password mo!
        database='barangay_online_services'
    )
    print("✅ Connected to MySQL successfully!")
    conn.close()
except Exception as e:
    print(f"❌ Error: {e}")