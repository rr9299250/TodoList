"""
TaskFlow - A Professional To-Do List Web Application
Built with Flask, SQLite, and Bootstrap
"""

from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, date
import os

# ─── App Configuration ───────────────────────────────────────────────────────

app = Flask(__name__)
app.config['SECRET_KEY'] = 'taskflow-secret-key-2024'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///taskflow.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'error'

# ─── Database Models ──────────────────────────────────────────────────────────

class User(UserMixin, db.Model):
    """User model representing application users."""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    tasks = db.relationship('Task', backref='owner', lazy=True, cascade='all, delete-orphan')

class Task(db.Model):
    """Task model representing a single to-do item."""
    __tablename__ = 'tasks'

    id          = db.Column(db.Integer, primary_key=True)
    title       = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    status      = db.Column(db.String(20), default='Pending')        # Pending / Completed
    priority    = db.Column(db.String(10), default='Medium')         # Low / Medium / High
    due_date    = db.Column(db.Date, nullable=True)
    created_at  = db.Column(db.DateTime, default=datetime.utcnow)
    user_id     = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def is_overdue(self):
        """Return True if the task is past its due date and still pending."""
        if self.due_date and self.status == 'Pending':
            return self.due_date < date.today()
        return False

    def due_date_str(self):
        """Return formatted due date string or empty string."""
        return self.due_date.strftime('%Y-%m-%d') if self.due_date else ''

    def __repr__(self):
        return f'<Task {self.id}: {self.title}>'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# ─── Helper ───────────────────────────────────────────────────────────────────

PRIORITY_ORDER = {'High': 0, 'Medium': 1, 'Low': 2}

def get_filtered_tasks(status_filter, search_query):
    """Return tasks filtered by status and search query, sorted by priority."""
    query = Task.query.filter_by(user_id=current_user.id)

    if status_filter == 'Completed':
        query = query.filter_by(status='Completed')
    elif status_filter == 'Pending':
        query = query.filter_by(status='Pending')

    if search_query:
        query = query.filter(Task.title.ilike(f'%{search_query}%'))

    tasks = query.order_by(Task.created_at.desc()).all()
    # Secondary sort: High → Medium → Low
    tasks.sort(key=lambda t: PRIORITY_ORDER.get(t.priority, 1))
    return tasks


# ─── Auth Routes ─────────────────────────────────────────────────────────────

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')

        if not username or not password:
            flash('Username and password are required.', 'error')
            return redirect(url_for('register'))
        
        if password != confirm_password:
            flash('Passwords do not match.', 'error')
            return redirect(url_for('register'))

        user = User.query.filter_by(username=username).first()
        if user:
            flash('Username already exists. Please choose a different one.', 'error')
            return redirect(url_for('register'))

        new_user = User(username=username, password_hash=generate_password_hash(password, method='pbkdf2:sha256'))
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            flash('Logged in successfully.', 'success')
            next_page = request.args.get('next')
            return redirect(next_page or url_for('index'))
        else:
            flash('Login unsuccessful. Please check username and password.', 'error')

    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('login'))

# ─── Task Routes ─────────────────────────────────────────────────────────────

@app.route('/')
@login_required
def index():
    """Home: display all tasks with optional filter and search."""
    status_filter = request.args.get('status', 'All')
    search_query  = request.args.get('search', '').strip()

    tasks = get_filtered_tasks(status_filter, search_query)

    # Summary counts for the dashboard
    total     = Task.query.filter_by(user_id=current_user.id).count()
    completed = Task.query.filter_by(user_id=current_user.id, status='Completed').count()
    pending   = Task.query.filter_by(user_id=current_user.id, status='Pending').count()
    overdue   = sum(1 for t in Task.query.filter_by(user_id=current_user.id, status='Pending').all() if t.is_overdue())

    return render_template(
        'index.html',
        tasks=tasks,
        status_filter=status_filter,
        search_query=search_query,
        total=total,
        completed=completed,
        pending=pending,
        overdue=overdue,
        today=date.today()
    )


@app.route('/add', methods=['GET', 'POST'])
@login_required
def add_task():
    """Add a new task."""
    if request.method == 'POST':
        title       = request.form.get('title', '').strip()
        description = request.form.get('description', '').strip()
        priority    = request.form.get('priority', 'Medium')
        due_date_str = request.form.get('due_date', '')

        # Validation
        if not title:
            flash('Task title is required.', 'error')
            return render_template('add_task.html', form_data=request.form)

        if len(title) > 200:
            flash('Task title must be under 200 characters.', 'error')
            return render_template('add_task.html', form_data=request.form)

        if priority not in ('Low', 'Medium', 'High'):
            flash('Invalid priority value.', 'error')
            return render_template('add_task.html', form_data=request.form)

        due_date = None
        if due_date_str:
            try:
                due_date = datetime.strptime(due_date_str, '%Y-%m-%d').date()
            except ValueError:
                flash('Invalid due date format.', 'error')
                return render_template('add_task.html', form_data=request.form)

        task = Task(
            title=title,
            description=description,
            priority=priority,
            due_date=due_date,
            user_id=current_user.id
        )
        db.session.add(task)
        db.session.commit()
        flash(f'Task "{title}" created successfully!', 'success')
        return redirect(url_for('index'))

    return render_template('add_task.html', form_data={})


@app.route('/update/<int:task_id>', methods=['GET', 'POST'])
@login_required
def update_task(task_id):
    """Edit an existing task."""
    task = Task.query.filter_by(id=task_id, user_id=current_user.id).first_or_404()

    if request.method == 'POST':
        title        = request.form.get('title', '').strip()
        description  = request.form.get('description', '').strip()
        priority     = request.form.get('priority', 'Medium')
        status       = request.form.get('status', 'Pending')
        due_date_str = request.form.get('due_date', '')

        if not title:
            flash('Task title is required.', 'error')
            return render_template('update_task.html', task=task)

        if len(title) > 200:
            flash('Task title must be under 200 characters.', 'error')
            return render_template('update_task.html', task=task)

        if priority not in ('Low', 'Medium', 'High'):
            flash('Invalid priority value.', 'error')
            return render_template('update_task.html', task=task)

        if status not in ('Pending', 'Completed'):
            flash('Invalid status value.', 'error')
            return render_template('update_task.html', task=task)

        due_date = None
        if due_date_str:
            try:
                due_date = datetime.strptime(due_date_str, '%Y-%m-%d').date()
            except ValueError:
                flash('Invalid due date format.', 'error')
                return render_template('update_task.html', task=task)

        task.title       = title
        task.description = description
        task.priority    = priority
        task.status      = status
        task.due_date    = due_date
        db.session.commit()
        flash(f'Task "{title}" updated successfully!', 'success')
        return redirect(url_for('index'))

    return render_template('update_task.html', task=task)


@app.route('/delete/<int:task_id>', methods=['POST'])
@login_required
def delete_task(task_id):
    """Delete a task permanently."""
    task = Task.query.filter_by(id=task_id, user_id=current_user.id).first_or_404()
    title = task.title
    db.session.delete(task)
    db.session.commit()
    flash(f'Task "{title}" deleted.', 'success')
    return redirect(url_for('index'))


@app.route('/toggle/<int:task_id>', methods=['POST'])
@login_required
def toggle_task(task_id):
    """Toggle task status between Pending and Completed (AJAX-friendly)."""
    task = Task.query.filter_by(id=task_id, user_id=current_user.id).first_or_404()
    task.status = 'Completed' if task.status == 'Pending' else 'Pending'
    db.session.commit()
    return jsonify({'status': task.status, 'id': task.id})


@app.route('/users')
@login_required
def users_database():
    """Admin-like view to see all registered users and their stats."""
    all_users = User.query.all()
    users_data = []
    for u in all_users:
        total = Task.query.filter_by(user_id=u.id).count()
        completed = Task.query.filter_by(user_id=u.id, status='Completed').count()
        pending = Task.query.filter_by(user_id=u.id, status='Pending').count()
        users_data.append({
            'user': u,
            'total': total,
            'completed': completed,
            'pending': pending
        })
    return render_template('users.html', users_data=users_data)


# ─── Error Handlers ──────────────────────────────────────────────────────────

@app.errorhandler(404)
def not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500


# ─── Entry Point ─────────────────────────────────────────────────────────────

if __name__ == '__main__':
    with app.app_context():
        db.create_all()          # Create tables if they don't exist
        print("✅  Database ready.")
    app.run(debug=True, port=5000)
