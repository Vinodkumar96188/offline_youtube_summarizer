"""Offline text summarization module using a transformer-based model.

This module:
1. Chunks long transcripts into manageable pieces.
2. Summarizes each chunk.
3. Optionally performs a second-stage summarization over partial summaries.

It uses the Hugging Face transformers summarization pipeline with a
pre-trained model (e.g., DistilBART CNN).

Author: VINOD KUMAR ANCHA
"""

from typing import List
from transformers import pipeline

# Load summarization pipeline once
# You can change the model to another summarization model if desired.
SUMMARIZATION_MODEL_NAME = "sshleifer/distilbart-cnn-12-6"
summarizer = pipeline("summarization", model=SUMMARIZATION_MODEL_NAME)


def chunk_text(text: str, max_chars: int = 3000) -> List[str]:
    """
    Simple character-based chunking for long transcripts.

    :param text: Full transcript text
    :param max_chars: Maximum characters per chunk
    :return: List of text chunks
    """
    text = text.strip()
    if not text:
        return []

    chunks = []
    start = 0
    while start < len(text):
        end = start + max_chars
        chunks.append(text[start:end])
        start = end
    return chunks


def summarize_chunk(chunk: str) -> str:
    """
    Summarize a single chunk of text.

    We do not force max_length/min_length here; we let the model decide
    an appropriate concise length, which avoids warnings about lengths.

    :param chunk: Input text chunk
    :return: Summary string
    """
    summary = summarizer(chunk)[0]["summary_text"]
    return summary.strip()


def summarize_long_text(text: str) -> str:
    """
    Summarize a potentially long transcript using hierarchical summarization.

    Steps:
    1) Chunk the transcript into pieces within the model's comfortable length.
    2) Summarize each chunk individually.
    3) Concatenate these partial summaries.
    4) Run a final summarization over the combined summary to produce a
       concise, global summary.

    :param text: Full transcript text
    :return: Final concise summary
    """
    text = text.strip()
    if not text:
        return "No transcript text available to summarize."

    chunks = chunk_text(text)
    if not chunks:
        return "No transcript text available to summarize."

    # Stage 1: summarize each chunk
    partial_summaries = [summarize_chunk(c) for c in chunks]

    # If only one chunk, we already have a decent summary
    if len(partial_summaries) == 1:
        return partial_summaries[0]

    # Stage 2: combine partial summaries and summarize again
    combined = " ".join(partial_summaries)
    final = summarize_chunk(combined)

    return final
