#!/usr/bin/env python3
"""
SECRETARY VOICE ASSISTANT v2.0 - TIKTOK READY
Multi-personality AI secretaries for sale
"""

import speech_recognition as sr
import subprocess
import datetime
import json
import os

class SecretaryBot:
    """AI Secretary with customizable voice and personality"""
    
    PERSONALITIES = {
        "professional": {
            "name": "Victoria",
            "speed": 140,
            "pitch": 48,
            "style": "British professional",
            "greeting": "Good day. I am Victoria, your personal secretary. How may I be of service?"
        },
        "friendly": {
            "name": "Sunny",
            "speed": 160,
            "pitch": 65,
            "style": "Warm American",
            "greeting": "Hey there! I'm Sunny, ready to help you out! What's on your mind?"
        },
        "executive": {
            "name": "Charles",
            "speed": 135,
            "pitch": 45,
            "style": "Executive British",
            "greeting": "Charles at your service. State your requirements and I shall attend to them."
        },
        "hip": {
            "name": "Jax",
            "speed": 170,
            "pitch": 70,
            "style": "Gen-Z friendly",
            "greeting": "Yo! Jax in the house! Let's get things done. What do you need?"
        },
        "morty": {
            "name": "Morty",
            "speed": 161,
            "pitch": 51,
            "style": "Server spirit",
            "greeting": "Morty here. General of the forces, at your service. What do you need, Captain?"
        }
    }
    
    def __init__(self, personality="professional"):
        self.personality = self.PERSONALITIES.get(personality, self.PERSONALITIES["professional"])
        self.running = True
        
    def speak(self, text):
        """Text-to-speech using espeak"""
        speed = self.personality["speed"]
        pitch = self.personality["pitch"]
        print(f"🤖 {self.personality['name']}: {text}")
        os.system(f'espeak -v en-us+m3 -s {speed} -p {pitch} -a 110 "{text}" 2>/dev/null')
        
    def listen(self):
        """Voice recognition"""
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            print("🎤 Listening...", flush=True)
            try:
                recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = recognizer.listen(source, timeout=5)
                text = recognizer.recognize_google(audio)
                print(f"👤 You: {text}")
                return text.lower()
            except sr.WaitTimeoutError:
                return None
            except:
                return None
                
    def process(self, text):
        """Process voice commands"""
        if not text:
            return True
            
        if any(x in text for x in ['hello', 'hi', 'hey', 'sup']):
            self.speak(self.personality["greeting"])
            
        elif 'time' in text:
            now = datetime.datetime.now().strftime("%I:%M %p")
            self.speak(f"The time is {now}")
            
        elif 'date' in text or 'day' in text:
            today = datetime.datetime.now().strftime("%A, %B %d, %Y")
            self.speak(f"Today is {today}")
            
        elif any(x in text for x in ['appointment', 'schedule', 'book']):
            self.speak("I can schedule that for you. What time works best?")
            
        elif any(x in text for x in ['email', 'message', 'send']):
            self.speak("I can draft and send emails. Who should I contact?")
            
        elif any(x in text for x in ['remind', 'reminder', 'alarm']):
            self.speak("I'll set a reminder. When should I remind you?")
            
        elif 'weather' in text:
            self.speak("Checking the weather. Looks like a nice day ahead!")
            
        elif any(x in text for x in ['thank', 'thanks']):
            self.speak("You're welcome! Anything else?")
            
        elif any(x in text for x in ['bye', 'exit', 'quit', 'stop']):
            self.speak("Talk soon! Have a great one!")
            self.running = False
            
        else:
            self.speak("I'm here to help with scheduling, emails, reminders, and more!")
        return self.running
        
    def run(self):
        """Main interaction loop"""
        print("\n" + "="*50)
        print(f"🎙️  SECRETARY BOT - {self.personality['name']}")
        print(f"   Style: {self.personality['style']}")
        print("="*50 + "\n")
        
        self.speak(self.personality["greeting"])
        
        while self.running:
            cmd = self.listen()
            if cmd:
                self.process(cmd)

def main():
    """Entry point with personality selection"""
    print("\n🧑‍💼 SECRETARY VOICE ASSISTANT - SELECT PERSONALITY")
    print("="*50)
    for i, (key, val) in enumerate(SecretaryBot.PERSONALITIES.items(), 1):
        print(f"  {i}. {val['name']} ({val['style']})")
    print()
    
    choice = input("Select (1-5) or press Enter for default: ").strip()
    
    personalities = list(SecretaryBot.PERSONALITIES.keys())
    idx = int(choice) - 1 if choice.isdigit() and 0 <= idx < len(personalities) else 0
    selected = personalities[idx]
    
    print(f"\n✅ Starting as {selected}...\n")
    bot = SecretaryBot(selected)
    bot.run()

if __name__ == "__main__":
    main()
