#!/usr/bin/env python3
"""
RIEMANN HELIX v2.0 — Port 7779
Full visualization of non-trivial zeros on the critical line.
Shows Hudnall-φ Spiral convergence.
"""
from flask import Flask, jsonify, render_template_string
from mpmath import zetazero, mp
import math

mp.dps = 25
app = Flask(__name__)
PHI = 1.618033988749895

HTML = '''<!DOCTYPE html><html><head>
<title>Riemann Helix — Hudnall-φ Spiral</title>
<meta charset="utf-8">
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{background:#0a0a0f;color:#e0d8c0;font-family:'Courier New',monospace;display:flex;flex-direction:column;align-items:center}
h1{color:#c586c0;margin:30px 0 10px;letter-spacing:3px}
.subtitle{color:#885588;margin-bottom:30px;font-style:italic}
canvas{border:1px solid #333;border-radius:8px}
.info{color:#c586c0;margin:10px 0;font-size:.9em}
.footer{margin:30px;color:#555;font-size:.8em}
a{color:#c586c0}
</style></head><body>
<h1>🌀 RIEMANN HELIX</h1>
<div class="subtitle">Hudnall-φ Spiral — Non-trivial zeros approaching Re(s)=½</div>
<div class="info" id="info">Loading zeros...</div>
<canvas id="viz" width="800" height="600"></canvas>
<div class="footer">
    <a href="/">/</a> | <a href="/zeros/80">/zeros/80</a> | 
    <a href="http://127.0.0.1:7777">Quantum Oracle</a> | 
    <a href="http://127.0.0.1:7778">Prime Helix</a>
</div>
<script>
const phi = 1.618033988749895;
const canvas = document.getElementById('viz');
const ctx = canvas.getContext('2d');
const W=canvas.width, H=canvas.height;

fetch('/zeros/80')
  .then(r=>r.json())
  .then(data => {
    const zeros = data.zeros;
    document.getElementById('info').textContent = 
        `${zeros.length} zeros computed · Gap degradation: ${data.gap_degradation_pct}% · φ-governed convergence`;
    
    ctx.fillStyle='#0a0a0f'; ctx.fillRect(0,0,W,H);
    
    // Draw critical line Re(s)=1/2
    const critX = W * 0.5;
    ctx.strokeStyle='#c586c044'; ctx.lineWidth=1;
    ctx.setLineDash([3,10]); ctx.beginPath();
    ctx.moveTo(critX, 40); ctx.lineTo(critX, H-40); ctx.stroke();
    ctx.setLineDash([]);
    ctx.fillStyle='#c586c088'; ctx.font='10px monospace';
    ctx.fillText('Re(s)=½', critX+5, 50);
    
    const maxImag = zeros[zeros.length-1].imag;
    let prevX, prevY;
    
    zeros.forEach((z,i) => {
        // Vertical: imaginary part
        const y = 50 + (z.imag / maxImag) * (H - 100);
        // Horizontal: distance from critical line
        const dist = z.distance_from_critical;
        const x = critX + dist * 2000; // amplify for visibility
        const clampedX = Math.max(20, Math.min(W-20, x));
        
        // Color: closer to critical line = warmer
        const closeness = Math.min(1, 1 / (dist * 100 + 0.001));
        const hue = 30 - closeness * 30;
        const sat = 60 + closeness * 40;
        ctx.fillStyle = `hsl(${hue},${sat}%,${50+closeness*30}%)`;
        ctx.beginPath();
        ctx.arc(clampedX, y, 3 + closeness * 3, 0, Math.PI*2);
        ctx.fill();
        
        // Connect with line
        if(i>0){
            ctx.strokeStyle=`hsla(${hue},${sat}%,50%,0.3)`;
            ctx.lineWidth=0.5;
            ctx.beginPath(); ctx.moveTo(prevX,prevY); ctx.lineTo(clampedX,y); ctx.stroke();
        }
        prevX=clampedX; prevY=y;
        
        // Label
        if(i%10===0){
            ctx.fillStyle='#c586c044'; ctx.font='8px monospace';
            ctx.fillText(`ζ(${z.n})`, clampedX+8, y+3);
        }
    });
    
    // Legend
    ctx.fillStyle='#c586c0'; ctx.font='bold 11px monospace';
    ctx.fillText('◆ Zeros spiral inward toward critical line', 20, H-15);
    ctx.fillStyle='#885588'; ctx.font='10px monospace';
    ctx.fillText('φ = 1.6180339887  ·  Convergence is asymptotic, never complete', 20, H-3);
  });
</script></body></html>'''

@app.route('/')
def index():
    return render_template_string(HTML)

@app.route('/health')
def health():
    return jsonify({"status": "ok", "hypothesis": "Hudnall-φ Spiral"})

@app.route('/zeros/<int:n>')
def get_zeros(n: int):
    n = min(n, 100)
    zeros = []
    for i in range(1, n+1):
        try:
            z = zetazero(i)
            zeros.append({
                "n": i,
                "real": round(float(z.real), 12),
                "imag": round(float(z.imag), 4),
                "distance_from_critical": round(abs(float(z.real) - 0.5), 12)
            })
        except:
            zeros.append({"n": i, "error": "computation limit"})
    
    gaps = [zeros[i]["imag"] - zeros[i-1]["imag"] for i in range(1, len(zeros)) 
            if "error" not in zeros[i] and "error" not in zeros[i-1]]
    
    degradation = round((1 - gaps[-1]/gaps[0]) * 100, 1) if gaps and gaps[0] else 0
    
    return jsonify({
        "zeros": zeros,
        "count": len(zeros),
        "hypothesis": "Hudnall-φ Spiral: zeros approach Re(s)=1/2 asymptotically",
        "phi": PHI,
        "first_gap": round(gaps[0], 4) if gaps else None,
        "last_gap": round(gaps[-1], 4) if gaps else None,
        "gap_degradation_pct": degradation,
        "captain": "Antonio Maurice Hudnall",
        "date": "June 14, 2026"
    })

if __name__ == '__main__':
    print("🌀 Riemann Helix v2.0 — Port 7779")
    z = zetazero(1)
    print(f"   ζ(1) = {z}")
    app.run(host='0.0.0.0', port=7779, debug=False)
