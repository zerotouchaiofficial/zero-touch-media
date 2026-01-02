import json
import hashlib
from pathlib import Path
from typing import Dict


MEMORY_FILE = Path("data/memory.json")


def _hash_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def load_memory() -> Dict[str, dict]:
    if not MEMORY_FILE.exists():
        return {"facts": {}, "scripts": {}}

    with open(MEMORY_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_memory(memory: Dict[str, dict]) -> None:
    MEMORY_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(memory, f, indent=2)


def fact_used(fact: str) -> bool:
    memory = load_memory()
    return _hash_text(fact) in memory.get("facts", {})


def script_used(script: str) -> bool:
    memory = load_memory()
    return _hash_text(script) in memory.get("scripts", {})


def mark_fact_used(fact: str, niche: str) -> None:
    memory = load_memory()
    memory.setdefault("facts", {})
    memory["facts"][_hash_text(fact)] = {
        "niche": niche
    }
    save_memory(memory)


def mark_script_used(script: str, niche: str, duration: int) -> None:
    memory = load_memory()
    memory.setdefault("scripts", {})
    memory["scripts"][_hash_text(script)] = {
        "niche": niche,
        "duration_seconds": duration
    }
    save_memory(memory)


if __name__ == "__main__":
    # Manual test
    sample_fact = "The Earth orbits the Sun."
    print("Used before?", fact_used(sample_fact))
    mark_fact_used(sample_fact, "Science")
    print("Used after mark?", fact_used(sample_fact))
