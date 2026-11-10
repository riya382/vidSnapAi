import os
import uuid
from elevenlabs import VoiceSettings
from elevenlabs.client import ElevenLabs

# Render pe key environment variable se aati hai.
# Local pe agar env variable nahi hai, to config.py se le lega.
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")

if not ELEVENLABS_API_KEY:
    try:
        from config import ELEVENLABS_API_KEY
    except ImportError:
        ELEVENLABS_API_KEY = None

if not ELEVENLABS_API_KEY:
    raise RuntimeError(
        "ELEVENLABS_API_KEY not found. Set it in Render Environment "
        "or in config.py for local use."
    )

client = ElevenLabs(
    api_key=ELEVENLABS_API_KEY,
)


def text_to_speech_file(text: str, folder: str) -> str:
    # Calling the text_to_speech conversion API with detailed parameters
    response = client.text_to_speech.convert(
        voice_id="pNInz6obpgDQGcFmaJgB",  # Adam pre-made voice
        output_format="mp3_22050_32",
        text=text,
        model_id="eleven_turbo_v2_5",  # use the turbo model for low latency
        voice_settings=VoiceSettings(
            stability=0.0,
            similarity_boost=1.0,
            style=0.0,
            use_speaker_boost=True,
            speed=1.0,
        ),
    )

    save_file_path = os.path.join(f"user_uploads/{folder}", "audio.mp3")

    # Writing the audio to a file
    with open(save_file_path, "wb") as f:
        for chunk in response:
            if chunk:
                f.write(chunk)

    print(f"{save_file_path}: A new audio file was saved successfully!", flush=True)

    return save_file_path