import subprocess
from pathlib import Path


TOLERANCE = 0.25  # seconds


def get_duration(path: Path) -> float:
    result = subprocess.run(
        [
            "ffprobe",
            "-v", "error",
            "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1",
            str(path),
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    return float(result.stdout.strip())


def validate_duration(
    video_path: Path,
    audio_path: Path,
    target_seconds: float,
):
    video_dur = get_duration(video_path)
    audio_dur = get_duration(audio_path)

    if abs(video_dur - target_seconds) > TOLERANCE:
        raise RuntimeError(
            f"Video duration {video_dur:.2f}s != target {target_seconds}s"
        )

    if abs(audio_dur - target_seconds) > TOLERANCE:
        raise RuntimeError(
            f"Audio duration {audio_dur:.2f}s != target {target_seconds}s"
        )

    return round(video_dur, 2)
