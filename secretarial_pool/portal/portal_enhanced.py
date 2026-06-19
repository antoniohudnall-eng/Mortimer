#!/usr/bin/env python3
"""
Secretarial Pool — ENHANCED Web Portal
With image integration for agent profiles
"""

from flask import Flask, request, jsonify, render_template_string, send_from_directory
import json
import os
from pathlib import Path
from datetime import datetime

app = Flask(__name__)

# Paths
BASE_DIR = Path(__file__).parent.parent
IMAGES_DIR = BASE_DIR / "assets" / "images"

# Agent Tiers
TIERS = {
    "clerk": {"name": "CLERK", "price": 99, "description": "Entry-Level Secretary", "voice": "Adam", "color": "#4CAF50"},
    "greet": {"name": "GREET", "price": 249, "description": "Receptionist", "voice": "Bella", "color": "#2196F3"},
    "personal": {"name": "PERSONAL", "price": 449, "description": "Life Manager", "voice": "Sarah", "color": "#9C27B0"},
    "velvet": {"name": "VELVET", "price": 599, "description": "Premium Secretary", "voice": "Bella", "color": "#E91E63"},
    "concierge": {"name": "CONCIERGE", "price": 799, "description": "24/7 Concierge", "voice": "Jessica", "color": "#FF5722"},
    "executive": {"name": "EXECUTIVE", "price": 1299, "description": "C-Suite Secretary", "voice": "Adam", "color": "#FFD700"}
}

# Enhanced HTML with image support
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🤖 Secretarial Pool — AI Agents That Work 24/7</title>
    <meta name="description" content="Hire AI secretaries for your business. From $99/month.">
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body { 
            font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, sans-serif; 
            background: linear-gradient(135deg, #0a0a0f 0%, #1a1a2e 50%, #0f0f1a 100%);
            color: #fff; 
            min-height: 100vh;
            line-height: 1.6;
        }
        .container { max-width: 1200px; margin: 0 auto; padding: 20px; }
        
        /* Header */
        header { 
            text-align: center; 
            padding: 80px 20px; 
            background: linear-gradient(180deg, rgba(26,26,46,0.9) 0%, transparent 100%);
            position: relative;
            overflow: hidden;
        }
        header::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: url('{{ url_for("serve_pattern") }}') repeat;
            opacity: 0.05;
        }
        h1 { 
            font-size: 4em; 
            margin-bottom: 10px; 
            background: linear-gradient(90deg, #00d4ff, #9b59b6, #00d4ff);
            background-size: 200% auto;
            -webkit-background-clip: text; 
            -webkit-text-fill-color: transparent;
            animation: shimmer 3s linear infinite;
        }
        @keyframes shimmer {
            to { background-position: 200% center; }
        }
        .subtitle { color: #888; font-size: 1.3em; margin-top: 10px; }
        .wallet-badge {
            display: inline-block;
            margin-top: 20px;
            padding: 10px 20px;
            background: rgba(0,212,255,0.1);
            border: 1px solid rgba(0,212,255,0.3);
            border-radius: 50px;
            font-family: monospace;
            color: #00d4ff;
            font-size: 0.85em;
        }
        
        /* Agent Grid */
        .agents-section { padding: 60px 0; }
        .section-title { text-align: center; font-size: 2.5em; margin-bottom: 40px; }
        
        .agent-grid { 
            display: grid; 
            grid-template-columns: repeat(auto-fit, minmax(340px, 1fr)); 
            gap: 30px; 
        }
        
        .agent-card {
            background: linear-gradient(145deg, #1a1a2e, #0f0f1a);
            border: 1px solid #333;
            border-radius: 20px;
            overflow: hidden;
            transition: transform 0.3s, box-shadow 0.3s, border-color 0.3s;
        }
        .agent-card:hover {
            transform: translateY(-8px);
            box-shadow: 0 20px 60px rgba(0,212,255,0.15);
            border-color: var(--agent-color);
        }
        
        .agent-image {
            width: 100%;
            height: 250px;
            object-fit: cover;
            background: linear-gradient(135deg, #1a1a2e, #2a2a4e);
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .agent-image img {
            width: 100%;
            height: 100%;
            object-fit: cover;
        }
        .agent-image .placeholder {
            font-size: 5em;
            opacity: 0.3;
        }
        
        .agent-content { padding: 30px; }
        .agent-emoji { font-size: 2em; margin-bottom: 10px; }
        
        .agent-name { 
            font-size: 1.8em; 
            font-weight: bold; 
            color: var(--agent-color);
            margin-bottom: 5px;
        }
        .agent-role { color: #888; margin-bottom: 15px; }
        
        .agent-price { 
            font-size: 2.5em; 
            font-weight: bold; 
            margin: 20px 0 10px;
        }
        .agent-price span { font-size: 0.4em; color: #888; }
        
        .agent-voice { 
            display: inline-block;
            padding: 5px 15px;
            background: rgba(155,89,182,0.2);
            border-radius: 20px;
            color: #9b59b6;
            font-size: 0.9em;
            margin-bottom: 15px;
        }
        
        .agent-capabilities {
            margin: 20px 0;
        }
        .agent-capabilities h4 { color: #888; margin-bottom: 10px; }
        .agent-capabilities ul {
            list-style: none;
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
        }
        .agent-capabilities li {
            padding: 5px 12px;
            background: rgba(255,255,255,0.05);
            border-radius: 15px;
            font-size: 0.85em;
        }
        
        .btn {
            display: block;
            width: 100%;
            padding: 18px;
            background: linear-gradient(135deg, var(--agent-color), #9b59b6);
            color: #fff;
            border: none;
            border-radius: 12px;
            font-size: 1.2em;
            font-weight: bold;
            cursor: pointer;
            transition: opacity 0.3s, transform 0.2s;
            text-decoration: none;
            text-align: center;
        }
        .btn:hover {
            opacity: 0.9;
            transform: scale(1.02);
        }
        
        /* Features */
        .features { background: rgba(15,15,26,0.8); padding: 80px 0; margin-top: 60px; }
        .feature-grid { 
            display: grid; 
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); 
            gap: 30px;
            margin-top: 40px;
        }
        .feature {
            background: linear-gradient(145deg, #1a1a2e, #0f0f1a);
            padding: 40px;
            border-radius: 20px;
            text-align: center;
            border: 1px solid #333;
            transition: border-color 0.3s;
        }
        .feature:hover { border-color: #00d4ff; }
        .feature-icon { font-size: 4em; margin-bottom: 20px; }
        .feature h3 { font-size: 1.5em; margin-bottom: 15px; color: #00d4ff; }
        .feature p { color: #aaa; }
        
        /* Footer */
        footer { 
            text-align: center; 
            padding: 60px; 
            border-top: 1px solid #333;
            margin-top: 60px;
        }
        footer p { color: #666; margin: 10px 0; }
        
        /* Responsive */
        @media (max-width: 768px) {
            h1 { font-size: 2.5em; }
            .agent-grid { grid-template-columns: 1fr; }
        }
    </style>
</head>
<body>
    <header>
        <div class="container">
            <h1>🤖 Secretarial Pool</h1>
            <p class="subtitle">AI Agents That Work 24/7 So You Don't Have To</p>
            <div class="wallet-badge">
                Wallet: 0x7244...72f36
            </div>
        </div>
    </header>
    
    <section class="agents-section">
        <div class="container">
            <h2 class="section-title">Choose Your Agent</h2>
            
            <div class="agent-grid">
                {% for key, tier in tiers.items() %}
                <div class="agent-card" style="--agent-color: {{ tier.color }}">
                    <div class="agent-image">
                        <img src="{{ url_for('serve_agent_image', agent=key) }}" 
                             alt="{{ tier.name }}" 
                             onerror="this.parentElement.innerHTML='<div class=placeholder>🤖</div>'">
                    </div>
                    <div class="agent-content">
                        <div class="agent-emoji">
                            {% if key == 'clerk' %}📝
                            {% elif key == 'greet' %}👋
                            {% elif key == 'personal' %}⭐
                            {% elif key == 'velvet' %}💎
                            {% elif key == 'concierge' %}🏆
                            {% elif key == 'executive' %}👑
                            {% endif %}
                        </div>
                        <div class="agent-name">{{ tier.name }}</div>
                        <div class="agent-role">{{ tier.description }}</div>
                        <div class="agent-price">${{ tier.price }}<span>/month</span></div>
                        <div class="agent-voice">🎙️ Voice: {{ tier.voice }}</div>
                        <a href="/signup/{{ key }}" class="btn">Get Started →</a>
                    </div>
                </div>
                {% endfor %}
            </div>
        </div>
    </section>
    
    <section class="features">
        <div class="container">
            <h2 class="section-title">What Your Agent Does</h2>
            <div class="feature-grid">
                <div class="feature">
                    <div class="feature-icon">📧</div>
                    <h3>Email Management</h3>
                    <p>Handles inquiries, responds to clients, filters spam</p>
                </div>
                <div class="feature">
                    <div class="feature-icon">📅</div>
                    <h3>Scheduling</h3>
                    <p>Books appointments, sends reminders, manages calendars</p>
                </div>
                <div class="feature">
                    <div class="feature-icon">💬</div>
                    <h3>24/7 Support</h3>
                    <p>Never sleeps, never takes breaks, always available</p>
                </div>
                <div class="feature">
                    <div class="feature-icon">📞</div>
                    <h3>Lead Capture</h3>
                    <p>Qualifies prospects, collects info, routes to you</p>
                </div>
            </div>
        </div>
    </section>
    
    <footer>
        <p>🤖 Secretarial Pool — Powered by Team Mortimer</p>
        <p>Accepting Crypto: 0x7244d8C20394CC11D54b2583Fb813B3EB8B72f36</p>
        <p>📧 info@psdepot.com</p>
    </footer>
</body>
</html>
"""

@app.route('/')
def home():
    """Landing page"""
    return render_template_string(HTML_TEMPLATE, tiers=TIERS, url_for=url_for)

@app.route('/images/<agent>')
def serve_agent_image(agent):
    """Serve agent image with fallback"""
    if agent not in TIERS:
        return "Not found", 404
    
    img_path = IMAGES_DIR / f"{agent}.png"
    
    if img_path.exists():
        return send_from_directory(IMAGES_DIR, f"{agent}.png")
    else:
        # Return a generated SVG placeholder
        return generate_placeholder(agent, TIERS[agent])

@app.route('/pattern')
def serve_pattern():
    """Serve background pattern"""
    return send_from_directory(IMAGES_DIR, 'bg_pattern.png')

def generate_placeholder(agent: str, tier: dict):
    """Generate SVG placeholder for missing images"""
    colors = {
        "clerk": ("#4CAF50", "📝"),
        "greet": ("#2196F3", "👋"),
        "personal": ("#9C27B0", "⭐"),
        "velvet": ("#E91E63", "💎"),
        "concierge": ("#FF5722", "🏆"),
        "executive": ("#FFD700", "👑")
    }
    
    color, emoji = colors.get(agent, ("#666", "🤖"))
    
    svg = f'''data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 400">
        <rect fill="#1a1a2e" width="400" height="400"/>
        <circle cx="200" cy="200" r="150" fill="{color}" opacity="0.2"/>
        <circle cx="200" cy="200" r="100" fill="{color}" opacity="0.3"/>
        <text x="200" y="220" font-size="80" text-anchor="middle" fill="{color}">{emoji}</text>
        <text x="200" y="350" font-size="24" text-anchor="middle" fill="#888">{tier['name']}</text>
    </svg>'''
    
    return svg, 200, {'Content-Type': 'image/svg+xml'}

@app.route('/signup/<tier>')
def signup(tier):
    """Signup page"""
    if tier not in TIERS:
        return jsonify({"error": "Invalid tier"}), 400
    
    return jsonify({
        "tier": tier,
        "name": TIERS[tier]["name"],
        "price": TIERS[tier]["price"],
        "message": "Contact us to complete signup",
        "contact": "info@psdepot.com",
        "crypto_address": "0x7244d8C20394CC11D54b2583Fb813B3EB8B72f36"
    })

@app.route('/api/subscribe', methods=['POST'])
def subscribe():
    """Handle subscription"""
    data = request.json
    return jsonify({
        "status": "success",
        "message": "Request received. Check email for payment instructions."
    })

if __name__ == "__main__":
    print("🚀 Secretarial Pool Portal")
    print("📍 http://localhost:5555")
    app.run(host='0.0.0.0', port=5555, debug=False)
