"""
Example: use an MBTI personality with LangChain.

Install:  pip install langchain-core langchain-anthropic
      or: pip install langchain-core langchain-openai
Run:      python examples/example_langchain.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from loader import load
from loader.adapters import build_langchain_prompt_template


def main() -> None:
    # ── Swap this import for langchain_openai.ChatOpenAI if preferred ─────────
    from langchain_anthropic import ChatAnthropic
    llm = ChatAnthropic(model="claude-opus-4-5")  # reads ANTHROPIC_API_KEY from env

    personality = load("ENTP")
    print(f"Loaded: {personality}\n")

    # Build a reusable chain
    chain = build_langchain_prompt_template(personality) | llm

    result = chain.invoke({"user_input": "Argue both sides of working from home vs. office."})
    print(result.content)


if __name__ == "__main__":
    main()
