"""
    Validation module for form data in the application.

    This module provides validation functions for author and book data. It checks
    for required fields, proper formats, and logical consistency (e.g., birth date
    before death date).
"""
import datetime
from data_models import Author


def validate_author_data(form_data):
    """
    Validates the form data for adding an author.

    Args:
        form_data (dict): A dictionary containing form data with keys:
            - 'name' (str): The name of the author.
            - 'birth_date' (str): The birth date of the author in 'YYYY-MM-DD' format (optional).
            - 'date_of_death' (str): The date of death of the author in 'YYYY-MM-DD' format (optional).

    Returns:
        tuple: A tuple containing:
            - errors (list): A list of error messages. Empty if no errors are found.
            - validated_data (dict): A dictionary with processed data or None if there are errors.
              Keys:
                - 'name' (str): The validated author name.
                - 'birth_date' (datetime.date or None): The validated birth date.
                - 'date_of_death' (datetime.date or None): The validated date of death.
    """
    errors = []
    validated_data = {
        'name': form_data.get('name'),
        'birth_date': form_data.get('birth_date'),
        'date_of_death': form_data.get('date_of_death')
    }

    # Validate the author name
    if not validated_data['name']:
        errors.append("Author name is required.")

    # Validate the birth date
    if validated_data['birth_date'] and validated_data['birth_date'] != '':
        try:
            # Convert string to date
            validated_data['birth_date'] = datetime.datetime.strptime(validated_data['birth_date'],
                                                                      '%Y-%m-%d').date()
            if validated_data['birth_date'] > datetime.date.today():
                errors.append("Birth date cannot be in the future.")
        except ValueError:
            errors.append("Invalid birth date format.")
    else:
        validated_data['birth_date'] = None  # Set to None if no birth date is provided

    # Validate the date of death
    if validated_data['date_of_death'] and validated_data['date_of_death'] != '':
        try:
            # Convert string to date
            validated_data['date_of_death'] = datetime.datetime.strptime(validated_data['date_of_death'],
                                                                         '%Y-%m-%d').date()
            # Ensure date of death is after birth date if both are provided
            if validated_data['birth_date'] and validated_data['date_of_death'] < validated_data['birth_date']:
                errors.append("Date of death must be after birth date.")
        except ValueError:
            errors.append("Invalid date of death format.")
    else:
        validated_data['date_of_death'] = None  # Set to None if no date of death is provided

    return errors, validated_data


def validate_book_data(form_data):
    """
    Validates the form data for adding a book.

    Args:
        form_data (dict): A dictionary containing form data with keys:
            - 'title' (str): The title of the book.
            - 'isbn' (str): The ISBN of the book (13 characters long, required).
            - 'publication_year' (str): The publication year of the book (optional).
            - 'author_id' (str): The ID of the associated author.

    Returns:
        tuple: A tuple containing:
            - errors (list): A list of error messages. Empty if no errors are found.
            - validated_data (dict): A dictionary with processed data or None if there are errors.
              Keys:
                - 'title' (str): The validated book title.
                - 'isbn' (str): The validated ISBN.
                - 'publication_year' (int or None): The validated publication year.
                - 'author_id' (int): The validated author ID.
    """
    errors = []
    validated_data = {
        'title': form_data.get('title'),
        'isbn': form_data.get('isbn'),
        'publication_year': form_data.get('publication_year'),
        'author_id': form_data.get('author_id')
    }

    # Validate the book title
    if not validated_data['title']:
        errors.append("Book title is required.")
    elif len(validated_data['title']) > 255:
        errors.append("Book title must not exceed 255 characters.")

    # Validate the ISBN
    if validated_data['isbn']:
        if len(validated_data['isbn']) != 13 or not validated_data['isbn'].isdigit():
            errors.append("ISBN must be a 13-digit number.")
    else:
        errors.append("ISBN is required.")

    # Validate the publication year
    if validated_data['publication_year']:
        try:
            publication_year = int(validated_data['publication_year'])
            if publication_year > datetime.datetime.now().year:
                errors.append("Publication year cannot be in the future.")
        except ValueError:
            errors.append("Invalid publication year format.")
    else:
        validated_data['publication_year'] = None

    # Validate the author selection
    if not validated_data['author_id']:
        errors.append("Please select an author.")
    else:
        try:
            validated_data['author_id'] = int(validated_data['author_id'])
            if not Author.query.get(validated_data['author_id']):
                errors.append("Selected author does not exist.")
        except (ValueError, TypeError):
            errors.append("Invalid author ID.")

    return errors, validated_data
