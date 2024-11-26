from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from data import PATH  # Import the database path
from data_models import db, Author, Book


# Initialize the Flask application
app = Flask(__name__)

# Configure the database URI
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{PATH}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy
db.init_app(app)


# Testing setup
@app.route('/')
def home():
    return "Library app is connected to the database!"



if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
