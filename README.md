# Offline YouTube Video Summarizer – by VINOD KUMAR ANCHA

A small end-to-end offline system that takes a YouTube URL, downloads the audio, transcribes it using Whisper, and generates a concise summary using a local transformer model (no cloud APIs).

## 1. Project Overview

This project implements an **Offline YouTube Video Summarizer**

Given a public YouTube URL, the system:

1. Downloads the best audio track using `yt-dlp`
2. Converts the audio to WAV
3. Runs **offline speech-to-text (STT)** using **Whisper**
4. Runs **offline text summarization** using a Hugging Face transformer model
5. Returns a concise text summary (via CLI or a simple web UI)

All AI inference (STT and summarization) happens **offline** once models are downloaded.

Author: **VINOD KUMAR ANCHA**

---

## 2. Project Structure

```text
offline_youtube_summarizer/
│
├── app.py                # Main entrypoint (CLI + optional Flask)
├── downloader.py         # YouTube audio downloader
├── stt.py                # Offline speech-to-text (Whisper)
├── summarizer.py         # Offline text summarization (Transformers)
├── requirements.txt      # Python dependencies
├── scripts/
│   └── download_models.py  # Pre-download STT & summarization models
└── README.md             # This file
```

---

## 3. Installation & Setup (Step by Step)

### 3.1. Clone or copy the project

If you download this as a ZIP:

1. Unzip it to a folder, e.g. `offline_youtube_summarizer/`
2. Open a terminal in that folder.

### 3.2. Create and activate a Python virtual environment (recommended)

```bash
python -m venv .venv
source .venv/bin/activate        # On Windows: .venv\Scripts\activate
```

### 3.3. Install system dependency: ffmpeg

On Ubuntu/Debian:

```bash
sudo apt update
sudo apt install -y ffmpeg
```

On macOS (Homebrew):

```bash
brew install ffmpeg
```

On Windows, install ffmpeg from the official website or a package manager (e.g. choco).

### 3.4. Install Python dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 3.5. (Optional but recommended) Pre-download models

This ensures all required models are downloaded **once** and cached locally for fully offline inference later.

```bash
python scripts/download_models.py
```

This will download:

- Whisper (\"tiny\") for speech-to-text  
- DistilBART CNN summarization model for text summarization  

---

## 4. Usage

You can run the project in **CLI mode** (main requirement) or **Flask web mode** (bonus).

### 4.1. CLI mode (default)

From inside the project folder (with virtualenv active):

```bash
python app.py "https://www.youtube.com/watch?v=YOUR_VIDEO_ID"
```

Example:

```bash
python app.py "https://www.youtube.com/watch?v=0CmtDk-joT4"
```

What happens:

1. `[1/3]` The audio is downloaded using `yt-dlp`
2. `[2/3]` The audio is converted & transcribed offline using Whisper
3. `[3/3]` The transcript is summarized offline

You will see:

```text
=== SUMMARY ===

<Concise summary text here>
```

If you also want to see the **full transcript**, you can open `app.py` and uncomment the lines under `# If you also want to show full transcript, uncomment:`.

---

### 4.2. Flask web mode (bonus)

You can also run a simple web interface (for bonus points in the assignment).

1. Set an environment variable to switch to Flask mode:

   ```bash
   export APP_MODE=flask          # On Windows (CMD): set APP_MODE=flask
   ```

2. Run the app:

   ```bash
   python app.py
   ```

3. Open your browser at:

   ```text
   http://localhost:5000
   ```

4. Paste a public YouTube URL and click **Summarize**  
5. The page will show:
   - A **summary**
   - (Optional) a **full transcript** inside a `<details>` block

---

## 5. Design Choices & Model Justification

### 5.1. Speech-to-Text (STT): Whisper

- **Model**: `tiny` variant of [OpenAI Whisper](https://github.com/openai/whisper)
- **Why Whisper?**
  - Robust to real-world YouTube audio (noise, accents, etc.)
  - Fully offline once the model is downloaded
  - Simple API (`model.transcribe()`)
- **Why \"tiny\"?**
  - Much faster and lighter than larger variants
  - Good trade-off between speed and accuracy for this assignment
  - For higher accuracy, the model name can be changed to `base` or `small` with no code structure changes.

### 5.2. Summarization: DistilBART CNN

- **Model**: `sshleifer/distilbart-cnn-12-6`
- **Why this model?**
  - Pre-trained for **abstractive summarization**
  - Produces concise, human-readable summaries
  - Runs locally via Hugging Face `transformers`
- **Hierarchical summarization**
  - Long transcripts are split into **chunks** (by characters)
  - Each chunk is summarized individually
  - Partial summaries are combined and summarized again
  - This approach handles longer videos that would otherwise exceed the model's context length.

---

## 6. Robustness & Long Videos

- **Invalid URLs / download errors**
  - Wrapping the pipeline in `try/except` in `app.py` to catch and display errors.
- **Long videos**
  - Audio length does not break the pipeline: Whisper transcribes the full audio.
  - Long transcripts are broken into chunks in `summarizer.py` to avoid context overflow.
- **Offline requirement**
  - After running `scripts/download_models.py` once and downloading models, STT and summarization do not require the internet.

## 7. Author

**VINOD KUMAR ANCHA**  
Offline YouTube Video Summarizer
