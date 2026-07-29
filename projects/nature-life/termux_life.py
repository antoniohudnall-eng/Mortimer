#!/usr/bin/env python3
"""
Nature-Life Simulator + Mandelbrot OODA Engine — TERMINAL EDITION v2.0
Mortimer/Morty — SEED3 — 2026-07-26
Uses curses native colors (no raw ANSI) for Termux compatibility.
"""

import curses
import math
import random
import time
import json
import os
from pathlib import Path
from datetime import datetime

# ============================================================================
# Universal Constants
# ============================================================================
SPEED_OF_LIGHT = 299792458
GRAVITY_CONSTANT = 6.674e-11
PLANCK_CONSTANT = 6.626e-34
ELEMENTARY_CHARGE = 1.602e-19
BOLTZMANN_CONSTANT = 1.381e-23
AVOGADRO_CONSTANT = 6.022e23
GAS_CONSTANT = 8.314
PERMITTIVITY_FREE = 8.854e-12
PERMEABILITY_FREE = 1.257e-6
FINE_STRUCTURE = 0.007297
ELECTRON_MASS = 9.109e-31
PROTON_MASS = 1.673e-27
NEUTRON_MASS = 1.675e-27
PLANCK_LENGTH = 1.616e-35
PLANCK_TIME = 5.391e-44
COULOMB_CONSTANT = 8.987e9
STEFAN_BOLTZMANN = 5.670e-8
WIEN_DISPLACEMENT = 2.897e-3
RYDBERG_CONSTANT = 1.097e7
BOHR_RADIUS = 5.292e-11
BOHR_MAGNETON = 9.274e-24
ELECTRIC_CONSTANT = 8.854e-12
HUBBLE_CONSTANT = 70
COSMOLOGICAL_CONSTANT = 1e-52
EULER_NUMBER = 2.718281828459045
PI = 3.141592653589793
GM = 1.618033988749895


# ============================================================================
# Neural Network — All fixes applied
# ============================================================================
class NeuralNetwork:
    def __init__(self, input_size, hidden_size, output_size):
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.output_size = output_size
        self.weights1 = self._random_matrix(input_size, hidden_size)
        self.weights2 = self._random_matrix(hidden_size, output_size)
        self.memory = []

    def _random_matrix(self, rows, cols):
        return [[random.uniform(-1, 1) for _ in range(cols)] for _ in range(rows)]

    @staticmethod
    def sigmoid(x):
        try:
            return 1.0 / (1.0 + math.exp(-x))
        except OverflowError:
            return 0.0 if x < 0 else 1.0

    def feedforward(self, inputs):
        if len(inputs) != self.input_size:
            return [0.0] * self.output_size
        hidden_raw = self._matrix_multiply(inputs, self.weights1)
        hidden_act = [self.sigmoid(h) for h in hidden_raw]
        output_raw = self._matrix_multiply(hidden_act, self.weights2)
        output_act = [self.sigmoid(o) for o in output_raw]
        return output_act

    def _matrix_multiply(self, a, b):
        if not a or not b or not b[0] or len(a) != len(b):
            return [0.0] * len(b[0]) if b and b[0] else []
        result = [0.0] * len(b[0])
        for i in range(len(b[0])):
            for j in range(len(a)):
                result[i] += a[j] * b[j][i]
        return result

    def train(self, inputs, target, epochs=10, lr=0.1):
        if len(inputs) != self.input_size or len(target) != self.output_size:
            return
        for _ in range(epochs):
            hidden_raw = self._matrix_multiply(inputs, self.weights1)
            hidden_act = [self.sigmoid(h) for h in hidden_raw]
            output_raw = self._matrix_multiply(hidden_act, self.weights2)
            output_act = [self.sigmoid(o) for o in output_raw]

            output_delta = [(target[k] - output_act[k]) * output_act[k] * (1 - output_act[k])
                          for k in range(self.output_size)]

            hidden_error = [0.0] * self.hidden_size
            for j in range(self.hidden_size):
                for k in range(self.output_size):
                    hidden_error[j] += output_delta[k] * self.weights2[j][k]
            hidden_delta = [hidden_error[j] * hidden_act[j] * (1 - hidden_act[j])
                          for j in range(self.hidden_size)]

            for j in range(self.hidden_size):
                for k in range(self.output_size):
                    self.weights2[j][k] += lr * output_delta[k] * hidden_act[j]
            for i in range(self.input_size):
                for j in range(self.hidden_size):
                    self.weights1[i][j] += lr * hidden_delta[j] * inputs[i]

    def train_q(self, state, action, reward, next_state):
        if len(state) != self.input_size or not (0 <= action < self.output_size):
            return
        hidden_raw = self._matrix_multiply(state, self.weights1)
        hidden_act = [self.sigmoid(h) for h in hidden_raw]
        output_raw = self._matrix_multiply(hidden_act, self.weights2)
        output_act = [self.sigmoid(o) for o in output_raw]

        current_q = output_act[action]
        next_output = self.feedforward(next_state)
        next_q = max(next_output[:self.output_size])
        target_q = reward + Simulation.GAMMA * next_q
        error = target_q - current_q

        output_delta = error * output_act[action] * (1 - output_act[action])

        hidden_delta = [0.0] * self.hidden_size
        for j in range(self.hidden_size):
            hidden_delta[j] = output_delta * self.weights2[j][action] * hidden_act[j] * (1 - hidden_act[j])

        for j in range(self.hidden_size):
            self.weights2[j][action] += Simulation.ALPHA * output_delta * hidden_act[j]
        for i in range(self.input_size):
            for j in range(self.hidden_size):
                self.weights1[i][j] += Simulation.ALPHA * hidden_delta[j] * state[i]

    def train_batch(self, batch):
        for exp in batch:
            self.train_q(exp['state'], exp['action'], exp['reward'], exp['next_state'])

    def add_node(self):
        self.hidden_size += 1
        self.weights1 = [row + [random.uniform(-1, 1)] for row in self.weights1]
        self.weights2.append([random.uniform(-1, 1) for _ in range(self.output_size)])
        self.memory.append({'type': 'node', 'hiddenSize': self.hidden_size})

    def add_layer(self, size):
        if not isinstance(size, int) or size <= 0:
            return
        old_hidden = self.hidden_size
        old_w1, old_w2 = self.weights1, self.weights2
        self.weights1 = self._random_matrix(self.input_size, size)
        self.weights2 = self._random_matrix(size, self.output_size)
        self.hidden_size = size
        ratio = size / old_hidden
        for i in range(self.input_size):
            for j in range(old_hidden):
                ni = int(j * ratio)
                self.weights1[i][ni] = (self.weights1[i][ni] + old_w1[i][j]) / 2
        for j in range(old_hidden):
            ni = int(j * ratio)
            for k in range(self.output_size):
                self.weights2[ni][k] = (self.weights2[ni][k] + old_w2[j][k]) / 2
        self.memory.append({'type': 'layer', 'size': size, 'migratedFrom': old_hidden})


# ============================================================================
# Simulation State
# ============================================================================
class Simulation:
    ALPHA = 0.1
    GAMMA = 0.9

    def __init__(self):
        self.animals = []
        self.microbes = []
        self.environment = {'grass': [], 'shrubs': [], 'trees': []}
        self.mandelbrot_nn = NeuralNetwork(4, 5, 1)
        self.voice_input = ""
        self.last_ooda_time = 0
        self.epsilon = 0.1
        self.replay_buffer = []
        self.buffer_size = 1000
        self.batch_size = 32
        self.running = True
        self.paused = False
        self.log_messages = []
        self._generate_nature()

    def _sunlight(self):
        now = datetime.now()
        hours = now.hour + now.minute / 60.0
        return math.sin((hours / 24) * 2 * PI - PI / 2) * PI / 2

    def _create_animal(self, class_type):
        sf = random.uniform(0.7, 1.0) if class_type == "Prey" else random.uniform(0.5, 0.8)
        mass = random.uniform(10, 40) if class_type == "Prey" else random.uniform(30, 80)
        energy = random.uniform(300, 500) if class_type == "Prey" else random.uniform(800, 1200)
        return {
            'type': class_type,
            'x': random.random() * 0.9, 'y': random.random() * 0.7,
            'speed': sf,
            'mass': mass, 'energy': energy,
            'nn': NeuralNetwork(6, 4, 3),
            'complexity': 1
        }

    def _generate_nature(self):
        self.animals = []
        self.microbes = []
        self.environment = {'grass': [], 'shrubs': [], 'trees': []}

        for i in range(6):
            t = ["Short", "Tall", "Dense"][i % 3]
            h = 0.05 if t == "Short" else (0.2 if t == "Tall" else 0.1)
            d = 1.5 if t == "Dense" else (0.5 if t == "Short" else 1.0)
            self.environment['grass'].append({
                'type': f"Grass_{t}", 'x': random.random() * 0.9, 'y': random.random() * 0.7,
                'height': PLANCK_CONSTANT * 1e34 * h,
                'density': AVOGADRO_CONSTANT / 1e22 * d,
                'regenRate': 0.02 if t == "Short" else (0.01 if t == "Tall" else 0.015)
            })

        for i in range(4):
            t = ["Thorny", "Leafy", "Flowering"][i % 3]
            ey = 2 if t == "Flowering" else (1.5 if t == "Leafy" else 1)
            r = 0.4 if t == "Flowering" else (0.2 if t == "Thorny" else 0.3)
            self.environment['shrubs'].append({
                'type': f"Shrub_{t}", 'x': random.random() * 0.9, 'y': random.random() * 0.7,
                'height': GRAVITY_CONSTANT * 1e11 * (0.8 if t == "Thorny" else (1.2 if t == "Leafy" else 1)),
                'radius': PI * r, 'energyYield': ey
            })

        for i in range(3):
            t = ["Deciduous", "Evergreen", "Fruit"][i % 3]
            st = 1.5 if t == "Evergreen" else (0.8 if t == "Fruit" else 1)
            tr = 0.15 if t == "Deciduous" else (0.1 if t == "Fruit" else 0.2)
            self.environment['trees'].append({
                'type': f"Tree_{t}", 'x': random.random() * 0.9, 'y': random.random() * 0.7,
                'height': EULER_NUMBER ** (3.5 if t == "Evergreen" else (2.5 if t == "Fruit" else 3)),
                'trunkRadius': GM * tr, 'stability': st
            })

        for _ in range(5):
            self.microbes.append({
                'type': "Microbe", 'x': random.random() * 0.9, 'y': random.random() * 0.7,
                'activity': ELECTRON_MASS * 1e31 * (random.random() * 0.5 + 0.5),
                'nutrientBoost': PLANCK_LENGTH * 1e35 * (random.random() * 0.1 + 0.05)
            })

        for i in range(4):
            self.animals.append(self._create_animal("Prey" if i % 2 == 0 else "Predator"))

    def _dist(self, a, b):
        return math.hypot(a['x'] - b['x'], a['y'] - b['y'])

    def _nearest(self, items, ref):
        if not items:
            return None
        return min(items, key=lambda item: self._dist(item, ref))

    def _get_animal_state(self, animal):
        if animal['type'] == "Prey":
            all_food = self.environment['grass'] + self.environment['shrubs']
            nf = self._nearest(all_food, animal)
            nt = self._nearest([a for a in self.animals if a['type'] == "Predator"], animal)
        else:
            nf = self._nearest([a for a in self.animals if a['type'] == "Prey" and a is not animal], animal)
            nt = None
        fd = self._dist(animal, nf) if nf else 1.0
        td = self._dist(animal, nt) if nt else 1.0
        sun = self._sunlight() / PI
        return [
            min(1.0, animal['energy'] / (500.0 if animal['type'] == "Prey" else 1500.0)),
            min(1.0, animal['speed'] / 1.0),
            min(1.0, animal['mass'] / 80.0),
            min(1.0, fd / 0.9),
            min(1.0, (td if animal['type'] == "Prey" else fd) / 0.9),
            max(0.0, min(1.0, sun))
        ]

    def tick_animals(self):
        if self.paused:
            return
        for animal in list(self.animals):
            state = self._get_animal_state(animal)
            reward = 0.01
            q_vals = animal['nn'].feedforward(state)
            action = random.randrange(3) if random.random() < self.epsilon else q_vals.index(max(q_vals[:3]))

            if animal['type'] == "Prey":
                all_food = self.environment['grass'] + self.environment['shrubs']
                nf = self._nearest(all_food, animal)
                nt = self._nearest([a for a in self.animals if a['type'] == "Predator"], animal)
            else:
                nf = self._nearest([a for a in self.animals if a['type'] == "Prey" and a is not animal], animal)
                nt = None

            fd = self._dist(animal, nf) if nf else 1.0
            td = self._dist(animal, nt) if nt else 1.0

            if action == 0 and nf:
                dx, dy = nf['x'] - animal['x'], nf['y'] - animal['y']
                dist = math.hypot(dx, dy) or 0.001
                animal['x'] += (dx / dist) * animal['speed'] * 0.02
                animal['y'] += (dy / dist) * animal['speed'] * 0.02
                animal['energy'] -= 5 + animal['mass'] * 0.1
            elif action == 2 and nt and animal['type'] == "Prey":
                dx, dy = animal['x'] - nt['x'], animal['y'] - nt['y']
                dist = math.hypot(dx, dy) or 0.001
                animal['x'] += (dx / dist) * animal['speed'] * 0.03
                animal['y'] += (dy / dist) * animal['speed'] * 0.03
                animal['energy'] -= 10 + animal['mass'] * 0.2
                if td > 0.3:
                    reward = -0.5
            elif action == 2 and nf and animal['type'] == "Predator":
                dx, dy = nf['x'] - animal['x'], nf['y'] - animal['y']
                dist = math.hypot(dx, dy) or 0.001
                animal['x'] += (dx / dist) * animal['speed'] * 0.025
                animal['y'] += (dy / dist) * animal['speed'] * 0.025
                animal['energy'] -= 8 + animal['mass'] * 0.15
            elif action == 1 and fd < 0.05 and nf:
                if animal['type'] == "Prey":
                    gain = 200 * nf.get('density', 1) * nf.get('energyYield', 1)
                    animal['energy'] += gain
                    nf['density'] = nf.get('density', 1) * 0.5
                    if nf['density'] < 0.1:
                        self.environment['grass'] = [g for g in self.environment['grass'] if g is not nf]
                        self.environment['shrubs'] = [s for s in self.environment['shrubs'] if s is not nf]
                else:
                    animal['energy'] += 500
                    self.animals = [a for a in self.animals if a is not nf]
                reward = 1

            animal['x'] = max(0, min(0.9, animal['x']))
            animal['y'] = max(0, min(0.7, animal['y']))

            ns = self._get_animal_state(animal)
            self.replay_buffer.append({'state': state, 'action': action, 'reward': reward, 'next_state': ns})
            if len(self.replay_buffer) > self.buffer_size:
                self.replay_buffer.pop(0)

            if len(self.replay_buffer) >= self.batch_size:
                batch = [self.replay_buffer[random.randrange(len(self.replay_buffer))]
                        for _ in range(self.batch_size)]
                animal['nn'].train_batch(batch)

            threshold = 500 if animal['type'] == "Prey" else 1500
            if animal['energy'] > threshold and random.random() < COSMOLOGICAL_CONSTANT * 1e52 * animal['complexity']:
                animal['complexity'] += 1
                if random.random() < 0.7:
                    animal['nn'].add_node()
                else:
                    animal['nn'].add_layer(4)
                self.log(f"{animal['type']} Evolved! Complexity: {animal['complexity']}")

            if animal['energy'] < 0:
                self.animals = [a for a in self.animals if a is not animal]
                self.replay_buffer.append({'state': state, 'action': action, 'reward': -1, 'next_state': ns})

        self.epsilon = max(0.01, self.epsilon * 0.995)

    def tick_microbes(self):
        if self.paused:
            return
        for m in list(self.microbes):
            dead = [item for item in (self.environment['grass'] + self.environment['shrubs'])
                   if item.get('density', 1) < 0.2]
            nearest = self._nearest(dead, m)
            if nearest and self._dist(m, nearest) < 0.05:
                nearest['density'] = nearest.get('density', 0) + m['nutrientBoost']
                m['activity'] -= PLANCK_LENGTH * 1e35 * 0.01
            if random.random() < m['activity']:
                m['x'] += (random.random() - 0.5) * PLANCK_TIME * 1e44
                m['y'] += (random.random() - 0.5) * PLANCK_TIME * 1e44
                m['x'] = max(0, min(0.9, m['x']))
                m['y'] = max(0, min(0.7, m['y']))
            if random.random() < WIEN_DISPLACEMENT * 1e3:
                self.environment['grass'].append({
                    'type': f"Grass_{random.choice(['Short','Tall','Dense'])}",
                    'x': m['x'] + (random.random() - 0.5) * 0.1,
                    'y': m['y'] + (random.random() - 0.5) * 0.1,
                    'height': PLANCK_CONSTANT * 1e34 * (random.random() * 0.15 + 0.05),
                    'density': AVOGADRO_CONSTANT / 1e22 * (random.random() * 0.5 + 0.5),
                    'regenRate': 0.015
                })
        self.microbes = [m for m in self.microbes if m['activity'] > 0]

    def tick_events(self):
        if self.paused:
            return
        if random.random() < 0.05:
            if random.random() < 0.5:
                for a in self.animals:
                    a['energy'] *= 0.8
                self.log("Storm hits!")
            else:
                for g in self.environment['grass']:
                    g['density'] = g.get('density', 1) * 1.2
                self.log("Nutrient surge!")

    def tick_mandelbrot(self):
        now = time.time()
        if now - self.last_ooda_time > 5.0:
            self.last_ooda_time = now
            obs = [0.8, random.random(), len(self.voice_input) / 100.0, self._sunlight() / PI]
            situation = self.mandelbrot_nn.feedforward(obs)[0]
            if situation > 0.7:
                self.mandelbrot_nn.add_node()
                self.log(f"Mandelbrot NN: +node (s={situation:.3f})")
            elif situation < 0.3:
                self.mandelbrot_nn.add_layer(6)
                self.log(f"Mandelbrot NN: +layer (s={situation:.3f})")

    def log(self, msg):
        self.log_messages.append(msg)
        if len(self.log_messages) > 100:
            self.log_messages = self.log_messages[-50:]

    def run_command(self, cmd):
        cmd = cmd.lower().strip()
        if cmd == 'p':
            self.paused = not self.paused
            self.log("Paused" if self.paused else "Resumed")
        elif cmd == 'r':
            self._generate_nature()
            self.log("Simulation reset")
        elif cmd == 's':
            self.animals.append(self._create_animal("Prey"))
            self.log("Spawned prey")
        elif cmd == 'd':
            self.animals.append(self._create_animal("Predator"))
            self.log("Spawned predator")
        elif cmd == 'e':
            for a in self.animals:
                if a['type'] == "Prey":
                    all_food = self.environment['grass'] + self.environment['shrubs']
                    food = self._nearest(all_food, a)
                else:
                    food = self._nearest([x for x in self.animals if x['type'] == "Prey" and x is not a], a)
                if food and self._dist(a, food) < 0.05:
                    if a['type'] == "Prey":
                        a['energy'] += STEFAN_BOLTZMANN * 1e8 * food.get('density', 1) * food.get('energyYield', 1)
                        food['density'] = food.get('density', 1) * 0.5
                    else:
                        a['energy'] += STEFAN_BOLTZMANN * 1e8 * food['energy'] / 1e3
                        self.animals = [x for x in self.animals if x is not food]
            self.log("Animals eating")
        elif cmd == 'g':
            self.environment['grass'].append({
                'type': f"Grass_{random.choice(['Short','Tall','Dense'])}",
                'x': random.random() * 0.9, 'y': random.random() * 0.7,
                'height': PLANCK_CONSTANT * 1e34 * (random.random() * 0.15 + 0.05),
                'density': AVOGADRO_CONSTANT / 1e22 * (random.random() * 0.5 + 0.5),
                'regenRate': 0.015
            })
            self.log("Growing grass")
        elif cmd == 'm':
            self.log("Rendering Mandelbrot...")
        elif cmd == '+':
            for a in self.animals:
                a['nn'].add_node()
            self.log("Increased NN complexity")
        elif cmd == 'c':
            self.mandelbrot_nn.add_node()
            self.log("Added node to Mandelbrot NN")

    def save_weights(self):
        data = {
            'animals': [{'w1': a['nn'].weights1, 'w2': a['nn'].weights2, 'hs': a['nn'].hidden_size}
                       for a in self.animals],
            'mandelbrot': {'w1': self.mandelbrot_nn.weights1, 'w2': self.mandelbrot_nn.weights2,
                          'hs': self.mandelbrot_nn.hidden_size}
        }
        path = Path.home() / 'mortimer' / 'projects' / 'nature-life' / 'weights_terminal.json'
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, 'w') as f:
            json.dump(data, f)
        self.log("Weights saved")

    def load_weights(self):
        path = Path.home() / 'mortimer' / 'projects' / 'nature-life' / 'weights_terminal.json'
        if not path.exists():
            self.log("No saved weights found")
            return
        with open(path) as f:
            data = json.load(f)
        for i, a in enumerate(self.animals):
            if i < len(data['animals']):
                a['nn'].weights1 = data['animals'][i]['w1']
                a['nn'].weights2 = data['animals'][i]['w2']
                a['nn'].hidden_size = data['animals'][i]['hs']
        self.mandelbrot_nn.weights1 = data['mandelbrot']['w1']
        self.mandelbrot_nn.weights2 = data['mandelbrot']['w2']
        self.mandelbrot_nn.hidden_size = data['mandelbrot']['hs']
        self.log("Weights loaded")


# ============================================================================
# Curses Color Setup — Bob Ross palette mapped to curses color pairs
# ============================================================================

# Bob Ross palette RGB values
BOB_ROSS_RGB = [
    (227, 38, 54),   # 0  Alizarin Crimson
    (255, 99, 71),   # 1  Bright Red
    (255, 215, 0),   # 2  Cadmium Yellow
    (60, 20, 20),    # 3  Dark Sienna
    (255, 179, 71),  # 4  Indian Yellow
    (0, 0, 0),       # 5  Midnight Black
    (0, 15, 137),    # 6  Phthalo Blue
    (18, 53, 36),    # 7  Phthalo Green
    (0, 49, 83),     # 8  Prussian Blue
    (80, 125, 42),   # 9  Sap Green
    (102, 66, 40),   # 10 Van Dyke Brown
    (240, 187, 94),  # 11 Yellow Ochre
    (253, 245, 230), # 12 Titanium White
    (220, 220, 220), # 13 Light Gray
]

# Mapped to 8 standard terminal colors (best approximation per Bob Ross swatch)
# color_pair index -> (curses fg color constant, curses bg color constant)
COLOR_MAP = {}  # filled at init

# Mandelbrot ASCII ramp (dark to bright)
MANDEL_CHARS = " .:;+=xX$@#"


def init_colors():
    """Initialize curses color pairs from Bob Ross palette."""
    # We'll use 8 base curses colors as our palette, mapping Bob Ross values to
    # the closest base color. We define named pairs.
    # curses colors: 0=BLACK, 1=RED, 2=GREEN, 3=YELLOW, 4=BLUE, 5=MAGENTA, 6=CYAN, 7=WHITE

    # Create pairs: (pair_num, fg_color, bg_color)
    # We'll use pairs 1-14 for the Bob Ross colors on black background
    pair_map = {
        0:  curses.COLOR_RED,        # Alizarin Crimson
        1:  curses.COLOR_RED,        # Bright Red
        2:  curses.COLOR_YELLOW,     # Cadmium Yellow
        3:  curses.COLOR_BLACK,      # Dark Sienna (use red for visibility)
        4:  curses.COLOR_YELLOW,     # Indian Yellow
        5:  curses.COLOR_BLACK,      # Midnight Black
        6:  curses.COLOR_BLUE,       # Phthalo Blue
        7:  curses.COLOR_GREEN,      # Phthalo Green
        8:  curses.COLOR_BLUE,       # Prussian Blue
        9:  curses.COLOR_GREEN,      # Sap Green
        10: curses.COLOR_YELLOW,      # Van Dyke Brown
        11: curses.COLOR_YELLOW,      # Yellow Ochre
        12: curses.COLOR_WHITE,       # Titanium White
        13: curses.COLOR_WHITE,       # Light Gray
    }
    # Override: Dark Sienna & Midnight Black -> use RED dimly, BLACK is invisible
    pair_map[3] = curses.COLOR_RED    # Dark Sienna -> dim red
    pair_map[5] = curses.COLOR_BLACK  # Midnight Black -> black (invisible on black bg: use white)

    for i, fg in pair_map.items():
        try:
            # Use black background for everything
            curses.init_pair(i + 1, fg, curses.COLOR_BLACK)
        except Exception:
            pass
    # Fix Midnight Black: use white so it's visible
    try:
        curses.init_pair(6, curses.COLOR_WHITE, curses.COLOR_BLACK)  # pair 6 = Midnight Black -> white
    except Exception:
        pass


def ross_pair(value):
    """Map a 0-1 value to the closest Bob Ross color pair number (1-14)."""
    value = max(0, min(1, value))
    idx = min(int(value * (len(BOB_ROSS_RGB) - 1)), len(BOB_ROSS_RGB) - 1)
    return idx + 1  # pairs are 1-indexed


# ============================================================================
# Terminal Rendering
# ============================================================================

def put_char(win, y, x, char, pair_num=0):
    """Safely draw a character with optional color pair."""
    try:
        if pair_num:
            win.addstr(y, x, char, curses.color_pair(pair_num))
        else:
            win.addstr(y, x, char)
    except curses.error:
        pass


def draw_mandelbrot(win, start_y, start_x, width, height):
    """Render Mandelbrot using character ramp with curses color pairs."""
    mi = 35
    for py in range(height):
        for px in range(width):
            real = -2.0 + (px / width) * 3.0 * GM
            imag = -1.0 + (py / height) * 2.0
            zr, zi, it = 0.0, 0.0, 0
            while zr * zr + zi * zi <= 4 and it < mi:
                zr, zi = zr * zr - zi * zi + real, 2 * zr * zi + imag
                it += 1
            val = it / mi
            char = MANDEL_CHARS[min(int(val * (len(MANDEL_CHARS) - 0.01)), len(MANDEL_CHARS) - 1)]
            pair = ross_pair(val)
            put_char(win, start_y + py, start_x + px, char, pair)


def draw_nature(win, start_y, start_x, width, height):
    """Render nature simulation as colored ASCII map using curses color pairs."""

    def mx(x):
        return start_x + int(x * width)
    def my(y):
        return start_y + int(y * height * 0.75)

    # Grass
    for g in Simulation._sim.environment['grass']:
        pair = ross_pair(g.get('density', 0.5) / 2)
        put_char(win, my(g['y']), mx(g['x']), ',', pair)

    # Shrubs
    for s in Simulation._sim.environment['shrubs']:
        pair = ross_pair(s.get('energyYield', 1) / 2)
        put_char(win, my(s['y']), mx(s['x']), '*', pair)

    # Trees
    for t in Simulation._sim.environment['trees']:
        pair = ross_pair(t.get('stability', 1) / 1.5)
        put_char(win, my(t['y']), mx(t['x']), 'T', pair)

    # Microbes
    for m in Simulation._sim.microbes:
        pair = ross_pair(m['activity'] / (ELECTRON_MASS * 1e31))
        put_char(win, my(m['y']), mx(m['x']), '.', pair)

    # Animals
    for a in Simulation._sim.animals:
        pair = ross_pair(a['energy'] / (500 if a['type'] == "Prey" else 1500))
        ch = 'p' if a['type'] == "Prey" else 'P'
        put_char(win, my(a['y']), mx(a['x']), ch, pair)


def safe_addstr(win, y, x, text, attr=0):
    """Add a string safely, truncating to window bounds."""
    try:
        max_y, max_x = win.getmaxyx()
        if y >= max_y or x >= max_x:
            return
        text = text[:max_x - x - 1]
        win.addstr(y, x, text, attr)
    except curses.error:
        pass


def main(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(True)
    stdscr.timeout(50)

    # Initialize colors
    if curses.has_colors():
        curses.start_color()
        try:
            curses.use_default_colors()
        except Exception:
            pass
        init_colors()

    sim = Simulation()
    # Store sim on class for render functions
    Simulation._sim = sim

    sim.log("Nature-Life Terminal v2.0 — SEED3")
    sim.log("[p]ause [r]eset [s]pawn prey [d]predator [e]at [g]rass [+]complex [c]Mandel+node [w]save [l]oad [q]uit")

    microbe_timer = 0
    event_timer = 0
    animal_timer = 0
    running = True

    while running:
        try:
            key = stdscr.getch()
        except Exception:
            key = -1

        cmd_map = {
            ord('q'): 'quit',
            ord('p'): 'p', ord('r'): 'r', ord('s'): 's', ord('d'): 'd',
            ord('e'): 'e', ord('g'): 'g', ord('m'): 'm',
            ord('+'): '+', ord('='): '+', ord('c'): 'c',
            ord('w'): 'save', ord('l'): 'load',
        }

        if key in cmd_map:
            cmd = cmd_map[key]
            if cmd == 'quit':
                running = False
            elif cmd == 'save':
                sim.save_weights()
            elif cmd == 'load':
                sim.load_weights()
            else:
                sim.run_command(cmd)

        # Tick
        animal_timer += 1
        if animal_timer >= 10:
            sim.tick_animals()
            animal_timer = 0

        microbe_timer += 1
        if microbe_timer >= 20:
            sim.tick_microbes()
            microbe_timer = 0

        event_timer += 1
        if event_timer >= 20:
            sim.tick_events()
            event_timer = 0

        sim.tick_mandelbrot()

        # Render
        stdscr.erase()
        max_y, max_x = stdscr.getmaxyx()

        # Status bar
        status = f" Nature: {len(sim.animals)} animals | {len(sim.microbes)} microbes | e={sim.epsilon:.3f} | "
        status += "PAUSED " if sim.paused else "RUNNING"
        safe_addstr(stdscr, 0, 0, status.ljust(max_x), curses.A_REVERSE)

        # Layout
        map_w = max_x // 2
        map_h = min((max_y - 10) // 2, 12)

        if map_w > 10 and map_h > 3:
            draw_nature(stdscr, 1, 1, map_w - 2, map_h)

        if max_x - map_w - 2 > 10 and map_h > 3:
            draw_mandelbrot(stdscr, 1, map_w + 1, max_x - map_w - 2, map_h)

        # Legend
        legend_y = 1 + map_h + 1
        safe_addstr(stdscr, legend_y, 1, "Nature: p=prey P=predator ,=grass *=shrub T=tree .=microbe")
        legend_y += 1
        nn_info = f"Mandelbrot NN: hidden={sim.mandelbrot_nn.hidden_size} memory={len(sim.mandelbrot_nn.memory)}"
        safe_addstr(stdscr, legend_y, 1, nn_info)

        # Animal details
        detail_y = 1 + map_h + 3
        for i, a in enumerate(sim.animals[:5]):
            if detail_y + i >= max_y - 2:
                break
            char = 'p' if a['type'] == "Prey" else 'P'
            info = f"  {char} {a['type']:<8} pos=({a['x']:.2f},{a['y']:.2f})  hs={a['nn'].hidden_size} c={a['complexity']} e={a['energy']:.1f}"
            safe_addstr(stdscr, detail_y + i, 1, info)

        # Log area
        log_start = max(detail_y + 6, max_y - 8)
        safe_addstr(stdscr, log_start - 1, 1, "-" * (max_x - 2))
        for i, msg in enumerate(sim.log_messages[-6:]):
            y = log_start + i
            if y < max_y - 1:
                safe_addstr(stdscr, y, 1, f"  {msg}")

        # Help bar
        help_text = " [q]uit [p]ause [r]eset [s]pawn [e]at [g]rass [+]complex [m]andel [w]save [l]oad"
        safe_addstr(stdscr, max_y - 1, 1, help_text)

        stdscr.refresh()
        time.sleep(0.05)

    # Cleanup
    sim.save_weights()


if __name__ == '__main__':
    curses.wrapper(main)
