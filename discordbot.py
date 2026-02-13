# ---------------- Definitions ---------------- #
import re
import os
import asyncio
import discord
from discord import app_commands
from dotenv import load_dotenv
from .model.response import generate_reply
from .model.speak import synthesize_text 
from discord.ext import voice_recv
from discord import FFmpegPCMAudio
import speech_recognition as sr
import time
import logging

# Silence noisy recv warnings
logging.getLogger("discord.ext.voice_recv.reader").setLevel(logging.ERROR)
logging.getLogger("discord.ext.voice_recv.opus").setLevel(logging.ERROR)

if not discord.opus.is_loaded():
    discord.opus.load_opus('/opt/homebrew/lib/libopus.dylib')

# Environment Variables
ENV_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), 'model', 'data', '.env'))
load_dotenv(ENV_PATH)
TOKEN = os.getenv("REM_TOKEN")

# Speech recognizer
recognizer = sr.Recognizer()

def remove_mentions(text: str) -> str:
    ''' Removes Discord Mentions from incoming messages '''
    return re.sub(r'<[@#]\d+>','',text)

# ---------------- Speak into VC ---------------- #
async def speak_text_vc(vc: discord.VoiceClient, text: str, filename: str = "response.wav"):
    from discord import FFmpegPCMAudio

    # Make the audio file with Coqui TTS
    output_path = synthesize_text(text, filename)

    # If VC is already playing something, stop it
    if vc.is_playing():
        vc.stop()

    # Play into Discord VC
    audio_src = FFmpegPCMAudio(
        executable="ffmpeg",  # assumes ffmpeg is in PATH
        source=output_path
    )
    vc.play(audio_src)


# ---------------- Voice Receiving Sink ---------------- # - Code is not written by Developer, Need more Understanding to be Replaced 
class SpeechSink(voice_recv.BasicSink):
    def __init__(self, loop, vc, silence_timeout=0.5):
        super().__init__(asyncio.Event())
        self.loop = loop
        self.vc = vc
        self.buffers = {}         # user_id -> bytearray
        self.last_active = {}     # user_id -> last time we got audio
        self.silence_timeout = silence_timeout
        self.sample_rate = 48000
        self.sample_width = 2
        self.channels = 1

    def write(self, user, data: voice_recv.VoiceData):
        if not data.pcm:
            return

        # Downmix stereo → mono
        mono_pcm = bytearray()
        for i in range(0, len(data.pcm), 4):
            mono_pcm.extend(data.pcm[i:i+2])

        # Append to buffer
        buf = self.buffers.setdefault(user.id, bytearray())
        buf.extend(mono_pcm)
        self.last_active[user.id] = time.time()

        # ✅ Schedule silence check safely on the bot’s loop
        self.loop.call_soon_threadsafe(
            asyncio.create_task, self._check_silence(user)
        )

    async def _check_silence(self, user):
        await asyncio.sleep(self.silence_timeout)
        last = self.last_active.get(user.id, 0)
        if time.time() - last >= self.silence_timeout and self.buffers.get(user.id):
            buf = self.buffers.pop(user.id)
            try:
                audio_data = sr.AudioData(bytes(buf), self.sample_rate, self.sample_width)
                text = recognizer.recognize_google(audio_data)
                print(f"🎤 {user}: {text}")

                reply = generate_reply(text)
                print(f"🤖 Rem: {reply}")

                await speak_text_vc(self.vc, reply)

            except sr.UnknownValueError:
                pass  # unintelligible speech → ignore
            except sr.RequestError as e:
                print(f"🌐 API error: {e}")
            except Exception as e:
                print(f"⚠️ Audio decode error for {user}: {e}")


# ---------------- Client ---------------- #
class MyClient(discord.Client):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.voice_states = True
        super().__init__(intents=intents)

        self.tree = app_commands.CommandTree(self)
        self.greenlight = False
        self.learning_buffer = []
        self.learning_user = None
        self.vc = None  # store active voice client

    async def on_ready(self):
        print(f"✅ Logged in as {self.user}")
        await self.change_presence(activity=discord.Game("AI by Evan Nicholas"))

        try:
            synced = await self.tree.sync()
            print(f"🔧 Synced {len(synced)} command(s).")
        except Exception as e:
            print(f"Error syncing commands: {e}")

    async def on_message(self, message):
        if message.author.bot:
            return

        mentioned = any(role in message.role_mentions for role in message.guild.me.roles) or self.user in message.mentions
        replied = (message.reference and (await message.channel.fetch_message(message.reference.message_id)).author == self.user)

        if mentioned or replied or self.greenlight:
            cleaned_content = remove_mentions(message.content)
            cleaned_content = re.sub(r"[^a-zA-Z0-9\s]", "", cleaned_content).strip()
            print(f"User input: {cleaned_content}")
            reply = generate_reply(cleaned_content)
            print(f"Bot reply: {reply}")

            # Send in chat
            await message.channel.send(reply)

            # ✅ If in VC, also speak reply
            if self.vc:
                await speak_text_vc(self.vc, reply)
        else:
            self.learning_buffer = []


# ---------------- Commands ---------------- #

client = MyClient()

# /idle command
@client.tree.command(name="idle", description="Rem will only respond when mentioned.")
async def be_quiet_command(interaction: discord.Interaction):
    client.greenlight = False
    client.learning_buffer = []
    await interaction.response.send_message("Quiet Mode Enabled", ephemeral=True)

# /active command
@client.tree.command(name="active", description="Rem will respond to all messages.")
@app_commands.describe(confirm="Type 'yes' or 'y' to confirm")
async def speak_command(interaction: discord.Interaction, confirm: str):
    if confirm.lower() not in ("yes", "y"):
        await interaction.response.send_message(
            "You must type 'yes' or 'y' to confirm this action.",
            ephemeral=True
        )
        return
    client.greenlight = True
    await interaction.response.send_message("Quiet Mode Disabled", ephemeral=True)

# /join command
@client.tree.command(name="join", description="Rem will join the vc of the user and listen")
async def join_command(interaction: discord.Interaction):
    if interaction.user.voice:  # check if user is in a VC
        channel = interaction.user.voice.channel
        if interaction.guild.voice_client:  # already in a VC
            client.vc = interaction.guild.voice_client
            await interaction.guild.voice_client.move_to(channel)
        else:
            # Important: use VoiceRecvClient for receiving audio
            vc = await channel.connect(cls=voice_recv.VoiceRecvClient)
            client.vc = vc
            sink = SpeechSink(loop=client.loop, vc=vc) 
            vc.listen(sink)      # Start listening
        await interaction.response.send_message(f"✅ Joined {channel} and listening.", ephemeral=True)
    else:
        await interaction.response.send_message("❌ You need to be in a voice channel first!", ephemeral=True)

# /leave command
@client.tree.command(name="leave", description="Rem will disconnect from the vc of the user")
async def leave_command(interaction: discord.Interaction):
    if interaction.guild.voice_client:
        channel_name = interaction.guild.voice_client.channel
        await interaction.guild.voice_client.disconnect()
        client.vc = None
        await interaction.response.send_message(f"✅ Left {channel_name}.", ephemeral=True)
    else:
        await interaction.response.send_message("❌ I'm not in a voice channel.", ephemeral=True)


# ---------------- Run ---------------- #
client.run(TOKEN)