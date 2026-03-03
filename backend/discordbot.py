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

        mentioned = any(role in message.role_mentions for role in message.guild.me.roles) or self.user in message.mentions
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

# /idle command
@client.tree.command(name="idle", description="Rem will only respond when mentioned.")
async def be_quiet_command(interaction: discord.Interaction):
    client.greenlight = False
    await interaction.response.send_message("Quiet Mode Enabled", ephemeral=True)

# /active command
@client.tree.command(name="active", description="Rem will respond to all messages.")
@app_commands.describe(confirm="Type 'yes' or 'y' to confirm")
async def speak_command(interaction: discord.Interaction, confirm: str):
    if confirm.lower() not in ("yes", "y"):
        await interaction.response.send_message(
            "You must type 'yes' or 'y' to confirm this action.", ephemeral=True)
        return
    client.greenlight = True
    await interaction.response.send_message("Quiet Mode Disabled", ephemeral=True)

# ---------------- Run ---------------- 
client.run(TOKEN)