---
name: lang-polish
description: Polski (polish) translation skill — translate to/from polish using C3P0 Universal Translator.
metadata:
  emoji: 🇵🇱
  triggers:
    - translate polish
    - polish
    - /polish
    - Polski
---

# 🇵🇱 Polski (polish) Language Skill

Translates between polish and other languages via C3P0 Protocol Droid.

## Quick Translate

```bash
python3 ~/sandboxes/c3p0/translator.py translate "Hello world" --to pl
```

## From polish to English

```bash
python3 ~/sandboxes/c3p0/translator.py translate "text in polish" --to en
```

## Phrasebook

```bash
python3 ~/sandboxes/c3p0/translator.py phrasebook "common phrase"
```

## Backend

- **Agent:** C3P0 (Protocol Droid)
- **Engine:** Google Translate (deep-translator)
- **Code:** ~/sandboxes/c3p0/translator.py
- **Language code:** `pl`
