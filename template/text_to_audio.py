import os
from elevenlabs import VoiceSettings
from elevenlabs.client import ElevenLabs


def clean_key(value):
    """Remove spaces, quotes and new lines that break the HTTP header."""
    if not value:
        return None
    return value.strip().strip('"').strip("'").strip()


# Render pe key environment variable se aati hai.
ELEVENLABS_API_KEY = clean_key(os.getenv("ELEVENLABS_API_KEY"))

# Local pe env variable na ho to config.py se le lega.
if not ELEVENLABS_API_KEY:
    try:
        from config import ELEVENLABS_API_KEY as _cfg_key
        ELEVENLABS_API_KEY = clean_key(_cfg_key)
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
    response = client.text_to_speech.convert(
        voice_id="pNInz6obpgDQGcFmaJgB",  # Adam pre-made voice
        output_format="mp3_22050_32",
        text=text,
        model_id="eleven_turbo_v2_5",
        voice_settings=VoiceSettings(
            stability=0.0,
            similarity_boost=1.0,
            style=0.0,
            use_speaker_boost=True,
            speed=1.0,
        ),
    )

    save_file_path = os.path.join(f"user_uploads/{folder}", "audio.mp3")

    with open(save_file_path, "wb") as f:
        for chunk in response:
            if chunk:
                f.write(chunk)

    print(f"{save_file_path}: A new audio file was saved successfully!", flush=True)

    return save_file_path