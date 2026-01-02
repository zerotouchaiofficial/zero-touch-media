import json
import hashlib
from datetime import datetime
from pathlib import Path
from typing import List


ASSET_LOG_PATH = Path("memory/final_assets.json")


def _load():
    if ASSET_LOG_PATH.exists():
        return json.loads(ASSET_LOG_PATH.read_text(encoding="utf-8"))
    return []


def _save(data):
    ASSET_LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    ASSET_LOG_PATH.write_text(
        json.dumps(data, indent=2),
        encoding="utf-8",
    )


def log_asset(
    niche: str,
    script: str,
    voice_name: str,
    target_seconds: float,
    actual_seconds: float,
    background_images: List[str],
    output_file: str,
):
    logs = _load()

    asset_id = hashlib.sha256(
        f"{script}{output_file}{actual_seconds}".encode("utf-8")
    ).hexdigest()

    logs.append(
        {
            "asset_id": asset_id,
            "niche": niche,
            "script_hash": hashlib.sha256(script.encode("utf-8")).hexdigest(),
            "voice": voice_name,
            "target_seconds": target_seconds,
            "actual_seconds": round(actual_seconds, 2),
            "background_images": background_images,
            "output": output_file,
            "timestamp": datetime.utcnow().isoformat() + "Z",
        }
    )

    _save(logs)
