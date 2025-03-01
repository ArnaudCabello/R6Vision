import sys
import PIL.Image
from google import genai

client = genai.Client(api_key="API KEY" )

if len(sys.argv) < 2:
    print("Error: No image path provided.")
    sys.exit(1)

image_path = sys.argv[1]
image = PIL.Image.open(image_path)

response = client.models.generate_content(
    model="gemini-2.0-flash",
    contents=["Extract score of each team, names, kills, deaths, and assists from this Rainbow Six Siege scoreboard image. From left to right the text goes team score, name, player score, kills, deaths, assists, ping. I only want the team score, kills, deaths, and assists(if all the assists are in double digits you are getting the wrong values). Display the text like this: Team 1: (team score) Player 1: name kills deaths assists", image])

print(response.text)
