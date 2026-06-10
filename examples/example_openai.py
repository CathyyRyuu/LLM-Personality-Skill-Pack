"""
Example: use an MBTI personality with OpenAI ChatGPT.

Install:  pip install openai
Run:      python examples/example_openai.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from openai import OpenAI
from loader import load
from loader.adapters import build_openai_kwargs


def main() -> None:
    client = OpenAI()  # reads OPENAI_API_KEY from env

    personality = load("ENFP")
    print(f"Loaded: {personality}")
    print(f"Tone: {personality.tone} | Energy: {personality.energy}\n")

    user_messages = [{"role": "user", "content": "I'm stuck on what side project to start. Help me brainstorm."}]

    response = client.chat.completions.create(
        **build_openai_kwargs(personality, user_messages)
    )

    print(response.choices[0].message.content)


if __name__ == "__main__":
    main()
