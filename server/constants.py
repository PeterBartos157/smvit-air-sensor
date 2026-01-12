"""constants.py - Constants used on server-side."""

# Server Config
SERVER_HOST = "0.0.0.0"
SERVER_PORT = 5000
DEBUG = True

# Database Config
DATABASE = "database.db"

# Data Schema
USER = "user"
TIMESTAMP = "timestamp"
TEMPERATURE = "temperature"
HUMIDITY = "humidity"
AQI = "aqi"
CO2 = "co2"
TVOC = "tvoc"

# Placeholder for unreaded values
NULL_PLACEHOLDER = -1000

# Data Schema Validation
REQUIRED_KEYS = [USER, TEMPERATURE, HUMIDITY, AQI, CO2, TVOC]

# Response Schema
STATUS = "status"
ERROR = "error"
DATA = "data"

# Response Status Codes
STATUS_OK = 0
STATUS_ADD = 1
STATUS_BAD = 2
STATUS_ERROR = 3

# Response Status
STATUS_LABEL_OK = "OK"
STATUS_LABEL_ADD = "Success"
STATUS_LABEL_BAD = "Bad request"
STATUS_LABEL_ERROR = "Error"

# Response Codes
STATUS_CODE_OK = 200
STATUS_CODE_ADD = 201
STATUS_CODE_BAD = 400
STATUS_CODE_ERROR = 500

# Resonse Lists
STATUS_RESPONSES = [STATUS_OK, STATUS_ADD, STATUS_BAD, STATUS_ERROR]
STATUS_RESPONSE_CODES = [STATUS_CODE_OK, STATUS_CODE_ADD, STATUS_CODE_BAD, STATUS_CODE_ERROR]
STATUS_RESPONSE_LABELS = [STATUS_LABEL_OK, STATUS_LABEL_ADD, STATUS_LABEL_BAD, STATUS_LABEL_ERROR]

# HTML template
RESPONSE_MATCHER = "__response__"
CSS_RESPONSE_TEMPLATE = """
    body {
        font-family: Arial, sans-serif;
        margin: 40px;
        background-color: #f5f5f5;
    }
    h1 {
        text-align: center;
    }
    .button-container {
        display: flex;
        justify-content: flex-start;
        gap: 10px;
        margin-bottom: 20px;
    }
    button {
        padding: 8px 16px;
        border: none;
        border-radius: 5px;
        background-color: #007BFF;
        color: white;
        cursor: pointer;
    }
    button:hover {
        background-color: #0056b3;
    }
    .chart-container {
        background-color: #fff;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 0 10px rgba(0,0,0,0.1);
        display: grid;
        grid-template-columns: 1fr;  /* default: 1 column */
        gap: 20px;
    }
    /* When screen width >= 1040px, show 2x2 grid */
    @media (min-width: 1040px) {
        .chart-container {
            grid-template-columns: repeat(2, 1fr);
        }
        .chart-container > div {
            height: 400px; /* optional fixed height */
        }
    }
"""
JS_RESPONSE_TEMPLATE = """
    // Automatically refresh the page every 30 seconds
    function autoRefresh() {
        setTimeout(function() {
            window.location.reload();
        }, 60000); // 60 seconds
    }

    // Start auto-refresh when the page loads
    window.onload = autoRefresh;

    // Helper to get query parameter
    function getQueryParam(param) {
        const urlParams = new URLSearchParams(window.location.search);
        return urlParams.get(param);
    }

    // Helper to format date as YYYY-MM-DD
    function formatDate(date) {
        const year = date.getFullYear();
        const month = String(date.getMonth() + 1).padStart(2, '0');
        const day = String(date.getDate()).padStart(2, '0');
        return `${year}-${month}-${day}`;
    }

    function navigateToDate(daysOffset) {
        let dateStr = getQueryParam('date');
        if (!dateStr) {
            dateStr = new Date().toISOString().slice(0, 10); // today if not provided
        }
        const dateObj = new Date(dateStr);
        dateObj.setDate(dateObj.getDate() + daysOffset);
        const newDateStr = formatDate(dateObj);
        const userParam = getQueryParam('user') || '';
        const url = new URL(window.location.href);
        url.searchParams.set('date', newDateStr);
        if (userParam) url.searchParams.set('user', userParam);
        window.location.href = url.toString();
    }
    // Assign it to the buttons
    document.getElementById('prevDayBtn').onclick = function() { navigateToDate(-1); };
    document.getElementById('nextDayBtn').onclick = function() { navigateToDate(1); };
    // Hide nextDayBtn if on current date
    const todayStr = new Date().toISOString().slice(0, 10);
    const currentDate = getQueryParam('date') || todayStr;
    if (currentDate === todayStr) {
        const nextBtn = document.getElementById('nextDayBtn');
        if (nextBtn) nextBtn.style.display = 'none';
    }
"""
HTML_RESPONSE_TEMPLATE = f"""
    <html>
    <head>
        <title>Sensor Data</title>
        <style>{CSS_RESPONSE_TEMPLATE}</style>
    </head>
    <body>
        <div class="button-container">
            <button id="prevDayBtn">Previous Day</button>
            <button id="nextDayBtn">Next Day</button>
        </div>
        <div class="chart-container">
            {RESPONSE_MATCHER}
        </div>
    </body>
    </html>
    <script>{JS_RESPONSE_TEMPLATE}</script>
"""
