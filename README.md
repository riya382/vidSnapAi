  # 🎬 VidSnapAI
  ### AI-Powered Reel Generator

  **Python · Flask · ElevenLabs · FFmpeg · HTML · CSS · JavaScript**

VidSnapAI is an AI-powered reel generation platform that transforms multiple images and text into vertical video reels with AI-generated voice narration.

Upload your images, enter a script, and let VidSnapAI handle the rest. The application uses the ElevenLabs Text-to-Speech API to convert text into audio and FFmpeg to combine the uploaded images with the generated narration into an MP4 video.

🔗 Live Demo · 📖 Documentation · 🐛 Report a Bug

---

## 📋 Table of Contents

- 🤖 Overview
- 📸 Screenshots
- ⚙️ Tech Stack
- 🔋 Key Features
- 🧠 How the Reel Generation Pipeline Works
- 🏗️ Architecture Highlights
- 📁 Project Structure
- 🚀 Getting Started
- 🔐 Environment Variables
- 🔭 Future Improvements
- 👩‍💻 Author

---

## 🤖 Overview

VidSnapAI simplifies the process of creating short-form vertical videos. Instead of manually editing images, recording voiceovers, and combining everything into a video, users can generate reels through a simple web interface.

**How it works:**

- 🖼️ **Upload Images** — select and upload multiple images to create a reel.
- ✍️ **Add Your Script** — enter the text that will be converted into voice narration.
- 🗣️ **AI Voice Generation** — ElevenLabs converts the submitted text into natural-sounding speech.
- 🎞️ **Automatic Video Creation** — FFmpeg combines the uploaded images and generated audio into a vertical MP4 video.
- 📂 **Reel Gallery** — browse and play previously generated reels directly from the application.

Built using Flask and Python on the backend, with ElevenLabs for AI voice generation and FFmpeg for video processing.

---

## 📸 Screenshots

Add your project screenshots in this section.

**Home Page**

The landing page introduces VidSnapAI and provides access to the reel creation workflow.

**Create Reel Page**

Upload multiple images and enter a script for AI-generated voice narration.

**Reel Gallery**

View and play generated MP4 reels.

---

## ⚙️ Tech Stack

| Layer | Technology | Purpose |
|---|---|---|
| Backend | Python | Application logic and processing |
| Web Framework | Flask | Routing and request handling |
| Frontend | HTML, CSS, JavaScript | User interface |
| Templating | Jinja2 | Dynamic HTML rendering |
| Text-to-Speech | ElevenLabs API | AI-generated voice narration |
| Video Processing | FFmpeg | Combining images and audio into MP4 |
| File Handling | Werkzeug | Secure uploaded filenames |
| Unique Identification | UUID | Separate folders for individual reel requests |

---

## 🔋 Key Features

### 🖼️ Image Upload

- Upload multiple images through the reel creation form.
- Dynamically add or remove file input fields.
- Store uploaded images in separate folders using unique UUIDs.

### 🗣️ AI Voice Generation

- Convert user-provided text into speech using ElevenLabs.
- Generate MP3 audio files automatically.
- Save generated audio alongside the corresponding uploaded images.

### 🎞️ Automated Reel Generation

- Combine multiple images with generated voice narration.
- Use FFmpeg for automated video processing.
- Generate vertical videos in 1080 × 1920 resolution.
- Encode videos using H.264 video and AAC audio.

### ⚙️ Background Processing

- Run video generation through a separate Python worker.
- Monitor uploaded folders for new reel requests.
- Automatically process pending requests.
- Track completed requests using `done.txt`.

### 📂 Reel Gallery

- Display generated MP4 files in a gallery.
- Play videos directly in the browser using HTML video controls.
- Access previously generated reels.

---

## 🧠 How the Reel Generation Pipeline Works

The application follows an automated image-to-video generation workflow.

```text
User Uploads Images + Text
          │
          ▼
     Flask Application
          │
          ▼
Create Unique UUID Folder
          │
          ▼
Save Images + desc.txt
          │
          ▼
Generate input.txt
          │
          ▼
Background Worker
(generate_process.py)
          │
          ▼
   ElevenLabs API
          │
          ▼
   Generate audio.mp3
          │
          ▼
       FFmpeg
          │
          ▼
Combine Images + Audio
          │
          ▼
   Generate MP4 Reel
          │
          ▼
   static/reels/
          │
          ▼
      Reel Gallery
```

### Step-by-step workflow

1. The user uploads multiple images and enters text through the Create Reel page.
2. Flask receives the POST request and generates a unique UUID for the request.
3. Uploaded images and the text description are stored in a dedicated folder inside `user_uploads/`.
4. An `input.txt` file is created containing image paths and durations for FFmpeg.
5. The background worker continuously checks for unprocessed upload folders.
6. The worker sends the submitted text to ElevenLabs to generate an MP3 voiceover.
7. FFmpeg combines the image sequence and generated audio into a vertical MP4 video.
8. The generated reel is saved inside `static/reels/`.
9. The completed request ID is recorded in `done.txt`.
10. The Reel Gallery displays available generated videos.

---

## 🏗️ Architecture Highlights

**Separate Background Worker**

Video generation runs independently from the Flask web application through `generate_process.py`. This separates the upload and request-handling workflow from the resource-intensive video generation process.

**UUID-Based File Organization**

Every reel request receives a unique UUID. Uploaded images, descriptions, audio, and processing files are stored in a dedicated folder, helping keep different reel requests organized.

**AI-Powered Voice Generation**

The ElevenLabs API converts user-provided scripts into speech, eliminating the need to record voiceovers manually.

**Automated FFmpeg Processing**

FFmpeg handles image sequencing, video scaling, padding, frame rate, and audio-video encoding to produce vertical MP4 reels.

**File-Based Processing Queue**

The background worker monitors `user_uploads/` for new requests and uses `done.txt` to track completed processing jobs.

---

## 📁 Project Structure

```text
VidSnapAI/
│
├── .gitignore
│
└── template/
    │
    ├── main.py                 # Flask application and routes
    ├── generate_process.py     # Background reel generation worker
    ├── text_to_audio.py        # ElevenLabs text-to-speech integration
    ├── config.py               # API key configuration (not committed)
    ├── done.txt                # Tracks completed reel requests
    │
    ├── templates/
    │   ├── base.html           # Base template
    │   ├── index.html          # Home page
    │   ├── create.html         # Reel creation page
    │   └── gallery.html        # Generated reels gallery
    │
    ├── static/
    │   ├── css/
    │   │   ├── style.css
    │   │   ├── create.css
    │   │   └── gallery.css
    │   │
    │   ├── reels/              # Generated MP4 videos
    │   ├── songs/              # Audio assets
    │   └── images              # Static image assets
    │
    └── user_uploads/           # Uploaded images and generated audio
```

---

## 🚀 Getting Started

### Prerequisites

Make sure you have the following installed:

- Python 3.10+
- pip
- Git
- FFmpeg
- An ElevenLabs API account and API key

### 1. Clone the Repository

```bash
git clone https://github.com/riya382/vidSnapAi-main.git
cd vidSnapAi-main
```

### 2. Navigate to the Application Folder

```bash
cd template
```

### 3. Create a Virtual Environment (Recommended)

```bash
python -m venv venv
```

Activate it on Windows:

```powershell
.\venv\Scripts\Activate.ps1
```

### 4. Install Dependencies

```bash
pip install flask elevenlabs
```

### 5. Configure the ElevenLabs API

Create a `config.py` file inside the `template/` directory:

```python
ELEVENLABS_API_KEY = "YOUR_ELEVENLABS_API_KEY"
```

Replace the placeholder with your own ElevenLabs API key.

**Important:** Never commit `config.py`, `.env`, or API keys to GitHub.

### 6. Start the Flask Application

Open the first terminal inside the `template/` directory:

```bash
python main.py
```

### 7. Start the Background Worker

Open a second terminal in the same `template/` directory and activate the virtual environment if necessary.

```bash
python generate_process.py
```

Keep both processes running while generating reels.

### 8. Open the Application

Visit:

```text
http://127.0.0.1:5000
```

Navigate to the Create Reel page, upload images, enter your text, and submit the form.

Once processing is complete, visit the Reel Gallery and refresh it to see the generated video.

---

## 🔐 Environment Variables

The application uses an ElevenLabs API key configured through `config.py`.

| Variable | Description |
|---|---|
| `ELEVENLABS_API_KEY` | API key used for ElevenLabs text-to-speech generation |


## 🔭 Future Improvements

- Add real-time reel generation progress.
- Display the generated reel immediately after processing.
- Add video upload support.
- Introduce background music and sound effects.
- Add customizable AI voices and narration styles.
- Add image transitions, animations, and visual effects.
- Allow users to download generated reels.
- Add user authentication and personalized reel history.
- Improve error handling and processing queue management.
- Deploy the application to a cloud platform.

---

## 👩‍💻 Author

**Riya Gupta**

GitHub: [@riya382](https://github.com/riya382)

Repository: [VidSnapAI](https://github.com/riya382/vidSnapAi-main)
