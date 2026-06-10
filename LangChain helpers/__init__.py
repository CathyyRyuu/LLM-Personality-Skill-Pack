"""
mbti-personality-pack loader
----------------------------
Public API surface. Import from here.

    from loader import load, load_all, list_available
    from loader.adapters import build_claude_kwargs, build_openai_kwargs, build_langchain_prompt_template
"""

from .personality import Personality, load, load_all, list_available

__all__ = [
    "Personality",
    "load",
    "load_all",
    "list_available",
]
