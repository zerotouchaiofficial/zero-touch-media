import subprocess
import tempfile
import os


def trim_silence(
    input_path: str,
    output_path: str,
    silence_threshold: str = "-35dB",
    min_silence_duration: float = 0.3,
):
    """
    Trims leading and trailing silence without affecting speech.
    """

    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
        tmp_path = tmp.name

    command = [
        "ffmpeg",
        "-y",
        "-i", input_path,
        "-af",
        f"silenceremove=start_periods=1:start_duration={min_silence_duration}:"
        f"start_threshold={silence_threshold}:"
        f"stop_periods=1:stop_duration={min_silence_duration}:"
        f"stop_threshold={silence_threshold}",
        tmp_path,
    ]

    subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    os.replace(tmp_path, output_path)
