import os
import requests
import random
from pathlib import Path
import json


UNSPLASH_ENDPOINT = "https://api.unsplash.com/search/photos"
IMAGE_DIR = Path("assets/backgrounds")
MEMORY_PATH = Path("memory/used_images.json")


def _load_memory():
    if MEMORY_PATH.exists():
        return set(json.loads(MEMORY_PATH.read_text()))
    return set()


def _save_memory(data: set):
    MEMORY_PATH.parent.mkdir(parents=True, exist_ok=True)
    MEMORY_PATH.write_text(json.dumps(list(data), indent=2))


def fetch_images(
    query: str,
    count: int,
):
    access_key = os.getenv("UNSPLASH_ACCESS_KEY")
    if not access_key:
        raise RuntimeError("UNSPLASH_ACCESS_KEY not set")

    used_ids = _load_memory()

    headers = {"Authorization": f"Client-ID {access_key}"}

    params = {
        "query": query,
        "orientation": "portrait",
        "per_page": 30,
    }

    resp = requests.get(UNSPLASH_ENDPOINT, headers=headers, params=params, timeout=20)
    resp.raise_for_status()

    results = resp.json().get("results", [])
    random.shuffle(results)

    selected = []

    for item in results:
        if item["id"] in used_ids:
            continue

        url = item["urls"]["regular"]
        image_id = item["id"]

        IMAGE_DIR.mkdir(parents=True, exist_ok=True)
        image_path = IMAGE_DIR / f"{image_id}.jpg"

        img_data = requests.get(url, timeout=20).content
        image_path.write_bytes(img_data)

        selected.append(image_path)
        used_ids.add(image_id)

        if len(selected) >= count:
            break

    if len(selected) < count:
        raise RuntimeError("Not enough fresh images available")

    _save_memory(used_ids)

    return selected
