from PIL import Image, ImageDraw, ImageFont
import json
import os

def load_weather_data(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def get_icon_path(weather_main):
    icons = {
        "Rain": "Rainy.png",
        "Wind": "Windy.png",
        "Clouds": "Cloudy.png",
        "Clear": "Sunny.png",
        "Clouds with Rain": "SunnyWith_Rain.png",
        "Partly Cloudy": "Partly_Sunny.png"
    }
    return icons.get(weather_main, "default.png")  # Use the actual default icon path

def create_weather_image(weather_data, filename, icon_folder):
    # Set up the dimensions for the image
    width, height = 800, 100  # Adjust the height based on the number of entries
    background_color = 'white'
    font_size = 18

    # Load a font (use an absolute path if the font is not in the script's directory)
    font = ImageFont.truetype("/Library/Fonts/Arial.ttf", font_size)

    # Create a new image with white background
    img = Image.new('RGB', (width, height * len(weather_data)), color=background_color)
    draw = ImageDraw.Draw(img)

    for i, entry in enumerate(weather_data):
        # Calculate positions
        y_position = i * height
        icon_path = os.path.join(icon_folder, get_icon_path(entry["weather"]["main"]))
        icon = Image.open(icon_path).resize((64, 64))

        # Paste the icon onto the image
        img.paste(icon, (20, y_position + (height - 64) // 2), icon)

        # Draw the text next to the icon
        text_position = (20 + 64 + 10, y_position + (height - font_size) // 2)
        weather_text = f"{entry['date']}: {entry['weather']['main']}, {entry['temperature']['day']}°F (Min: {entry['temperature']['min']}°F, Max: {entry['temperature']['max']}°F)"
        draw.text(text_position, weather_text, font=font, fill="black")

    # Save the image
    img.save(filename)

if __name__ == '__main__':
    file_path = 'output.json'  # Replace with your actual file path
    output_image_path = 'weather_dashboard.png'
    icons_folder_path = ''  # Assuming icons are in the same directory as the script

    weather_data = load_weather_data(file_path)
    create_weather_image(weather_data, output_image_path, icons_folder_path)
