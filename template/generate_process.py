
# This file processes uploaded folders and generates reels

import os
import time
import subprocess

from text_to_audio import text_to_speech_file


def text_to_audio(folder):
    print("TTA -", folder)

    with open(f"user_uploads/{folder}/desc.txt", "r", encoding="utf-8") as f:
        text = f.read()

    text_to_speech_file(text, folder)


def create_reel(folder):
    input_file = f"user_uploads/{folder}/input.txt"
    audio_file = f"user_uploads/{folder}/audio.mp3"
    output_file = f"static/reels/{folder}.mp4"

    command = [
        "ffmpeg",
        "-y",
        "-stream_loop", "-1",
        "-f", "concat",
        "-safe", "0",
        "-i", input_file,
        "-i", audio_file,
        "-vf",
        "scale=1080:1920:force_original_aspect_ratio=decrease,"
        "pad=1080:1920:(ow-iw)/2:(oh-ih)/2:black",
        "-c:v", "libx264",
        "-c:a", "aac",
        "-shortest",
        "-r", "30",
        "-pix_fmt", "yuv420p",
        output_file
    ]

    subprocess.run(command, check=True)

    print("CR -", folder)


if __name__ == "__main__":

    # Create required folders and file
    os.makedirs("static/reels", exist_ok=True)
    os.makedirs("user_uploads", exist_ok=True)

    if not os.path.exists("done.txt"):
        with open("done.txt", "w") as f:
            pass

    while True:
        print("Processing queue...")

        with open("done.txt", "r") as f:
            done_folders = [folder.strip() for folder in f.readlines()]

        folders = [
            folder for folder in os.listdir("user_uploads")
            if os.path.isdir(os.path.join("user_uploads", folder))
        ]

        for folder in folders:

            if folder not in done_folders:

                try:
                    # Check required files
                    record_folder = os.path.join("user_uploads", folder)

                    if not os.path.exists(os.path.join(record_folder, "desc.txt")):
                        continue

                    if not os.path.exists(os.path.join(record_folder, "input.txt")):
                        continue

                    # Generate audio
                    text_to_audio(folder)

                    # Generate video
                    create_reel(folder)

                    # Mark folder as completed
                    with open("done.txt", "a") as f:
                        f.write(folder + "\n")

                except Exception as e:
                    print("Error processing", folder, ":", e)

        time.sleep(4)
