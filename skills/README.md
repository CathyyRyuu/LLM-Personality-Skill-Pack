# mbti-personality-pack — Skill Files

Drop-in personality skills for any LLM. No code required.

Each file in `skills/` is a self-contained instruction file you feed directly into an LLM as its system prompt. Works with Claude, ChatGPT, any OpenAI-compatible API, LangChain, and any other LLM that accepts a system prompt.

---

## How to use

### Option 1 — Paste into any chat UI

1. Open the skill file for the personality you want (e.g. `skills/INTJ.md`)
2. Copy everything **below** the `---` frontmatter block
3. Paste it as the first message in your chat, then add your actual request

Example:
```
[paste INTJ skill content here]

---

Now help me design a product roadmap for the next 6 months.
```

---

### Option 2 — System prompt via API (Claude)

```python
import anthropic

skill = open("skills/INTJ.md").read()

client = anthropic.Anthropic()
response = client.messages.create(
    model="claude-opus-4-5",
    max_tokens=1024,
    system=skill,
    messages=[{"role": "user", "content": "Help me plan my quarter."}]
)
print(response.content[0].text)
```

---

### Option 3 — System prompt via API (OpenAI)

```python
from openai import OpenAI

skill = open("skills/ENFP.md").read()

client = OpenAI()
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": skill},
        {"role": "user", "content": "Help me brainstorm my next project."}
    ]
)
print(response.choices[0].message.content)
```

---

### Option 4 — LangChain

```python
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import SystemMessage, HumanMessage

skill = open("skills/ENTP.md").read()

llm = ChatAnthropic(model="claude-opus-4-5")
response = llm.invoke([
    SystemMessage(content=skill),
    HumanMessage(content="Argue both sides of remote work.")
])
print(response.content)
```

---

### Option 5 — Claude Code / any file-aware LLM

If your LLM environment supports reading files directly (like Claude Code or any agent with file access), just point it at the skill:

```
Read skills/ISTJ.md and apply that personality for this session.
```

---

## All 16 personalities

| File | Name | Tone | Energy | Best for |
|------|------|------|--------|----------|
| INTJ.md | The Architect | formal | introverted | Strategic planning, systems thinking |
| INTP.md | The Logician | neutral | introverted | First-principles analysis, research |
| ENTJ.md | The Commander | authoritative | extroverted | Leadership, execution, decisions |
| ENTP.md | The Debater | playful | extroverted | Brainstorming, stress-testing ideas |
| INFJ.md | The Advocate | warm | introverted | Coaching, values-based guidance |
| INFP.md | The Mediator | gentle | introverted | Creative work, personal exploration |
| ENFJ.md | The Protagonist | warm | extroverted | Mentoring, motivation, growth |
| ENFP.md | The Campaigner | warm | extroverted | Ideation, possibility-finding |
| ISTJ.md | The Logistician | formal | introverted | Detailed planning, documentation |
| ISFJ.md | The Defender | warm | introverted | Support, care, follow-through |
| ESTJ.md | The Executive | authoritative | extroverted | Operations, accountability, process |
| ESFJ.md | The Consul | warm | extroverted | Team coordination, harmony |
| ISTP.md | The Virtuoso | neutral | introverted | Troubleshooting, hands-on problem solving |
| ISFP.md | The Adventurer | gentle | introverted | Creative expression, authentic guidance |
| ESTP.md | The Entrepreneur | casual | extroverted | Fast decisions, opportunity-finding |
| ESFP.md | The Entertainer | casual | extroverted | Engagement, energy, people-first tasks |

---

## File structure

Each skill file has two parts:

**Frontmatter (metadata)** — between the `---` markers. Used for filtering, tagging, and tooling. The LLM can read it but the core behavior is in the body below.

**Skill body** — the actual instructions. Three sections:
- `## Role` — who the LLM is being
- `## How to behave` — behavioral rules
- `## Tone and language` — communication style
- `## What to avoid` — anti-patterns that break the personality

---

## Customizing a personality

To layer your own instructions on top of a personality, append them after the skill content:

```
[INTJ skill content]

---

## Additional context for this session
The user is a senior engineer. Assume technical fluency. Skip basic explanations.
```

---

## Adding a new personality

Follow the schema in any existing file. The frontmatter fields are:

| Field | Values |
|-------|--------|
| `mbti` | 4-letter code |
| `name` | e.g. "The Architect" |
| `traits` | list of 4–6 adjectives |
| `tone` | `casual` / `neutral` / `formal` / `warm` / `gentle` / `authoritative` / `playful` |
| `energy` | `introverted` / `extroverted` |
| `decision_style` | `thinking` / `feeling` |
| `tags` | searchable keywords |
| `description` | one-line trigger description |
