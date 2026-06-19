#!/bin/bash
# TikTok Video Creator - Combines images + espeak voiceovers
# Requires: ffmpeg, espeak (already installed)

echo "🎬 TikTok Video Creator"
echo "======================="
echo ""

CAMPAIGN_DIR="campaigns"
IMAGES_DIR="../assets"
AUDIO_DIR="campaigns/audio_espeak"
OUTPUT_DIR="videos"

mkdir -p "$OUTPUT_DIR"

# Find latest campaign
CAMPAIGN=$(ls -t $CAMPAIGN_DIR/campaign_*.json 2>/dev/null | head -1)

if [ -z "$CAMPAIGN" ]; then
    echo "❌ No campaign found. Run: python3 tiktok_voice_campaign.py"
    exit 1
fi

echo "📋 Campaign: $CAMPAIGN"
echo "📁 Images: $IMAGES_DIR"
echo "🎙️ Audio: $AUDIO_DIR"
echo ""

# Extract video IDs from campaign
VIDEO_IDS=$(python3 -c "
import json
with open('$CAMPAIGN') as f:
    data = json.load(f)
    for v in data.get('videos', []):
        print(v['id'])
")

COUNT=0
for VID in $VIDEO_IDS; do
    ((COUNT++))
    
    # Get agent from campaign
    AGENT=$(python3 -c "
import json
with open('$CAMPAIGN') as f:
    data = json.load(f)
    for v in data.get('videos', []):
        if v['id'] == '$VID':
            print(v.get('agent_tier', 'clerk'))
            break
")
    
    IMAGE="$IMAGES_DIR/${AGENT}.png"
    AUDIO="$AUDIO_DIR/${VID}.wav"
    OUTPUT="$OUTPUT_DIR/${VID}.mp4"
    
    if [ ! -f "$IMAGE" ]; then
        echo "⚠️  Missing image: $IMAGE"
        continue
    fi
    
    if [ ! -f "$AUDIO" ]; then
        echo "⚠️  Missing audio: $AUDIO"
        continue
    fi
    
    echo "🎬 Video $COUNT: $AGENT ($VID)"
    echo "   Image: $IMAGE"
    echo "   Audio: $AUDIO"
    
    # Create video with ffmpeg
    ffmpeg -y -loop 1 -i "$IMAGE" -i "$AUDIO" \
        -c:v libx264 -tune stillimage \
        -pix_fmt yuv420p -c:a aac -b:a 192k \
        -shortest \
        -vf "scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2" \
        "$OUTPUT" 2>/dev/null
    
    if [ -f "$OUTPUT" ]; then
        SIZE=$(ls -lh "$OUTPUT" | awk '{print $5}')
        echo "   ✅ $OUTPUT ($SIZE)"
    else
        echo "   ❌ Failed"
    fi
    echo ""
done

echo "======================="
echo "✅ Created $COUNT videos"
echo "📁 Output: $OUTPUT_DIR/"
ls -la "$OUTPUT_DIR/" 2>/dev/null | head -10
