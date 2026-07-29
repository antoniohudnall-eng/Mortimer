from flask import Flask, send_from_directory
app = Flask(__name__)

@app.route('/')
def index():
    return send_from_directory('static', 'nogverse-galaxy.html')

@app.route('/health')
def health():
    return {"status": "ok", "service": "Hudnall Galaxy", "ship": "SEED3", "systems": "420", "rogue_planets": 80, "arms": 3}

if __name__ == '__main__':
    print("🌀 Hudnall Galaxy v2 — Port 7783")
    app.run(host='0.0.0.0', port=7783, debug=False)
