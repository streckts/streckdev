from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
# Database configuration
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://username:password@localhost/database_name'
#app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

@app.route("/")
def home():
    return "Hello, World!"

if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Create database tables for our data models
    app.run(host="0.0.0.0", port=8000, debug=True)
