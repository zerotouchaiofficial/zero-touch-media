import asyncio
import os
import tempfile
import yaml
import subprocess

import edge_tts


VOICE_CONFIG = "configs/voice.yaml"
TARGET_TOLERANCE = 0.3  # seconds


def load_voice_config():
    with open(VOICE_CONFIG, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)["voice"]


def get_audio_duration(path: str) -> float:
    result = subprocess.run(
        [
            "ffprobe",
            "-v", "error",
            "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1",
            path,
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    return float(result.stdout.strip())


async def synthesize(
    text: str,
    output_path: str,
    target_seconds: float,
):
    voice = load_voice_config()

    rate = 0.0  # start neutral
    attempt = 0

    while True:
        attempt += 1

        communicate = edge_tts.Communicate(
            text=text,
            voice=voice["name"],
            rate=f"{rate:+.0f}%",
            pitch=f"{voice['pitch']}Hz",
            volume=f"{voice['volume']}%",
        )

        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
            tmp_path = tmp.name

        await communicate.save(tmp_path)

        duration = get_audio_duration(tmp_path)

        delta = target_seconds - duration

        if abs(delta) <= TARGET_TOLERANCE:
            os.replace(tmp_path, output_path)
            break

        # Adjust rate proportionally
        rate += (delta / target_seconds) * 100

        if attempt > 8:
            os.replace(tmp_path, output_path)
            break

    return get_audio_duration(output_path)


def generate_voice(
    script: str,
    output_path: str,
    target_seconds: float,
):
    asyncio.run(
        synthesize(
            text=script,
            output_path=output_path,
            target_seconds=target_seconds,
        )
    )
