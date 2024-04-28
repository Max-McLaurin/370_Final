import requests
import json
from datetime import datetime
import socket

class WeatherScraper:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = 'https://api.openweathermap.org/data/2.5/weather'

    def fetch_weather_data(self, city_id):
        params = {
            'id': city_id,  # City ID for Denver, Colorado
            'appid': self.api_key,
            'units': 'metric'  # or 'imperial' for Fahrenheit
        }
        response = requests.get(self.base_url, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            error_message = response.json().get('message', 'Failed to fetch data')
            raise Exception(f"API Error: {error_message} - Status Code: {response.status_code}")

def scrape_weather_data():
    api_key = '1ca0f59fe93a61361be975d8d29c21c7'
    city_id = 5419384  # City ID for Denver, Colorado
    scraper = WeatherScraper(api_key)
    weather_data = scraper.fetch_weather_data(city_id)
    with open('weather_data.json', 'w') as f:
        json.dump(weather_data, f, indent=4)
    return weather_data

def connect_to_server(server_ip, port=65433):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((server_ip, port))
            print("Connected to server.")
            weather_data = scrape_weather_data()
            serialized_data = json.dumps(weather_data).encode('utf-8')
            sock.sendall(serialized_data)
            print("Weather data sent to server.")
            response = sock.recv(1024)
            print("Received response:", response.decode())
    except socket.error as e:
        print(f"Could not connect to server {server_ip} on port {port}: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    SERVER_IP = '10.0.0.224' 
    connect_to_server(SERVER_IP)
