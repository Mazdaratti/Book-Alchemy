from flask import Flask, render_template, request, redirect, url_for, flash
from data import PATH  # Import the database path
from data_models import db, Author, Book
from validation import validate_author_data

# Initialize the Flask application
app = Flask(__name__)

# Configure the database URI
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{PATH}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = "123456"
# Initialize SQLAlchemy
db.init_app(app)


# Create the database tables. Run once
#with app.app_context():
#db.create_all()
#print("Tables created successfully!")


@app.route('/add_author', methods=['GET', 'POST'])
def add_author():
    if request.method == 'POST':
        form_data = request.form.to_dict()  # Capture form data

        # Call validation function
        errors, validated_data = validate_author_data(form_data)

        # If there are errors, flash them and re-render the form
        if errors:
            for error in errors:
                flash(error, "error")
        else:
            # If no errors, proceed to create the new author
            new_author = Author(
                name=validated_data['name'],
                birth_date=validated_data['birth_date'],
                date_of_death=validated_data['date_of_death']
            )
            db.session.add(new_author)
            db.session.commit()
            flash("Author added successfully!", "success")

        # Redirect back to the form
        return redirect(url_for('add_author'))

    # For GET request, just render the form
    return render_template('add_author.html')


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
