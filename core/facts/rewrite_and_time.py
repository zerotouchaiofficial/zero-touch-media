import random
import re
from typing import List


WORDS_PER_MINUTE = 130


def estimate_duration_seconds(text: str) -> float:
    words = len(text.split())
    minutes = words / WORDS_PER_MINUTE
    return minutes * 60


def clean_sentence(sentence: str) -> str:
    sentence = sentence.strip()
    sentence = re.sub(r"\s+", " ", sentence)
    if not sentence.endswith((".", "!", "?")):
        sentence += "."
    return sentence


def rewrite_sentence(sentence: str) -> str:
    """
    Light rewriting to sound natural without hallucinating facts.
    """
    sentence = clean_sentence(sentence)

    starters = [
        "Interestingly,",
        "In simple terms,",
        "Researchers have found that",
        "It’s important to know that",
        "One fascinating fact is that",
        "What many people don’t realize is that",
    ]

    if random.random() < 0.5:
        return f"{random.choice(starters)} {sentence[0].lower() + sentence[1:]}"
    return sentence


def build_script(
    facts: List[str],
    target_seconds: int
) -> str:
    """
    Build a narration script that fits the target duration.
    """
    script_lines = []
    current_text = ""

    for fact in facts:
        rewritten = rewrite_sentence(fact)
        candidate = current_text + " " + rewritten

        if estimate_duration_seconds(candidate) > target_seconds:
            break

        script_lines.append(rewritten)
        current_text = " ".join(script_lines)

    return current_text.strip()


if __name__ == "__main__":
    # Manual test
    sample_facts = [
        "The universe is approximately 13.8 billion years old",
        "Light from the Sun takes about eight minutes to reach Earth",
        "Neutron stars are among the densest objects in the universe",
    ]

    script = build_script(sample_facts, target_seconds=60)
    print(script)
    print("Estimated seconds:", estimate_duration_seconds(script))
