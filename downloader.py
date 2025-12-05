"""YouTube audio downloader module.

Given a public YouTube URL, this module downloads the best available audio
track using yt-dlp and returns the local file path.

Author: VINOD KUMAR ANCHA
"""

import os
import tempfile
import yt_dlp


def download_audio_from_youtube(url: str) -> str:
    """
    Download best audio from a YouTube URL and return local file path.

    :param url: Public YouTube video URL
    :return: Path to downloaded audio file (e.g., .m4a)
    """
    tmp_dir = tempfile.mkdtemp(prefix="yt_audio_")
    audio_path = os.path.join(tmp_dir, "audio.m4a")

    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": audio_path,
        "noplaylist": True,
        "quiet": True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    return audio_path
