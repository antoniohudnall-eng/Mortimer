#!/usr/bin/env python3
"""
Secretarial Pool Client Portal
Web interface for signing up and managing agents
"""

from flask import Flask, request, jsonify, render_template_string
import json
import os
from datetime import datetime

app = Flask(__name__)

# Agent Tiers
TIERS = {
    "clerk": {"name": "CLERK", "price": 99, "description": "Entry-Level Secretary", "voice": "Adam"},
    "greet": {"name": "GREET", "price": 249, "description": "Receptionist", "voice": "Bella"},
    "personal": {"name": "PERSONAL", "price": 449, "description": "Life Manager", "voice": "Sarah"},
    "velvet": {"name": "VELVET", "price": 599, "description": "Premium Secretary", "voice": "Bella"},
    "concierge": {"name": "CONCIERGE", "price": 799, "description": "24/7 Concierge", "voice": "Jessica"},
    "executive": {"name": "EXECUTIVE", "price": 1299, "description": "C-Suite Secretary", "voice": "Adam"}
}

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Secretarial Pool - AI Agents for Your Business</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: #0a0a0f; color: #fff; min-height: 100vh; }
        .container { max-width: 1200px; margin: 0 auto; padding: 20px; }
        header { text-align: center; padding: 60px 0; background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%); border-bottom: 1px solid #333; }
        h1 { font-size: 3em; margin-bottom: 10px; background: linear-gradient(90deg, #00d4ff, #9b59b6); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
        .subtitle { color: #888; font-size: 1.2em; }
        .tiers { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; padding: 40px 0; }
        .tier-card { background: linear-gradient(145deg, #1a1a2e, #0f0f1a); border: 1px solid #333; border-radius: 16px; padding: 30px; transition: transform 0.3s, border-color 0.3s; }
        .tier-card:hover { transform: translateY(-5px); border-color: #00d4ff; }
        .tier-name { font-size: 1.5em; font-weight: bold; margin-bottom: 10px; color: #00d4ff; }
        .tier-price { font-size: 2.5em; font-weight: bold; margin-bottom: 5px; }
        .tier-period { color: #888; font-size: 0.9em; }
        .tier-desc { color: #aaa; margin: 15px 0; }
        .tier-voice { color: #9b59b6; font-size: 0.9em; margin-bottom: 20px; }
        .btn { display: block; width: 100%; padding: 15px; background: linear-gradient(135deg, #00d4ff, #9b59b6); color: #fff; border: none; border-radius: 8px; font-size: 1.1em; cursor: pointer; transition: opacity 0.3s; text-decoration: none; text-align: center; }
        .btn:hover { opacity: 0.9; }
        .features { background: #0f0f1a; padding: 40px 0; }
        .features h2 { text-align: center; margin-bottom: 30px; font-size: 2em; }
        .feature-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; }
        .feature { background: #1a1a2e; padding: 20px; border-radius: 12px; text-align: center; }
        .feature-icon { font-size: 2em; margin-bottom: 10px; }
        .cta-section { text-align: center; padding: 60px 0; }
        .cta-section h2 { font-size: 2.5em; margin-bottom: 20px; }
        footer { text-align: center; padding: 40px; color: #666; border-top: 1px solid #333; margin-top: 40px; }
    </style>
</head>
<body>
    <header>
        <div class="container">
            <h1>🤖 Secretarial Pool</h1>
            <p class="subtitle">AI Agents That Work 24/7 So You Don't Have To</p>
        </div>
    </header>
    
    <section class="container">
        <h2 style="text-align:center; margin: 40px 0;">Choose Your Agent</h2>
        <div class="tiers">
            {% for key, tier in tiers.items() %}
            <div class="tier-card">
                <div class="tier-name">{{ tier.name }}</div>
                <div class="tier-price">${{ tier.price }}</div>
                <div class="tier-period">per month</div>
                <div class="tier-desc">{{ tier.description }}</div>
                <div class="tier-voice">Voice: {{ tier.voice }}</div>
                <a href="/signup/{{ key }}" class="btn">Get Started</a>
            </div>
            {% endfor %}
        </div>
    </section>
    
    <section class="features">
        <div class="container">
            <h2>What Your Agent Does</h2>
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
    
    <section class="cta-section">
        <div class="container">
            <h2>Ready to Scale?</h2>
            <p style="color: #888; margin-bottom: 30px;">Your AI workforce is waiting</p>
            <a href="#tiers" class="btn" style="max-width: 300px; margin: 0 auto;">View All Tiers</a>
        </div>
    </section>
    
    <footer>
        <p>🤖 Secretarial Pool - Powered by Team Mortimer</p>
        <p style="margin-top: 10px;">Wallet: 0x7244d8C20394CC11D54b2583Fb813B3EB8B72f36</p>
    </footer>
</body>
</html>
"""

@app.route('/')
def home():
    """Landing page"""
    return render_template_string(HTML_TEMPLATE, tiers=TIERS)

@app.route('/signup/<tier>')
def signup(tier):
    """Signup page for specific tier"""
    if tier not in TIERS:
        return "Invalid tier", 400
    
    return jsonify({
        "tier": tier,
        "name": TIERS[tier]["name"],
        "price": TIERS[tier]["price"],
        "signup_form": "Contact us to sign up",
        "contact": "info@psdepot.com"
    })

@app.route('/api/subscribe', methods=['POST'])
def subscribe():
    """Handle subscription request"""
    data = request.json
    email = data.get('email')
    tier = data.get('tier')
    
    if not email or tier not in TIERS:
        return jsonify({"error": "Invalid request"}), 400
    
    return jsonify({
        "status": "success",
        "message": f"Subscription request received for {TIERS[tier]['name']}",
        "next_step": "Check your email for payment instructions"
    })

@app.route('/api/status/<email>')
def status(email):
    """Check subscription status"""
    return jsonify({
        "email": email,
        "status": "pending",
        "message": "Connect payment to activate"
    })

if __name__ == "__main__":
    print("🚀 Starting Secretarial Pool Portal...")
    print("📍 http://localhost:5555")
    app.run(host='0.0.0.0', port=5555, debug=True)
