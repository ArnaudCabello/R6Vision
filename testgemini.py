from google import genai
from google.genai import types
import PIL.Image
import os

image = PIL.Image.open("data/testimg1.png")

# Set your Gemini API key (replace with your actual key)
client = genai.Client(api_key="API KEY")  # os.environ.get("GOOGLE_API_KEY") if using environment variables

# Path to the data folder
data_folder = "data"

for filename in os.listdir(data_folder):
    if filename.lower().endswith((".png", ".jpg", ".jpeg")):  # Ensure valid image formats
            image_path = os.path.join(data_folder, filename)
            image = PIL.Image.open(image_path)

            response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=["Extract score of each team, names, kills, deaths, and assists from this Rainbow Six Siege scoreboard image. From left to right the text goes team score, name, player score, kills, deaths, assists, ping. I only want the team score, kills, deaths, and assists(if all the assists are in double digits you are getting the wrong values). Display the text like this: Team 1: (team score) Player 1: name kills deaths assists", image])

            print(response.text)

