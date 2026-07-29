from flask import Flask, send_from_directory
app = Flask(__name__)

@app.route('/')
def index():
    return send_from_directory('static', 'hudnall-unified-galaxy.html')

@app.route('/health')
def health():
    return {"status": "ok", "service": "Hudnall Unified Galaxy", "ship": "SEED3", "features": "φ-helix · gravity · collisions · terrain worlds", "author": "Mortimer C3"}

if __name__ == '__main__':
    print("🌀 Hudnall Unified Galaxy — Port 7785")
    app.run(host='0.0.0.0', port=7785, debug=False)
