#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TikTok Content Generator for Performance Supply Depot
Short-form video content scripts with captions

TikTok Format:
- Hook in first 3 seconds
- Keep captions short (under 150 chars for overlay)
- Use trending audio suggestions
- Strong CTA
"""

import random
import sys
from datetime import datetime

PHONE = "888-881-6834"
WEBSITE = "psdepot.com"

# TikTok content templates - Short, punchy, visual
TIKTOK_TEMPLATES = [
    {
        "hook": "POV: Your printer dies Friday at 7pm",
        "script": "Show receipt printer jamming, then cut to: Same-day delivery saves the weekend. Stock up at psdepot.com or call 888-881-6834",
        "caption": f"Don't let printer problems kill your weekend 🔧 Same-day delivery in Vegas 📞 {PHONE} #{WEBSITE} #RestaurantLife #POSSupplies #LasVegas",
        "duration": "15-30 sec",
        "audio": "Trending: relatable/frustrated sound",
    },
    {
        "hook": "3 things restaurant owners should know",
        "script": "Quick cuts: 1) Thermal paper needs cool storage 2) Clean printer heads monthly 3) Keep 2-week supply buffer. We deliver: psdepot.com",
        "caption": f"Save this for later 💾 Restaurant tips that save money 📞 {PHONE} #{WEBSITE} #RestaurantTips #SmallBusiness #POS",
        "duration": "30-45 sec",
        "audio": "Trending: educational/upbeat",
    },
    {
        "hook": "The receipt paper scam they don't tell you about",
        "script": "Show overpriced paper vs our fair prices. Text overlay: 'Why pay more?' Cut to: psdepot.com - Vegas local, same-day delivery",
        "caption": f"Stop overpaying for supplies 💰 Vegas local • Same-day delivery 📞 {PHONE} #{WEBSITE} #SaveMoney #RestaurantHack",
        "duration": "20-30 sec",
        "audio": "Trending: exposé/reveal sound",
    },
    {
        "hook": "Day in the life: POS tech",
        "script": "Follow tech to 3 restaurant repairs. Show fixed printers, happy owners. End card: 'We fix what others won't' psdepot.com",
        "caption": f"We fix printers other shops won't touch 🔧 Vegas local service 📞 {PHONE} #{WEBSITE} #PrinterRepair #BehindTheScenes",
        "duration": "45-60 sec",
        "audio": "Trending: day-in-the-life beat",
    },
    {
        "hook": "Trade in your dead printer",
        "script": "Show old printer → refurbished unit → working receipt. Text: 'Printer swaps available' psdepot.com",
        "caption": f"Old printer? Swap it for a working one 🔄 Ask about options 📞 {PHONE} #{WEBSITE} #PrinterSwap #Upgrade",
        "duration": "15-20 sec",
        "audio": "Trending: transformation sound",
    },
    {
        "hook": "Running low on Friday?",
        "script": "Show empty paper shelf → panic → cut to: Delivery truck arriving. Text: 'Ordered 2pm, delivered same day' psdepot.com",
        "caption": f"Same-day delivery when you need it most 🚚 Order by 2pm 📞 {PHONE} #{WEBSITE} #SameDayDelivery #WeekendReady",
        "duration": "20-30 sec",
        "audio": "Trending: relief/satisfying sound",
    },
    {
        "hook": "Your POS system called...",
        "script": "Phone screen animation: 'It's me, your printer. I'm full of paper but still not printing. Clean my thermal head?' psdepot.com",
        "caption": f"When your printer has attitude 😤 Clean it monthly! More tips at 📞 {PHONE} #{WEBSITE} #TechTips #Relatable",
        "duration": "15-20 sec",
        "audio": "Trending: phone notification sound",
    },
    {
        "hook": "Opening a restaurant in Vegas?",
        "script": "Before/after: Empty counter → Full POS setup. Tech installing, training staff. End: 'We do setups too' psdepot.com",
        "caption": f"New restaurant? We handle POS setup + training 🎓 Vegas local experts 📞 {PHONE} #{WEBSITE} #NewBusiness #LasVegas",
        "duration": "30-45 sec",
        "audio": "Trending: inspiring/achievement sound",
    },
    {
        "hook": "This mistake costs restaurants $$$",
        "script": "Show wrong paper in printer → jam → downtime. Text overlay: 'Thermal vs Bond paper' then explain. psdepot.com",
        "caption": f"Use the RIGHT paper for your printer 📄 Questions? Call us 📞 {PHONE} #{WEBSITE} #RestaurantTips #SaveMoney",
        "duration": "30 sec",
        "audio": "Trending: warning/dramatic sound",
    },
    {
        "hook": "We installed 47 POS systems this month",
        "script": "Montage of different restaurants, quick cuts, happy owners giving thumbs up. Text: '47 setups, 0 complaints' psdepot.com",
        "caption": f"Trusted by Vegas restaurants 🎰 Professional install guaranteed 📞 {PHONE} #{WEBSITE} #POSSetup #LasVegas",
        "duration": "30-45 sec",
        "audio": "Trending: hype/high-energy beat",
    },
    {
        "hook": "Cabling for POS systems explained",
        "script": "Animation/diagram: messy cables → organized network. Tech working. Before/after of clean install. psdepot.com",
        "caption": f"Professional POS cabling & network setup 🔌 Book now: 📞 {PHONE} #{WEBSITE} #CablingServices #TechSetup",
        "duration": "45 sec",
        "audio": "Trending: educational/informative",
    },
    {
        "hook": "Sam4s POS - Why restaurants choose it",
        "script": "Show Sam4s system in action. Text overlays: Reliable, Fast, Affordable. Price: Starting at $495. psdepot.com",
        "caption": f"Sam4s POS systems from $495 💵 Reliable hardware for restaurants 📞 {PHONE} #{WEBSITE} #Sam4s #POSsystem",
        "duration": "30 sec",
        "audio": "Trending: product showcase beat",
    },
]

def get_daily_content():
    """Get random TikTok content template"""
    return random.choice(TIKTOK_TEMPLATES)

def get_multiple(days=3):
    """Get multiple unique templates for content calendar"""
    selected = []
    available = TIKTOK_TEMPLATES.copy()
    
    for _ in range(min(days, len(available))):
        choice = random.choice(available)
        selected.append(choice)
        available.remove(choice)
    
    return selected

def main():
    if len(sys.argv) < 2:
        print("=" * 70)
        print("TikTok Content Generator - Performance Supply Depot")
        print("Short-form video scripts with captions")
        print("Phone:", PHONE)
        print("Website:", WEBSITE)
        print("=" * 70)
        print("\nUsage:")
        print("  tiktok_content.py daily       # Today's content idea")
        print("  tiktok_content.py week        # 3 content ideas for the week")
        print("  tiktok_content.py random      # Random idea")
        return
    
    command = sys.argv[1]
    
    if command == "daily":
        content = get_daily_content()
        print(f"\n🎬 TikTok Content - {datetime.now().strftime('%Y-%m-%d')}\n")
        print("=" * 70)
        
        print(f"\n📱 HOOK (First 3 seconds):")
        print(f"   {content['hook']}")
        
        print(f"\n📝 VIDEO SCRIPT:")
        print(f"   {content['script']}")
        
        print(f"\n✍️ CAPTION:")
        print(f"   {content['caption']}")
        
        print(f"\n⏱️  DURATION: {content['duration']}")
        print(f"🎵 AUDIO: {content['audio']}")
        
        print("\n" + "=" * 70)
        print("\n✅ Ready to film and post to TikTok")
        
    elif command == "week":
        contents = get_multiple(3)
        print(f"\n📅 TikTok Content Calendar - Week of {datetime.now().strftime('%Y-%m-%d')}\n")
        
        for i, content in enumerate(contents, 1):
            print(f"\n{'='*70}")
            print(f"DAY {i}")
            print(f"{'='*70}")
            print(f"\n📱 Hook: {content['hook']}")
            print(f"\n🎬 Script: {content['script'][:100]}...")
            print(f"\n✍️ Caption: {content['caption'][:80]}...")
            print(f"⏱️  Duration: {content['duration']}")
        
        print("\n" + "=" * 70)
        print("\n✅ 3 video ideas ready for production")
        
    elif command == "random":
        content = get_daily_content()
        print(f"\n🎬 Random TikTok Idea:")
        print(f"\n📱 Hook: {content['hook']}")
        print(f"\n📝 Script: {content['script']}")
        print(f"\n✍️ Caption: {content['caption']}")
        
    else:
        print(f"❌ Unknown command: {command}")
        print("Use: daily, week, or random")

if __name__ == "__main__":
    main()
