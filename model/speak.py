import os
from TTS.api import TTS
import discord

BASE_DIR = os.path.dirname(__file__)
AUDIO_DIR = os.path.join(BASE_DIR, "audio")
os.makedirs(AUDIO_DIR, exist_ok=True)

tts = TTS("tts_models/en/vctk/vits", gpu=False)


def synthesize_text(input_text: str, filename: str = "response.wav"):     # Generate TTS and save as WAV file, return full path.
    output_path = os.path.join(AUDIO_DIR, filename)
    tts.tts_to_file(
        text=input_text,
        file_path=output_path,
        speaker="p227"  # change speaker ID if you want
    )
    return output_path


async def speak_text(vc, input_text: str, filename: str = "response.wav"):
    # make audio file
    output_path = synthesize_text(input_text, filename)

    # stop anything currently playing
    if vc.is_playing():
        vc.stop()

    # play through FFmpeg into Discord
    vc.play(
        source=vc.loop.create_task(
            _make_ffmpeg_source(output_path)
        )
    )


async def _make_ffmpeg_source(path: str):
    return discord.FFmpegPCMAudio(
        executable="ffmpeg",  # assumes ffmpeg is in PATH
        source=path
    )