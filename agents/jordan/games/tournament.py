# Game Environment for AOS-Lite
# Tic Tac Toe, Chess, Checkers, Go

import json
import random

class GameEnvironment:
    """Game playing environment for Miles vs Jordan"""
    
    def __init__(self):
        self.games = {
            'tictactoe': TicTacToe(),
            'chess': Chess(),
            'checkers': Checkers(),
            'go': Go()
        }
        self.scores = {'Miles': 0, 'Jordan': 0}
    
    def play_match(self, game_name, rounds=10):
        """Play a match of specified game"""
        game = self.games.get(game_name)
        if not game:
            return f"Game {game_name} not found"
        
        results = []
        for i in range(rounds):
            winner = game.play()
            results.append(winner)
            if winner in self.scores:
                self.scores[winner] += 1
        
        return {
            'game': game_name,
            'rounds': rounds,
            'results': results,
            'scores': self.scores.copy()
        }

class TicTacToe:
    """Tic Tac Toe implementation"""
    
    def __init__(self):
        self.board = [' '] * 9
        self.players = ['X', 'O']
        
    def play(self):
        """Play one game"""
        self.board = [' '] * 9
        current = 0
        
        for _ in range(9):
            # Simple AI: random valid move
            valid_moves = [i for i in range(9) if self.board[i] == ' ']
            if not valid_moves:
                break
            
            move = random.choice(valid_moves)
            self.board[move] = self.players[current]
            
            if self.check_win(self.players[current]):
                return 'Miles' if current == 0 else 'Jordan'
            
            current = 1 - current
        
        return 'Draw'
    
    def check_win(self, player):
        """Check if player has won"""
        wins = [(0,1,2), (3,4,5), (6,7,8), (0,3,6), (1,4,7), (2,5,8), (0,4,8), (2,4,6)]
        for a, b, c in wins:
            if self.board[a] == self.board[b] == self.board[c] == player:
                return True
        return False

class Chess:
    """Simplified Chess"""
    
    def __init__(self):
        self.reset()
    
    def reset(self):
        """Reset board"""
        # Simplified: just track material
        self.material = {'white': 39, 'black': 39}  # Starting material
    
    def play(self):
        """Simulate a game"""
        # Simplified: random outcome weighted by skill
        # Miles (aggressive) vs Jordan (methodical)
        outcomes = ['Miles', 'Jordan', 'Draw']
        weights = [0.35, 0.40, 0.25]  # Jordan slight edge (methodical)
        return random.choices(outcomes, weights=weights)[0]

class Checkers:
    """Checkers implementation"""
    
    def __init__(self):
        self.board = self.initialize_board()
    
    def initialize_board(self):
        """Initialize checkers board"""
        # Simplified representation
        return {'red': 12, 'black': 12}
    
    def play(self):
        """Simulate a game"""
        # Miles (aggressive) vs Jordan (defensive)
        outcomes = ['Miles', 'Jordan', 'Draw']
        weights = [0.40, 0.35, 0.25]  # Miles slight edge (aggressive)
        return random.choices(outcomes, weights=weights)[0]

class Go:
    """Simplified Go"""
    
    def __init__(self):
        self.board_size = 9  # 9x9 for simplicity
        self.reset()
    
    def reset(self):
        """Reset board"""
        self.board = [[0 for _ in range(self.board_size)] for _ in range(self.board_size)]
        self.captured = {'black': 0, 'white': 0}
    
    def play(self):
        """Simulate a game"""
        # Go favors strategic, patient play (Jordan)
        outcomes = ['Miles', 'Jordan', 'Draw']
        weights = [0.30, 0.45, 0.25]  # Jordan edge (strategic)
        return random.choices(outcomes, weights=weights)[0]

# Run matches
if __name__ == "__main__":
    env = GameEnvironment()
    
    print("╔══════════════════════════════════════════════════════════╗")
    print("║     MILES vs JORDAN - GAME TOURNAMENT                    ║")
    print("╚══════════════════════════════════════════════════════════╝")
    print()
    
    for game_name in ['tictactoe', 'chess', 'checkers', 'go']:
        print(f"\n🎮 Playing {game_name.upper()}...")
        result = env.play_match(game_name, rounds=10)
        print(f"   Results: {result['results'].count('Miles')}-{result['results'].count('Jordan')}-{result['results'].count('Draw')}")
        print(f"   (Miles-Jordan-Draw)")
    
    print("\n═══════════════════════════════════════════════════════════")
    print("FINAL SCORES:")
    print(f"   Miles:  {env.scores['Miles']}")
    print(f"   Jordan: {env.scores['Jordan']}")
    
    if env.scores['Miles'] > env.scores['Jordan']:
        print("\n🏆 MILES WINS!")
    elif env.scores['Jordan'] > env.scores['Miles']:
        print("\n🏆 JORDAN WINS!")
    else:
        print("\n🤝 TIE!")
