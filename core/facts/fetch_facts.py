import requests
import re


WIKIPEDIA_API = "https://en.wikipedia.org/api/rest_v1/page/summary/"


def fetch_facts(topic: str, max_sentences: int = 20) -> list[str]:
    """
    Fetch factual sentences from Wikipedia for a given topic.

    Args:
        topic (str): Topic or page title
        max_sentences (int): Maximum number of sentences to return

    Returns:
        List of cleaned factual sentences
    """
    topic = topic.replace(" ", "_")
    url = WIKIPEDIA_API + topic

    response = requests.get(url, timeout=10)

    if response.status_code != 200:
        return []

    data = response.json()
    extract = data.get("extract", "")

    if not extract:
        return []

    # Clean citations like [1], [2]
    extract = re.sub(r"\[\d+\]", "", extract)

    # Split into sentences
    sentences = re.split(r"(?<=[.!?]) +", extract)

    # Filter short or malformed sentences
    facts = [
        s.strip()
        for s in sentences
        if len(s.strip()) > 40
    ]

    return facts[:max_sentences]


if __name__ == "__main__":
    # Simple manual test
    sample = fetch_facts("Space")
    for line in sample:
        print("-", line)
