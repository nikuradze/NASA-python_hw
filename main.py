import requests
import json
import sqlite3
from win10toast import ToastNotifier

# Function to retrieve APOD data from NASA API
def get_apod_data(api_key):
    base_url = "https://api.nasa.gov/planetary/apod"
    params = {"api_key": api_key}
    response = requests.get(base_url, params=params)
    return response.json(), response.status_code, response.headers

# Function to save data to a JSON file
def save_to_json(data, file_name):
    with open(file_name, "w") as file:
        json.dump(data, file, indent=4)

# Function to print information from APOD data
def print_apod_info(data):
    title = data["title"]
    date = data["date"]
    explanation = data["explanation"]
    print(f"Title: {title}")
    print(f"Date: {date}")
    print(f"Explanation: {explanation}")

# Function to save APOD information to the database
def save_to_database(data):
    conn = sqlite3.connect("nasa.db")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS apod (title TEXT, date TEXT, explanation TEXT)")
    cursor.execute("INSERT INTO apod VALUES (?, ?, ?)", (data["title"], data["date"], data["explanation"]))
    conn.commit()
    conn.close()

# Function to display a Windows notification
def display_notification(title, explanation):
    toaster = ToastNotifier()
    message = f"{title}\n{explanation}"
    toaster.show_toast("NASA APOD", message, duration=10)

# API key
api_key = "UFK98lKIwOe1PclJO9aHFsGEcJmLCFRrqy1cZA2l"

# Retrieve APOD data, status code, and headers
response, status_code, headers = get_apod_data(api_key)

# Save data to a JSON file
save_to_json(response, "apod_data.json")

# Print information from APOD data
print_apod_info(response)

# Save APOD information to the database
save_to_database(response)

# Display a Windows notification
display_notification(response["title"], response["explanation"])

# Print the status code and headers
print(f"Status Code: {status_code}")
print("Headers:")
for header, value in headers.items():
    print(f"{header}: {value}")