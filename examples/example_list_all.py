"""
Example: load all 16 personalities and inspect metadata.
No LLM API key required — just demonstrates the loader.

Run: python examples/example_list_all.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from loader import load_all, list_available


def main() -> None:
    print("Available personalities:", list_available())
    print()

    all_personalities = load_all()

    for code, p in all_personalities.items():
        meta = p.metadata()
        print(f"{code:4s}  {p.name:<22}  tone={meta['tone']:<15} tags={meta['tags']}")

    print(f"\nTotal: {len(all_personalities)} personalities loaded.")

    # Show the full system prompt for one
    print("\n" + "─" * 60)
    print("Sample system prompt for INFJ:")
    print("─" * 60)
    print(all_personalities["INFJ"].as_system_prompt())


if __name__ == "__main__":
    main()
