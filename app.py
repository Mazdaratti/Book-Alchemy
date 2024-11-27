from flask import Flask, render_template, request, redirect, url_for, flash
from data import PATH  # Import the database path
from data_models import db, Author, Book
from validation import validate_author_data, validate_book_data

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


@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    if request.method == 'POST':
        form_data = request.form.to_dict()  # Capture form data

        # Call validation function
        errors, validated_data = validate_book_data(form_data)

        # If there are errors, flash them and re-render the form
        if errors:
            for error in errors:
                flash(error, "error")
        else:
            # If no errors, proceed to create the new book
            try:
                # Fetch the selected author from the database by ID
                author_id = validated_data['author_id']
                author = Author.query.get(author_id)

                new_book = Book(
                    title=validated_data['title'],
                    isbn=validated_data['isbn'],
                    publication_year=validated_data['publication_year'],
                    author_id=author.id  # Associate the book with the selected author
                )
                db.session.add(new_book)
                db.session.commit()
                flash("Book added successfully!", "success")
            except Exception as e:
                flash(f"An unexpected error occurred: {str(e)}", "error")

        return redirect(url_for('add_book'))

    # For GET request, just render the form
    authors = Author.query.all()  # Get all authors from the database
    return render_template('add_book.html', authors=authors)


@app.route('/')
@app.route('/home')
def home():
    # Capture query parameter
    sort_by = request.args.get('sort_by', 'title')
    search_query = request.args.get('search_query', '')

    # Base query
    query = Book.query.join(Author)

    # Add search filter if a query exists
    if search_query:
        search_filter = (Book.title.ilike(f"%{search_query}%") |
                         Author.name.ilike(f"%{search_query}%"))
        query = query.filter(search_filter)

    # Add sorting
    if sort_by == 'author':
        query = query.order_by(Author.name)
    else:  # Default sorting is by title
        query = query.order_by(Book.title)

    books = query.all()

    # Flash a message if no books match the search criteria
    if not books and search_query:
        flash("No books match the search criteria.", "warning")

    return render_template('home.html', books=books)


@app.route('/book/<int:book_id>/delete', methods=['POST'])
def delete_book(book_id):
    try:
        # Find the book by ID
        book = Book.query.get(book_id)
        if not book:
            flash("Book not found.", "error")
            return redirect(url_for('home'))

        # Find the author
        author = book.author

        # Delete the book
        db.session.delete(book)
        db.session.commit()

        # Check if the author has any remaining books
        remaining_books = Book.query.filter_by(author_id=author.id).count()
        if remaining_books == 0:
            db.session.delete(author)
            db.session.commit()
            flash(f"Book and its author '{author.name}' have been deleted.", "success")
        else:
            flash("Book has been deleted.", "success")

    except Exception as e:
        db.session.rollback()
        flash(f"An error occurred while deleting the book: {str(e)}", "error")

    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
