---
name: lang-russian
description: Русский (russian) translation skill — translate to/from russian using C3P0 Universal Translator.
metadata:
  emoji: 🇷🇺
  triggers:
    - translate russian
    - russian
    - /russian
    - Русский
---

# 🇷🇺 Русский (russian) Language Skill

Translates between russian and other languages via C3P0 Protocol Droid.

## Quick Translate

```bash
python3 ~/sandboxes/c3p0/translator.py translate "Hello world" --to ru
```

## From russian to English

```bash
python3 ~/sandboxes/c3p0/translator.py translate "text in russian" --to en
```

## Phrasebook

```bash
python3 ~/sandboxes/c3p0/translator.py phrasebook "common phrase"
```

## Backend

- **Agent:** C3P0 (Protocol Droid)
- **Engine:** Google Translate (deep-translator)
- **Code:** ~/sandboxes/c3p0/translator.py
- **Language code:** `ru`
