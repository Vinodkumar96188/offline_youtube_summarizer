"""Pre-download models so that all inference can run fully offline later.

This script will:
1) Load the Whisper model for STT
2) Load the summarization pipeline model

Running this once will cache the models locally.

Author: VINOD KUMAR ANCHA
"""

import whisper
from transformers import pipeline


def download_whisper_model(model_name: str = "tiny"):
    print(f"[Whisper] Downloading/loading model '{model_name}'...")
    _ = whisper.load_model(model_name)
    print("[Whisper] Done.")


def download_summarization_model(model_name: str = "sshleifer/distilbart-cnn-12-6"):
    print(f"[Summarizer] Downloading/loading model '{model_name}'...")
    _ = pipeline("summarization", model=model_name)
    print("[Summarizer] Done.")


if __name__ == "__main__":
    download_whisper_model("tiny")
    download_summarization_model("sshleifer/distilbart-cnn-12-6")
    print("All models downloaded and cached.")
