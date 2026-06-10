"""
Example: use an MBTI personality with Anthropic Claude.

Install:  pip install anthropic
Run:      python examples/example_claude.py
"""

import sys
from pathlib import Path

# Allow running from the repo root without installing the package
sys.path.insert(0, str(Path(__file__).parent.parent))

import anthropic
from loader import load
from loader.adapters import build_claude_kwargs


def main() -> None:
    client = anthropic.Anthropic()  # reads ANTHROPIC_API_KEY from env

    personality = load("INTJ")
    print(f"Loaded: {personality}")
    print(f"Traits: {personality.traits}\n")

    response = client.messages.create(
        messages=[{"role": "user", "content": "Help me prioritize my goals for this quarter."}],
        **build_claude_kwargs(personality),
    )

    print(response.content[0].text)


if __name__ == "__main__":
    main()
