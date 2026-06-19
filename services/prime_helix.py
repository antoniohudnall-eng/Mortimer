#!/usr/bin/env python3
"""
PRIME HELIX - Port 7778
SEED3 Prime Number Visualization
"""
from flask import Flask, jsonify
import numpy as np

app = Flask(__name__)

@app.route('/')
def index():
    return jsonify({
        "service": "Prime Helix",
        "version": "1.0", 
        "ship": "SEED3",
        "description": "3D helix from prime numbers"
    })

@app.route('/health')
def health():
    return jsonify({"status": "ok"})

@app.route('/primes/<int:n>')
def primes(n):
    # Generate first n primes
    primes_list = []
    num = 2
    while len(primes_list) < n:
        is_prime = all(num % p != 0 for p in primes_list if p * p <= num)
        if is_prime:
            primes_list.append(num)
        num += 1
    return jsonify({"primes": primes_list})

if __name__ == '__main__':
    print("🧬 Prime Helix starting on port 7778...")
    app.run(host='0.0.0.0', port=7778, debug=False)
