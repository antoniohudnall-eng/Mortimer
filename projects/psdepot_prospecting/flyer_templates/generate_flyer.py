#!/usr/bin/env python3
"""
Performance Supply Depot - Flyer Generator
Usage: python3 generate_flyer.py [event_name]
"""

import os
import sys

# Event configurations
EVENTS = {
    "july_4th": {
        "name": "July 4th",
        "title": "🇺🇸 4TH OF JULY 🇺🇸",
        "greeting": "Happy Independence Day",
        "tagline": "Land of the Tree, Home of the Trade",
        "message": """
            As we celebrate <strong>Freedom, Enterprise & Innovation</strong>, 
            we at <strong>Performance Supply Depot</strong> remain committed to 
            powering American businesses with <strong>premium supplies</strong> 
            and <strong>reliable service</strong>.
            <br><br>
            From thermal rolls to toners, we've got your business covered 
            — because a well-supplied business is a <strong>thriving</strong> business.
        """,
        "phone_icon_left": "🎆",
        "phone_icon_right": "🎇",
        "event_icon": "🏛️",
    },
    "labor_day": {
        "name": "Labor Day",
        "title": "🛠️ LABOR DAY 🛠️",
        "greeting": "Honoring American Workers",
        "tagline": "Land of the Tree, Home of the Trade",
        "message": """
            This <strong>Labor Day</strong>, we salute the <strong>hard-working Americans</strong> 
            who keep our businesses running. At <strong>Performance Supply Depot</strong>, 
            we're dedicated to providing the <strong>tools and supplies</strong> you need 
            to get the job done right.
            <br><br>
            Honor the worker. Support the trade. <strong>Shop local.</strong>
        """,
        "phone_icon_left": "🔧",
        "phone_icon_right": "⚙️",
        "event_icon": "👷",
    },
    "halloween": {
        "name": "Halloween",
        "title": "🎃 HALLOWEEN 🎃",
        "greeting": "Spooky Savings Season",
        "tagline": "Land of the Tree, Home of the Trade",
        "message": """
            Don't let your supplies run <strong>dry</strong> this Halloween! 
            <strong>Performance Supply Depot</strong> has all your business needs 
            — from paper to toners, we're your <strong>one-stop shop</strong>.
            <br><br>
            No tricks, just <strong>treats</strong> for your business! BOO-tiful deals await.
        """,
        "phone_icon_left": "👻",
        "phone_icon_right": "🦇",
        "event_icon": "🎃",
    },
    "thanksgiving": {
        "name": "Thanksgiving",
        "title": "🦃 THANKSGIVING 🦃",
        "greeting": "Grateful for American Business",
        "tagline": "Land of the Tree, Home of the Trade",
        "message": """
            This <strong>Thanksgiving</strong>, we're thankful for <strong>YOU</strong> — 
            the American businesses that keep our economy strong. 
            <strong>Performance Supply Depot</strong> is grateful to serve your supply needs.
            <br><br>
            From our family to yours — <strong>Happy Thanksgiving!</strong> 🦃
        """,
        "phone_icon_left": "🦃",
        "phone_icon_right": "🥧",
        "event_icon": "🦃",
    },
    "christmas": {
        "name": "Christmas",
        "title": "🎄 MERRY CHRISTMAS 🎄",
        "greeting": "Season of Giving",
        "tagline": "Land of the Tree, Home of the Trade",
        "message": """
            'Tis the season to be <strong>prepared</strong>! Make sure your business 
            has everything it needs before the holiday rush. <strong>Performance Supply Depot</strong> 
            is here with <strong>premium supplies</strong> for all your needs.
            <br><br>
            Wishing you and your team a <strong>joyful holiday season!</strong> 🎁
        """,
        "phone_icon_left": "🎅",
        "phone_icon_right": "🎁",
        "event_icon": "🎄",
    },
    "new_year": {
        "name": "New Year",
        "title": "🎆 NEW YEAR 🎆",
        "greeting": "Happy New Year 2027",
        "tagline": "Land of the Tree, Home of the Trade",
        "message": """
            Ring in the new year with a <strong>fully stocked</strong> business! 
            <strong>Performance Supply Depot</strong> helps you start 2027 
            with <strong>premium supplies</strong> and <strong>reliable service</strong>.
            <br><br>
            New Year. New goals. <strong>Same great partner.</strong> Let's make it count!
        """,
        "phone_icon_left": "🎉",
        "phone_icon_right": "🥂",
        "event_icon": "🎆",
    },
    "valentines": {
        "name": "Valentine's Day",
        "title": "💝 VALENTINE'S DAY 💝",
        "greeting": "Love Your Business",
        "tagline": "Land of the Tree, Home of the Trade",
        "message": """
            Show your business some <strong>love</strong> this Valentine's Day! 
            <strong>Performance Supply Depot</strong> delivers <strong>premium supplies</strong> 
            with the care and attention your business deserves.
            <br><br>
            Because your business is worth <strong>valuing</strong>. 💕
        """,
        "phone_icon_left": "💕",
        "phone_icon_right": "🌹",
        "event_icon": "💝",
    },
    "back_to_school": {
        "name": "Back to School",
        "title": "📚 BACK TO SCHOOL 📚",
        "greeting": "Ready for the School Year",
        "tagline": "Land of the Tree, Home of the Trade",
        "message": """
            Back to school means <strong>back to business</strong>! Whether you're 
            an educator, administrator, or business owner, <strong>Performance Supply Depot</strong> 
            has the <strong>paper, ink, and supplies</strong> you need.
            <br><br>
            Start the school year <strong>prepared</strong> and <strong>productive</strong>! 📚
        """,
        "phone_icon_left": "✏️",
        "phone_icon_right": "📖",
        "event_icon": "🎒",
    },
    "memorial_day": {
        "name": "Memorial Day",
        "title": "🕯️ MEMORIAL DAY 🕯️",
        "greeting": "Honoring Those Who Served",
        "tagline": "Land of the Tree, Home of the Trade",
        "message": """
            This <strong>Memorial Day</strong>, we remember and honor the 
            <strong>brave men and women</strong> who gave their lives for our freedom.
            <strong>Performance Supply Depot</strong> is proud to support the 
            <strong>land of the free</strong>.
            <br><br>
            Never forgotten. Always grateful. 🇺🇸
        """,
        "phone_icon_left": "🇺🇸",
        "phone_icon_right": "🕯️",
        "event_icon": "🕯️",
    },
}

# Static values
STATIC = {
    "company_name": "Performance Supply Depot",
    "company_full_name": "Performance Supply Depot LLC",
    "company_tagline": "Where American Businesses Trade with Pride",
    "products": """
        <div class="product">
            <a href="https://psdepot.com" target="_blank">
                <div class="product-icon">🖨️</div>
                <div class="product-name">Thermal Rolls</div>
            </a>
        </div>
        <div class="product">
            <a href="https://psdepot.com" target="_blank">
                <div class="product-icon">📦</div>
                <div class="product-name">Paper Supply</div>
            </a>
        </div>
        <div class="product">
            <a href="https://psdepot.com" target="_blank">
                <div class="product-icon">🖊️</div>
                <div class="product-name">Toners & Ink</div>
            </a>
        </div>
    """,
    "cta_title": "Ready to Partner with Excellence?",
    "cta_strong": "Visit us today",
    "cta_url": "psdepot.com",
    "cta_email": "info@psdepot.com",
    "phone": "888-881-6834",
    "phone_label": "📞 Call Us Today 📞",
    "website_url": "https://psdepot.com",
    "website_domain": "psdepot.com",
    "email": "info@psdepot.com",
    "footer_tagline": "Empowering American Businesses Since Day One",
    "disclaimer": "Celebrate responsibly. Happy holidays from Performance Supply Depot!",
    "year": "2026",
}

def generate_flyer(event_key, output_dir="."):
    """Generate a flyer for the given event."""
    
    if event_key not in EVENTS:
        print(f"Unknown event: {event_key}")
        print(f"Available events: {', '.join(EVENTS.keys())}")
        return False
    
    event = EVENTS[event_key]
    
    # Read template
    template_path = os.path.join(os.path.dirname(__file__), "base_template.html")
    with open(template_path, "r") as f:
        template = f.read()
    
    # Replace placeholders
    replacements = {
        "{{TITLE}}": f"Happy {event['name']} | Performance Supply Depot",
        "{{GREETING}}": event["greeting"],
        "{{EMOJI_TITLE}}": event["title"],
        "{{TAGLINE}}": event["tagline"],
        "{{MESSAGE}}": event["message"],
        "{{EVENT_ICON}}": event["event_icon"],
        "{{PHONE_ICON_LEFT}}": event["phone_icon_left"],
        "{{PHONE_ICON_RIGHT}}": event["phone_icon_right"],
        "{{PRODUCTS}}": STATIC["products"],
        "{{CTA_TITLE}}": STATIC["cta_title"],
        "{{CTA_STRONG}}": STATIC["cta_strong"],
        "{{CTA_URL}}": STATIC["cta_url"],
        "{{CTA_EMAIL}}": STATIC["cta_email"],
        "{{PHONE}}": STATIC["phone"],
        "{{PHONE_LABEL}}": STATIC["phone_label"],
        "{{COMPANY_NAME}}": STATIC["company_name"],
        "{{COMPANY_TAGLINE}}": STATIC["company_tagline"],
        "{{COMPANY_FULL_NAME}}": STATIC["company_full_name"],
        "{{FOOTER_ICON}}": event["event_icon"],
        "{{WEBSITE_URL}}": STATIC["website_url"],
        "{{WEBSITE_DOMAIN}}": STATIC["website_domain"],
        "{{EMAIL}}": STATIC["email"],
        "{{FOOTER_TAGLINE}}": STATIC["footer_tagline"],
        "{{DISCLAIMER}}": STATIC["disclaimer"],
        # Colors (patriotic theme)
        "{{GRADIENT_START}}": "#0a1628",
        "{{GRADIENT_MID}}": "#1a365d",
        "{{GRADIENT_END}}": "#c53030",
        "{{HEADER_BG}}": "#1e3a5f",
        "{{BG_END}}": "#0a1628",
        "{{BG_RGB}}": "10,22,40",
        "{{BG_START}}": "#0a1628",
        "{{ACCENT_RED}}": "#c53030",
        "{{ACCENT_NAVY}}": "#1e3a5f",
        "{{ACCENT_CYAN}}": "#00d4ff",
        "{{CYAN_RGB}}": "0,212,255",
        "{{GOLD}}": "#ffd700",
        "{{GOLD_RGB}}": "255,215,0",
        "{{TAGLINE_DARK}}": "#9b2c2c",
        "{{PRODUCT_BG}}": "30,58,95",
        "{{CTA_DARK}}": "#0099cc",
        "{{PHONE_GLOW}}": "#ff6b6b",
        "{{GLOW1}}": "#ff0",
        "{{GLOW2}}": "#f00",
        "{{GLOW3}}": "#00f",
        "{{GLOW4}}": "#f0f",
        "{{GLOW5}}": "#0ff",
        "{{GLOW6}}": "#0f0",
    }
    
    for placeholder, value in replacements.items():
        template = template.replace(placeholder, value)
    
    # Write output
    output_path = os.path.join(output_dir, f"{event_key}_flyer.html")
    with open(output_path, "w") as f:
        f.write(template)
    
    print(f"✅ Generated: {output_path}")
    return True


def list_events():
    """List all available events."""
    print("\n🎨 Available Flyer Events:")
    print("-" * 40)
    for key, event in EVENTS.items():
        print(f"  {key:15} - {event['name']}")
    print("-" * 40)
    print(f"\nUsage: python3 generate_flyer.py [event_name]")
    print("       python3 generate_flyer.py all  # Generate all")


def main():
    if len(sys.argv) < 2:
        list_events()
        return
    
    arg = sys.argv[1].lower()
    
    if arg == "all":
        print("\n🎆 Generating all flyers...\n")
        for event_key in EVENTS:
            generate_flyer(event_key)
        print("\n✅ All flyers generated!")
    elif arg in EVENTS:
        generate_flyer(arg)
    else:
        print(f"\n❌ Unknown event: {arg}")
        list_events()


if __name__ == "__main__":
    main()
