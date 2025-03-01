import discord
import os
import subprocess
import sys

# Load bot token from environment variable
TOKEN = "API KEY"   # Set this in your system environment variables
UPLOAD_FOLDER = "uploads"

# Ensure the upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True  # Required for reading message content
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"Logged in as {client.user}")

@client.event
async def on_message(message):
    if message.author.bot:
        return

    if message.content.startswith("!upload"):
        if message.attachments:
            for attachment in message.attachments:
                if attachment.filename.lower().endswith((".png", ".jpg", ".jpeg")):
                    image_path = os.path.join(UPLOAD_FOLDER, attachment.filename)
                    await attachment.save(image_path)
                    await message.channel.send(f"Image received: `{attachment.filename}`. Processing...")

                    # Run Gemini on the uploaded image
                    process = subprocess.run(["python", "gemini.py", image_path], capture_output=True, text=True)
                    if process.stderr:
                        await message.channel.send(f"Error processing image: `{process.stderr.strip()}`")
                        return

                    gemini_output = process.stdout.strip()
                    await message.channel.send(f"Extracted Data:\n```\n{gemini_output}\n```")
                    
                    # Run Sheets script to update Google Sheets
                    process_sheets = subprocess.run(["python", "sheets.py"], input=gemini_output, text=True, capture_output=True)

                    if process_sheets.stderr:
                        await message.channel.send(f"Error updating sheets: `{process_sheets.stderr.strip()}`")
                    else:
                        await message.channel.send("Google Sheets updated successfully!")

        else:
            await message.channel.send("Please upload an image with your command!")

client.run(TOKEN)