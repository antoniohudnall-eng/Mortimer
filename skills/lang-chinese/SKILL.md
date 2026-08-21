---
name: lang-chinese
description: 中文 (chinese) translation skill — translate to/from chinese using C3P0 Universal Translator.
metadata:
  emoji: 🇨🇳
  triggers:
    - translate chinese
    - chinese
    - /chinese
    - 中文
---

# 🇨🇳 中文 (chinese) Language Skill

Translates between chinese and other languages via C3P0 Protocol Droid.

## Quick Translate

```bash
python3 ~/sandboxes/c3p0/translator.py translate "Hello world" --to zh-CN
```

## From chinese to English

```bash
python3 ~/sandboxes/c3p0/translator.py translate "text in chinese" --to en
```

## Phrasebook

```bash
python3 ~/sandboxes/c3p0/translator.py phrasebook "common phrase"
```

## Backend

- **Agent:** C3P0 (Protocol Droid)
- **Engine:** Google Translate (deep-translator)
- **Code:** ~/sandboxes/c3p0/translator.py
- **Language code:** `zh-CN`
