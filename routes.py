from app import app, db
from models import User, Student, Room, Payment, Maintenance, Attendance
from flask import render_template, request, redirect, url_for, flash, session, jsonify
from datetime import datetime, date, timedelta
from sqlalchemy import desc
import json

# Add this function to get attendance statistics for charts
def get_attendance_stats():
    # Get all students
    students = Student.query.all()
    student_count = len(students)
    
    # Get today's date
    today = date.today()
    
    # Get attendance records for today
    today_records = Attendance.query.filter_by(date=today).all()
    
    # Count by status
    present_count = sum(1 for record in today_records if record.status == 'present')
    absent_count = sum(1 for record in today_records if record.status == 'absent')
    late_count = sum(1 for record in today_records if record.status == 'late')
    not_marked = student_count - (present_count + absent_count + late_count)
    
    # Get weekly attendance data
    week_start = today - timedelta(days=today.weekday())
    week_end = week_start + timedelta(days=6)
    
    weekly_data = {
        'days': [],
        'present': [],
        'absent': [],
        'late': []
    }
    
    for i in range(7):
        current_date = week_start + timedelta(days=i)
        weekly_data['days'].append(current_date.strftime('%a'))
        
        day_records = Attendance.query.filter_by(date=current_date).all()
        weekly_data['present'].append(sum(1 for record in day_records if record.status == 'present'))
        weekly_data['absent'].append(sum(1 for record in day_records if record.status == 'absent'))
        weekly_data['late'].append(sum(1 for record in day_records if record.status == 'late'))
    
    return {
        'today': {
            'present': present_count,
            'absent': absent_count,
            'late': late_count,
            'not_marked': not_marked
        },
        'weekly': weekly_data
    }

# Login and authentication routes
@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            session['user_id'] = user.id
            session['username'] = user.username
            session['role'] = user.role
            
            flash(f'Welcome back, {user.username}!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password', 'danger')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out', 'info')
    return redirect(url_for('login'))

# Dashboard route
@app.route('/')
def index():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    # Initialize variables
    students_count = 0
    available_rooms = 0
    pending_payments = 0
    maintenance_issues = 0
    recent_payments = []
    recent_issues = []
    student = None
    student_payments = []
    student_attendance = []
    
    # Admin/Staff dashboard data
    if session['role'] in ['admin', 'staff']:
        students_count = Student.query.count()
        available_rooms = Room.query.filter_by(status='available').count()
        pending_payments = Payment.query.filter_by(payment_status='pending').count()
        maintenance_issues = Maintenance.query.filter_by(status='pending').count()
        
        recent_payments = Payment.query.order_by(Payment.payment_date.desc()).limit(5).all()
        recent_issues = Maintenance.query.order_by(Maintenance.reported_date.desc()).limit(5).all()
    
    # Student dashboard data
    else:
        student = Student.query.filter_by(user_id=session['user_id']).first()
        if student:
            student_payments = Payment.query.filter_by(student_id=student.id).order_by(Payment.payment_date.desc()).all()
            student_attendance = Attendance.query.filter_by(student_id=student.id).order_by(Attendance.date.desc()).limit(10).all()
    
    return render_template('index.html', 
                          students_count=students_count,
                          available_rooms=available_rooms,
                          pending_payments=pending_payments,
                          maintenance_issues=maintenance_issues,
                          recent_payments=recent_payments,
                          recent_issues=recent_issues,
                          student=student,
                          student_payments=student_payments,
                          student_attendance=student_attendance)

# Student Management
@app.route('/students')
def students():
    if 'user_id' not in session or session['role'] not in ['admin', 'staff']:
        flash('Unauthorized access', 'danger')
        return redirect(url_for('index'))
    
    students = Student.query.all()
    return render_template('students.html', students=students)

@app.route('/students/add', methods=['GET', 'POST'])
def add_student():
    if 'user_id' not in session or session['role'] not in ['admin', 'staff']:
        flash('Unauthorized access', 'danger')
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        # Create user account
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        
        # Check if username or email already exists
        if User.query.filter_by(username=username).first():
            flash('Username already exists', 'danger')
            return redirect(url_for('add_student'))
        
        if User.query.filter_by(email=email).first():
            flash('Email already exists', 'danger')
            return redirect(url_for('add_student'))
        
        user = User(username=username, email=email, role='student')
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        
        # Create student profile
        student = Student(
            user_id=user.id,
            first_name=request.form.get('first_name'),
            last_name=request.form.get('last_name'),
            gender=request.form.get('gender'),
            contact_number=request.form.get('contact_number'),
            address=request.form.get('address'),
            emergency_contact=request.form.get('emergency_contact')
        )
        
        db.session.add(student)
        db.session.commit()
        
        flash('Student added successfully', 'success')
        return redirect(url_for('students'))
    
    return render_template('add_student.html')

@app.route('/students/edit/<int:student_id>', methods=['GET', 'POST'])
def edit_student(student_id):
    if 'user_id' not in session or session['role'] not in ['admin', 'staff']:
        flash('Unauthorized access', 'danger')
        return redirect(url_for('index'))
    
    student = Student.query.get_or_404(student_id)
    user = User.query.get_or_404(student.user_id)
    
    if request.method == 'POST':
        # Update user information
        user.email = request.form.get('email')
        
        # Update student information
        student.first_name = request.form.get('first_name')
        student.last_name = request.form.get('last_name')
        student.gender = request.form.get('gender')
        student.contact_number = request.form.get('contact_number')
        student.address = request.form.get('address')
        student.emergency_contact = request.form.get('emergency_contact')
        
        db.session.commit()
        
        flash('Student information updated successfully', 'success')
        return redirect(url_for('students'))
    
    return render_template('edit_student.html', student=student, user=user)

# Room Management
@app.route('/rooms')
def rooms():
    if 'user_id' not in session or session['role'] not in ['admin', 'staff']:
        flash('Unauthorized access', 'danger')
        return redirect(url_for('index'))
    
    rooms = Room.query.all()
    return render_template('rooms.html', rooms=rooms)

@app.route('/rooms/add', methods=['GET', 'POST'])
def add_room():
    if 'user_id' not in session or session['role'] not in ['admin', 'staff']:
        flash('Unauthorized access', 'danger')
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        room = Room(
            room_number=request.form.get('room_number'),
            room_type=request.form.get('room_type'),
            capacity=request.form.get('capacity'),
            price=request.form.get('price'),
            status=request.form.get('status')
        )
        
        db.session.add(room)
        db.session.commit()
        
        flash('Room added successfully', 'success')
        return redirect(url_for('rooms'))
    
    return render_template('add_room.html')

# Room Allocation
@app.route('/allocate/<int:student_id>', methods=['GET', 'POST'])
def allocate_room(student_id):
    if 'user_id' not in session or session['role'] not in ['admin', 'staff']:
        flash('Unauthorized access', 'danger')
        return redirect(url_for('index'))
    
    student = Student.query.get_or_404(student_id)
    
    if request.method == 'POST':
        room_id = request.form.get('room_id')
        room = Room.query.get_or_404(room_id)
        
        # Check if room is available
        if room.status != 'available':
            flash('Room is not available', 'danger')
            return redirect(url_for('allocate_room', student_id=student_id))
        
        # Count current occupants
        current_occupants = Student.query.filter_by(room_id=room_id).count()
        
        if current_occupants >= room.capacity:
            flash('Room is already at full capacity', 'danger')
            return redirect(url_for('allocate_room', student_id=student_id))
        
        # Allocate room to student
        student.room_id = room_id
        
        # Update room status if it's now full
        if current_occupants + 1 >= room.capacity:
            room.status = 'occupied'
        
        db.session.commit()
        
        flash('Room allocated successfully', 'success')
        return redirect(url_for('students'))
    
    available_rooms = Room.query.filter_by(status='available').all()
    return render_template('allocate_room.html', student=student, rooms=available_rooms)

# Payment Management
@app.route('/payments')
def payments():
    if 'user_id' not in session or session['role'] not in ['admin', 'staff']:
        flash('Unauthorized access', 'danger')
        return redirect(url_for('index'))
    
    payments = Payment.query.order_by(Payment.payment_date.desc()).all()
    return render_template('payments.html', payments=payments)

@app.route('/payments/add', methods=['GET', 'POST'])
def add_payment():
    if 'user_id' not in session or session['role'] not in ['admin', 'staff']:
        flash('Unauthorized access', 'danger')
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        payment = Payment(
            student_id=request.form.get('student_id'),
            amount=request.form.get('amount'),
            payment_method=request.form.get('payment_method'),
            payment_status=request.form.get('payment_status'),
            description=request.form.get('description')
        )
        
        db.session.add(payment)
        db.session.commit()
        
        flash('Payment recorded successfully', 'success')
        return redirect(url_for('payments'))
    
    students = Student.query.all()
    return render_template('add_payment.html', students=students)

# Maintenance Management
@app.route('/maintenance')
def maintenance():
    if 'user_id' not in session:
        flash('Please login to continue', 'danger')
        return redirect(url_for('login'))
    
    if session['role'] in ['admin', 'staff']:
        issues = Maintenance.query.order_by(Maintenance.reported_date.desc()).all()
    else:
        student = Student.query.filter_by(user_id=session['user_id']).first()
        if student and student.room_id:
            issues = Maintenance.query.filter_by(room_id=student.room_id).order_by(Maintenance.reported_date.desc()).all()
        else:
            issues = []
    
    return render_template('maintenance.html', issues=issues)

@app.route('/maintenance/report', methods=['GET', 'POST'])
def report_issue():
    if 'user_id' not in session:
        flash('Please login to continue', 'danger')
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        room_id = request.form.get('room_id')
        issue = request.form.get('issue')
        
        maintenance = Maintenance(
            room_id=room_id,
            reported_by=session['user_id'],
            issue=issue,
            status='pending'
        )
        
        db.session.add(maintenance)
        db.session.commit()
        
        flash('Maintenance issue reported successfully', 'success')
        return redirect(url_for('maintenance'))
    
    if session['role'] in ['admin', 'staff']:
        rooms = Room.query.all()
    else:
        student = Student.query.filter_by(user_id=session['user_id']).first()
        if student and student.room_id:
            rooms = [student.room]
        else:
            flash('You are not assigned to any room', 'danger')
            return redirect(url_for('index'))
    
    return render_template('report_issue.html', rooms=rooms)

@app.route('/maintenance/update/<int:issue_id>', methods=['POST'])
def update_issue(issue_id):
    if 'user_id' not in session or session['role'] not in ['admin', 'staff']:
        flash('Unauthorized access', 'danger')
        return redirect(url_for('index'))
    
    issue = Maintenance.query.get_or_404(issue_id)
    status = request.form.get('status')
    
    issue.status = status
    if status == 'completed':
        issue.resolved_date = datetime.utcnow()
    
    db.session.commit()
    
    flash('Maintenance issue updated successfully', 'success')
    return redirect(url_for('maintenance'))

# Attendance Management
@app.route('/attendance')
def attendance():
    if 'user_id' not in session:
        flash('Please login to continue', 'danger')
        return redirect(url_for('login'))
    
    if session['role'] in ['admin', 'staff']:
        # For admin/staff, show all students with their latest attendance
        students = Student.query.all()
        today = date.today()
        
        # Get today's attendance records
        today_attendance = Attendance.query.filter_by(date=today).all()
        attendance_dict = {record.student_id: record for record in today_attendance}
        
        # Get attendance statistics
        attendance_stats = get_attendance_stats()
        
        return render_template('attendance.html', 
                              students=students, 
                              attendance_dict=attendance_dict, 
                              today=today,
                              attendance_stats=attendance_stats)
    else:
        # For students, show their own attendance history
        student = Student.query.filter_by(user_id=session['user_id']).first()
        if student:
            attendance_records = Attendance.query.filter_by(student_id=student.id).order_by(Attendance.date.desc()).all()
            return render_template('student_attendance.html', student=student, attendance_records=attendance_records)
        else:
            flash('Student profile not found', 'danger')
            return redirect(url_for('index'))

@app.route('/attendance/mark', methods=['POST'])
def mark_attendance():
    if 'user_id' not in session or session['role'] not in ['admin', 'staff']:
        flash('Unauthorized access', 'danger')
        return redirect(url_for('index'))
    
    student_id = request.form.get('student_id')
    attendance_date = datetime.strptime(request.form.get('date'), '%Y-%m-%d').date()
    status = request.form.get('status')
    remarks = request.form.get('remarks', '')
    
    # Check if attendance already exists for this student on this date
    existing_attendance = Attendance.query.filter_by(student_id=student_id, date=attendance_date).first()
    
    if existing_attendance:
        # Update existing attendance
        existing_attendance.status = status
        existing_attendance.remarks = remarks
        existing_attendance.marked_by = session['user_id']
        flash('Attendance updated successfully', 'success')
    else:
        # Create new attendance record
        attendance = Attendance(
            student_id=student_id,
            date=attendance_date,
            status=status,
            remarks=remarks,
            marked_by=session['user_id']
        )
        db.session.add(attendance)
        flash('Attendance marked successfully', 'success')
    
    db.session.commit()
    return redirect(url_for('attendance'))

@app.route('/attendance/bulk', methods=['GET', 'POST'])
def bulk_attendance():
    if 'user_id' not in session or session['role'] not in ['admin', 'staff']:
        flash('Unauthorized access', 'danger')
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        attendance_date = datetime.strptime(request.form.get('date'), '%Y-%m-%d').date()
        
        # Get all student IDs from the form
        for key, value in request.form.items():
            if key.startswith('student_'):
                student_id = key.split('_')[1]
                status = value
                remarks = request.form.get(f'remarks_{student_id}', '')
                
                # Check if attendance already exists
                existing_attendance = Attendance.query.filter_by(student_id=student_id, date=attendance_date).first()
                
                if existing_attendance:
                    # Update existing attendance
                    existing_attendance.status = status
                    existing_attendance.remarks = remarks
                    existing_attendance.marked_by = session['user_id']
                else:
                    # Create new attendance record
                    attendance = Attendance(
                        student_id=student_id,
                        date=attendance_date,
                        status=status,
                        remarks=remarks,
                        marked_by=session['user_id']
                    )
                    db.session.add(attendance)
        
        db.session.commit()
        flash('Bulk attendance marked successfully', 'success')
        return redirect(url_for('attendance'))
    
    students = Student.query.all()
    return render_template('bulk_attendance.html', students=students, today=date.today())

@app.route('/student/view_attendance')
def view_student_attendance():
    if 'user_id' not in session:
        flash('Please login to continue', 'danger')
        return redirect(url_for('login'))
    
    student = Student.query.filter_by(user_id=session['user_id']).first()
    if not student:
        flash('Student profile not found', 'danger')
        return redirect(url_for('index'))
    
    attendance_records = Attendance.query.filter_by(student_id=student.id).order_by(Attendance.date.desc()).all()
    
    # Calculate attendance statistics
    total_records = len(attendance_records)
    present_count = sum(1 for record in attendance_records if record.status == 'present')
    absent_count = sum(1 for record in attendance_records if record.status == 'absent')
    late_count = sum(1 for record in attendance_records if record.status == 'late')
    
    attendance_percentage = (present_count / total_records * 100) if total_records > 0 else 0
    
    return render_template('view_attendance.html', 
                          student=student, 
                          attendance_records=attendance_records,
                          present_count=present_count,
                          absent_count=absent_count,
                          late_count=late_count,
                          attendance_percentage=attendance_percentage)

# API endpoint for attendance statistics
@app.route('/api/attendance/stats')
def attendance_stats_api():
    if 'user_id' not in session or session['role'] not in ['admin', 'staff']:
        return jsonify({'error': 'Unauthorized access'}), 403
    
    stats = get_attendance_stats()
    return jsonify(stats)

print("Routes for the Hostel Management System have been defined.")
