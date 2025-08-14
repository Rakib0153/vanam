import os
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from datetime import datetime, timedelta
from twilio.rest import Client
from dotenv import load_dotenv
import pytz
from flask import make_response
from io import BytesIO
import pandas as pd
from sqlalchemy.orm import joinedload  # For timeline query
# Load environment variables

# In Python shell:
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'your-secret-key-here')

# Database configuration
#app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'postgresql://username:password@localhost/task_manager')
# Neon db
#app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'postgresql://neondb_owner:npg_SDi5EoXCzLW6@ep-winter-frost-a145a81d-pooler.ap-southeast-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'postgresql://neondb_owner:npg_SDi5EoXCzLW6@ep-winter-frost-a145a81d-pooler.ap-southeast-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require')

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)



# Twilio configuration
TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
TWILIO_WHATSAPP_NUMBER = os.getenv('TWILIO_WHATSAPP_NUMBER')
twilio_client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

# Models
class Employee(db.Model):
    __tablename__ = 'employees'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False, unique=True)
    email = db.Column(db.String(100), unique=True)
    position = db.Column(db.String(100))
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())
    tasks = db.relationship('Task', backref='assignee', foreign_keys='Task.assigned_to')
    updates = db.relationship('TaskUpdate', backref='updater', foreign_keys='TaskUpdate.updated_by')
    performance = db.relationship('PerformanceScore', backref='employee_perf', uselist=False)

class TeamLeader(db.Model):
    __tablename__ = 'team_leaders'
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id', ondelete='CASCADE'))
    department = db.Column(db.String(100))
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())
    employee = db.relationship('Employee', backref='leader_info')
    assigned_tasks = db.relationship('Task', backref='assigner', foreign_keys='Task.assigned_by')

class Task(db.Model):
    __tablename__ = 'tasks'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    assigned_to = db.Column(db.Integer, db.ForeignKey('employees.id', ondelete='SET NULL'))
    assigned_by = db.Column(db.Integer, db.ForeignKey('team_leaders.id', ondelete='SET NULL'))
    status = db.Column(db.String(50), default='Pending')
    priority = db.Column(db.String(20), default='Medium')
    deadline = db.Column(db.Date)
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())
    updated_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    updates = db.relationship('TaskUpdate', backref='task', cascade='all, delete-orphan')

class TaskUpdate(db.Model):
    __tablename__ = 'task_updates'
    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.Integer, db.ForeignKey('tasks.id', ondelete='CASCADE'))
    update_text = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(50), nullable=False)
    updated_by = db.Column(db.Integer, db.ForeignKey('employees.id', ondelete='SET NULL'))
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())
    #source = db.Column(db.String(20), default='web')

class PerformanceScore(db.Model):
    __tablename__ = 'performance_scores'
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id', ondelete='CASCADE'))
    task_completion_score = db.Column(db.Integer, default=0)
    timeliness_score = db.Column(db.Integer, default=0)
    quality_score = db.Column(db.Integer, default=0)
    last_updated = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())
    
class TaskReview(db.Model):
    __tablename__ = 'task_reviews'
    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.Integer, db.ForeignKey('tasks.id'))
    rating = db.Column(db.Integer)  # 1-5 scale
    comments = db.Column(db.Text)
    reviewer_id = db.Column(db.Integer, db.ForeignKey('team_leaders.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# Helper functions
def send_whatsapp_notification(to_number, message):
    try:
        message = twilio_client.messages.create(
            body=message,
            from_=f'whatsapp:{TWILIO_WHATSAPP_NUMBER}',
            to=f'whatsapp:{to_number}'
        )
        return True
    except Exception as e:
        print(f"Error sending WhatsApp message: {e}")
        return False
'''
def calculate_performance(employee_id):
    # Calculate performance based on completed tasks and timeliness
    completed_tasks = Task.query.filter_by(assigned_to=employee_id, status='Completed').count()
    total_tasks = Task.query.filter_by(assigned_to=employee_id).count()
    on_time_tasks = Task.query.filter(
        Task.assigned_to == employee_id,
        Task.status == 'Completed',
        Task.deadline >= func.date(Task.updated_at)
    ).count()
    
    completion_score = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
    timeliness_score = (on_time_tasks / completed_tasks * 100) if completed_tasks > 0 else 0
    
    # Quality score could be based on some other metrics or manual input
    quality_score = 80  # Placeholder - you can implement your own logic
    
    performance = PerformanceScore.query.filter_by(employee_id=employee_id).first()
    if not performance:
        performance = PerformanceScore(employee_id=employee_id)
    
    performance.task_completion_score = int(completion_score)
    performance.timeliness_score = int(timeliness_score)
    performance.quality_score = quality_score
    db.session.add(performance)
    db.session.commit()
'''

def calculate_performance(employee_id):
    # Task completion calculation
    completed_tasks = Task.query.filter_by(assigned_to=employee_id, status='Completed').count()
    total_tasks = Task.query.filter_by(assigned_to=employee_id).count()
    
    # Timeliness calculation
    on_time_tasks = Task.query.filter(
        Task.assigned_to == employee_id,
        Task.status == 'Completed',
        Task.deadline >= func.date(Task.updated_at)
    ).count()
    
    # Quality calculation - NEW IMPLEMENTATION
    quality_score = calculate_quality_score(employee_id)
    
    # Calculate percentages
    completion_score = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
    timeliness_score = (on_time_tasks / completed_tasks * 100) if completed_tasks > 0 else 0
    
    # Update performance record
    performance = PerformanceScore.query.filter_by(employee_id=employee_id).first()
    if not performance:
        performance = PerformanceScore(employee_id=employee_id)
    
    performance.task_completion_score = int(completion_score)
    performance.timeliness_score = int(timeliness_score)
    performance.quality_score = quality_score
    db.session.add(performance)
    db.session.commit()

def calculate_quality_score(employee_id):
    """Calculate quality score based on task reviews (1-5 scale converted to 0-100%)"""
    reviews = TaskReview.query.join(Task).filter(
        Task.assigned_to == employee_id,
        TaskReview.rating.isnot(None)
    ).all()
    
    if not reviews:
        return 0  # Or set a default like 80 if you prefer
    
    avg_rating = sum(r.rating for r in reviews) / len(reviews)
    return int((avg_rating / 5) * 100)  # Convert 1-5 to 0-100%



# Routes
@app.route('/')
def home():
    if 'employee_id' not in session:
        return redirect(url_for('login'))
    
    employee = Employee.query.get(session['employee_id'])
    if not employee:
        return redirect(url_for('login'))
    
    is_leader = TeamLeader.query.filter_by(employee_id=employee.id).first() is not None
    
    if is_leader:
        # Get filter parameters from request
        status_filter = request.args.get('status')
        assigned_to_filter = request.args.get('assigned_to')
        priority_filter = request.args.get('priority')
        date_range_filter = request.args.get('date_range')
        
        # Base query
        query = Task.query
        
        # Apply filters
        if status_filter:
            query = query.filter_by(status=status_filter)
        if assigned_to_filter:
            query = query.filter_by(assigned_to=assigned_to_filter)
        if priority_filter:
            query = query.filter_by(priority=priority_filter)
        if date_range_filter:
            today = datetime.now().date()
            if date_range_filter == 'today':
                query = query.filter(db.func.date(Task.created_at) == today)
            elif date_range_filter == 'week':
                start_of_week = today - timedelta(days=today.weekday())
                query = query.filter(db.func.date(Task.created_at) >= start_of_week)
            elif date_range_filter == 'month':
                start_of_month = today.replace(day=1)
                query = query.filter(db.func.date(Task.created_at) >= start_of_month)
        
        # Get assigned_to name for display if filter is active
        assigned_to_name = None
        if assigned_to_filter:
            assigned_employee = Employee.query.get(assigned_to_filter)
            assigned_to_name = assigned_employee.name if assigned_employee else None
        
        team_members = Employee.query.all()
        tasks = query.order_by(Task.deadline).all()
        
        # Count tasks created today
        today_tasks_count = Task.query.filter(
            db.func.date(Task.created_at) == datetime.now().date()
        ).count()
        
        # Check if any filters are active
        active_filters = any([status_filter, assigned_to_filter, priority_filter, date_range_filter])
        
        return render_template('leader_dashboard.html', 
                            employee=employee,
                            team_members=team_members,
                            tasks=tasks,
                            today_tasks_count=today_tasks_count,
                            assigned_to_name=assigned_to_name,
                            active_filters=active_filters,
                            is_leader=True)
   
    
    else:
        # Get today's date
        today = datetime.now().date()
        
        # Get all tasks (existing functionality)
        my_tasks = Task.query.filter_by(assigned_to=employee.id).order_by(Task.deadline).all()
        
        # Filter today's tasks from all tasks (new addition)
        todays_tasks = [task for task in my_tasks 
                       if task.deadline and task.deadline == today]
        
        return render_template('employee_dashboard.html', 
                            employee=employee,
                            tasks=my_tasks,          # Existing parameter
                            todays_tasks=todays_tasks, # New parameter
                            is_leader=False)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Handle login form submission
        email = request.form.get('email')
        phone = request.form.get('phone')
        
        if email:
            employee = Employee.query.filter_by(email=email).first()
        elif phone:
            employee = Employee.query.filter_by(phone=phone).first()
        else:
            flash('Please provide email or phone number', 'error')
            return redirect(url_for('login'))
        
        if employee:
            session['employee_id'] = employee.id
            return redirect(url_for('home'))
        else:
            flash('User not found. Please contact admin.', 'error')
    
    # GET request - show login form
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('employee_id', None)
    return redirect(url_for('login'))
'''
@app.route('/assign_task', methods=['POST'])
def assign_task():
    if 'employee_id' not in session:
        return redirect(url_for('login'))
    
    leader = TeamLeader.query.filter_by(employee_id=session['employee_id']).first()
    if not leader:
        flash('Only team leaders can assign tasks', 'error')
        return redirect(url_for('home'))
    
    title = request.form.get('title')
    description = request.form.get('description')
    employee_id = request.form.get('employee_id')
    priority = request.form.get('priority')
    deadline = request.form.get('deadline')
    
    if not all([title, employee_id, deadline]):
        flash('Please fill all required fields', 'error')
        return redirect(url_for('home'))
    
    try:
        deadline_date = datetime.strptime(deadline, '%Y-%m-%d').date()
    except ValueError:
        flash('Invalid date format', 'error')
        return redirect(url_for('home'))
    
    new_task = Task(
        title=title,
        description=description,
        assigned_to=employee_id,
        assigned_by=leader.id,
        priority=priority,
        deadline=deadline_date
    )
    
    db.session.add(new_task)
    db.session.commit()
    
    # Send WhatsApp notification
    employee = Employee.query.get(employee_id)
    if employee and employee.phone:
        message = f"New Task Assigned:\nTitle: {title}\nDescription: {description}\nDeadline: {deadline}\nPriority: {priority}\n\nPlease update your progress via the task management system."
        send_whatsapp_notification(employee.phone, message)
    
    flash('Task assigned successfully!', 'success')
    return redirect(url_for('home'))
'''


@app.route('/assign_task', methods=['POST'])
def assign_task():
    if 'employee_id' not in session:
        return redirect(url_for('login'))
    
    leader = TeamLeader.query.filter_by(employee_id=session['employee_id']).first()
    if not leader:
        flash('Only team leaders can assign tasks', 'error')
        return redirect(url_for('home'))
    
    title = request.form.get('title')
    description = request.form.get('description')
    employee_id = request.form.get('employee_id')
    priority = request.form.get('priority')
    deadline = request.form.get('deadline')
    
    if not all([title, employee_id, deadline]):
        flash('Please fill all required fields', 'error')
        return redirect(url_for('home'))
    
    try:
        deadline_date = datetime.strptime(deadline, '%Y-%m-%d').date()
        formatted_deadline = deadline_date.strftime('%d %b %Y')  # Format as "05 Aug 2025"
    except ValueError:
        flash('Invalid date format', 'error')
        return redirect(url_for('home'))
    
    new_task = Task(
        title=title,
        description=description,
        assigned_to=employee_id,
        assigned_by=leader.id,
        priority=priority,
        deadline=deadline_date
    )
    
    db.session.add(new_task)
    db.session.commit()
    
    # Send WhatsApp notification
    employee = Employee.query.get(employee_id)
    if employee and employee.phone:
        message = f"""🆕 *New Task Assigned*

🆔 Task ID: {new_task.id}
📌 Title: {title}
📝 Description: {description}
⏰ Deadline: {formatted_deadline}
🔥 Priority: {priority}

💬 To update your progress, reply on WhatsApp using:
update: {new_task.id} in progress [your update]"""
        send_whatsapp_notification(employee.phone, message)
    
    flash('Task assigned successfully!', 'success')
    return redirect(url_for('home'))

@app.route('/update_task/<int:task_id>', methods=['POST'])
def update_task(task_id):
    if 'employee_id' not in session:
        return redirect(url_for('login'))
    
    task = Task.query.get_or_404(task_id)
    if task.assigned_to != session['employee_id']:
        flash('You can only update your own tasks', 'error')
        return redirect(url_for('home'))
    
    update_text = request.form.get('update_text')
    status = request.form.get('status')
    
    if not all([update_text, status]):
        flash('Please fill all required fields', 'error')
        return redirect(url_for('home'))
    
    # Create update record
    new_update = TaskUpdate(
        task_id=task.id,
        update_text=update_text,
        status=status,
        updated_by=session['employee_id']
    )
    
    # Update task status
    task.status = status
    
    db.session.add(new_update)
    db.session.commit()
    
    # Calculate performance if task is completed
    if status == 'Completed':
        calculate_performance(task.assigned_to)
    
    # Notify team leader
    leader = TeamLeader.query.get(task.assigned_by)
    if leader and leader.employee.phone:
        employee = Employee.query.get(session['employee_id'])
        message = f"Task Update:\nTask: {task.title}\nStatus: {status}\nUpdate: {update_text}\nUpdated by: {employee.name}"
        send_whatsapp_notification(leader.employee.phone, message)
    
    flash('Task updated successfully!', 'success')
    return redirect(url_for('home'))

@app.route('/task_details/<int:task_id>')
def task_details(task_id):
    if 'employee_id' not in session:
        return redirect(url_for('login'))
    
    employee = Employee.query.get(session['employee_id'])
    if not employee:
        return redirect(url_for('login'))
    
    task = Task.query.get_or_404(task_id)
    updates = TaskUpdate.query.filter_by(task_id=task_id).order_by(TaskUpdate.created_at.desc()).all()
    
    # Check if current user is team leader
    is_leader = TeamLeader.query.filter_by(employee_id=employee.id).first() is not None
    
    return render_template('task_details.html', 
                         task=task, 
                         updates=updates,
                         employee=employee,
                         is_leader=is_leader)

@app.route('/employee_performance/<int:employee_id>')
def employee_performance(employee_id):
    if 'employee_id' not in session:
        return redirect(url_for('login'))
    
    # Check if current user is team leader
    leader = TeamLeader.query.filter_by(employee_id=session['employee_id']).first()
    if not leader:
        flash('Only team leaders can view performance', 'error')
        return redirect(url_for('home'))
    
    # Force performance recalculation to get fresh data
    calculate_performance(employee_id)
    
    # Get employee and performance data
    employee = Employee.query.get_or_404(employee_id)
    performance = PerformanceScore.query.filter_by(employee_id=employee_id).first()
    
    # Get tasks and review count for the employee
    tasks = Task.query.filter_by(assigned_to=employee_id).all()
    task_reviews_count = TaskReview.query.join(Task).filter(
        Task.assigned_to == employee_id
    ).count()
    
    return render_template('employee_performance.html', 
                         employee=employee,
                         performance=performance,
                         tasks=tasks,
                         task_reviews_count=task_reviews_count)
# API Endpoints
@app.route('/api/tasks', methods=['GET'])
def api_tasks():
    if 'employee_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    employee = Employee.query.get(session['employee_id'])
    if not employee:
        return jsonify({'error': 'User not found'}), 404
    
    tasks = Task.query.filter_by(assigned_to=employee.id).all()
    tasks_data = [{
        'id': task.id,
        'title': task.title,
        'status': task.status,
        'priority': task.priority,
        'deadline': task.deadline.isoformat() if task.deadline else None,
        'created_at': task.created_at.isoformat()
    } for task in tasks]
    
    return jsonify(tasks_data)

@app.route('/api/update_task_status', methods=['POST'])
def api_update_task_status():
    if 'employee_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    data = request.get_json()
    task_id = data.get('task_id')
    status = data.get('status')
    update_text = data.get('update_text', '')
    
    if not all([task_id, status]):
        return jsonify({'error': 'Missing required fields'}), 400
    
    task = Task.query.get(task_id)
    if not task or task.assigned_to != session['employee_id']:
        return jsonify({'error': 'Task not found or unauthorized'}), 404
    
    # Create update record
    new_update = TaskUpdate(
        task_id=task.id,
        update_text=update_text,
        status=status,
        updated_by=session['employee_id']
    )
    
    # Update task status
    task.status = status
    
    db.session.add(new_update)
    db.session.commit()
    
    # Calculate performance if task is completed
    if status == 'Completed':
        calculate_performance(task.assigned_to)
    
    return jsonify({'success': True})

from flask import request
'''
@app.route('/whatsapp_webhook', methods=['POST'])
def whatsapp_webhook():
    # Step 1: Extract message data
    incoming_msg = request.values.get('Body', '').strip().lower()
    sender_phone = request.values.get('From', '').replace('whatsapp:', '')
    
    # Step 2: Find employee
    employee = Employee.query.filter_by(phone=sender_phone).first()
    if not employee:
        return "Employee not registered", 404

    # Step 3: Parse update command
    if incoming_msg.startswith(('update:', 'status:')):
        try:
            # Expected format: "update: [task_id] [status] [details]"
            parts = incoming_msg.split(' ', 3)
            if len(parts) < 4:
                return "Invalid format", 400
                
            _, task_id, status, update_text = parts
            
            # Step 4: Validate status
            valid_statuses = ['pending', 'in progress', 'completed']
            if status not in valid_statuses:
                return f"Status must be: {', '.join(valid_statuses)}", 400
            
            # Step 5: Verify task assignment
            task = Task.query.filter(
                Task.id == int(task_id),
                Task.assigned_to == employee.id
            ).first()
            
            if not task:
                return "Task not found or not assigned to you", 404
            
            # Step 6: Record update
            new_update = TaskUpdate(
                task_id=task.id,
                update_text=update_text,
                status=status.capitalize(),  # Converts to "In Progress"
                updated_by=employee.id,
                source='whatsapp'  # Track update source
            )
            
            # Step 7: Update task status
            task.status = status.capitalize()
            task.updated_at = datetime.utcnow()
            
            db.session.add(new_update)
            db.session.commit()
            
            # Step 8: Send confirmation
            confirmation_msg = f"""✓ Update Recorded
Task: {task.title}
Status: {status}
Update: {update_text}

View: {url_for('task_details', task_id=task.id, _external=True)}"""
            
            send_whatsapp_notification(sender_phone, confirmation_msg)
            return "OK", 200
            
        except Exception as e:
            return f"Error: {str(e)}", 500
    
    # Help message for invalid formats
    help_msg = """To update tasks:
    
Update: [TaskID] [Status] [Details]

Example:
Update: 42 in progress Working on section 3"""
    send_whatsapp_notification(sender_phone, help_msg)
    return "OK", 200
'''


@app.route('/whatsapp_webhook', methods=['POST'])
def whatsapp_webhook():
    try:
        # Step 1: Extract message & sender
        incoming_msg = request.values.get('Body', '').strip().lower()
        sender_phone = request.values.get('From', '').replace('whatsapp:', '')

        # Step 2: Find employee by phone
        employee = Employee.query.filter_by(phone=sender_phone).first()
        if not employee:
            send_whatsapp_notification(sender_phone, "⚠️ Your number is not registered in the system.")
            return "Employee not registered", 404

        # Step 3: Check for valid command
        if incoming_msg.startswith(('update:', 'status:')):
            valid_statuses = ['pending', 'in progress', 'completed']

            # Clean the command prefix
            cleaned_msg = incoming_msg.replace('update:', '').replace('status:', '').strip()

            # Split to get task_id and the rest
            task_id, *rest = cleaned_msg.split(' ', 1)
            if not rest:
                send_whatsapp_notification(sender_phone, "⚠️ Invalid format. Please provide status and update message.")
                return "Invalid format", 400

            remaining_text = rest[0]

            # Match status from the beginning of remaining_text
            matched_status = None
            for status in valid_statuses:
                if remaining_text.startswith(status):
                    matched_status = status
                    update_text = remaining_text[len(status):].strip()
                    break

            if not matched_status:
                send_whatsapp_notification(sender_phone, f"⚠️ Status must be one of: {', '.join(valid_statuses)}.")
                return "Invalid status", 400

            # Step 4: Validate Task ID and assignment
            task = Task.query.filter(
                Task.id == int(task_id),
                Task.assigned_to == employee.id
            ).first()

            if not task:
                send_whatsapp_notification(sender_phone, "⚠️ Task not found or not assigned to you.")
                return "Task not found", 404

            # Step 5: Create task update
            new_update = TaskUpdate(
                task_id=task.id,
                update_text=update_text,
                status=matched_status.capitalize(),
                updated_by=employee.id,
                #source='whatsapp'
            )

            # Step 6: Update task main status
            task.status = matched_status.capitalize()
            task.updated_at = datetime.utcnow()

            db.session.add(new_update)
            db.session.commit()

            # Step 7: Send confirmation back
            confirmation_msg = f"""✅ *Update Recorded*

📌 *Task:* {task.title}
📋 *Status:* {matched_status.title()}
📝 *Update:* {update_text}

🔗 View Task: {url_for('task_details', task_id=task.id, _external=True)}"""

            send_whatsapp_notification(sender_phone, confirmation_msg)
            return "OK", 200

        # Help fallback message if not valid command
        help_msg = """
📝 *To update your task via WhatsApp:*

Type:
update: <task_id> <status> <details>

✅ *Example:*
update: 42 in progress Working on backend API

📌 *Allowed Status Values:* pending, in progress, completed
"""
        send_whatsapp_notification(sender_phone, help_msg)
        return "OK", 200

    except Exception as e:
        # Optional: log error or alert admin
        error_msg = f"❌ Error processing your request:\n{str(e)}"
        send_whatsapp_notification(sender_phone, error_msg)
        return f"Error: {str(e)}", 500


            
            
@app.route('/tasks')
def view_tasks():
    if 'employee_id' not in session:
        return redirect(url_for('login'))
    
    employee = Employee.query.get(session['employee_id'])
    if not employee:
        return redirect(url_for('login'))
    
    is_leader = TeamLeader.query.filter_by(employee_id=employee.id).first() is not None
    
    # Get filter parameters
    status_filter = request.args.get('status')
    priority_filter = request.args.get('priority')
    assigned_to_filter = request.args.get('assigned_to')
    
    # Base query
    query = Task.query
    
    # Apply filters
    if status_filter:
        query = query.filter_by(status=status_filter)
    if priority_filter:
        query = query.filter_by(priority=priority_filter)
    
    if is_leader:
        if assigned_to_filter:
            query = query.filter_by(assigned_to=assigned_to_filter)
        team_members = Employee.query.all()
    else:
        # Employees only see their own tasks
        query = query.filter_by(assigned_to=employee.id)
        team_members = None
    
    tasks = query.order_by(Task.deadline).all()
    
    if is_leader:
        return render_template('leader_dashboard.html',
                            tasks=tasks,
                            team_members=team_members,
                            is_leader=True)
    else:
        return render_template('employee_dashboard.html',
                            tasks=tasks,
                            is_leader=False) 
        
        
@app.route('/download_tasks')
def download_tasks():
    if 'employee_id' not in session:
        return redirect(url_for('login'))
    
    # Verify user is team leader
    leader = TeamLeader.query.filter_by(employee_id=session['employee_id']).first()
    if not leader:
        flash('Only team leaders can download tasks', 'error')
        return redirect(url_for('home'))
    
    # Get the same filters as the dashboard
    status_filter = request.args.get('status')
    assigned_to_filter = request.args.get('assigned_to')
    priority_filter = request.args.get('priority')
    date_range_filter = request.args.get('date_range')
    
    # Apply the same filtering logic as the dashboard
    query = Task.query
    
    if status_filter:
        query = query.filter_by(status=status_filter)
    if assigned_to_filter:
        query = query.filter_by(assigned_to=assigned_to_filter)
    if priority_filter:
        query = query.filter_by(priority=priority_filter)
    if date_range_filter:
        today = datetime.now().date()
        if date_range_filter == 'today':
            query = query.filter(db.func.date(Task.created_at) == today)
        elif date_range_filter == 'week':
            start_of_week = today - timedelta(days=today.weekday())
            query = query.filter(db.func.date(Task.created_at) >= start_of_week)
        elif date_range_filter == 'month':
            start_of_month = today.replace(day=1)
            query = query.filter(db.func.date(Task.created_at) >= start_of_month)
    
    tasks = query.order_by(Task.deadline).all()
    
    # Convert tasks to pandas DataFrame
    task_data = []
    for task in tasks:
        task_data.append({
            'Title': task.title,
            'Description': task.description,
            'Assigned To': task.assignee.name if task.assignee else 'Unassigned',
            'Assigned By': task.assigner.employee.name if task.assigner else 'System',
            'Status': task.status,
            'Priority': task.priority,
            'Deadline': task.deadline.strftime('%Y-%m-%d') if task.deadline else 'N/A',
            'Created At': task.created_at.strftime('%Y-%m-%d %H:%M'),
            'Last Updated': task.updated_at.strftime('%Y-%m-%d %H:%M')
        })
    
    df = pd.DataFrame(task_data)
    
    # Create Excel file in memory
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, sheet_name='Tasks', index=False)
    
    # Auto-adjust columns' width
    for column in df:
        column_width = max(df[column].astype(str).map(len).max(), len(column))
        col_idx = df.columns.get_loc(column)
        writer.sheets['Tasks'].set_column(col_idx, col_idx, column_width)
    
    writer.close()
    output.seek(0)
    
    # Create response
    response = make_response(output.getvalue())
    response.headers['Content-Disposition'] = 'attachment; filename=tasks_export.xlsx'
    response.headers['Content-type'] = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    
    return response



"""
# Help Slip Submission (Employee)
@app.route('/help_slip', methods=['GET', 'POST'])
def help_slip():
    if 'employee_id' not in session:
        return redirect(url_for('login'))
    
    employee = Employee.query.get(session['employee_id'])
    if not employee:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        priority = request.form.get('priority')
        contact_info = request.form.get('contact_info')
        
        new_slip = HelpSlip(
            employee_id=employee.id,
            title=title,
            description=description,
            priority=priority,
            contact_info=contact_info
        )
        
        db.session.add(new_slip)
        db.session.commit()
        
        # Notify team leaders
        leaders = TeamLeader.query.all()
        for leader in leaders:
            if leader.employee.phone:
                message = f"New Help Request:\nTitle: {title}\nFrom: {employee.name}\nPriority: {priority}"
                send_whatsapp_notification(leader.employee.phone, message)
        
        flash('Help slip submitted successfully!', 'success')
        return redirect(url_for('help_slip_status'))
    
    return render_template('help_slip_form.html', employee=employee)

# Help Slip Status (Employee)
@app.route('/help_slip_status')
def help_slip_status():
    if 'employee_id' not in session:
        return redirect(url_for('login'))
    
    employee = Employee.query.get(session['employee_id'])
    if not employee:
        return redirect(url_for('login'))
    
    slips = HelpSlip.query.filter_by(employee_id=employee.id).order_by(HelpSlip.created_at.desc()).all()
    return render_template('help_slip_status.html', slips=slips)

# Help Slip Management (Team Leader)
@app.route('/help_slip_management', methods=['GET', 'POST'])
def help_slip_management():
    if 'employee_id' not in session:
        return redirect(url_for('login'))
    
    leader = TeamLeader.query.filter_by(employee_id=session['employee_id']).first()
    if not leader:
        return redirect(url_for('home'))
    
    # Handle assignment/status update
    if request.method == 'POST':
        slip_id = request.form.get('slip_id')
        status = request.form.get('status')
        assigned_to = request.form.get('assigned_to')
        remarks = request.form.get('remarks')
        
        slip = HelpSlip.query.get(slip_id)
        if slip:
            slip.status = status
            slip.assigned_to = assigned_to if assigned_to else None
            slip.remarks = remarks
            
            if status == 'Resolved':
                slip.resolved_by = session['employee_id']
                slip.resolve_date = db.func.current_timestamp()
                slip.tat_hours = db.func.extract('epoch', slip.resolve_date - slip.created_at) / 3600
            
            db.session.commit()
            
            # Notify employee if assigned or resolved
            if assigned_to or status == 'Resolved':
                employee = Employee.query.get(slip.employee_id)
                if employee and employee.phone:
                    message = f"Help Request Update:\nTitle: {slip.title}\nStatus: {status}"
                    if assigned_to:
                        message += f"\nAssigned To: {Employee.query.get(assigned_to).name}"
                    if remarks:
                        message += f"\nRemarks: {remarks}"
                    send_whatsapp_notification(employee.phone, message)
            
            flash('Help slip updated successfully!', 'success')
    
    # Get filter parameters
    status_filter = request.args.get('status')
    employee_filter = request.args.get('employee_id')
    
    # Base query
    query = HelpSlip.query
    
    # Apply filters
    if status_filter:
        query = query.filter_by(status=status_filter)
    if employee_filter:
        query = query.filter_by(employee_id=employee_filter)
    
    slips = query.order_by(HelpSlip.created_at.desc()).all()
    employees = Employee.query.all()
    
    return render_template('help_slip_management.html', 
                         slips=slips,
                         employees=employees,
                         current_status=status_filter,
                         selected_employee=employee_filter)

# Help Slip Dashboard (Both)
@app.route('/help_dashboard')
def help_dashboard():
    if 'employee_id' not in session:
        return redirect(url_for('login'))
    
    employee = Employee.query.get(session['employee_id'])
    if not employee:
        return redirect(url_for('login'))
    
    is_leader = TeamLeader.query.filter_by(employee_id=employee.id).first() is not None
    
    # Common stats
    total_requests = HelpSlip.query.count()
    pending = HelpSlip.query.filter_by(status='Request Submitted').count()
    in_progress = HelpSlip.query.filter_by(status='In Progress').count()
    done = HelpSlip.query.filter_by(status='Resolved').count()
    
    # Leader-only stats
    resolved_today = 0
    avg_tat = 0
    
    if is_leader:
        resolved_today = HelpSlip.query.filter(
            HelpSlip.status == 'Resolved',
            db.func.date(HelpSlip.resolve_date) == db.func.current_date()
        ).count()
        
        avg_tat = db.session.query(
            db.func.avg(HelpSlip.tat_hours)
        ).filter(
            HelpSlip.status == 'Resolved'
        ).scalar() or 0
    
    return render_template('help_dashboard.html',
                         is_leader=is_leader,
                         total_requests=total_requests,
                         pending=pending,
                         in_progress=in_progress,
                         done=done,
                         resolved_today=resolved_today,
                         avg_tat=round(avg_tat, 2) if avg_tat else 0)

    
    
"""


@app.route('/submit_review/<int:task_id>', methods=['POST'])
def submit_review(task_id):
    if 'employee_id' not in session:
        return redirect(url_for('login'))
    
    # Verify reviewer is team leader
    leader = TeamLeader.query.filter_by(employee_id=session['employee_id']).first()
    if not leader:
        flash('Only team leaders can submit reviews', 'error')
        return redirect(url_for('task_details', task_id=task_id))
    
    task = Task.query.get_or_404(task_id)
    if task.status != 'Completed':
        flash('Can only review completed tasks', 'error')
        return redirect(url_for('task_details', task_id=task_id))
    
    rating = request.form.get('rating')
    comments = request.form.get('comments', '')
    
    if not rating:
        flash('Rating is required', 'error')
        return redirect(url_for('task_details', task_id=task_id))
    
    # Create or update review
    review = TaskReview.query.filter_by(task_id=task_id).first()
    if not review:
        review = TaskReview(
            task_id=task_id,
            reviewer_id=leader.id
        )
    
    review.rating = int(rating)
    review.comments = comments
    db.session.add(review)
    db.session.commit()
    
    # Recalculate performance
    calculate_performance(task.assigned_to)
    
    flash('Review submitted successfully!', 'success')
    return redirect(url_for('task_details', task_id=task_id))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    app.run(debug=True)

