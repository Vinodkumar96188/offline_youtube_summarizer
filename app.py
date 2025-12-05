"""Offline YouTube Video Summarizer

End-to-end system that:
1. Takes a YouTube URL as input
2. Downloads the audio track
3. Transcribes the audio using an offline STT model (Whisper)
4. Summarizes the transcript using an offline summarization model
5. Returns a concise summary (CLI or via a simple web interface)

Author: VINOD KUMAR ANCHA
"""

import os
import sys
import traceback

from downloader import download_audio_from_youtube
from stt import transcribe_audio
from summarizer import summarize_long_text


def run_pipeline(url: str) -> tuple[str, str]:
    """
    Run the full pipeline: URL -> audio -> transcript -> summary.

    :param url: Public YouTube video URL
    :return: (transcript, summary)
    """
    # 1. Download audio
    print("[1/3] Downloading audio from YouTube...")
    audio_path = download_audio_from_youtube(url)
    print(f"[INFO] Audio downloaded to: {audio_path}")

    # 2. Transcribe audio (offline STT)
    print("[2/3] Transcribing audio (offline Whisper)...")
    transcript = transcribe_audio(audio_path)
    print(f"[INFO] Transcript length: {len(transcript)} characters")

    # 3. Summarize transcript (offline)
    print("[3/3] Summarizing transcript (offline summarizer)...")
    summary = summarize_long_text(transcript)

    return transcript, summary


# =======================
# CLI MODE
# =======================

def main_cli():
    """
    CLI entrypoint.

    Usage:
        python app.py "YOUTUBE_URL"
    """
    if len(sys.argv) != 2:
        print("Usage: python app.py \"YOUTUBE_URL\"")
        sys.exit(1)

    url = sys.argv[1].strip()
    if not url:
        print("Error: Empty URL.")
        sys.exit(1)

    try:
        transcript, summary = run_pipeline(url)

        print("\n=== SUMMARY ===\n")
        print(summary)

        # If you also want to show full transcript, uncomment:
        # print("\n=== FULL TRANSCRIPT ===\n")
        # print(transcript)

    except Exception as e:
        print("\n[ERROR] An exception occurred during processing:")
        print(e)
        traceback.print_exc()


# =======================
# FLASK WEB MODE (BONUS)
# =======================

def create_flask_app():
    """
    Create a simple Flask app that exposes the same pipeline via a web form.
    """
    from flask import Flask, request, render_template_string

    app = Flask(__name__)

    HTML = """
    <!doctype html>
    <title>Offline YouTube Video Summarizer</title>
    <h1>Offline YouTube Video Summarizer</h1>
    <p>Paste a public YouTube URL and get a concise offline-generated summary.</p>
    <form method="POST">
      <label for="url">YouTube URL:</label><br>
      <input type="text" id="url" name="url" style="width: 400px;" required>
      <button type="submit">Summarize</button>
    </form>

    {% if error %}
      <p style="color:red;"><strong>Error:</strong> {{ error }}</p>
    {% endif %}

    {% if summary %}
      <hr>
      <h2>Summary</h2>
      <p>{{ summary }}</p>

      <details>
        <summary>Show full transcript</summary>
        <pre style="white-space: pre-wrap;">{{ transcript }}</pre>
      </details>
    {% endif %}
    """

    @app.route("/", methods=["GET", "POST"])
    def index():
        summary = None
        transcript = None
        error = None

        if request.method == "POST":
            url = request.form.get("url", "").strip()
            if not url:
                error = "Please provide a YouTube URL."
            else:
                try:
                    transcript, summary = run_pipeline(url)
                except Exception as e:
                    error = str(e)

        return render_template_string(
            HTML,
            summary=summary,
            transcript=transcript,
            error=error,
        )

    return app


if __name__ == "__main__":
    mode = os.environ.get("APP_MODE", "cli").lower()

    if mode == "flask":
        # Run Flask web app (bonus)
        flask_app = create_flask_app()
        flask_app.run(host="0.0.0.0", port=5000, debug=True)
    else:
        # Default: CLI mode
        main_cli()
