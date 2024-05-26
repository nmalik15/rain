import requests
from datetime import datetime, timedelta
import os.path

# API endpoint
API_URL = "https://api.open-meteo.com/v1/forecast"

# Function to gett forecast
def forecast(date):
    # # Convert date to required format
    # date_str = date.strftime("%Y-%m-%d")

    # Check if the result is already in the file
    if os.path.isfile("rain.txt"):
        with open("rain.txt", "r") as f:
            for line in f:
                if date in line:
                    print(f"Result from file for {date}: {line.split(', ')[1]}")
                    return

    # Make API request
    params = {
        "latitude": 51.51,
        "longitude": -0.13,
        "daily": "precipitation_sum",
        "start_date": date,
        "end_date": date,
    }
    response = requests.get(API_URL, params=params)
    data = response.json()

    # Check if there is a result
    if "daily" in data and "precipitation_sum" in data["daily"]:
        precipitation = data["daily"]["precipitation_sum"][0]

        # Determine the precipitation state
        if precipitation > 0.0:
            result = f"It will rain, precipitation sum: {precipitation} mm"
        elif precipitation == 0.0:
            result = "It will not rain"
        else:
            result = "I don't know"

        # Save the result to the file
        with open("rain.txt", "a") as f:
            f.write(f"{date}, {result}\n")

        print(f"Result for {date}: {result}")
    else:
        print(f"No result available for {date}")

# Get the date from the user
date_input = input("Enter a date in YYYY-MM-DD format (or press Enter to use the next day): ")

# If no date is provided, use the next day
while True:
    date_input = input("Enter a date in the format YYYY-MM-DD (or press Enter to use tomorrow's date): ")

    if not date_input:
        # If the user didn't enter anything, use tomorrow's date
        date = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
        break

    try:
        datetime.strptime(date_input, "%Y-%m-%d")
        date = date_input
        break
    except ValueError:
        print("Invalid date format. Please try again.")

# Get the weather forecast
forecast(date)