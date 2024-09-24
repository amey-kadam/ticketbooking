from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app.models import User
from app import db
from flask import jsonify
from app.models import Museum

# Define the Blueprint
main_bp = Blueprint('main_bp', __name__)

@main_bp.route('/')
def home():
    if current_user.is_authenticated:
        return redirect(url_for('main_bp.dashboard'))
    return redirect(url_for('main_bp.login'))

@main_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        if current_user.is_admin:
            return redirect(url_for('admin.admin_dashboard'))  # Admin dashboard for admin users
        return redirect(url_for('main_bp.dashboard'))  # Normal dashboard for regular users
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username and password:
            user = User.query.filter_by(username=username).first()
            if user and user.check_password(password):
                login_user(user)
                flash('Login successful!', 'success')
                # Redirect based on whether the user is an admin
                if user.is_admin:
                    return redirect(url_for('admin.admin_dashboard'))
                else:
                    return redirect(url_for('main_bp.dashboard'))
            else:
                flash('Invalid username or password', 'error')
        else:
            flash('Please provide both username and password', 'error')
    
    return render_template('login.html')


@main_bp.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

@main_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main_bp.dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')  # Capture email from the form
        password = request.form.get('password')
        
        # Ensure that all fields are provided
        if username and email and password:
            existing_user = User.query.filter_by(username=username).first()
            existing_email = User.query.filter_by(email=email).first()
            if existing_user is None and existing_email is None:
                new_user = User(username=username, email=email)
                new_user.set_password(password)
                db.session.add(new_user)
                db.session.commit()
                flash('Registration successful! Please log in.', 'success')
                return redirect(url_for('main_bp.login'))
            else:
                flash('Username or email already exists. Please choose a different one.', 'error')
        else:
            flash('Please fill in all fields', 'error')
    
    return render_template('register.html')




@main_bp.route('/book_ticket')
@login_required
def book_ticket():
    return render_template('book_ticket.html')

@main_bp.route('/get_museums', methods=['POST'])
@login_required
def get_museums():
    data = request.json
    state = data.get('state')
    district = data.get('district')
    city = data.get('city')
    
    museums = Museum.query.filter_by(state=state, district=district, city=city).all()
    museum_list = [{"id": museum.id, "name": museum.name} for museum in museums]
    
    return jsonify(museum_list)



@main_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main_bp.login'))



@main_bp.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    if current_user.is_authenticated and current_user.is_admin:
        return redirect(url_for('main_bp.admin_dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username and password:
            user = User.query.filter_by(username=username).first()
            if user and user.check_password(password):
                if user.is_admin:  # Check if the user is an admin
                    login_user(user)
                    flash('Admin login successful!', 'success')
                    return redirect(url_for('main_bp.admin_dashboard'))
                else:
                    flash('Access denied. Admin only.', 'error')
            else:
                flash('Invalid username or password', 'error')
        else:
            flash('Please provide both username and password', 'error')
    
    return render_template('admin_login.html')
