import random
import yaml

from core.facts.fetch_facts import fetch_facts
from core.facts.rewrite_and_time import build_script, estimate_duration_seconds
from core.memory.memory_store import (
    fact_used,
    script_used,
    mark_fact_used,
    mark_script_used,
)


NICHES_FILE = "configs/niches.yaml"


def load_niches() -> list[str]:
    with open(NICHES_FILE, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return data.get("niches", [])


def generate_content(target_seconds: int) -> dict:
    niches = load_niches()
    if not niches:
        raise RuntimeError("No niches configured")

    niche = random.choice(niches)

    raw_facts = fetch_facts(niche, max_sentences=30)

    if not raw_facts:
        raise RuntimeError("No facts fetched")

    # Filter out used facts
    fresh_facts = [f for f in raw_facts if not fact_used(f)]

    if not fresh_facts:
        raise RuntimeError("No unused facts available")

    script = build_script(fresh_facts, target_seconds)

    if not script:
        raise RuntimeError("Script generation failed")

    if script_used(script):
        raise RuntimeError("Generated script already used")

    # Mark facts used
    for fact in fresh_facts:
        mark_fact_used(fact, niche)

    # Mark script used
    mark_script_used(script, niche, target_seconds)

    duration = estimate_duration_seconds(script)

    return {
        "niche": niche,
        "script": script,
        "estimated_seconds": round(duration, 2),
    }


if __name__ == "__main__":
    # Manual test run
    TARGET_SECONDS = 60  # change to 600 later for long videos

    result = generate_content(TARGET_SECONDS)

    print("\n--- GENERATED CONTENT ---")
    print("Niche:", result["niche"])
    print("Estimated Duration:", result["estimated_seconds"], "seconds")
    print("\nScript:\n")
    print(result["script"])

