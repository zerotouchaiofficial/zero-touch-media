import json
import hashlib
from datetime import datetime
from pathlib import Path


VOICE_MEMORY_PATH = Path("memory/voice_logs.json")


def _load():
    if VOICE_MEMORY_PATH.exists():
        return json.loads(VOICE_MEMORY_PATH.read_text(encoding="utf-8"))
    return []


def _save(data):
    VOICE_MEMORY_PATH.parent.mkdir(parents=True, exist_ok=True)
    VOICE_MEMORY_PATH.write_text(
        json.dumps(data, indent=2),
        encoding="utf-8",
    )


def log_voice(
    script: str,
    voice_name: str,
    target_seconds: float,
    actual_seconds: float,
    output_file: str,
):
    logs = _load()

    script_hash = hashlib.sha256(script.encode("utf-8")).hexdigest()

    logs.append(
        {
            "script_hash": script_hash,
            "voice": voice_name,
            "target_seconds": target_seconds,
            "actual_seconds": round(actual_seconds, 3),
            "output": output_file,
            "timestamp": datetime.utcnow().isoformat() + "Z",
        }
    )

    _save(logs)
