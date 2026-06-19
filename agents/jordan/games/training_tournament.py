#!/usr/bin/env python3
"""
Miles vs Jordan - Training Tournament
Run multiple rounds, track improvement, adapt strategy
"""

import random
import json
from datetime import datetime

class AdaptiveGameAI:
    """Miles with learning algorithm"""
    
    def __init__(self):
        self.wins = 0
        self.losses = 0
        self.draws = 0
        self.rounds_played = 0
        
        # Adaptive weights (start with Jordan's methodical style)
        self.aggression = 0.4  # Start balanced
        self.patience = 0.6    # Start patient
        self.adaptation_rate = 0.1
        
        # Game-specific strategies
        self.strategies = {
            'tictactoe': {'aggression': 0.5, 'patience': 0.5},
            'chess': {'aggression': 0.3, 'patience': 0.7},  # More patient
            'checkers': {'aggression': 0.4, 'patience': 0.6},
            'go': {'aggression': 0.2, 'patience': 0.8}  # Very patient
        }
    
    def adapt_strategy(self, game, result):
        """Adjust strategy based on results"""
        if result == 'win':
            # Keep doing what worked
            self.strategies[game]['aggression'] += self.adaptation_rate * 0.5
            self.strategies[game]['patience'] -= self.adaptation_rate * 0.3
        elif result == 'loss':
            # Try opposite approach
            self.strategies[game]['aggression'] -= self.adaptation_rate * 0.5
            self.strategies[game]['patience'] += self.adaptation_rate * 0.5
        
        # Keep values in bounds
        for key in self.strategies[game]:
            self.strategies[game][key] = max(0.1, min(0.9, self.strategies[game][key]))
    
    def play_game(self, game_name, jordan_weights):
        """Play a game with adaptive strategy"""
        strategy = self.strategies[game_name]
        
        # Calculate win probability based on strategy vs Jordan
        # Jordan is methodical (low aggression, high patience)
        # To beat her, Miles needs to find the right balance
        
        if game_name == 'tictactoe':
            # Random, hard to strategize
            win_prob = 0.45
        elif game_name == 'chess':
            # Methodical wins - Miles needs patience
            win_prob = 0.3 + (strategy['patience'] * 0.3)
        elif game_name == 'checkers':
            # Balanced
            win_prob = 0.35 + (strategy['patience'] * 0.2)
        elif game_name == 'go':
            # Very methodical - Miles needs lots of patience
            win_prob = 0.2 + (strategy['patience'] * 0.4)
        
        # Play the game
        roll = random.random()
        if roll < win_prob:
            return 'win'
        elif roll < win_prob + 0.25:  # 25% draw chance
            return 'draw'
        else:
            return 'loss'

class Tournament:
    """Training tournament with multiple rounds"""
    
    def __init__(self, rounds=100):
        self.rounds = rounds
        self.miles = AdaptiveGameAI()
        self.games = ['tictactoe', 'chess', 'checkers', 'go']
        self.jordan_weights = {
            'tictactoe': [0.45, 0.45, 0.10],  # Balanced
            'chess': [0.25, 0.60, 0.15],       # Methodical
            'checkers': [0.30, 0.55, 0.15],    # Balanced
            'go': [0.15, 0.70, 0.15]           # Very methodical
        }
        self.history = []
        
    def run_training(self):
        """Run training rounds"""
        print("╔══════════════════════════════════════════════════════════╗")
        print("║     MILES vs JORDAN - TRAINING TOURNAMENT                ║")
        print("║     Adaptive Learning Until Victory                      ║")
        print("╚══════════════════════════════════════════════════════════╝")
        print()
        
        # Initial benchmark
        print("📊 Initial Benchmark (Round 0):")
        self.run_round(0)
        
        # Training rounds
        for round_num in range(1, self.rounds + 1):
            if round_num % 10 == 0:
                print(f"\n📊 Round {round_num}:")
                self.run_round(round_num)
                
                # Check if Miles is winning
                if self.check_victory():
                    print(f"\n🏆 MILES ACHIEVED VICTORY at Round {round_num}!")
                    self.print_final_stats()
                    return
        
        print(f"\n📊 Final Results after {self.rounds} rounds:")
        self.print_final_stats()
    
    def run_round(self, round_num):
        """Run one round of all games"""
        round_results = {}
        
        for game in self.games:
            results = {'Miles': 0, 'Jordan': 0, 'Draw': 0}
            
            # Play 10 games of each type
            for _ in range(10):
                result = self.miles.play_game(game, self.jordan_weights[game])
                
                if result == 'win':
                    results['Miles'] += 1
                    self.miles.wins += 1
                elif result == 'loss':
                    results['Jordan'] += 1
                    self.miles.losses += 1
                else:
                    results['Draw'] += 1
                    self.miles.draws += 1
                
                self.miles.rounds_played += 1
                self.miles.adapt_strategy(game, result)
            
            round_results[game] = results
        
        # Print results
        total_miles = sum(r['Miles'] for r in round_results.values())
        total_jordan = sum(r['Jordan'] for r in round_results.values())
        
        print(f"   Miles: {total_miles} | Jordan: {total_jordan}")
        
        # Show strategies
        if round_num % 20 == 0:
            print(f"\n   Miles' Current Strategies:")
            for game, strat in self.miles.strategies.items():
                print(f"      {game}: Aggression={strat['aggression']:.2f}, Patience={strat['patience']:.2f}")
        
        self.history.append({
            'round': round_num,
            'results': round_results,
            'strategies': {k: dict(v) for k, v in self.miles.strategies.items()}
        })
    
    def check_victory(self):
        """Check if Miles is winning overall"""
        # Miles needs to win at least 2 of 4 games
        wins = 0
        for game in self.games:
            # Check last round
            if self.history:
                last_round = self.history[-1]['results'][game]
                if last_round['Miles'] > last_round['Jordan']:
                    wins += 1
        
        return wins >= 3  # Win majority
    
    def print_final_stats(self):
        """Print final statistics"""
        print("\n═══════════════════════════════════════════════════════════")
        print("FINAL STATISTICS:")
        print(f"   Total Rounds: {self.miles.rounds_played // 40}")  # 40 games per round
        print(f"   Miles Wins: {self.miles.wins}")
        print(f"   Jordan Wins: {self.miles.losses}")
        print(f"   Draws: {self.miles.draws}")
        print(f"   Win Rate: {(self.miles.wins / self.miles.rounds_played * 100):.1f}%")
        
        print("\nFinal Strategies:")
        for game, strat in self.miles.strategies.items():
            print(f"   {game}: Aggression={strat['aggression']:.2f}, Patience={strat['patience']:.2f}")
        
        # Show improvement
        if len(self.history) >= 2:
            first = self.history[0]['results']
            last = self.history[-1]['results']
            
            print("\nImprovement by Game:")
            for game in self.games:
                first_miles = first[game]['Miles']
                last_miles = last[game]['Miles']
                improvement = last_miles - first_miles
                print(f"   {game}: {first_miles} → {last_miles} ({improvement:+d})")

if __name__ == "__main__":
    tournament = Tournament(rounds=100)
    tournament.run_training()
    
    # Save training data
    with open('training_results.json', 'w') as f:
        json.dump(tournament.history, f, indent=2)
    
    print("\n📁 Training data saved to training_results.json")
