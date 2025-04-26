# Hostel Management System

A web-based hostel management system built with Python Flask and MySQL database.

## Features

- User authentication (Admin, Staff, Student)
- Student management
- Room management and allocation
- Payment tracking
- Maintenance request system
- Attendance tracking
- Dashboard with statistics and recent activities

## Requirements

- Python 3.7+
- Flask
- SQLAlchemy
- MySQL (XAMPP)
- Werkzeug

## Installation

1. Clone the repository
2. Install required packages:
   \`\`\`
   pip install -r requirements.txt
   \`\`\`
3. Set up XAMPP and start MySQL service
4. Run the database creation script:
   \`\`\`
   python create_mysql_db.py
   \`\`\`
5. Start the application:
   \`\`\`
   python app.py
   \`\`\`

## User Roles

### Admin (Warden)
- Create and update student details
- Manage room allocations
- Track payments
- View and update maintenance issues
- Mark and update student attendance

### Student
- View personal information
- View room details
- Report maintenance issues
- View attendance records

### Student
![Admin Dashboard](https://github.com/MADHANKUMAR-C/Hostel-Management-System/tree/main/assets/AdminDashboard.png)

![Admin Attendance Panel](https://github.com/MADHANKUMAR-C/Hostel-Management-System/tree/main/assets/AdminAttendancePanel.png)

![Admin Mark Attendance Panel](https://github.com/MADHANKUMAR-C/Hostel-Management-System/tree/main/assets/AdminMarkAttendancePanel.png)

![Maintenance](https://github.com/MADHANKUMAR-C/Hostel-Management-System/tree/main/assets/Maintenance.png)

![Room Panel](https://github.com/MADHANKUMAR-C/Hostel-Management-System/tree/main/assets/RoomPanel.png)

![Student Details](https://github.com/MADHANKUMAR-C/Hostel-Management-System/tree/main/assets/StudentDetails.png)

![Student Dashboard](https://github.com/MADHANKUMAR-C/Hostel-Management-System/tree/main/assets/StudentDashboard.png)

![Student Attendance Panel](https://github.com/MADHANKUMAR-C/Hostel-Management-System/tree/main/assets/StudentAttendancePanel.png)

![Student Maintenance](https://github.com/MADHANKUMAR-C/Hostel-Management-System/tree/main/assets/StudentMaintenance.png)

![DataBase](https://github.com/MADHANKUMAR-C/Hostel-Management-System/tree/main/assets/DataBase.png)

## Default Login Credentials

- Admin: 
  - Username: admin
  - Password: admin123
