from flask import Flask, send_from_directory
app = Flask(__name__)

@app.route('/')
def index():
    return send_from_directory('static', 'hudnall-galaxy.html')

@app.route('/health')
def health():
    return {"status": "ok", "service": "Hudnall Galaxy v1", "ship": "SEED3"}

if __name__ == '__main__':
    print("🌀 Hudnall Galaxy v1 — Port 7784")
    app.run(host='0.0.0.0', port=7784, debug=False)
