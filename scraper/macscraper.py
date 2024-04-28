import requests
import json
from datetime import datetime
import socket

class WeatherScraper:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = 'https://api.openweathermap.org/data/3.0/onecall'

    def fetch_weather_forecast(self, latitude, longitude):
        params = {
            'lat': latitude,
            'lon': longitude,
            'exclude': 'current,minutely,hourly,alerts',  # Exclude unnecessary parts
            'appid': self.api_key,
            'units': 'imperial'  # Using imperial for demonstration (°F)
        }
        response = requests.get(self.base_url, params=params)
        if response.status_code == 200:
            data = response.json()
            # Extract only the daily forecast's temperature and weather
            forecast = [
                {
                    'date': datetime.fromtimestamp(day['dt']).strftime('%Y-%m-%d'),
                    'temperature': day['temp'],
                    'weather': day['weather'][0] if day['weather'] else {}
                } for day in data['daily']
            ]
            return forecast
        else:
            error_message = response.json().get('message', 'Failed to fetch data')
            raise Exception(f"API Error: {error_message} - Status Code: {response.status_code}")

def scrape_weather_forecast():
    api_key = '1ca0f59fe93a61361be975d8d29c21c7'
    latitude = 39.7392  # Latitude for Denver, Colorado
    longitude = -104.9903  # Longitude for Denver, Colorado
    scraper = WeatherScraper(api_key)
    forecast_data = scraper.fetch_weather_forecast(latitude, longitude)
    with open('forecast_data.json', 'w') as f:
        json.dump(forecast_data, f, indent=4)
    return forecast_data

def connect_to_server(server_ip, port=65433):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((server_ip, port))
            print("Connected to server.")
            forecast_data = scrape_weather_forecast()
            serialized_data = json.dumps(forecast_data).encode('utf-8')
            sock.sendall(serialized_data)
            print("Weather forecast data sent to server.")
            response = sock.recv(8192)
            print("Received response:", response.decode())
    except socket.error as e:
        print(f"Could not connect to server {server_ip} on port {port}: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    SERVER_IP = '10.0.0.224' 
    connect_to_server(SERVER_IP)
