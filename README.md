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

### Screenshots

1. Admin Dashboard
   
![Admin Dashboard](https://github.com/MADHANKUMAR-C/Hostel-Management-System/blob/main/assets/AdminDashboard.png)

2. Admin Attendance Panel
   
![Admin Attendance Panel](https://github.com/MADHANKUMAR-C/Hostel-Management-System/blob/main/assets/AdminAttendancePanel.png)

3. Admin Mark Attendance Panel
   
![Admin Mark Attendance Panel](https://github.com/MADHANKUMAR-C/Hostel-Management-System/blob/main/assets/AdminMarkAttendancePanel.png)

4. Maintenance
  
![Maintenance](https://github.com/MADHANKUMAR-C/Hostel-Management-System/blob/main/assets/Maintenance.png)

5. Room Panel
   
![Room Panel](https://github.com/MADHANKUMAR-C/Hostel-Management-System/blob/main/assets/RoomPanel.png)

6. Student Details
  
![Student Details](https://github.com/MADHANKUMAR-C/Hostel-Management-System/blob/main/assets/StudentDetails.png)

7. Student Dashboard
  
![Student Dashboard](https://github.com/MADHANKUMAR-C/Hostel-Management-System/blob/main/assets/StudentDashboard.png)

8. Student Attendance Panel
  
![Student Attendance Panel](https://github.com/MADHANKUMAR-C/Hostel-Management-System/blob/main/assets/StudentAttendancePanel.png)

9. Student Maintenance Panel
  
![Student Maintenance](https://github.com/MADHANKUMAR-C/Hostel-Management-System/blob/main/assets/StudentMaintenance.png)

10. DataBase
  
![DataBase](https://github.com/MADHANKUMAR-C/Hostel-Management-System/blob/main/assets/DataBase.png)

## Default Login Credentials

- Admin: 
  - Username: admin
  - Password: admin123
