---
name: lang-arabic
description: العربية (arabic) translation skill — translate to/from arabic using C3P0 Universal Translator.
metadata:
  emoji: 🇸🇦
  triggers:
    - translate arabic
    - arabic
    - /arabic
    - العربية
---

# 🇸🇦 العربية (arabic) Language Skill

Translates between arabic and other languages via C3P0 Protocol Droid.

## Quick Translate

```bash
python3 ~/sandboxes/c3p0/translator.py translate "Hello world" --to ar
```

## From arabic to English

```bash
python3 ~/sandboxes/c3p0/translator.py translate "text in arabic" --to en
```

## Phrasebook

```bash
python3 ~/sandboxes/c3p0/translator.py phrasebook "common phrase"
```

## Backend

- **Agent:** C3P0 (Protocol Droid)
- **Engine:** Google Translate (deep-translator)
- **Code:** ~/sandboxes/c3p0/translator.py
- **Language code:** `ar`
