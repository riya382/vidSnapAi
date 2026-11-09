from flask import Flask, render_template, request, redirect, url_for
import uuid
import shutil
from werkzeug.utils import secure_filename
import os

UPLOAD_FOLDER = 'user_uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/create", methods=["GET", "POST"])
def create():
    myid = str(uuid.uuid1())

    if request.method == "POST":
        rec_id = request.form.get("uuid")
        desc = request.form.get("text", "")

        if not rec_id:
            return "UUID is missing", 400

        myid = rec_id

        # Create a separate folder for this reel
        record_folder = os.path.join(app.config['UPLOAD_FOLDER'], rec_id)
        os.makedirs(record_folder, exist_ok=True)

        input_files = []

        # Save uploaded images
        for key, file in request.files.items():
            print(key, file)

            if file and file.filename:
                filename = secure_filename(file.filename)

                file.save(os.path.join(record_folder, filename))

                input_files.append(filename)
                print(filename)

        # Save description only once
        with open(os.path.join(record_folder, "desc.txt"), "w", encoding="utf-8") as f:
            f.write(desc)

        # Create input.txt for FFmpeg
        with open(os.path.join(record_folder, "input.txt"), "w") as f:
            for filename in input_files:
                image_path = os.path.abspath(
                    os.path.join(record_folder, filename)
                ).replace("\\", "/")

                f.write(f"file '{image_path}'\nduration 1\n")

        return redirect(url_for("gallery"))

    return render_template("create.html", myid=myid)


@app.route("/gallery")
def gallery():
    reels_dir = os.path.join(app.static_folder, "reels")
    reels = []
    if os.path.exists(reels_dir):
        reels = [f for f in os.listdir(reels_dir) if f.endswith(".mp4")]
    return render_template("gallery.html", reels=reels)


@app.route("/delete/<reel_id>", methods=["POST"])
def delete_reel(reel_id):
    reel_id = os.path.basename(reel_id)  # safety: no path tricks

    reel_path = os.path.join(app.static_folder, "reels", f"{reel_id}.mp4")
    upload_folder = os.path.join(app.config['UPLOAD_FOLDER'], reel_id)

    if os.path.exists(reel_path):
        os.remove(reel_path)
    if os.path.isdir(upload_folder):
        shutil.rmtree(upload_folder)

    return redirect(url_for("gallery"))


if __name__ == "__main__":
    app.run(debug=True)