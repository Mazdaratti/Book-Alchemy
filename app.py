from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from data import PATH  # Import the database path

# Initialize the Flask application
app = Flask(__name__)

# Configure the database URI
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{PATH}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy
db = SQLAlchemy(app)


# Testing setup
@app.route('/')
def home():
    return "Flask app is running!"



if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
