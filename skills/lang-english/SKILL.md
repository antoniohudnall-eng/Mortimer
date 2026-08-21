---
name: lang-english
description: English (english) translation skill — translate to/from english using C3P0 Universal Translator.
metadata:
  emoji: 🇺🇸
  triggers:
    - translate english
    - english
    - /english
    - English
---

# 🇺🇸 English (english) Language Skill

Translates between english and other languages via C3P0 Protocol Droid.

## Quick Translate

```bash
python3 ~/sandboxes/c3p0/translator.py translate "Hello world" --to en
```

## From english to English

```bash
python3 ~/sandboxes/c3p0/translator.py translate "text in english" --to en
```

## Phrasebook

```bash
python3 ~/sandboxes/c3p0/translator.py phrasebook "common phrase"
```

## Backend

- **Agent:** C3P0 (Protocol Droid)
- **Engine:** Google Translate (deep-translator)
- **Code:** ~/sandboxes/c3p0/translator.py
- **Language code:** `en`
