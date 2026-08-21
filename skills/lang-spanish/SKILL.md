---
name: lang-spanish
description: Español (spanish) translation skill — translate to/from spanish using C3P0 Universal Translator.
metadata:
  emoji: 🇪🇸
  triggers:
    - translate spanish
    - spanish
    - /spanish
    - Español
---

# 🇪🇸 Español (spanish) Language Skill

Translates between spanish and other languages via C3P0 Protocol Droid.

## Quick Translate

```bash
python3 ~/sandboxes/c3p0/translator.py translate "Hello world" --to es
```

## From spanish to English

```bash
python3 ~/sandboxes/c3p0/translator.py translate "text in spanish" --to en
```

## Phrasebook

```bash
python3 ~/sandboxes/c3p0/translator.py phrasebook "common phrase"
```

## Backend

- **Agent:** C3P0 (Protocol Droid)
- **Engine:** Google Translate (deep-translator)
- **Code:** ~/sandboxes/c3p0/translator.py
- **Language code:** `es`
