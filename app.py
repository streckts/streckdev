from flask import Flask, render_template, redirect, url_for, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash

app = Flask(__name__)
# Database configuration (replace with your actual database URI)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://username:password@localhost/database_name'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

@app.route("/")
def home():
    if 'logged_in' not in session:
        return redirect(url_for('login'))  # Assumes you have a 'login' route defined
    return render_template('index.html')

@app.route('/api/login', methods=['POST'])
def login():
    # Dummy data for demonstration
    users = {'user@example.com': 'hashed_password'}

    # Get the data from the request
    data = request.get_json()

    email = data.get('email')
    password = data.get('password')
    
    # Replace the following line with the actual database check
    if email in users and check_password_hash(users[email], password):
        # Authentication successful
        # Create token here if you're using JWT, etc.
        return jsonify({'message': 'Login successful'}), 200
    else:
        # Authentication failed
        return jsonify({'message': 'Invalid credentials'}), 401

if __name__ == "__main__":
    app.run(debug=True)
