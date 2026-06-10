"""
mbti-personality-pack — core loader
Parses MBTI Markdown personality files and returns
a ready-to-use system prompt for any LLM.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

try:
    import yaml
    HAS_YAML = True
except ImportError:
    HAS_YAML = False


# ── Directory that holds all personality .md files ────────────────────────────
_DEFAULT_DIR = Path(__file__).parent.parent / "personalities"


# ── Data model ────────────────────────────────────────────────────────────────

@dataclass
class Personality:
    mbti: str                          # e.g. "INTJ"
    name: str                          # e.g. "The Architect"
    traits: list[str] = field(default_factory=list)
    tone: str = ""
    energy: str = ""
    decision_style: str = ""
    tags: list[str] = field(default_factory=list)
    prompt_body: str = ""              # everything after the frontmatter

    # ── Convenience ───────────────────────────────────────────────────────────

    def as_system_prompt(self, extra_instructions: str = "") -> str:
        """
        Return a complete system prompt string ready to pass to any LLM.
        Optionally append caller-supplied instructions at the end.
        """
        parts = [self.prompt_body.strip()]
        if extra_instructions:
            parts.append(extra_instructions.strip())
        return "\n\n".join(parts)

    def metadata(self) -> dict[str, Any]:
        """Return the frontmatter fields as a plain dict (useful for logging / UIs)."""
        return {
            "mbti": self.mbti,
            "name": self.name,
            "traits": self.traits,
            "tone": self.tone,
            "energy": self.energy,
            "decision_style": self.decision_style,
            "tags": self.tags,
        }

    def __repr__(self) -> str:
        return f"<Personality {self.mbti} – {self.name}>"


# ── Parser ────────────────────────────────────────────────────────────────────

def _parse_frontmatter(raw: str) -> tuple[dict[str, Any], str]:
    """
    Split a Markdown file into (frontmatter_dict, body).
    Works with or without PyYAML installed.
    """
    stripped = raw.strip()
    if not stripped.startswith("---"):
        return {}, stripped

    # Find closing ---
    end = stripped.find("\n---", 3)
    if end == -1:
        return {}, stripped

    fm_text = stripped[3:end].strip()
    body = stripped[end + 4:].strip()

    if HAS_YAML:
        fm = yaml.safe_load(fm_text) or {}
    else:
        fm = _simple_yaml(fm_text)

    return fm, body


def _simple_yaml(text: str) -> dict[str, Any]:
    """
    Minimal YAML parser for the subset used in personality files.
    Handles scalars, inline lists `[a, b, c]`, and block lists.
    Falls back gracefully — no external dependency required.
    """
    result: dict[str, Any] = {}
    current_key: str | None = None
    list_buffer: list[str] | None = None

    for line in text.splitlines():
        if not line.strip() or line.strip().startswith("#"):
            continue

        # Top-level key: value
        if re.match(r"^[a-zA-Z_][a-zA-Z0-9_\-]*\s*:", line) and not line.startswith(" "):
            if list_buffer is not None and current_key:
                result[current_key] = list_buffer
            list_buffer = None

            key, _, rest = line.partition(":")
            key = key.strip()
            val = rest.strip()

            if val.startswith("[") and val.endswith("]"):
                # Inline list
                inner = val[1:-1]
                result[key] = [v.strip().strip("'\"") for v in inner.split(",") if v.strip()]
                current_key = None
            elif val == "":
                # Block list follows
                current_key = key
                list_buffer = []
            else:
                result[key] = val.strip("'\"")
                current_key = key

        # Block list item
        elif line.strip().startswith("- ") and list_buffer is not None:
            list_buffer.append(line.strip()[2:].strip().strip("'\""))

    if list_buffer is not None and current_key:
        result[current_key] = list_buffer

    return result


# ── Public API ────────────────────────────────────────────────────────────────

def load(mbti: str, personalities_dir: str | Path = _DEFAULT_DIR) -> Personality:
    """
    Load a single personality by its 4-letter MBTI code.

    Parameters
    ----------
    mbti : str
        Case-insensitive MBTI code, e.g. "intj" or "ENFP".
    personalities_dir : path-like, optional
        Override the default personalities/ directory.

    Returns
    -------
    Personality

    Raises
    ------
    FileNotFoundError if the personality file doesn't exist.
    """
    code = mbti.upper()
    path = Path(personalities_dir) / f"{code}.md"

    if not path.exists():
        available = list_available(personalities_dir)
        raise FileNotFoundError(
            f"No personality file found for '{code}'. "
            f"Available: {available}"
        )

    raw = path.read_text(encoding="utf-8")
    fm, body = _parse_frontmatter(raw)

    return Personality(
        mbti=fm.get("mbti", code),
        name=fm.get("name", code),
        traits=fm.get("traits", []),
        tone=fm.get("tone", ""),
        energy=fm.get("energy", ""),
        decision_style=fm.get("decision_style", ""),
        tags=fm.get("tags", []),
        prompt_body=body,
    )


def load_all(personalities_dir: str | Path = _DEFAULT_DIR) -> dict[str, Personality]:
    """
    Load all personality files from the directory.

    Returns
    -------
    dict mapping MBTI code → Personality
    """
    base = Path(personalities_dir)
    return {
        p.stem.upper(): load(p.stem, base)
        for p in sorted(base.glob("*.md"))
    }


def list_available(personalities_dir: str | Path = _DEFAULT_DIR) -> list[str]:
    """Return a sorted list of available MBTI codes."""
    return sorted(p.stem.upper() for p in Path(personalities_dir).glob("*.md"))
