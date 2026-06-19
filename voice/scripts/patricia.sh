#!/bin/bash
cd ~/mortimer
source voice/config.sh
python3 -c "
import requests, os, sys, time
key = os.environ.get('ELEVENLABS_API_KEY')
text = ' '.join(sys.argv[1:])
resp = requests.post(
    'https://api.elevenlabs.io/v1/text-to-speech/50BdVlngDYeoh9pVuQof',
    headers={'xi-api-key': key, 'Content-Type': 'application/json'},
    json={'text': text, 'model_id': 'eleven_multilingual_v2'}
)
if resp.ok:
    with open(f'/tmp/voice_patricia_{int(time.time())}.mp3', 'wb') as f:
        f.write(resp.content)
    import subprocess
    subprocess.run(['termux-media-player', 'play', f'/tmp/voice_patricia_{int(time.time())}.mp3'])
else:
    print('Error:', resp.status_code)
"
