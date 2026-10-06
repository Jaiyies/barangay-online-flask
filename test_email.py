from app import app, send_email

with app.app_context():
    result = send_email(
        'barangay.stonino.paranaque@gmail.com',
        'Test Email',
        '<h1>Gumagana!</h1><p>Kung nabasa mo ito, okay ang email setup.</p>'
    )
    print("SUCCESS" if result else "FAILED")