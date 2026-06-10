# mbti-personality-pack

A plug-and-play collection of all 16 Myers-Briggs personality wrappers for any LLM.  
No framework required. No frontend. Just system prompts that work.

---

## What it is

Each MBTI type ships as a **Markdown file** with:
- A YAML frontmatter block of structured metadata (traits, tone, tags, energy, decision style)
- A complete **system prompt** you inject directly into any LLM

A thin Python **loader** parses those files and returns ready-to-use kwargs for:
- **Anthropic Claude** (`anthropic` SDK)
- **OpenAI ChatGPT** (`openai` SDK)
- **LangChain** (`langchain-core`)

---

## Repository layout

```
mbti-personality-pack/
│
├── personalities/          # 16 Markdown personality files
│   ├── INTJ.md
│   ├── ENFP.md
│   └── ... (all 16 types)
│
├── loader/
│   ├── __init__.py         # Public API: load, load_all, list_available
│   ├── personality.py      # Parser + Personality dataclass
│   └── adapters.py         # Claude / OpenAI / LangChain helpers
│
├── examples/
│   ├── example_claude.py
│   ├── example_openai.py
│   ├── example_langchain.py
│   └── example_list_all.py
│
└── docs/
    └── personality_schema.md
```

---

## Quick start

### No dependencies needed (raw system prompt)

```python
from loader import load

p = load("INTJ")
print(p.as_system_prompt())   # pass this string to any LLM as the system prompt
```

### Anthropic Claude

```python
import anthropic
from loader import load
from loader.adapters import build_claude_kwargs

client = anthropic.Anthropic()
p = load("INTJ")

response = client.messages.create(
    messages=[{"role": "user", "content": "Help me plan my quarter."}],
    **build_claude_kwargs(p),
)
print(response.content[0].text)
```

### OpenAI ChatGPT

```python
from openai import OpenAI
from loader import load
from loader.adapters import build_openai_kwargs

client = OpenAI()
p = load("ENFP")

response = client.chat.completions.create(
    **build_openai_kwargs(p, [{"role": "user", "content": "Help me brainstorm."}])
)
print(response.choices[0].message.content)
```

### LangChain

```python
from langchain_anthropic import ChatAnthropic   # or ChatOpenAI
from loader import load
from loader.adapters import build_langchain_prompt_template

llm = ChatAnthropic(model="claude-opus-4-5")
p = load("ENTP")

chain = build_langchain_prompt_template(p) | llm
result = chain.invoke({"user_input": "Argue both sides of remote work."})
print(result.content)
```

---

## Personality metadata

Every personality file exposes structured metadata:

```python
p = load("INFJ")
print(p.metadata())
# {
#   "mbti": "INFJ",
#   "name": "The Advocate",
#   "traits": ["insightful", "empathetic", "principled", "visionary", "private"],
#   "tone": "warm",
#   "energy": "introverted",
#   "decision_style": "feeling",
#   "tags": ["counselor", "idealist", "deep-listener", "values-driven"]
# }
```

---

## All 16 personalities

| Code | Name | Tone | Energy |
|------|------|------|--------|
| INTJ | The Architect | formal | introverted |
| INTP | The Logician | neutral | introverted |
| ENTJ | The Commander | authoritative | extroverted |
| ENTP | The Debater | playful | extroverted |
| INFJ | The Advocate | warm | introverted |
| INFP | The Mediator | gentle | introverted |
| ENFJ | The Protagonist | warm | extroverted |
| ENFP | The Campaigner | warm | extroverted |
| ISTJ | The Logistician | formal | introverted |
| ISFJ | The Defender | warm | introverted |
| ESTJ | The Executive | authoritative | extroverted |
| ESFJ | The Consul | warm | extroverted |
| ISTP | The Virtuoso | neutral | introverted |
| ISFP | The Adventurer | gentle | introverted |
| ESTP | The Entrepreneur | casual | extroverted |
| ESFP | The Entertainer | casual | extroverted |

---

## Adding your own personality

1. Create `personalities/XXXX.md` following the schema in `docs/personality_schema.md`
2. It is automatically discovered by `load_all()` and `list_available()`

---

## Requirements

- Python 3.9+
- No required dependencies for the loader
- `pyyaml` *(optional)* — improves frontmatter parsing robustness
- `anthropic` — only needed for Claude examples
- `openai` — only needed for OpenAI examples
- `langchain-core` + `langchain-anthropic` or `langchain-openai` — only needed for LangChain examples
