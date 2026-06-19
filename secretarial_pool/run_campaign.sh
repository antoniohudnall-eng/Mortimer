#!/bin/bash
# Secretarial Pool — Run Full TikTok Campaign
# Generates scripts, voiceovers, and videos

echo "🎬 SECRETARIAL POOL — TikTok Campaign Runner"
echo "============================================="
echo ""

cd ~/mortimer/secretarial_pool/tiktok

# Step 1: Generate Scripts
echo "📝 Step 1: Generating scripts..."
python3 tiktok_voice_campaign.py
echo ""

# Step 2: Generate Voiceovers
echo "🎙️ Step 2: Generating voiceovers..."
CAMPAIGN=$(ls -t campaigns/campaign_*.json 2>/dev/null | head -1)
if [ -n "$CAMPAIGN" ]; then
    python3 create_voiceovers.py "$CAMPAIGN"
else
    echo "❌ No campaign found"
fi
echo ""

# Step 3: Create Videos (requires images)
echo "🎬 Step 3: Creating videos..."
IMAGES="../assets/images"
CAMPAIGN=$(ls -t campaigns/campaign_*.json 2>/dev/null | head -1)
if [ -n "$CAMPAIGN" ]; then
    python3 create_video.py "$CAMPAIGN" "$IMAGES"
else
    echo "❌ No campaign found"
fi
echo ""

# Summary
echo "============================================="
echo "✅ Campaign Complete!"
echo ""
echo "📁 Output:"
echo "   Scripts:  campaigns/"
echo "   Audio:    campaigns/audio/"
echo "   Videos:   campaigns/videos/"
echo ""
echo "🖼️ Add images to $IMAGES to enable video creation"
