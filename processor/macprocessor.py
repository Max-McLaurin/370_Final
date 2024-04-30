import socket
import zlib
import json
import os
import time
from PIL import Image, ImageDraw, ImageFont

# Function to get the weather icon path
def get_icon_path(weather_main):
    icons = {
        "Rain": "Rainy.png",
        "Wind": "Windy.png",
        "Clouds": "Cloudy.png",
        "Clear": "Sunny.png",
        "Clouds with Rain": "SunnyWith_Rain.png",
        "Partly Cloudy": "Partly_Sunny.png"
    }
    return icons.get(weather_main, "default.png")

# Function to create an image from weather data
def create_weather_image(weather_data, filename, icon_folder):
    width, height = 800, 100
    font = ImageFont.truetype("/Library/Fonts/Arial.ttf", 18)
    img = Image.new('RGB', (width, height * len(weather_data)), color='white')
    draw = ImageDraw.Draw(img)

    for i, entry in enumerate(weather_data):
        y_position = i * height
        icon_path = os.path.join(icon_folder, get_icon_path(entry["weather"]["main"]))
        icon = Image.open(icon_path).resize((64, 64))
        img.paste(icon, (20, y_position + (height - 64) // 2), icon)

        text_position = (20 + 64 + 10, y_position + (height - font_size) // 2)
        weather_text = f"{entry['date']}: {entry['weather']['main']}, {entry['temperature']['day']}°F " \
                       f"(Min: {entry['temperature']['min']}°F, Max: {entry['temperature']['max']}°F)"
        draw.text(text_position, weather_text, font=font, fill="black")

    img.save(filename)

# Function to send a file to the server
def send_file_to_server(server_ip, server_port, file_path):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((server_ip, server_port))
        file_size = os.path.getsize(file_path)
        sock.sendall(file_size.to_bytes(8, byteorder='big'))
        with open(file_path, 'rb') as file:
            sock.sendfile(file)
        print(f"File {file_path} has been sent successfully.")

def connect_to_server(server_ip, port=65433):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((server_ip, port))
            print("Connected to server.")
            # Receive the size of the compressed data first
            data_size = int.from_bytes(sock.recv(4), 'big')
            compressed_data = b''
            while len(compressed_data) < data_size:
                packet = sock.recv(4096)
                if not packet:
                    break
                compressed_data += packet  # Ensure this is inside the loop

            # Decompress the data
            decompressed_data = zlib.decompress(compressed_data)
            data = json.loads(decompressed_data.decode('utf-8'))
            print("Received decompressed JSON data:")
            print(json.dumps(data, indent=4))

            # Save data to a JSON file
            with open('output.json', 'w') as json_file:
                json.dump(data, json_file, indent=4)
            print("Data saved to 'output.json'.")

    except socket.error as e:
        print(f"Could not connect to server {server_ip} on port {port}: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")



# Function to initiate the process
def main(server_ip, port, output_json_path, output_image_path, icons_folder_path):
    # Connect to the server and receive data
    connect_to_server(server_ip, port)

    # Load the received data
    weather_data = load_weather_data(output_json_path)

    # Generate the weather image
    create_weather_image(weather_data, output_image_path, icons_folder_path)

    # Wait for 20 seconds to let other processes execute
    time.sleep(20)

    # Send the generated image back to the server
    send_file_to_server(server_ip, port, output_image_path)

if __name__ == '__main__':
    SERVER_IP = '10.0.0.224'  # Replace with the Raspberry Pi's IP address
    PORT = 65433  # Replace with the port number on which the server is listening
    OUTPUT_JSON_PATH = 'output.json'  # Path for the JSON data received from the server
    OUTPUT_IMAGE_PATH = 'weather_dashboard.png'  # Path for the generated image
    ICONS_FOLDER_PATH = ''  # Folder path where icons are stored

    main(SERVER_IP, PORT, OUTPUT_JSON_PATH, OUTPUT_IMAGE_PATH, ICONS_FOLDER_PATH)
