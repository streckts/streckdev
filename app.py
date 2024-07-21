from flask import Flask, render_template, redirect, url_for, session, jsonify, request, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import os
from portfolio_tracker import portfolio_tracker

from models import db, User, Asset, UserAsset

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key'

login_manager = LoginManager(app)
login_manager.login_view = 'login'

db.init_app(app) # initialize db

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route("/")
def home():
    #if 'logged_in' not in session:
    #    return redirect(url_for('login'))  # Assumes you have a 'login' route defined
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        new_user = User(username=username, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash('Your account has been created! You can now log in', 'success')
        return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/logout', methods=['GET','POST'])
def logout():
    if request.method == 'POST':
        logout_user()
        return redirect(url_for('login'))

@app.route('/profile')
def profile():
    return render_template('profile.html')

@app.route("/azure")
def azure():
    return render_template('azure.html')

app.register_blueprint(portfolio_tracker)

if __name__ == "__main__":

    # Initialize database w/ SQLite
    with app.app_context():
        db.create_all()

    # Run site
    app.run(debug=True)
