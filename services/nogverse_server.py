from flask import Flask, send_from_directory
app = Flask(__name__)

@app.route('/')
def index():
    return send_from_directory('static', 'nogverse.html')

@app.route('/health')
def health():
    return {"status": "ok", "service": "NogVerse Complete", "ship": "SEED3", "author": "A13 SeedIV"}

if __name__ == '__main__':
    print("🌌 NogVerse Complete — Port 7782")
    app.run(host='0.0.0.0', port=7782, debug=False)
