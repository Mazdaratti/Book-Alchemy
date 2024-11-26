"""
data_models.py

This module defines the database models for the Library application.
It includes the `Author` and `Book` models, which represent the authors and
books in the library, respectively. These models are linked by a foreign key
relationship to establish a connection between authors and the books they have written.

Classes:
    Author: Represents an author in the library.
    Book: Represents a book in the library.

Attributes:
    db (SQLAlchemy): The SQLAlchemy object used for ORM operations.
"""
from flask_sqlalchemy import SQLAlchemy

# Initialize SQLAlchemy
db = SQLAlchemy()


class Author(db.Model):
    """
        Represents an author in the library.

        Attributes:
            id (int): The primary key, an auto-incrementing unique identifier.
            name (str): The name of the author.
            birth_date (date, optional): The birth date of the author.
            date_of_death (date, optional): The date of death of the author, if applicable.
    """
    __tablename__ = 'authors'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # Primary Key
    name = db.Column(db.String(100), nullable=False)  # Author name
    birth_date = db.Column(db.Date, nullable=True)  # Date of birth
    date_of_death = db.Column(db.Date, nullable=True)  # Date of death

    def __repr__(self):
        """
            Returns a detailed string representation of the Author instance.

            Returns:
                str: A detailed representation of the Author instance.
        """
        return f"<Author(id={self.id}, name={self.name}, birth_date={self.birth_date}, date_of_death={self.date_of_death})>"

    def __str__(self):
        """
            Returns a human-readable string representation of the Author instance.

            Returns:
                str: A human-readable representation of the author's name and lifespan.
        """
        return f"{self.name} (Born: {self.birth_date}, Died: {self.date_of_death})"


class Book(db.Model):
    """
        Represents a book in the library.

        Attributes:
            id (int): The primary key, an auto-incrementing unique identifier.
            isbn (str): The ISBN number of the book (unique and required).
            title (str): The title of the book.
            publication_year (int, optional): The year the book was published.
            author_id (int): Foreign key linking the book to an author.
            author (Author): The relationship to the Author instance who wrote the book.
    """
    __tablename__ = 'books'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # Primary Key
    isbn = db.Column(db.String(13), unique=True, nullable=False)  # ISBN number
    title = db.Column(db.String(150), nullable=False)  # Book title
    publication_year = db.Column(db.Integer, nullable=True)  # Publication year
    author_id = db.Column(db.Integer, db.ForeignKey('authors.id'), nullable=False)  # Foreign Key to Author table

    # Relationship to the Author model
    author = db.relationship('Author', backref='books', lazy=True)

    def __repr__(self):
        """
            Returns a detailed string representation of the Book instance.

            Returns:
                str: A detailed representation of the Book instance.
        """
        return f"<Book(id={self.id}, title={self.title}, isbn={self.isbn}, publication_year={self.publication_year})>"

    def __str__(self):
        """
            Returns a human-readable string representation of the Book instance.

            Returns:
                str: A human-readable representation of the book's title and author.
        """
        return f"'{self.title}' by {self.author.name} (ISBN: {self.isbn})"
