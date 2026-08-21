---
name: lang-japanese
description: 日本語 (japanese) translation skill — translate to/from japanese using C3P0 Universal Translator.
metadata:
  emoji: 🇯🇵
  triggers:
    - translate japanese
    - japanese
    - /japanese
    - 日本語
---

# 🇯🇵 日本語 (japanese) Language Skill

Translates between japanese and other languages via C3P0 Protocol Droid.

## Quick Translate

```bash
python3 ~/sandboxes/c3p0/translator.py translate "Hello world" --to ja
```

## From japanese to English

```bash
python3 ~/sandboxes/c3p0/translator.py translate "text in japanese" --to en
```

## Phrasebook

```bash
python3 ~/sandboxes/c3p0/translator.py phrasebook "common phrase"
```

## Backend

- **Agent:** C3P0 (Protocol Droid)
- **Engine:** Google Translate (deep-translator)
- **Code:** ~/sandboxes/c3p0/translator.py
- **Language code:** `ja`
