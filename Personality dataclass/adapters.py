"""
mbti-personality-pack — LLM adapters
Thin wrappers that inject a Personality into Claude, OpenAI, and LangChain.
None of these are required — the loader alone gives you the system prompt string.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from .personality import Personality


# ── Anthropic Claude ───────────────────────────────────────────────────────────

def build_claude_kwargs(
    personality: "Personality",
    *,
    model: str = "claude-opus-4-5",
    max_tokens: int = 1024,
    extra_instructions: str = "",
    **kwargs: Any,
) -> dict[str, Any]:
    """
    Return a dict of kwargs ready to pass directly to anthropic.Anthropic().messages.create().

    Usage
    -----
    import anthropic
    from loader.personality import load
    from loader.adapters import build_claude_kwargs

    client = anthropic.Anthropic()
    p = load("INTJ")
    response = client.messages.create(
        messages=[{"role": "user", "content": "Help me plan my week."}],
        **build_claude_kwargs(p)
    )
    """
    return {
        "model": model,
        "max_tokens": max_tokens,
        "system": personality.as_system_prompt(extra_instructions),
        **kwargs,
    }


# ── OpenAI ChatCompletion ──────────────────────────────────────────────────────

def build_openai_messages(
    personality: "Personality",
    user_messages: list[dict[str, str]],
    *,
    extra_instructions: str = "",
) -> list[dict[str, str]]:
    """
    Prepend the personality system prompt to a list of OpenAI-style messages.

    Usage
    -----
    from openai import OpenAI
    from loader.personality import load
    from loader.adapters import build_openai_messages

    client = OpenAI()
    p = load("ENFP")
    messages = build_openai_messages(p, [{"role": "user", "content": "Brainstorm ideas for my app."}])
    response = client.chat.completions.create(model="gpt-4o", messages=messages)
    """
    system_msg = {"role": "system", "content": personality.as_system_prompt(extra_instructions)}
    return [system_msg, *user_messages]


def build_openai_kwargs(
    personality: "Personality",
    user_messages: list[dict[str, str]],
    *,
    model: str = "gpt-4o",
    extra_instructions: str = "",
    **kwargs: Any,
) -> dict[str, Any]:
    """
    Return a dict of kwargs ready for openai.OpenAI().chat.completions.create().

    Usage
    -----
    response = client.chat.completions.create(
        **build_openai_kwargs(p, [{"role": "user", "content": "..."}])
    )
    """
    return {
        "model": model,
        "messages": build_openai_messages(personality, user_messages, extra_instructions=extra_instructions),
        **kwargs,
    }


# ── LangChain ─────────────────────────────────────────────────────────────────

def build_langchain_system_message(
    personality: "Personality",
    extra_instructions: str = "",
) -> Any:
    """
    Return a LangChain SystemMessage with the personality prompt.

    Usage
    -----
    from langchain_anthropic import ChatAnthropic   # or ChatOpenAI
    from langchain_core.messages import HumanMessage
    from loader.personality import load
    from loader.adapters import build_langchain_system_message

    llm = ChatAnthropic(model="claude-opus-4-5")
    p = load("ENTP")
    system = build_langchain_system_message(p)
    response = llm.invoke([system, HumanMessage(content="Argue both sides of remote work.")])
    """
    try:
        from langchain_core.messages import SystemMessage
    except ImportError:
        raise ImportError(
            "langchain-core is not installed. "
            "Run: pip install langchain-core"
        )

    return SystemMessage(content=personality.as_system_prompt(extra_instructions))


def build_langchain_prompt_template(
    personality: "Personality",
    extra_instructions: str = "",
) -> Any:
    """
    Return a LangChain ChatPromptTemplate with the personality baked in.

    Usage
    -----
    from langchain_anthropic import ChatAnthropic
    from loader.personality import load
    from loader.adapters import build_langchain_prompt_template

    llm = ChatAnthropic(model="claude-opus-4-5")
    p = load("ISTJ")
    chain = build_langchain_prompt_template(p) | llm
    response = chain.invoke({"user_input": "Explain version control to a beginner."})
    """
    try:
        from langchain_core.prompts import ChatPromptTemplate
    except ImportError:
        raise ImportError(
            "langchain-core is not installed. "
            "Run: pip install langchain-core"
        )

    return ChatPromptTemplate.from_messages([
        ("system", personality.as_system_prompt(extra_instructions)),
        ("human", "{user_input}"),
    ])
