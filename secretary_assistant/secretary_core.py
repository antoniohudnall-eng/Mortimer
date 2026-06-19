#!/usr/bin/env python3
"""
SECRETARY VOICE ASSISTANT - SEED3
Voice-powered AI secretary with personality
"""

import speech_recognition as sr
import pyttsx3
import datetime
import os

class SecretaryAssistant:
    def __init__(self, name="Secretary", voice_profile=None):
        self.name = name
        self.voice_profile = voice_profile or {
            'speed': 150,
            'pitch': 55,
            'volume': 100
        }
        self.engine = pyttsx3.init()
        self._configure_voice()
        
    def _configure_voice(self):
        """Configure espeak or system TTS"""
        # Try espeak first
        if os.path.exists('/usr/bin/espeak'):
            self.engine.setProperty('voice', 'en-us')
        
    def speak(self, text):
        """Speak text with configured voice"""
        print(f"🤖 {self.name}: {text}")
        os.system(f'espeak -v en-us+m3 -s {self.voice_profile["speed"]} '
                  f'-p {self.voice_profile["pitch"]} -a {self.voice_profile["volume"]} '
                  f'"{text}" 2>/dev/null')
                  
    def listen(self):
        """Listen for voice input"""
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            print("🎤 Listening...")
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio)
            print(f"👤 You: {text}")
            return text
        except:
            return None
            
    def greet(self):
        """Morning greeting"""
        hour = datetime.datetime.now().hour
        if hour < 12:
            greeting = f"Good morning! I am {self.name}, your AI secretary. How may I assist you today?"
        elif hour < 17:
            greeting = f"Good afternoon! I am {self.name}, your AI secretary. How may I help you?"
        else:
            greeting = f"Good evening! I am {self.name}, your AI secretary. What can I do for you?"
        self.speak(greeting)
        
    def handle_command(self, text):
        """Handle user commands"""
        if not text:
            self.speak("I didn't catch that. Could you please repeat?")
            return
            
        text = text.lower()
        
        if 'time' in text:
            now = datetime.datetime.now().strftime("%I:%M %p")
            self.speak(f"The current time is {now}")
        elif 'date' in text:
            today = datetime.datetime.now().strftime("%B %d, %Y")
            self.speak(f"Today is {today}")
        elif 'appointment' in text or 'schedule' in text:
            self.speak("I can help you with appointments. What would you like to schedule?")
        elif 'contact' in text or 'phone' in text:
            self.speak("I can manage your contacts. Who would you like to reach?")
        elif 'email' in text:
            self.speak("I can draft and send emails for you. What would you like to communicate?")
        elif 'exit' in text or 'bye' in text:
            self.speak("Have a wonderful day! I'm always here when you need me.")
            return False
        else:
            self.speak("I'm here to help with scheduling, calls, emails, and more. How may I assist you?")
        return True
        
    def run(self):
        """Main loop"""
        self.greet()
        running = True
        while running:
            user_input = self.listen()
            if user_input:
                running = self.handle_command(user_input)

if __name__ == "__main__":
    assistant = SecretaryAssistant(name="Secretary")
    assistant.run()
