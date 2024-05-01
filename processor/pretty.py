from PIL import Image, ImageDraw, ImageFont
import json
import os

def load_weather_data(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def get_icon_path(weather_main):
    icons = {
        "Rain": "Partly_Sunny.png",
        "Wind": "Windy.png",
        "Clouds": "Cloudy.png",
        "Clear": "Sunny.png",
        "Clouds with Rain": "SunnyWith_Rain.png",
        "Partly Cloudy": "Partly_Sunny.png"
    }
    return icons.get(weather_main, "default.png")

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

        text_position = (20 + 64 + 10, y_position + 20)
        # Removed `entry["weather"]["main"]` from the string formatting
        weather_text = f"{entry['date']}: {entry['temperature']['day']}°F " \
                       f"(Min: {entry['temperature']['min']}°F, Max: {entry['temperature']['max']}°F)"
        draw.text(text_position, weather_text, font=font, fill="black")

    img.save(filename)

if __name__ == '__main__':
    print("In Pretty.py")
    file_path = 'output.json'  # JSON file with weather data
    output_image_path = 'weather_dashboard.png'  # Path to save the dashboard image
    icons_folder_path = ''  # Assuming icons are in the same directory
    weather_data = load_weather_data(file_path)
    create_weather_image(weather_data, output_image_path, icons_folder_path)
