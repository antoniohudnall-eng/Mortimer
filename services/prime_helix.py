#!/usr/bin/env python3
"""
PRIME HELIX v2.0 — Port 7778
3D helix from prime numbers, φ-pattern visualization
"""
from flask import Flask, jsonify, render_template_string
import math

app = Flask(__name__)
PHI = 1.618033988749895

def primes_upto(n: int) -> list:
    """Sieve of Eratosthenes"""
    sieve = [True] * (n + 1)
    sieve[0] = sieve[1] = False
    for i in range(2, int(n**0.5) + 1):
        if sieve[i]:
            for j in range(i*i, n+1, i):
                sieve[j] = False
    return [i for i, is_prime in enumerate(sieve) if is_prime]

HTML = '''<!DOCTYPE html><html><head>
<title>Prime Helix — SEED3</title>
<meta charset="utf-8">
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{background:#0a0a0f;color:#e0d8c0;font-family:'Courier New',monospace;display:flex;flex-direction:column;align-items:center}
h1{color:#7eb8da;margin:30px 0 10px;letter-spacing:3px}
.subtitle{color:#5a8aaa;margin-bottom:30px;font-style:italic}
canvas{border:1px solid #333;border-radius:8px}
.footer{margin:30px;color:#555;font-size:.8em}
a{color:#7eb8da}
</style></head><body>
<h1>🧬 PRIME HELIX</h1>
<div class="subtitle">3D Projection — φ-weighted prime distribution — SEED3</div>
<canvas id="helix" width="800" height="600"></canvas>
<div class="footer">
    <a href="/">/</a> | <a href="/primes/500">/primes/500</a> | 
    <a href="http://127.0.0.1:7777">Quantum Oracle</a> | 
    <a href="http://127.0.0.1:7779">Riemann Helix</a>
</div>
<script>
const phi = 1.618033988749895;
const canvas = document.getElementById('helix');
const ctx = canvas.getContext('2d');
const W=canvas.width, H=canvas.height, cx=W/2, cy=H/2;

fetch('/primes/200')
  .then(r=>r.json())
  .then(data => {
    const primes = data.primes;
    ctx.fillStyle='#0a0a0f'; ctx.fillRect(0,0,W,H);
    
    // Critical line
    ctx.strokeStyle='#7eb8da22'; ctx.lineWidth=1;
    ctx.setLineDash([5,15]); ctx.beginPath();
    ctx.moveTo(cx,0); ctx.lineTo(cx,H); ctx.stroke();
    ctx.setLineDash([]);
    
    primes.forEach((p,i) => {
        const angle = (i * phi * 0.5) % (Math.PI*8);
        const r = 30 + (i / primes.length) * 300;
        const x = cx + Math.cos(angle) * r * 0.8;
        const y = cy + Math.sin(angle) * r * 0.5;
        const size = 1 + (p % 5) * 0.5;
        
        // Phi-weighted color
        const hue = (i * phi * 37) % 360;
        ctx.fillStyle = `hsl(${hue},70%,60%)`;
        ctx.beginPath(); ctx.arc(x, y, size, 0, Math.PI*2); ctx.fill();
        
        if(i%20===0) {
            ctx.fillStyle='#7eb8da44';
            ctx.font='9px monospace';
            ctx.fillText(p, x+5, y-3);
        }
    });
    
    // Key stats
    ctx.fillStyle='#7eb8da'; ctx.font='bold 12px monospace';
    ctx.fillText(`◆ ${primes.length} primes · φ = ${phi.toFixed(8)}`,20,H-20);
    ctx.fillStyle='#5a8aaa'; ctx.font='10px monospace';
    
    // Prime gaps and φ-ratios
    let phiHits=0, total=0;
    for(let i=2;i<primes.length;i++){
        const g1=primes[i-1]-primes[i-2], g2=primes[i]-primes[i-1];
        if(g1>0){total++; if(Math.abs(g2/g1-phi)<0.1) phiHits++;}
    }
    ctx.fillText(`φ-gap ratio matches: ${phiHits}/${total}`,20,H-5);
  });
</script></body></html>'''

@app.route('/')
def index():
    return render_template_string(HTML)

@app.route('/health')
def health():
    return jsonify({"status": "ok"})

@app.route('/primes/<int:n>')
def get_primes(n: int):
    n = min(n, 2000)
    primes = primes_upto(n * 15)[:n]
    
    gaps = [primes[i] - primes[i-1] for i in range(1, len(primes))]
    phi_matches = sum(1 for i in range(1, len(gaps)) 
                      if gaps[i-1] > 0 and abs(gaps[i]/gaps[i-1] - PHI) < 0.15)
    
    return jsonify({
        "primes": primes,
        "count": len(primes),
        "max_prime": primes[-1] if primes else 0,
        "phi": PHI,
        "phi_gap_matches": f"{phi_matches}/{len(gaps)-1}" if len(gaps) > 1 else "N/A",
        "average_gap": round(sum(gaps)/len(gaps), 2) if gaps else 0
    })

if __name__ == '__main__':
    print("🧬 Prime Helix v2.0 — Port 7778")
    app.run(host='0.0.0.0', port=7778, debug=False)
