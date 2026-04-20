# ---------------- Definitions ---------------- #
import re
import os
import asyncio
import discord
from discord import app_commands
from dotenv import load_dotenv
from model.response import generate_reply
from model.utils import clean_content
import time

# Environment Variables
ENV_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), 'model', 'data', '.env'))
load_dotenv(ENV_PATH)
TOKEN = os.getenv("REM_TOKEN")

def remove_mentions(text: str) -> str:
    ''' Removes Discord Mentions from incoming messages '''
    return re.sub(r'<[@#]\d+>','',text)


# ---------------- Client ---------------- #
class MyClient(discord.Client):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.voice_states = True
        super().__init__(intents=intents)

        self.tree = app_commands.CommandTree(self)
        self.greenlight = False

    async def on_ready(self):
        print(f"Logged in as {self.user}")
        await self.change_presence(activity=discord.Game("AI by Evan Nicholas"))

        try:
            synced = await self.tree.sync()
            print(f"Synced {len(synced)} command(s).")
        except Exception as e:
            print(f"Error syncing commands: {e}")

    async def on_message(self, message):
        if message.author.bot:
            return

        mentioned = self.user in message.mentions
        replied = (message.reference and (await message.channel.fetch_message(message.reference.message_id)).author == self.user)

        if mentioned or replied or self.greenlight:
            content = remove_mentions(message.content)
            content = clean_content(content)
            print(f"User input: {content}")
            reply = generate_reply(content)
            print(f"Bot reply: {reply}")

            # Send in chat
            await message.channel.send(reply)


# ---------------- Commands ---------------- 

client = MyClient()

# /help command
@client.tree.command(name="help", description="Learn how to use Rem!")
async def help_command(interaction: discord.Interaction):
    await interaction.response.send_message("Mention me in a message or reply to one of my previous messages to talk with me!", ephemeral=True)

# ---------------- Run ---------------- 
client.run(TOKEN)
