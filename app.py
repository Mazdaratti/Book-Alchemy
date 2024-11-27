"""
Flask application for managing books and authors.

This application allows users to perform CRUD operations on books and authors
and provides a simple interface for searching and sorting book data.

Modules:
    - data: Contains database configuration.
    - data_models: Defines the ORM models for authors and books.
    - validation: Handles data validation for forms.

Routes:
    - /add_author: Add a new author.
    - /add_book: Add a new book.
    - /home or /: View books with sorting and searching functionality.
    - /book/<int:book_id>/delete: Delete a book (and its author if no other books exist).
"""

from flask import Flask, render_template, request, redirect, url_for, flash
from data import PATH  # Import the database path
from data_models import db, Author, Book
from validation import validate_author_data, validate_book_data
import os

# Initialize the Flask application
app = Flask(__name__)

# Configure the database URI
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{PATH}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'default_secret_key'

# Initialize SQLAlchemy
db.init_app(app)


@app.route('/add_author', methods=['GET', 'POST'])
def add_author():
    """
    Handle adding a new author.

    GET: Render the add_author form.
    POST: Validate form data, create a new author if valid, and handle errors.

    Returns:
        A rendered template or redirect.
    """
    if request.method == 'POST':
        form_data = request.form.to_dict()

        # Validate author data
        errors, validated_data = validate_author_data(form_data)

        if errors:
            for error in errors:
                flash(error, "error")
        else:
            new_author = Author(
                name=validated_data['name'],
                birth_date=validated_data['birth_date'],
                date_of_death=validated_data['date_of_death']
            )
            try:
                db.session.add(new_author)
                db.session.commit()
                flash("Author added successfully!", "success")
            except Exception as e:
                db.session.rollback()
                flash(f"Error adding author: {str(e)}", "error")

        return redirect(url_for('add_author'))

    return render_template('add_author.html')


@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    """
    Handle adding a new book.

    GET: Render the add_book form with a list of authors.
    POST: Validate form data, create a new book if valid, and handle errors.

    Returns:
        A rendered template or redirect.
    """
    if request.method == 'POST':
        form_data = request.form.to_dict()

        # Validate book data
        errors, validated_data = validate_book_data(form_data)

        if errors:
            for error in errors:
                flash(error, "error")
        else:
            try:
                author = Author.query.get(validated_data['author_id'])
                if not author:
                    flash("Selected author does not exist.", "error")
                else:
                    new_book = Book(
                        title=validated_data['title'],
                        isbn=validated_data['isbn'],
                        publication_year=validated_data['publication_year'],
                        author_id=author.id
                    )
                    db.session.add(new_book)
                    db.session.commit()
                    flash("Book added successfully!", "success")
            except Exception as e:
                db.session.rollback()
                flash(f"Error adding book: {str(e)}", "error")

        return redirect(url_for('add_book'))

    authors = Author.query.all()
    return render_template('add_book.html', authors=authors)


@app.route('/')
@app.route('/home')
def home():
    """
    Display a list of books with sorting and search functionality.

    Query Parameters:
        - sort_by: Field to sort by (default is 'title').
        - search_query: Search term for books and authors.

    Returns:
        A rendered template.
    """
    sort_by = request.args.get('sort_by', 'title')
    search_query = request.args.get('search_query', '')

    query = Book.query.join(Author)

    if search_query:
        search_filter = (Book.title.ilike(f"%{search_query}%") |
                         Author.name.ilike(f"%{search_query}%"))
        query = query.filter(search_filter)

    if sort_by == 'author':
        query = query.order_by(Author.name)
    else:
        query = query.order_by(Book.title)

    books = query.all()

    if not books and search_query:
        flash("No books match the search criteria.", "warning")

    return render_template('home.html', books=books)


@app.route('/book/<int:book_id>/delete', methods=['POST'])
def delete_book(book_id):
    """
    Delete a book and its author if no other books are associated with them.

    Args:
        book_id (int): The ID of the book to delete.

    Returns:
        A redirect to the home route.
    """
    try:
        book = Book.query.get(book_id)
        if not book:
            flash("Book not found.", "error")
            return redirect(url_for('home'))

        author = book.author
        db.session.delete(book)
        db.session.commit()

        remaining_books = Book.query.filter_by(author_id=author.id).count()
        if remaining_books == 0:
            db.session.delete(author)
            db.session.commit()
            flash(f"Book and its author '{author.name}' have been deleted.", "success")
        else:
            flash("Book has been deleted.", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"Error deleting book: {str(e)}", "error")

    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
