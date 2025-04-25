from flask import Flask, render_template, request, redirect, url_for, flash, session
import os
from datetime import datetime
from models import db, User, Student, Room, Payment, Maintenance, Attendance

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'hostel_management_secret_key'
# Change SQLite to MySQL with XAMPP
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:@localhost/hostel_management'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database with app
db.init_app(app)

# Create database tables
with app.app_context():
    db.create_all()
    
    # Create admin user if not exists
    admin = User.query.filter_by(username='admin').first()
    if not admin:
        admin = User(username='admin', email='admin@hostel.com', role='admin')
        admin.set_password('admin123')
        db.session.add(admin)
        db.session.commit()
        print("Admin user created!")

# Import routes
from routes import *

# Run the application
if __name__ == '__main__':
    app.run(debug=True)

print("Hostel Management System initialized with MySQL database.")
