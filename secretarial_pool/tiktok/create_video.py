#!/usr/bin/env python3
"""
TikTok Video Creator
Combines: Image + Audio + Captions → Video File
"""

import os
import json
import subprocess
from pathlib import Path

def create_video_from_slides(image: str, audio: str, output: str, duration: int = None) -> dict:
    """
    Create video using FFmpeg
    Requires: ffmpeg installed
    """
    
    if not os.path.exists(image):
        return {"status": "error", "message": f"Image not found: {image}"}
    
    if not os.path.exists(audio):
        return {"status": "error", "message": f"Audio not found: {audio}"}
    
    # Get audio duration if not specified
    if not duration:
        result = subprocess.run(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration", 
             "-of", "default=noprint_wrappers=1:nokey=1", audio],
            capture_output=True, text=True
        )
        duration = float(result.stdout.strip() or 10)
    
    try:
        # Create video: static image + audio
        cmd = [
            "ffmpeg", "-y",
            "-loop", "1",
            "-i", image,
            "-i", audio,
            "-c:v", "libx264",
            "-tune", "stillimage",
            "-pix_fmt", "yuv420p",
            "-c:a", "aac",
            "-b:a", "192k",
            "-shortest",
            "-vf", f"scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2",
            output
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        
        if result.returncode == 0:
            return {"status": "success", "file": output, "duration": duration}
        else:
            return {"status": "error", "message": result.stderr}
            
    except subprocess.TimeoutExpired:
        return {"status": "error", "message": "Video creation timed out"}
    except FileNotFoundError:
        return {"status": "error", "message": "FFmpeg not installed. Install with: pkg install ffmpeg"}

def batch_create_videos(campaign_file: str, images_dir: str):
    """Create videos for entire campaign"""
    
    with open(campaign_file, 'r') as f:
        campaign = json.load(f)
    
    images_path = Path(images_dir)
    audio_path = Path(campaign_file).parent / "audio"
    output_path = Path(campaign_file).parent / "videos"
    output_path.mkdir(exist_ok=True)
    
    results = []
    
    for video in campaign.get('videos', []):
        video_id = video.get('id')
        agent = video.get('agent_tier')
        
        image_file = images_path / f"{agent}.png"
        audio_file = audio_path / f"{video_id}.mp3"
        output_file = output_path / f"{video_id}.mp4"
        
        print(f"🎬 Creating video for {agent.upper()}...")
        print(f"   Image: {image_file}")
        print(f"   Audio: {audio_file}")
        
        if not image_file.exists():
            print(f"   ⚠️ Image missing - using placeholder")
            image_file = images_path / "placeholder.png"
        
        result = create_video_from_slides(str(image_file), str(audio_file), str(output_file))
        
        if result['status'] == 'success':
            size = os.path.getsize(output_file)
            print(f"   ✅ {output_file} ({size:,} bytes, {result['duration']:.1f}s)")
        else:
            print(f"   ❌ {result.get('message', 'Unknown error')}")
        
        results.append({
            "video_id": video_id,
            "agent": agent,
            "output": str(output_file) if result['status'] == 'success' else None,
            "status": result['status']
        })
    
    return results

def create_placeholder_image(text: str, output: str, color: str = "#1a1a2e"):
    """Create placeholder image with text using PIL"""
    try:
        from PIL import Image, ImageDraw, ImageFont
        
        img = Image.new('RGB', (1080, 1920), color=color)
        draw = ImageDraw.Draw(img)
        
        # Try to get a font
        try:
            font = ImageFont.truetype("/system/fonts/Roboto-Regular.ttf", 80)
        except:
            font = ImageFont.load_default()
        
        # Center text
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        x = (1080 - text_width) // 2
        y = (1920 - text_height) // 2
        
        draw.text((x, y), text, fill="white", font=font)
        img.save(output)
        return {"status": "success", "file": output}
    except ImportError:
        return {"status": "error", "message": "Pillow not installed: pip install pillow"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    import sys
    
    campaign = "campaigns/campaign_20260618.json"
    images = "../assets/images"
    
    if len(sys.argv) > 1:
        campaign = sys.argv[1]
    if len(sys.argv) > 2:
        images = sys.argv[2]
    
    print("🎬 TikTok Video Creator")
    print(f"   Campaign: {campaign}")
    print(f"   Images: {images}")
    print()
    
    batch_create_videos(campaign, images)
