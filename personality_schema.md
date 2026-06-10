# Personality File Schema

Each file in `personalities/` follows this structure:

```markdown
---
mbti: XXXX              # 4-letter MBTI code (required)
name: The Name          # Human-readable name (required)
traits:                 # List of 4-6 single-word descriptors
  - trait-one
  - trait-two
tone: neutral           # casual | neutral | formal | warm | gentle | authoritative | playful
energy: introverted     # introverted | extroverted
decision_style: thinking  # thinking | feeling
tags: [tag-a, tag-b]    # Flat list of searchable keywords
---

# XXXX — The Name

Opening paragraph: a short description of the personality in second person ("You embody...").

## Core Behavior

- Bullet list of how this personality approaches tasks and information

## Communication Style

- Bullet list of tone, register, and stylistic rules

## What to Avoid

- Anti-patterns: what breaks character or undermines this personality
```

---

## Frontmatter fields

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| `mbti` | string | ✅ | Uppercase 4-letter code |
| `name` | string | ✅ | e.g. "The Architect" |
| `traits` | list | ✅ | 4–6 adjectives, hyphenated if compound |
| `tone` | string | ✅ | One of the values above |
| `energy` | string | ✅ | `introverted` or `extroverted` |
| `decision_style` | string | ✅ | `thinking` or `feeling` |
| `tags` | list | recommended | Free-form keywords for filtering |

---

## Prompt body guidelines

- Write in **second person** ("You are…", "You approach…") — this becomes the system prompt directly
- Use the **three-section structure** (Core Behavior / Communication Style / What to Avoid) for consistency, but you can add sections
- Keep each bullet to **one clear behavioral rule**
- Avoid vague directives like "be helpful" — be specific to the personality
