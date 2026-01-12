"""main.py - Main entry point for the server."""

from flask import Flask, request

from visualization import plot_data
from database import init_database, write_data, read_data
from utils import (
    validate_received_data_schema, fill_json_response, fill_html_response, is_valid_date_format
)
from constants import (
    SERVER_HOST, SERVER_PORT, DEBUG, STATUS_OK, STATUS_ADD, STATUS_BAD, STATUS_ERROR
)


# --- Init Flask app ----
app = Flask(__name__)


# ---- Routes ----
@app.route('/health', methods=['GET'])
@app.route('/health/', methods=['GET'])
def health_check():
    """Health check endpoint."""
    try:
        # Return health OK
        return fill_json_response(status=STATUS_OK)
    # Handle errors
    except ValueError as error:
        print("Error:", error)
        return fill_json_response(status=STATUS_ERROR, error="Internal server error")


@app.route('/send-data', methods=['POST'])
@app.route('/send-data/', methods=['POST'])
def receive_data():
    """Receive data endpoint."""
    try:
        # If no JSON is provided
        request_json = request.json
        if not request_json:
            return fill_json_response(status=STATUS_OK, error="No JSON provided")
        # Convert JSON to dictionary
        request_dict = dict(request_json)
        # Validate JSON schema
        valid, missing_key = validate_received_data_schema(data=request_dict)
        if not valid:
            return fill_json_response(status=STATUS_BAD, error=f"Missing key: {missing_key}")
        # Save to database
        write_data(data=request_dict)
        # Return success
        return fill_json_response(status=STATUS_ADD, error=None)
    # Handle errors
    except (ValueError, RuntimeError) as error:
        print("Error:", error)
        return fill_json_response(status=STATUS_ERROR, error="Internal server error")


@app.route('/read-data', methods=['GET'])
@app.route('/read-data/', methods=['GET'])
def send_data():
    """Read data endpoint."""
    try:
        # Get user from query
        user = request.args.get("user", None)
        # Validate the user parameter
        if user is None:
            return fill_json_response(status=STATUS_BAD, error="No user provided")
        # Get date from query
        date = request.args.get("date", None)
        # Validate the date format
        if not is_valid_date_format(date):
            return fill_json_response(status=STATUS_BAD, error="Invalid date format")
        # Read data from database
        db_data = read_data(user=user, date=date)
        return fill_json_response(status=STATUS_OK, data=db_data)
    # Handle errors
    except RuntimeError as error:
        print("Error:", error)
        return fill_json_response(status=STATUS_ERROR, error="Internal server error")


@app.route('/visualize-data', methods=['GET'])
@app.route('/visualize-data/', methods=['GET'])
def render_data():
    """Show data endpoint in HTML."""
    try:
        # Get user from query
        user = request.args.get("user", None)
        # Validate the user parameter
        if user is None:
            return fill_html_response(status=STATUS_BAD, html="<h3>No user provided.</h3>")
        # Get date from query
        date = request.args.get("date", None)
        # Validate the date format
        if not is_valid_date_format(date):
            return fill_html_response(status=STATUS_BAD, html="<h3>Invalid date format.</h3>")
        # Read data from database
        db_data = read_data(user=user, date=date)
        if not db_data:
            return fill_html_response(status=STATUS_OK, html="<h3>No data found.</h3>")
        # Get graphs
        graph_html = plot_data(data=db_data)
        # Return success
        return fill_html_response(status=STATUS_OK, html=graph_html)
    # Handle errors
    except (ValueError, RuntimeError) as error:
        print("Error:", error)
        return fill_html_response(status=STATUS_ERROR)


# ---- Main ----
if __name__ == "__main__":
    # Init database
    init_database()
    # Run server
    #app.run(host=SERVER_HOST, port=SERVER_PORT, debug=DEBUG)
