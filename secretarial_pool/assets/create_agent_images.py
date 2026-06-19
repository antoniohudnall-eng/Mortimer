#!/usr/bin/env python3
"""
Generate Agent Card Images
=========================
Creates branded TikTok thumbnail images for each agent
"""

import os
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

# Agent configurations
AGENTS = {
    "clerk": {
        "name": "CLERK",
        "emoji": "📝",
        "tagline": "Efficiency at Work",
        "color": (76, 175, 80),      # Green
        "gradient": (26, 26, 46),     # Dark blue
        "price": "$99/mo"
    },
    "greet": {
        "name": "GREET",
        "emoji": "👋",
        "tagline": "Welcome Every Call",
        "color": (33, 150, 243),      # Blue
        "gradient": (26, 26, 46),
        "price": "$249/mo"
    },
    "personal": {
        "name": "PERSONAL",
        "emoji": "⭐",
        "tagline": "Life, Managed",
        "color": (156, 39, 176),      # Purple
        "gradient": (26, 26, 46),
        "price": "$449/mo"
    },
    "velvet": {
        "name": "VELVET",
        "emoji": "💎",
        "tagline": "Premium Service",
        "color": (233, 30, 99),        # Pink
        "gradient": (26, 26, 46),
        "price": "$599/mo"
    },
    "concierge": {
        "name": "CONCIERGE",
        "emoji": "🏆",
        "tagline": "24/7 Excellence",
        "color": (255, 87, 34),        # Orange
        "gradient": (26, 26, 46),
        "price": "$799/mo"
    },
    "executive": {
        "name": "EXECUTIVE",
        "emoji": "👑",
        "tagline": "C-Suite Authority",
        "color": (255, 215, 0),        # Gold
        "gradient": (26, 26, 46),
        "price": "$1,299/mo"
    }
}

def hex_to_rgb(hex_color):
    """Convert hex to RGB tuple"""
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def create_gradient(width, height, color1, color2):
    """Create vertical gradient image"""
    img = Image.new('RGB', (width, height))
    draw = ImageDraw.Draw(img)
    
    for y in range(height):
        ratio = y / height
        r = int(color1[0] * (1 - ratio) + color2[0] * ratio)
        g = int(color1[1] * (1 - ratio) + color2[1] * ratio)
        b = int(color1[2] * (1 - ratio) + color2[2] * ratio)
        draw.line([(0, y), (width, y)], fill=(r, g, b))
    
    return img

def get_font(size, bold=False):
    """Get a font, fallback to default"""
    # Try common system fonts
    font_paths = [
        "/system/fonts/Roboto-Regular.ttf",
        "/system/fonts/Roboto-Bold.ttf",
        "/system/fonts/DroidSans.ttf",
        "/system/fonts/DroidSans-Bold.ttf",
    ]
    
    for path in font_paths:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except:
                pass
    
    return ImageFont.load_default()

def create_agent_card(agent_id, config, output_path):
    """Create a TikTok-style agent card"""
    
    width, height = 1080, 1920
    emoji_size = 300
    padding = 100
    
    # Create gradient background
    gradient_color = tuple(config["gradient"])
    img = create_gradient(width, height, gradient_color, (10, 10, 20))
    draw = ImageDraw.Draw(img)
    
    # Get fonts
    try:
        title_font = ImageFont.truetype("/system/fonts/Roboto-Bold.ttf", 120)
        tag_font = ImageFont.truetype("/system/fonts/Roboto-Regular.ttf", 60)
        price_font = ImageFont.truetype("/system/fonts/Roboto-Bold.ttf", 80)
        emoji_font = ImageFont.truetype("/system/fonts/NotoColorEmoji.ttf", emoji_size)
    except:
        title_font = get_font(80, True)
        tag_font = get_font(40)
        price_font = get_font(60, True)
        emoji_font = get_font(emoji_size)
    
    # Draw emoji/avatar circle
    center_x = width // 2
    avatar_y = height // 3
    
    # Draw circle background for emoji
    circle_color = config["color"]
    circle_size = 400
    draw.ellipse(
        [center_x - circle_size//2, avatar_y - circle_size//2,
         center_x + circle_size//2, avatar_y + circle_size//2],
        fill=circle_color
    )
    
    # Draw emoji
    emoji = config["emoji"]
    try:
        bbox = draw.textbbox((0, 0), emoji, font=emoji_font)
        emoji_width = bbox[2] - bbox[0]
        emoji_height = bbox[3] - bbox[1]
        draw.text(
            (center_x - emoji_width//2, avatar_y - emoji_height//2 - 30),
            emoji,
            font=emoji_font
        )
    except:
        # Fallback: just draw a circle with initial
        draw.ellipse(
            [center_x - 180, avatar_y - 180,
             center_x + 180, avatar_y + 180],
            fill=(100, 100, 120)
        )
        draw.text(
            (center_x - 50, avatar_y - 80),
            config["name"][0],
            font=title_font,
            fill=(255, 255, 255)
        )
    
    # Draw agent name
    name_y = avatar_y + 280
    bbox = draw.textbbox((0, 0), config["name"], font=title_font)
    name_width = bbox[2] - bbox[0]
    draw.text(
        (center_x - name_width//2, name_y),
        config["name"],
        font=title_font,
        fill=config["color"]
    )
    
    # Draw tagline
    tagline_y = name_y + 150
    bbox = draw.textbbox((0, 0), config["tagline"], font=tag_font)
    tagline_width = bbox[2] - bbox[0]
    draw.text(
        (center_x - tagline_width//2, tagline_y),
        config["tagline"],
        font=tag_font,
        fill=(150, 150, 150)
    )
    
    # Draw price
    price_y = tagline_y + 150
    bbox = draw.textbbox((0, 0), config["price"], font=price_font)
    price_width = bbox[2] - bbox[0]
    draw.text(
        (center_x - price_width//2, price_y),
        config["price"],
        font=price_font,
        fill=(0, 212, 255)
    )
    
    # Draw "AI AGENT" label at bottom
    label_y = height - 200
    label = "🤖 AI AGENT"
    bbox = draw.textbbox((0, 0), label, font=tag_font)
    label_width = bbox[2] - bbox[0]
    draw.text(
        (center_x - label_width//2, label_y),
        label,
        font=tag_font,
        fill=(155, 89, 182)
    )
    
    # Add border effect
    draw.rectangle(
        [padding, padding, width - padding, height - padding],
        outline=config["color"],
        width=8
    )
    
    # Save
    img.save(output_path)
    return output_path

def generate_all_cards(output_dir):
    """Generate all agent cards"""
    
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print("🎨 Generating agent card images...")
    print()
    
    for agent_id, config in AGENTS.items():
        output_path = output_dir / f"{agent_id}.png"
        create_agent_card(agent_id, config, output_path)
        
        size = os.path.getsize(output_path)
        print(f"  ✅ {agent_id.upper()}: {output_path} ({size:,} bytes)")
    
    print()
    print("✅ All agent cards generated!")

def create_hero_image(output_path):
    """Create a hero/banner image for the campaign"""
    
    width, height = 1200, 630
    img = create_gradient(width, height, (26, 26, 46), (15, 15, 30))
    draw = ImageDraw.Draw(img)
    
    # Try fonts
    try:
        title_font = ImageFont.truetype("/system/fonts/Roboto-Bold.ttf", 100)
        sub_font = ImageFont.truetype("/system/fonts/Roboto-Regular.ttf", 50)
    except:
        title_font = get_font(80, True)
        sub_font = get_font(40)
    
    # Title
    title = "🤖 SECRETARIAL POOL"
    bbox = draw.textbbox((0, 0), title, font=title_font)
    title_width = bbox[2] - bbox[0]
    draw.text(
        (width//2 - title_width//2, height//3),
        title,
        font=title_font,
        fill=(0, 212, 255)
    )
    
    # Subtitle
    subtitle = "AI Agents That Work 24/7"
    bbox = draw.textbbox((0, 0), subtitle, font=sub_font)
    sub_width = bbox[2] - bbox[0]
    draw.text(
        (width//2 - sub_width//2, height//3 + 150),
        subtitle,
        font=sub_font,
        fill=(150, 150, 150)
    )
    
    img.save(output_path)
    return output_path

if __name__ == "__main__":
    import sys
    
    output_dir = sys.argv[1] if len(sys.argv) > 1 else "."
    
    generate_all_cards(output_dir)
    
    # Also create hero image
    hero_path = Path(output_dir) / "hero.png"
    create_hero_image(hero_path)
    print(f"  ✅ Hero: {hero_path}")
