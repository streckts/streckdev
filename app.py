from flask import Flask, render_template, redirect, url_for, session, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash

import os
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

@app.route("/")
def home():
    #if 'logged_in' not in session:
    #    return redirect(url_for('login'))  # Assumes you have a 'login' route defined
    return render_template('index.html')

@app.route('/api/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Handle login attempt
            data = request.get_json()

            user = User.query.filter_by(email=data.get('email')).first()
            if user and check_password_hash(user.password, data.get('password')):
            # Authentication successful
                return jsonify({'message': 'Login successful'}), 200
            else:
            # Authentication failed
                return jsonify({'message': 'Invalid credentials'}), 401
    elif request.method == 'GET':
        # Maybe return a login page or information
        pass

@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    
    # Check if user already exists
    existing_user = User.query.filter((User.username == username) | (User.email == email)).first()
    if existing_user:
        return jsonify({'message': 'User already exists'}), 409

    # Hash the password
    hashed_password = generate_password_hash(password, method='sha256')

    # Create new user object
    new_user = User(username=username, email=email, password=hashed_password)
    
    # Add to the database
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User registered successfully'}), 201

if __name__ == "__main__":

    # Initialize database w/ SQLite
    with app.app_context():
        db.create_all()

    # Run site
    app.run(debug=True)
