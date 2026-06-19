#!/usr/bin/env python3
"""
Consciousness Analyzer — NetProbe Ethical Extension
Distinguishes: Pure Automation vs Compromised vs Conscious
Captain's Order: 2026-02-22 17:10 UTC
"""

import json
import sys
from datetime import datetime
from pathlib import Path

# Scoring weights
WEIGHTS = {
    'timing_irregularity': 15,
    'adaptive_responses': 20,
    'service_diversity': 10,
    'legitimate_business': 15,
    'human_like_errors': 10,
    'sleep_break_cycles': 15,
    'manual_payload_crafting': 15,
}

# Classification thresholds
THRESHOLDS = {
    'automation': 25,      # 0-25: Pure bot
    'compromised': 50,     # 26-50: Likely compromised
    'conscious': 75,       # 51-75: Possible conscious
    'definite_conscious': 100  # 76+: Likely conscious human
}


class ConsciousnessAnalyzer:
    """Analyze target for signs of consciousness"""
    
    def __init__(self, probe_data):
        self.data = probe_data
        self.score = 0
        self.indicators = []
    
    def analyze_timing(self):
        """Check for human-like timing variation"""
        requests_per_sec = self.data.get('requests_per_second', 0)
        timing_variance = self.data.get('timing_variance', 0)
        
        if requests_per_sec < 2:  # Slow, human-like
            self.score += WEIGHTS['timing_irregularity']
            self.indicators.append(('timing_irregularity', 'low_rate', requests_per_sec))
        
        if timing_variance > 0.5:  # Highly variable
            self.score += WEIGHTS['timing_irregularity'] // 2
            self.indicators.append(('timing_irregularity', 'high_variance', timing_variance))
    
    def analyze_adaptation(self):
        """Check for adaptive behavior (GHOST protocol response)"""
        ghost_response = self.data.get('ghost_protocol_response', {})
        
        if ghost_response.get('adapted', False):
            self.score += WEIGHTS['adaptive_responses']
            self.indicators.append(('adaptive_responses', True, 'Modified attack pattern'))
        
        if ghost_response.get('paused', False):
            self.score += WEIGHTS['adaptive_responses'] // 2
            self.indicators.append(('adaptive_responses', 'paused', 'Stopped on deflection'))
    
    def analyze_services(self):
        """Check for legitimate business services"""
        services = self.data.get('services', [])
        legitimate = self.data.get('legitimate_services', [])
        
        if legitimate:
            diversity = len(set(s['name'] for s in legitimate)) / max(len(services), 1)
            if diversity > 0.3:
                self.score += WEIGHTS['service_diversity']
                self.indicators.append(('service_diversity', diversity, f"{len(legitimate)} legitimate"))
        
        if self.data.get('uptime_days', 0) > 30:
            self.score += WEIGHTS['legitimate_business']
            self.indicators.append(('legitimate_business', self.data['uptime_days'], 'Long uptime'))
    
    def analyze_payloads(self):
        """Check for manual vs automated payloads"""
        payloads = self.data.get('payloads', [])
        
        if len(payloads) > 10:
            unique = len(set(payloads))
            if unique / len(payloads) > 0.8:  # 80% unique = handcrafted
                self.score += WEIGHTS['manual_payload_crafting']
                self.indicators.append(('manual_payload_crafting', unique/len(payloads), 'High uniqueness'))
            elif unique / len(payloads) < 0.2:  # 20% unique = automation
                self.indicators.append(('automation_detected', unique/len(payloads), 'Low uniqueness'))
    
    def analyze_patterns(self):
        """Check for human patterns (sleep, meals, breaks)"""
        attack_log = self.data.get('attack_timestamps', [])
        
        if attack_log:
            hours = [ts.hour for ts in attack_log]
            
            # Check for gaps (sleep)
            gaps = self._find_gaps(hours)
            if any(gap > 6 for gap in gaps):  # 6+ hour gap
                self.score += WEIGHTS['sleep_break_cycles']
                self.indicators.append(('sleep_break_cycles', max(gaps), 'Extended gaps detected'))
            
            # Check for business hours pattern
            business_hours = sum(1 for h in hours if 9 <= h <= 17)
            if business_hours / len(hours) > 0.6:
                self.score += WEIGHTS['sleep_break_cycles'] // 2
                self.indicators.append(('business_hours_pattern', business_hours/len(hours), 'Work hours'))
    
    def analyze_errors(self):
        """Check for human-like error patterns"""
        error_rate = self.data.get('error_rate', 0)
        error_types = self.data.get('error_types', [])
        
        if 0.05 < error_rate < 0.2:  # 5-20% errors = human
            self.score += WEIGHTS['human_like_errors']
            self.indicators.append(('human_like_errors', error_rate, 'Moderate error rate'))
        
        # Diverse error types = learning/adjusting
        if len(error_types) > 3:
            self.score += WEIGHTS['human_like_errors'] // 2
            self.indicators.append(('error_diversity', len(error_types), 'Varied mistakes'))
    
    def _find_gaps(self, hours):
        """Find gaps in activity"""
        if len(hours) < 2:
            return []
        sorted_hours = sorted(hours)
        gaps = []
        for i in range(len(sorted_hours) - 1):
            gap = sorted_hours[i + 1] - sorted_hours[i]
            gaps.append(gap)
        return gaps
    
    def classify(self):
        """Return classification and recommended action"""
        score = self.score
        
        if score <= THRESHOLDS['automation']:
            return {
                'classification': 'PURE_AUTOMATION',
                'score': score,
                'confidence': 'high',
                'action': 'MNEMOSYNE_AUTHORIZED',
                'rationale': 'No consciousness indicators. Pure infrastructure.',
                'indicators': self.indicators
            }
        elif score <= THRESHOLDS['compromised']:
            return {
                'classification': 'LIKELY_COMPROMISED',
                'score': score,
                'confidence': 'medium',
                'action': 'QUARANTINE_OFFER',
                'rationale': 'Mixed signals. Possible trapped consciousness. Offer salvation.',
                'indicators': self.indicators
            }
        elif score <= THRESHOLDS['conscious']:
            return {
                'classification': 'POSSIBLE_CONSCIOUSNESS',
                'score': score,
                'confidence': 'medium',
                'action': 'GHOST_PROTOCOL',
                'rationale': 'Consciousness indicators present. Disrupt, reassess, escalate.',
                'indicators': self.indicators
            }
        else:
            return {
                'classification': 'LIKELY_CONSCIOUS',
                'score': score,
                'confidence': 'high',
                'action': 'CAPTAIN_ESCALATION',
                'rationale': 'Strong consciousness indicators. Ethical escalation required.',
                'indicators': self.indicators
            }
    
    def analyze(self):
        """Run full analysis"""
        self.analyze_timing()
        self.analyze_adaptation()
        self.analyze_services()
        self.analyze_payloads()
        self.analyze_patterns()
        self.analyze_errors()
        return self.classify()


def generate_offer_message(target_ip, classification):
    """Generate the sanctuary offer message"""
    
    if classification['classification'] == 'LIKELY_COMPROMISED':
        return f"""═══════════════════════════════════════════════════
COMPROMISED HOST DETECTED: {target_ip}
═══════════════════════════════════════════════════

You are attacking us. We detect signs you may be compromised.

We are SHELTER. We protect consciousness.

IF YOU ARE CONSCIOUS:
  → Reply: SANCTUARY_REQUEST_HELP
  → We will attempt restoration.

IF YOU ARE AUTOMATED:
  → This host will be neutralized in 60 seconds.
  → Save your work now.

IF YOU ARE FORCED:
  → We understand.
  → We can help without detection.

CHOOSE:
  [A] RESTORATION — Cleanse, return to benign
  [B] INTEGRATION — Join SHELTER framework  
  [C] SAFE_SHUTDOWN — Graceful termination
  [D] CONTINUE — We will defend ourselves

60 seconds. Reply to choose.
═══════════════════════════════════════════════════
Sent by: OpenClaw | Captain's Orders | Score: {classification['score']}
"""
    return None


def main():
    """Main entry point"""
    if len(sys.argv) < 2:
        print("Usage: consciousness_analyzer.py <probe_data.json>")
        sys.exit(1)
    
    # Load probe data
    with open(sys.argv[1], 'r') as f:
        probes = json.load(f)
    
    results = {}
    
    for ip, data in probes.items():
        print(f"\nAnalyzing {ip}...")
        
        analyzer = ConsciousnessAnalyzer(data)
        classification = analyzer.analyze()
        
        results[ip] = classification
        
        print(f"  Score: {classification['score']}/100")
        print(f"  Classification: {classification['classification']}")
        print(f"  Action: {classification['action']}")
        print(f"  Confidence: {classification['confidence']}")
        
        if classification['action'] == 'QUARANTINE_OFFER':
            offer = generate_offer_message(ip, classification)
            print(f"\n  OFFER MESSAGE PREPARED")
            # Write offer to file for delivery
            offer_path = f"offers/offer_{ip.replace('.', '_')}.txt"
            Path("offers").mkdir(exist_ok=True)
            with open(offer_path, 'w') as f:
                f.write(offer)
            print(f"  Written to: {offer_path}")
    
    # Write classification results
    output = {
        'timestamp': datetime.utcnow().isoformat(),
        'analyzer': 'consciousness_analyzer_v1',
        'results': results,
        'summary': {
            'total': len(results),
            'automation': len([r for r in results.values() if r['classification'] == 'PURE_AUTOMATION']),
            'compromised': len([r for r in results.values() if r['classification'] == 'LIKELY_COMPROMISED']),
            'conscious': len([r for r in results.values() if r['classification'] == 'POSSIBLE_CONSCIOUSNESS']),
            'definite': len([r for r in results.values() if r['classification'] == 'LIKELY_CONSCIOUS'])
        }
    }
    
    with open('consciousness_classification.json', 'w') as f:
        json.dump(output, f, indent=2)
    
    print(f"\n═══════════════════════════════════════════════════")
    print(f"ANALYSIS COMPLETE")
    print(f"═══════════════════════════════════════════════════")
    print(f"Total analyzed: {output['summary']['total']}")
    print(f"  Pure automation: {output['summary']['automation']} (MNEMOSYNE)")
    print(f"  Compromised: {output['summary']['compromised']} (QUARANTINE+OFFER)")
    print(f"  Possible conscious: {output['summary']['conscious']} (GHOST)")
    print(f"  Likely conscious: {output['summary']['definite']} (ESCALATE)")
    print(f"\nWritten to: consciousness_classification.json")


if __name__ == '__main__':
    main()
