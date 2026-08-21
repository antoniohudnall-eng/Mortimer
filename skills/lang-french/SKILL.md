---
name: lang-french
description: Français (french) translation skill — translate to/from french using C3P0 Universal Translator.
metadata:
  emoji: 🇫🇷
  triggers:
    - translate french
    - french
    - /french
    - Français
---

# 🇫🇷 Français (french) Language Skill

Translates between french and other languages via C3P0 Protocol Droid.

## Quick Translate

```bash
python3 ~/sandboxes/c3p0/translator.py translate "Hello world" --to fr
```

## From french to English

```bash
python3 ~/sandboxes/c3p0/translator.py translate "text in french" --to en
```

## Phrasebook

```bash
python3 ~/sandboxes/c3p0/translator.py phrasebook "common phrase"
```

## Backend

- **Agent:** C3P0 (Protocol Droid)
- **Engine:** Google Translate (deep-translator)
- **Code:** ~/sandboxes/c3p0/translator.py
- **Language code:** `fr`
