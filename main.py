import requests
import os
import logging

# Set up logging to record debug information
logging.basicConfig(filename='debug.log', level=logging.DEBUG, format=f'%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def main():
    # Retrieve API key from environment variable
    key = os.environ.get('OPENWEATHERMAP_API_KEY')
    if not key:
        logging.error('API key is missing')
        print('API key is missing. Please set the OPENWEATHERMAP_API_KEY environment variable.')
        return
    
    try:
        # Retrieve city name from user input
        city = get_city()
        if not city:
            logging.warning('City name is blank')
            print('City name cannot be blank.')
            return
        
        # Retrieve weather forecast data from OpenWeatherMap API
        data = get_forecast(city, key)

        # Print weather forecast data to console
        print_forecast(data)
        
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 404:
            print(f"Invalid city: {city}")
            logging.info(f'User entered invalid city {city}')
        else:
            logging.exception(e)

def get_forecast(city, key):
    # Define API endpoint and query parameters
    url = "https://api.openweathermap.org/data/2.5/forecast"
    query = {
        "q": city,
        "appid": key,
        "units": "imperial",
        "cnt": 40
    }

    # Send GET request to OpenWeatherMap API and retrieve JSON response
    response = requests.get(url, params=query)
    response.raise_for_status()
    data = response.json()

    # Extract relevant forecast data from JSON response and return it as a list of dictionaries
    data = data['list']
    return data

def get_city():
    # Prompt user to enter a city name and return it
    city = input('Enter City: ').strip()
    return city

def get_datetime(data):
    try:
        # Extract date/time string from forecast data dictionary and return it
        date_time = data['dt_txt']
        return date_time
    except KeyError:
        logging.warning('Datetime data not in correct format')
        return 'Unknown'

def get_temp(data):
    try:
        # Extract temperature value from forecast data dictionary and return it
        temp = data['main']['temp']
        return temp
    except KeyError:
        logging.warning('Temperature data not in correct format')
        return 'Unknown'

def get_description(data):
    try:
        # Extract weather description string from forecast data dictionary and return it
        description = data['weather'][0]['description']
        return description
    except KeyError:
        logging.warning('Weather description not in correct format')
        return 'Unknown'

def get_wind_speed(data):
    try:
        # Extract wind speed value from forecast data dictionary and return it
        wind_speed = data['wind']['speed']
        return wind_speed
    except KeyError:
        logging.warning('Wind speed data not in correct format')
        return 'Unknown'

def print_forecast(data):
    # Print header row with column labels
    print(f"{'Date/Time':<20} {'Temperature (F)':<20} {'Description':<30} {'Wind Speed (mph)':<20}")
    # Print separator row with dashes
    print('-' * 90)

    # Iterate over forecast data and print each item
    for item in data:
        # Extract relevant forecast data from item dictionary
        date_time = get_datetime(item)
        temp = get_temp(item)
        description = get_description(item)
        wind_speed = get_wind_speed(item)

        # Print data for current date/time
        print(f"{date_time:<20} {temp:<20} {description:<30} {wind_speed:<20}")


if __name__ == '__main__':
    main()
