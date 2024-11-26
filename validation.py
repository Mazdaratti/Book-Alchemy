import datetime


def validate_author_data(form_data):
    """
    Validates the form data for adding an author.

    Args:
        form_data (dict): The form data to validate.

    Returns:
        tuple: A tuple containing:
            - A list of error messages (empty list if no errors).
            - A dictionary with processed (validated) data or None if there are errors.
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

    # Validate the birth date (optional field)
    if validated_data['birth_date'] and validated_data['birth_date'] != '':
        try:
            # Convert string to date
            validated_data['birth_date'] = datetime.datetime.strptime(validated_data['birth_date'], '%Y-%m-%d').date()
            if validated_data['birth_date'] > datetime.date.today():
                errors.append("Birth date cannot be in the future.")
        except ValueError:
            errors.append("Invalid birth date format.")
    else:
        validated_data['birth_date'] = None  # Set to None if no birth date is provided

    # Validate the date of death (optional field)
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
