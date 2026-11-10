# This file processes uploaded folders and generates reels

import os
import time
import subprocess

import imageio_ffmpeg
from text_to_audio import text_to_speech_file

FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()


def text_to_audio(folder):
    print("TTA -", folder, flush=True)

    with open(f"user_uploads/{folder}/desc.txt", "r", encoding="utf-8") as f:
        text = f.read()

    text_to_speech_file(text, folder)


def create_reel(folder):
    input_file = f"user_uploads/{folder}/input.txt"
    audio_file = f"user_uploads/{folder}/audio.mp3"
    output_file = f"static/reels/{folder}.mp4"

    command = [
        FFMPEG,
        "-y",
        "-nostdin",
        "-f", "concat",
        "-safe", "0",
        "-i", input_file,
        "-i", audio_file,
        "-vf",
        "scale=1080:1920:force_original_aspect_ratio=decrease,"
        "pad=1080:1920:(ow-iw)/2:(oh-ih)/2:black,"
        "tpad=stop_mode=clone:stop_duration=120",
        "-c:v", "libx264",
        "-c:a", "aac",
        "-shortest",
        "-r", "30",
        "-pix_fmt", "yuv420p",
        output_file
    ]

    subprocess.run(command, check=True, timeout=300)

    print("CR -", folder, flush=True)


def worker_loop():
    os.makedirs("static/reels", exist_ok=True)
    os.makedirs("user_uploads", exist_ok=True)

    if not os.path.exists("done.txt"):
        open("done.txt", "w").close()

    while True:
        with open("done.txt", "r") as f:
            done_folders = [x.strip() for x in f.readlines()]

        for folder in os.listdir("user_uploads"):
            if folder in done_folders:
                continue

            rec = os.path.join("user_uploads", folder)

            if not os.path.isdir(rec):
                continue
            if not os.path.exists(os.path.join(rec, "desc.txt")):
                continue
            if not os.path.exists(os.path.join(rec, "input.txt")):
                continue

            try:
                text_to_audio(folder)
                create_reel(folder)

                with open("done.txt", "a") as f:
                    f.write(folder + "\n")

            except Exception as e:
                print("Error processing", folder, ":", e, flush=True)
                # Mark as done so one bad upload doesn't retry forever
                with open("done.txt", "a") as f:
                    f.write(folder + "\n")

        time.sleep(4)


if __name__ == "__main__":
    worker_loop()