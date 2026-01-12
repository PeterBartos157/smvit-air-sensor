"""database.py - Database operations."""

import sys
import time
import random
from datetime import datetime
from typing import List, Dict

import sqlite3

from constants import DATABASE, NULL_PLACEHOLDER, USER, TEMPERATURE, HUMIDITY, AQI, CO2, TVOC


def init_database() -> None:
    """
    Initialize the database by creating the sensor_realtime table if it does not already exist.

    The sensor_realtime table contains the following columns:

        id (INTEGER PRIMARY KEY AUTOINCREMENT): Unique identifier for each record.
        user (TEXT NOT NULL): User ID.
        temperature (REAL NOT NULL): Temperature in degrees Celsius.
        humidity (REAL NOT NULL): Humidity in percentage.
        co2 (REAL NOT NULL): CO2 in ppm.
        tvoc (REAL NOT NULL): TVOC in mg/m³ or ppm equivalent.
        timestamp (DATETIME DEFAULT CURRENT_TIMESTAMP): Timestamp of the record.

    This function will create the table if it does not already exist.
    """
    # Connect to the database
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    # Create the sensor_realtime table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sensor_realtime (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user TEXT NOT NULL,
            temperature REAL NOT NULL,
            humidity REAL NOT NULL,
            aqi INTEGER NOT NULL,
            co2 INTEGER NOT NULL,
            tvoc INTEGER NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    # Close the connection
    conn.close()


def seed_database(num_records: int = 10, randomize_user: bool = False) -> None:
    """
    Generate and insert a number of fake sensor records into the database.

    Args:
        write_fn (callable): Function that writes a dict to the database (e.g., write_data).
        num_records (int): Number of fake records to generate and insert.
    """
    print(f"Seeding database with {num_records} fake records...")
    # Getting the samples
    samples = generate_data(num_records, randomize_user)
    # Inserting the samples to database
    for i, record in enumerate(samples, start=1):
        try:
            write_data(record)
            print(f"[{i}/{num_records}] Inserted: {record}")
        except RuntimeError as error:
            print(f"[{i}] Failed to insert record: {error}")
        # Sleep for some time to simulate real-time data
        time.sleep(60)
    # Seeding complete
    print("Database seeding complete!")


def clear_database() -> None:
    """
    Clear all data from the sensor_realtime table in the database.

    This function is used to reset the database to its initial state.
    It is typically used for testing purposes.

    Returns:
        None
    """
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM sensor_realtime")
    conn.commit()
    conn.close()
    print("All data cleared from the database.")


def write_data(data: dict) -> None:
    """
    Write a sensor record to the database.

    Args:
        data (dict): Sensor record to write to the database. Must contain the following keys:
            user (str): User ID.
            temperature (float): Temperature in degrees Celsius.
            humidity (float): Humidity in percentage.
            co2 (float): CO2 in ppm.
            tvoc (float): TVOC in mg/m³ or ppm equivalent.

    Raises:
        RuntimeError: If an error occurs while writing to the database.
    """
    try:
        # Connect to the database
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        # Construct data
        data_tuple = (
            str(data["user"]),
            float(data["temperature"]),
            float(data["humidity"]),
            int(data["aqi"]),
            int(data["co2"]),
            int(data["tvoc"]),
        )
        # Insert the data
        cursor.execute(
            """
            INSERT INTO sensor_realtime (user, temperature, humidity, aqi, co2, tvoc)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            data_tuple
        )
        conn.commit()
        # Close the connection
        conn.close()
        print("Data written to database successfully")
    # Raise an error, if something goes wrong
    except sqlite3.Error as error:
        raise RuntimeError("Failed to wrtie data to database") from error


def filter_data(data: list[dict]) -> list[dict]:
    """
    Filter out PLACEHOLDER values from a list of dictionaries and replace them with None.

    Args:
        data (list[dict]): List of dictionaries containing sensor records.

    Returns:
        list[dict]: List of dictionaries with -1000 values replaced with None.
    """
    for item in data:
        for key in item.keys():
            if item[key] == NULL_PLACEHOLDER:
                item[key] = None
    return data


def read_data(user: str, date: str = None) -> list[dict]:
    """
    Read sensor records from the database for a given user.

    Args:
        user (str): User ID to filter the records by.

    Returns:
        list[tuple[str, float, float, float, float, str]]: List of tuples containing the 
        sensor records. Each tuple contains the user ID, temperature, humidity, CO2, TVOC, and 
        timestamp of the record, in that order.

    Raises:
        RuntimeError: If an error occurs while reading from the database.
    """
    try:
        # If no date is provided, use the current date
        if date is None:
            date = datetime.now().strftime("%Y-%m-%d")
        # Connect to the database
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        # Read the data
        cursor.execute(
            """
            SELECT * FROM sensor_realtime WHERE user = ? AND date(timestamp) = ?
            """,
            (user, date,)
        )
        data = cursor.fetchall()
        # Close the connection
        conn.close()
        # Parse data into dictionary
        data_dict_list = []
        for item in data:
            data_dict = {
                "user": item[1],
                "temperature": item[2],
                "humidity": item[3],
                "aqi": item[4],
                "co2": item[5],
                "tvoc": item[6],
                "timestamp": item[7],
            }
            data_dict_list.append(data_dict)
        # Filter out placeholder values
        data_dict_list = filter_data(data_dict_list)
        # Return the data as a list of dictionaries
        return data_dict_list
    # Raise an error, if something goes wrong
    except sqlite3.Error as error:
        raise RuntimeError("Failed to read data from database") from error


def generate_data(num_samples: int, randomize_user: bool = False) -> List[Dict[str, object]]:
    """
    Generate a list of fake sensor records with specified number of samples.

    Args:
        num_samples (int): Number of fake records to generate.
        randomize_user (bool, optional): If True, generate random user IDs. Defaults to False.

    Returns:
        List[Dict[str, object]]: A list of fake sensor records. Each record is a dictionary 
        containing the following keys: user, temperature, humidity, co2, and tvoc.
    """
    samples = []
    for _ in range(num_samples):
        user = random.randint(1, 10) if randomize_user else 1
        sample = {
            USER: f"user_{user}",                              # simulate few users
            TEMPERATURE: round(random.uniform(18.0, 30.0), 2), # °C
            HUMIDITY: round(random.uniform(30.0, 70.0), 2),    # %
            AQI: random.randint(0, 5),                         # 0-5
            CO2: random.randint(400, 2000),                    # ppm
            TVOC: random.randint(20, 100),                     # mg/m³ or ppm eq.
        }
        samples.append(sample)
    return samples


if __name__ == "__main__":
    num_args = len(sys.argv)
    # Check for command line arguments
    if num_args not in (2, 3):
        print("Usage: python database.py <num_records> <randomize_user: optional>")
        sys.exit(1)
    # Parse command line arguments
    num_records_arg = int(sys.argv[1])
    randomize_user_arg = None #pylint: disable=invalid-name
    # Parse optional argument
    if len(sys.argv) == 3:
        randomize_user_arg = bool(int(sys.argv[2]))
    # Initialize the database
    init_database()
    # Clear the database
    if num_records_arg == -1:
        clear_database()
    # Seed the database
    else:
        seed_database(num_records=num_records_arg, randomize_user=randomize_user_arg)
    # Exit the program
    sys.exit(0)
