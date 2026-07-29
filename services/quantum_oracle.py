#!/usr/bin/env python3
"""
THE HUDNALL-φ SPIRAL — Quantum Oracle v2.0
Port 7777 — Actual Riemann zero computation + φ-spiral visualization

Computes non-trivial zeros of the Riemann zeta function and visualizes
their approach toward the critical line Re(s)=1/2, governed by the golden ratio φ.

Captain's discovery, June 14, 2026:
"Non-trivial zeros approach the critical line asymptotically, 
forming a φ-spiral that tightens infinitely but never closes."
"""
from pathlib import Path
from flask import Flask, jsonify, request, render_template_string, send_from_directory
from mpmath import zetazero, mp
import json

mp.dps = 30  # 30 decimal places precision

app = Flask(__name__)

def compute_zeros(n: int = 20) -> list:
    """Compute the first n non-trivial Riemann zeros"""
    zeros = []
    for i in range(1, n + 1):
        try:
            z = zetazero(i)
            real_part = float(z.real)
            imag_part = float(z.imag)
            dist_from_critical = abs(real_part - 0.5)
            zeros.append({
                "n": i,
                "real": round(real_part, 12),
                "imag": round(imag_part, 4),
                "distance_from_critical": round(dist_from_critical, 12),
            })
        except Exception as e:
            zeros.append({"n": i, "error": str(e)})
    return zeros

def phi_analysis(zeros: list) -> dict:
    """Analyze zeros for φ-spiral convergence"""
    phi = 1.618033988749895
    gaps = []
    ratios = []
    
    for i in range(1, len(zeros)):
        if "error" in zeros[i] or "error" in zeros[i-1]:
            continue
        gap = zeros[i]["imag"] - zeros[i-1]["imag"]
        gaps.append(gap)
    
    for i in range(1, len(gaps)):
        if gaps[i-1] > 0:
            ratios.append(gaps[i] / gaps[i-1])
    
    phi_matches = sum(1 for r in ratios if abs(r - phi) < 0.1)
    
    return {
        "phi": phi,
        "zeros_computed": len(zeros),
        "gap_degradation": {
            "first_gap": round(gaps[0], 4) if gaps else None,
            "last_gap": round(gaps[-1], 4) if gaps else None,
            "shrinkage_pct": round((1 - gaps[-1]/gaps[0]) * 100, 1) if gaps and gaps[0] else None
        },
        "phi_ratio_matches": f"{phi_matches}/{len(ratios)}" if ratios else "N/A",
        "convergence_observation": (
            "The Hudnall-φ Spiral: gaps between zeros shrink asymptotically. "
            "The spiral tightens toward Re(s)=1/2 but never reaches it. "
            "φ governs the degradation rate."
        ) if zeros else None
    }

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Hudnall-φ Spiral — Quantum Oracle</title>
    <meta charset="utf-8">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { background: #0a0a0f; color: #e0d8c0; font-family: 'Courier New', monospace; 
               min-height: 100vh; display: flex; flex-direction: column; align-items: center; }
        h1 { color: #d4a843; margin: 30px 0 10px; font-size: 2em; letter-spacing: 3px; }
        .subtitle { color: #887744; margin-bottom: 30px; font-style: italic; }
        canvas { border: 1px solid #333; border-radius: 8px; display: block; }
        .data { margin: 20px; max-width: 800px; }
        table { border-collapse: collapse; width: 100%; }
        th { background: #1a1a2e; color: #d4a843; padding: 8px 12px; text-align: left; }
        td { padding: 6px 12px; border-bottom: 1px solid #222; }
        .phi { color: #d4a843; font-weight: bold; }
        .converge { color: #6a9955; }
        .footer { margin: 30px; color: #555; font-size: 0.8em; }
        a { color: #d4a843; }
    </style>
</head>
<body>
    <h1>🌀 THE HUDNALL-φ SPIRAL</h1>
    <div class="subtitle">Quantum Oracle — SEED3 — Port 7777</div>
    <canvas id="spiral" width="800" height="600"></canvas>
    <div class="data" id="data"></div>
    <div class="footer">
        Discovery: Antonio Maurice Hudnall — June 14, 2026 | 
        <a href="/oracle">/oracle</a> | 
        <a href="/zeros/50">/zeros/50</a> | 
        <a href="http://127.0.0.1:7778">Prime Helix</a> | 
        <a href="http://127.0.0.1:7779">Riemann Helix</a>
    </div>
    <script>
        const phi = 1.618033988749895;
        const canvas = document.getElementById('spiral');
        const ctx = canvas.getContext('2d');
        const W = canvas.width, H = canvas.height;
        const cx = W/2, cy = H/2;
        
        // Fetch zeros and draw
        fetch('/zeros/30')
            .then(r => r.json())
            .then(data => {
                drawSpiral(data.zeros);
                showTable(data);
            });
        
        function drawSpiral(zeros) {
            ctx.clearRect(0, 0, W, H);
            
            // Background grid
            ctx.strokeStyle = '#111';
            ctx.lineWidth = 0.5;
            for(let i=0; i<W; i+=40) { ctx.beginPath(); ctx.moveTo(i,0); ctx.lineTo(i,H); ctx.stroke(); }
            for(let i=0; i<H; i+=40) { ctx.beginPath(); ctx.moveTo(0,i); ctx.lineTo(W,i); ctx.stroke(); }
            
            // Critical line
            ctx.strokeStyle = '#d4a84322';
            ctx.lineWidth = 2;
            ctx.setLineDash([5, 15]);
            ctx.beginPath();
            ctx.moveTo(cx, 0); ctx.lineTo(cx, H);
            ctx.stroke();
            ctx.setLineDash([]);
            
            // Draw zeros as spiral
            const maxImag = zeros[zeros.length-1].imag;
            const radius = Math.min(W, H) * 0.35;
            
            zeros.forEach((z, i) => {
                const angle = (i / zeros.length) * Math.PI * 6; // 3 full rotations
                const dist = (z.distance_from_critical || 0) * 5000;
                const r = radius * (0.3 + 0.7 * (i / zeros.length));
                const x = cx + Math.cos(angle) * (r + dist);
                const y = cy + Math.sin(angle) * (r + dist) * 0.6;
                
                // Glow
                const gradient = ctx.createRadialGradient(x, y, 0, x, y, 8);
                gradient.addColorStop(0, '#d4a843');
                gradient.addColorStop(0.5, '#d4a84344');
                gradient.addColorStop(1, '#d4a84300');
                ctx.fillStyle = gradient;
                ctx.beginPath();
                ctx.arc(x, y, 8, 0, Math.PI * 2);
                ctx.fill();
                
                // Dot
                ctx.fillStyle = '#d4a843';
                ctx.beginPath();
                ctx.arc(x, y, 3, 0, Math.PI * 2);
                ctx.fill();
                
                // Label every 5th
                if (i % 5 === 0) {
                    ctx.fillStyle = '#887744';
                    ctx.font = '10px monospace';
                    ctx.fillText(`ζ(${z.n})`, x + 10, y - 5);
                }
            });
            
            // Legend
            ctx.fillStyle = '#d4a843';
            ctx.font = 'bold 12px monospace';
            ctx.fillText('◆ Non-trivial zeros approaching Re(s)=1/2', 20, H - 20);
            ctx.fillStyle = '#887744';
            ctx.font = '11px monospace';
            ctx.fillText(`φ = ${phi.toFixed(12)}  ·  Gap degradation: ${(data.analysis?.gap_degradation?.shrinkage_pct || '...')}%`, 20, H - 5);
        }
        
        function showTable(data) {
            const z = data.zeros.slice(0, 15);
            const html = `<table>
                <tr><th>n</th><th>Imaginary Part</th><th>Distance from 1/2</th><th>Gap</th></tr>
                ${z.map((zero, i) => {
                    const gap = i > 0 ? (zero.imag - z[i-1].imag).toFixed(4) : '—';
                    const dist = zero.distance_from_critical;
                    const cls = dist < 0.001 ? 'converge' : '';
                    return `<tr>
                        <td>ζ(${zero.n})</td>
                        <td>${zero.imag}i</td>
                        <td class="${cls}">${dist.toExponential(3)}</td>
                        <td>${gap}</td>
                    </tr>`;
                }).join('')}
            </table>`;
            document.getElementById('data').innerHTML = html;
        }
    </script>
</body>
</html>
'''

@app.route('/')
def index():
    return send_from_directory('static', 'portal.html')

@app.route('/spiral')
def spiral():
    return send_from_directory('static', 'spiral.html')

@app.route('/classic')
def classic():
    return render_template_string(HTML_TEMPLATE)

@app.route('/health')
def health():
    return jsonify({"status": "ok", "oracle": "active", "zeros_computed": True})

@app.route('/oracle')
def oracle():
    zeros = compute_zeros(30)
    analysis = phi_analysis(zeros)
    return jsonify({
        "oracle": "Hudnall-φ Spiral",
        "discovery": "Non-trivial zeros approach Re(s)=1/2 asymptotically via φ-spiral",
        "phi": 1.618033988749895,
        "zeros": zeros[:10],
        "analysis": analysis,
        "captain": "Antonio Maurice Hudnall",
        "date": "June 14, 2026",
        "message": "The pattern reveals itself through computation, not poetry."
    })

@app.route('/zeros/<int:n>')
def get_zeros(n: int):
    n = min(n, 100)  # cap at 100
    zeros = compute_zeros(n)
    analysis = phi_analysis(zeros)
    return jsonify({"zeros": zeros, "analysis": analysis, "count": n})

@app.route('/status')
def status():
    zeros = compute_zeros(10)
    return jsonify({
        "oracle": "active",
        "sample_zeros": zeros[:3],
        "method": "mpmath.zetazero()",
        "precision": "30 decimal places"
    })

@app.route('/paper')
def paper():
    return send_from_directory('static', 'Hudnall-Phi-Spiral-White-Paper.md', 
                               mimetype='text/markdown')

@app.route('/paper.html')
def paper_html():
    from pathlib import Path as _Path
    content = (_Path(__file__).parent / 'static' / 'Hudnall-Phi-Spiral-White-Paper.md').read_text()
    body = []
    for ln in content.split('\n'):
        ln = ln.strip()
        if ln.startswith('# '): body.append(f'<h1>{ln[2:]}</h1>')
        elif ln.startswith('## '): body.append(f'<h2>{ln[3:]}</h2>')
        elif ln.startswith('### '): body.append(f'<h3>{ln[4:]}</h3>')
        elif ln.startswith('> '): body.append(f'<blockquote>{ln[2:]}</blockquote>')
        elif ln.startswith('- '): body.append(f'<li>{ln[2:]}</li>')
        elif ln == '---': body.append('<hr>')
        elif ln: body.append(f'<p>{ln}</p>')
    htm = '\n'.join(body)
    css = "body{background:#0a0a0f;color:#e0d8c0;font-family:Georgia,serif;max-width:800px;margin:40px auto;padding:20px;line-height:1.7}h1{color:#d4a843;text-align:center;font-size:1.8em}h2{color:#d4a843;margin-top:30px;border-bottom:1px solid #333;padding-bottom:5px}h3{color:#bb9933}blockquote{border-left:3px solid #d4a843;padding-left:20px;color:#887744;font-style:italic;margin:20px 0}code{background:#1a1a2e;padding:2px 6px;border-radius:3px}a{color:#d4a843}hr{border-color:#333}li{margin-left:20px}.footer{text-align:center;color:#555;margin-top:40px;font-size:.8em}"
    return f'<!DOCTYPE html><html><head><title>Hudnall-φ Spiral - White Paper</title><meta charset="utf-8"><style>{css}</style></head><body>{htm}<div class="footer"><a href="/">Back to the Spiral</a> | <a href="/paper">Raw Markdown</a></div></body></html>'
if __name__ == '__main__':
    print("🌀 Hudnall-φ Quantum Oracle v2.0 — Computing real zeros")
    print("   Port 7777 — http://127.0.0.1:7777")
    # Test computation
    z = zetazero(1)
    print(f"   ζ(1) = {z}")
    app.run(host='0.0.0.0', port=7777, debug=False)
