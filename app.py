from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import os

# Flask app initialization
app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'your-secret-key')  # Replace with a secure secret

# Database config (SQLite)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    account_type = db.Column(db.String(50), default='free')  # Options: 'free', 'student', 'university'

# Create DB tables
with app.app_context():
    db.create_all()

# Home route
@app.route('/', methods=['GET', 'POST'])
def index():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user = User.query.get(session['user_id'])

    if request.method == 'POST':
        text = request.form['text']
        if user.account_type == 'free':
            flash('This feature is available for paid users only. Please upgrade your account.', 'danger')
            return redirect(url_for('pricing'))

        # Simulated NLP analysis result (replace this with your logic)
        result = f"Analyzed: {text}"
        return render_template('index.html', result=result, user=user)

    return render_template('index.html', user=user)

# Registration route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        if not email or not password:
            flash('Please fill out all fields.', 'warning')
            return redirect(url_for('register'))

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Email already registered. Please login.', 'warning')
            return redirect(url_for('login'))

        hashed_password = generate_password_hash(password, method='sha256')
        new_user = User(email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful. Please login.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            flash('Login successful!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid email or password.', 'danger')

    return render_template('login.html')

# Logout route
@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully.', 'info')
    return redirect(url_for('login'))

# Pricing route
@app.route('/pricing')
def pricing():
    return render_template('pricing.html')

# Upgrade route
@app.route('/upgrade/<tier>')
def upgrade(tier):
    if 'user_id' not in session:
        flash('Please login first.', 'warning')
        return redirect(url_for('login'))

    user = User.query.get(session['user_id'])

    if tier in ['student', 'university']:
        user.account_type = tier
        db.session.commit()
        flash(f'Upgraded to {tier.title()} plan.', 'success')
    else:
        flash('Invalid upgrade option.', 'danger')

    return redirect(url_for('index'))

# Run the app
if __name__ == '__main__':
    app.run(debug=True)