"""Offline speech-to-text (STT) module using Whisper.

This module:
1. Converts the downloaded audio to 16 kHz mono WAV using ffmpeg.
2. Runs Whisper locally to generate a plain text transcript (no timestamps).

Author: VINOD KUMAR ANCHA
"""

import os
import subprocess
import tempfile
import whisper
import torch

# Select device: GPU if available, otherwise CPU
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
print(f"[STT] Using device: {DEVICE}")

# Choose Whisper model size: "tiny", "base", "small", ...
# For CPU-only environments, "tiny" or "base" is recommended.
WHISPER_MODEL_NAME = "tiny"

# Load Whisper model once at import time
model = whisper.load_model(WHISPER_MODEL_NAME, device=DEVICE)


def convert_to_wav(input_audio: str) -> str:
    """
    Convert input audio (e.g., .m4a) to 16 kHz mono WAV using ffmpeg.

    :param input_audio: Path to the source audio file
    :return: Path to the converted WAV file
    """
    tmp_wav = os.path.join(tempfile.gettempdir(), "audio_16k.wav")
    cmd = [
        "ffmpeg",
        "-i", input_audio,   # input file
        "-ar", "16000",      # sample rate
        "-ac", "1",          # channels: mono
        "-f", "wav",
        tmp_wav,
        "-y"                 # overwrite without asking
    ]
    subprocess.run(cmd, check=True)
    return tmp_wav


def transcribe_audio(audio_path: str) -> str:
    """
    Run offline speech-to-text using Whisper and return a plain text transcript.

    No timestamps or segment logs are printed. The result is a single text
    string representing the entire transcript.

    :param audio_path: Path to the original downloaded audio file
    :return: Transcript as a single string
    """
    wav_path = convert_to_wav(audio_path)
    fp16 = (DEVICE == "cuda")

    result = model.transcribe(
        wav_path,
        fp16=fp16,
        verbose=False,  # suppress segment-wise logs
        # Set language if you know it (for speed); otherwise let Whisper detect.
        # language="en",
    )

    text = result.get("text", "").strip()
    return text
