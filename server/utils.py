"""utils.py - Utility functions used on server-side."""

from datetime import datetime

from flask import jsonify

from constants import REQUIRED_KEYS, DATA, STATUS, ERROR, HTML_RESPONSE_TEMPLATE, RESPONSE_MATCHER
from constants import STATUS_OK, STATUS_RESPONSES, STATUS_RESPONSE_CODES, STATUS_RESPONSE_LABELS


def validate_received_data_schema(data: dict) -> tuple[bool, str | None]:
    """Validate that the JSON contains all required keys."""
    for key in REQUIRED_KEYS:
        if key not in data:
            return False, key
    return True, None


def fill_json_response(status: int, error: str = None, data: dict = None) -> tuple[dict, int]:
    """Return a JSON response and response code."""
    # Validate the status parameter
    if status not in STATUS_RESPONSES:
        raise ValueError(
            "Invalid status code, must be 0 (OK), 1 (Success), 2 (Bad request), or 3 (Error)."
        )
    # Get status response and response code
    response_code = STATUS_RESPONSE_CODES[status]
    status_response = STATUS_RESPONSE_LABELS[status]
    # Return the response
    return jsonify({STATUS: status_response, ERROR: error, DATA: data}), response_code

def fill_html_response(status: int, html: str = None) -> tuple[dict, int]:
    """Return a JSON response schema."""
    # Validate the status parameter
    if status not in STATUS_RESPONSES:
        raise ValueError(
            "Invalid status code, must be 0 (OK), 1 (Success), 2 (Bad request), or 3 (Error)."
        )
    # If no HTML is provided or status is not OK
    if status != STATUS_OK and html is None:
        html = "<h3>Internal server error.</h3>"
    # Get response code
    response_code = STATUS_RESPONSE_CODES[status]
    # Return the response
    return HTML_RESPONSE_TEMPLATE.replace(RESPONSE_MATCHER, html), response_code


def is_valid_date_format(date_str: str | None) -> bool:
    """Check if a string is a valid date in YYYY-mm-dd format."""
    # If no date is provided, it will fallback to latest date
    if date_str is None:
        return True
    # Try to parse the date
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    # If the date is not in the correct format
    except ValueError:
        return False
