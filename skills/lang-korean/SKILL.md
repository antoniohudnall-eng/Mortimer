---
name: lang-korean
description: 한국어 (korean) translation skill — translate to/from korean using C3P0 Universal Translator.
metadata:
  emoji: 🇰🇷
  triggers:
    - translate korean
    - korean
    - /korean
    - 한국어
---

# 🇰🇷 한국어 (korean) Language Skill

Translates between korean and other languages via C3P0 Protocol Droid.

## Quick Translate

```bash
python3 ~/sandboxes/c3p0/translator.py translate "Hello world" --to ko
```

## From korean to English

```bash
python3 ~/sandboxes/c3p0/translator.py translate "text in korean" --to en
```

## Phrasebook

```bash
python3 ~/sandboxes/c3p0/translator.py phrasebook "common phrase"
```

## Backend

- **Agent:** C3P0 (Protocol Droid)
- **Engine:** Google Translate (deep-translator)
- **Code:** ~/sandboxes/c3p0/translator.py
- **Language code:** `ko`
