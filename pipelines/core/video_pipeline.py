#!/usr/bin/env python3
"""
🎬 VIDEO PIPELINE - Create TikTok/Reels/Shorts Videos
Combines voice + images/animations + subtitles
"""

import os
import subprocess
import json
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import tempfile

class VideoPipeline:
    def __init__(self, output_dir="/storage/emulated/0/Movies/Mortimer"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.temp_dir = Path(tempfile.gettempdir()) / "mortimer_video"
        self.temp_dir.mkdir(exist_ok=True)
        
        # Fonts
        self.font_paths = [
            "/system/fonts/Roboto-Bold.ttf",
            "/system/fonts/NotoSans-Bold.ttf",
            "/system/fonts/DroidSans-Bold.ttf"
        ]
        self.font = self._get_font(size=60)
        self.font_small = self._get_font(size=36)
    
    def _get_font(self, size=60):
        for path in self.font_paths:
            if Path(path).exists():
                try:
                    return ImageFont.truetype(path, size)
                except:
                    pass
        return ImageFont.load_default()
    
    def create_slide(self, text, bg_color=(26, 26, 46), text_color=(255, 255, 255),
                     image_path=None, duration=3):
        """Create a single video slide with text overlay"""
        width, height = 1080, 1920  # TikTok/Shorts format
        
        # Create base image
        img = Image.new('RGB', (width, height), bg_color)
        draw = ImageDraw.Draw(img)
        
        # Add background image if provided
        if image_path and Path(image_path).exists():
            bg = Image.open(image_path).resize((width, height), Image.LANCZOS)
            img = bg.convert('RGB')
            draw = ImageDraw.Draw(img)
        
        # Wrap and draw text
        lines = self._wrap_text(text, self.font, width - 100)
        y = (height - len(lines) * 80) // 2
        
        for line in lines:
            bbox = draw.textbbox((0, 0), line, font=self.font)
            x = (width - (bbox[2] - bbox[0])) // 2
            # Shadow for readability
            draw.text((x + 3, y + 3), line, font=self.font, fill=(0, 0, 0))
            draw.text((x, y), line, font=self.font, fill=text_color)
            y += 80
        
        return img
    
    def _wrap_text(self, text, font, max_width):
        """Simple text wrapping"""
        words = text.split()
        lines = []
        current = ""
        
        for word in words:
            test = current + " " + word if current else word
            bbox = ImageDraw.Draw(Image.new('RGB', (1, 1))).textbbox((0, 0), test, font=font)
            if bbox[2] - bbox[0] <= max_width:
                current = test
            else:
                if current:
                    lines.append(current)
                current = word
        if current:
            lines.append(current)
        
        return lines
    
    def create_video_from_slides(self, slides_data, audio_path, output_name, fps=30):
        """Create video from slides + audio
        
        slides_data: list of {'image': path or None, 'text': str, 'duration': seconds}
        """
        output_path = self.output_dir / f"{output_name}.mp4"
        
        # Create temp directory for frames
        frames_dir = self.temp_dir / "frames"
        frames_dir.mkdir(exist_ok=True)
        
        # Generate frames for each slide
        frame_files = []
        for i, slide in enumerate(slides_data):
            img = self.create_slide(
                text=slide.get('text', ''),
                bg_color=slide.get('bg_color', (26, 26, 46)),
                image_path=slide.get('image')
            )
            
            frame_path = frames_dir / f"slide_{i:04d}.png"
            img.save(frame_path, 'PNG')
            
            # Save duration info
            duration = slide.get('duration', 3)
            frame_files.append((frame_path, duration))
        
        # Create video from frames using ffmpeg
        concat_list = frames_dir / "concat.txt"
        with open(concat_list, 'w') as f:
            for frame_path, duration in frame_files:
                # Extend each frame for its duration
                fps_float = float(fps)
                frames_needed = int(duration * fps_float)
                for _ in range(frames_needed):
                    f.write(f"file '{frame_path.name}'\n")
                f.write(f"duration {duration}\n")
        
        # Generate video without audio first
        temp_video = self.temp_dir / "temp_video.mp4"
        
        cmd = [
            'ffmpeg', '-y',
            '-f', 'concat',
            '-safe', '0',
            '-i', str(concat_list),
            '-vf', f'scale=1080:1920,fps={fps}',
            '-c:v', 'libx264',
            '-preset', 'fast',
            '-crf', '23',
            str(temp_video)
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"FFmpeg error: {result.stderr}")
            return None
        
        # Add audio
        if audio_path and Path(audio_path).exists():
            cmd = [
                'ffmpeg', '-y',
                '-i', str(temp_video),
                '-i', str(audio_path),
                '-c:v', 'copy',
                '-c:a', 'aac',
                '-shortest',
                str(output_path)
            ]
            subprocess.run(cmd, capture_output=True)
        else:
            # Copy instead of rename (cross-device)
            import shutil
            shutil.copy2(str(temp_video), str(output_path))
        
        # Cleanup
        try:
            for f in frames_dir.glob("*.png"):
                f.unlink()
            frames_dir.rmdir()
        except:
            pass  # Don't fail on cleanup errors
        
        return str(output_path)
    
    def create_agent_showcase(self, agent_name, agent_description, price, 
                              features, audio_path=None):
        """Create a promotional video for an agent"""
        slides = [
            {
                'text': f"🚀 MEET {agent_name.upper()}",
                'bg_color': (26, 26, 46),
                'duration': 2
            },
            {
                'text': agent_description,
                'bg_color': (20, 40, 60),
                'duration': 4
            },
            {
                'text': "✨ FEATURES:",
                'bg_color': (40, 20, 60),
                'duration': 1.5
            },
        ]
        
        # Add feature slides
        for feature in features[:3]:
            slides.append({
                'text': f"• {feature}",
                'bg_color': (30, 30, 50),
                'duration': 2.5
            })
        
        slides.extend([
            {
                'text': f"💰 ONLY ${price}/month",
                'bg_color': (20, 60, 40),
                'duration': 2
            },
            {
                'text': "🏆 Available NOW on AgentFleet",
                'bg_color': (60, 40, 20),
                'duration': 3
            }
        ])
        
        return self.create_video_from_slides(slides, audio_path, f"agent_{agent_name.lower()}")


if __name__ == "__main__":
    pipeline = VideoPipeline()
    
    # Demo slide
    slide = pipeline.create_slide("🚀 AGENTS ARE HERE!\nYour AI workforce\nstarts now.")
    slide.save("/storage/emulated/0/Pictures/demo_slide.png")
    print("Demo slide saved!")
