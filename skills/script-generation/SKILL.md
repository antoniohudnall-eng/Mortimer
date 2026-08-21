---
name: script-generation
description: "Generate marketing video scripts for AGI Company products using AI. Creates scripts for HumanPal, MilkMan, ReggieStarr, Dark Factory and other products."
user-invocable: true
---

# Script Generation Skill

Generate professional marketing video scripts for AGI Company products.

## Usage

/script-generation [product] [--duration 30] [--style modern]

## Products Available

- `humanpal` - HumanPal avatar generation
- `milkman` - MilkMan delivery optimization  
- `reggiestarr` - ReggieStarr POS system
- `darkfactory` - Dark Factory manufacturing
- `all` - Generate scripts for all products

## Options

- `--duration` - Script length in seconds (default: 30)
- `--style` - Script style: modern, professional, casual (default: modern)
- `--platform` - Target platform: tiktok, youtube, web (default: web)

## Example

```
/script-generation milkman --duration 60 --style professional
```

## Output

Generates complete video scripts with:
- Opening hook
- Problem statement
- Solution reveal
- Features showcase
- Call-to-action
- Scene directions

Scripts saved to `/marketing/scripts/[product]_script.txt`
