from flask import Flask, render_template, redirect, url_for, session, jsonify, request
from flask_sqlalchemy import SQLAlchemy

import os
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.db')
#app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#db = SQLAlchemy(app)

@app.route("/")
def home():
    #if 'logged_in' not in session:
    #    return redirect(url_for('login'))  # Assumes you have a 'login' route defined
    return render_template('home.html')

@app.route("/projects")
def projects():
    return render_template('projects.html')

if __name__ == "__main__":

    # Initialize database w/ SQLite
    #with app.app_context():
    #    db.create_all()

    # Run site
    app.run(debug=True)
