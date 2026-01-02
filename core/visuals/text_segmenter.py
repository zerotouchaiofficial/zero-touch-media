import math
from typing import List, Dict


AVERAGE_WPM = 150  # calm narration


def estimate_seconds(text: str) -> float:
    words = len(text.split())
    return (words / AVERAGE_WPM) * 60


def split_sentences(script: str) -> List[str]:
    raw = script.replace("\n", " ").split(". ")
    return [s.strip().rstrip(".") for s in raw if len(s.strip()) > 10]


def build_text_segments(
    script: str,
    target_seconds: float,
    min_segment: float,
    max_segment: float,
) -> List[Dict]:
    sentences = split_sentences(script)

    segments = []
    current_text = []
    current_time = 0.0
    start_time = 0.0

    for sentence in sentences:
        est = estimate_seconds(sentence)

        if current_time + est <= max_segment:
            current_text.append(sentence)
            current_time += est
        else:
            if current_time >= min_segment:
                segments.append(
                    {
                        "start": round(start_time, 2),
                        "duration": round(current_time, 2),
                        "text": ". ".join(current_text) + ".",
                    }
                )
                start_time += current_time
                current_text = [sentence]
                current_time = est
            else:
                current_text.append(sentence)
                current_time += est

    if current_text:
        segments.append(
            {
                "start": round(start_time, 2),
                "duration": round(current_time, 2),
                "text": ". ".join(current_text) + ".",
            }
        )

    # Safety normalization (trim or merge if needed)
    total = sum(s["duration"] for s in segments)
    scale = target_seconds / total if total > 0 else 1

    for s in segments:
        s["start"] = round(s["start"] * scale, 2)
        s["duration"] = round(s["duration"] * scale, 2)

    return segments
