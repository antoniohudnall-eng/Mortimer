from flask import Flask, send_from_directory
app = Flask(__name__)

@app.route('/')
def index():
    return send_from_directory('static', 'system-grid.html')

@app.route('/health')
def health():
    return {"status": "ok", "service": "Unified System Viewer", "ship": "SEED3", "author": "A13 SeedIV"}

if __name__ == '__main__':
    print("🌌 Unified System Viewer — Port 7781")
    app.run(host='0.0.0.0', port=7781, debug=False)
