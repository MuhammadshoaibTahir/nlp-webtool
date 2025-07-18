from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import os

# Initialize Flask app
app = Flask(__name__)
import secrets
app.secret_key = secrets.token_hex(32)
app.config['DEBUG'] = True

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    account_type = db.Column(db.String(50), default='free')  # 'free', 'student', 'university'

# Create database tables
with app.app_context():
    db.create_all()

# Home route (analysis page)
@app.route('/', methods=['GET', 'POST'])
def index():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user = User.query.get(session['user_id'])

    # 🔥 FIX: handle missing user
    if user is None:
        session.clear()
        flash("Session expired or user not found. Please log in again.", "warning")
        return redirect(url_for('login'))

    if request.method == 'POST':
        text = request.form.get('text', '')
        # Show output to free users without downloads or visuals
        result = f"Analyzed: {text}"
        return render_template('index.html', user=user, output=result, is_paid=(user.account_type != 'free'), text=text)

    return render_template('index.html', user=user, is_paid=(user.account_type != 'free'))

# Register route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            return redirect(url_for('index'))
        else:
            flash('Invalid credentials.', 'danger')
    return render_template('login.html')



@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        hashed_password = generate_password_hash(password)
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Email already registered.', 'warning')
        else:
            new_user = User(email=email, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            session['user_id'] = new_user.id
            return redirect(url_for('index'))
    return render_template('register.html')


# Logout route
@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully.', 'info')
    return redirect(url_for('login'))

# # Pricing route
# @app.route('/pricing')
# def pricing():
#     return render_template('pricing.html')

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

# Run app
if __name__ == '__main__':
    app.run(debug=True)