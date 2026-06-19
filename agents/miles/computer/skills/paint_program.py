import matplotlib.pyplot as plt
import numpy as np

def draw_solar_system():
    fig, ax = plt.subplots(figsize=(10, 10))
    ax.set_facecolor('black')

    # Define planets and moons
    celestial_bodies = [
        {"name": "Sun", "color": "yellow", "size": 3, "distance": 0},
        {"name": "Mercury", "color": "gray", "size": 0.5, "distance": 4},
        {"name": "Venus", "color": "gold", "size": 0.9, "distance": 6},
        {"name": "Earth", "color": "blue", "size": 1, "distance": 8},
        {"name": "Mars", "color": "red", "size": 0.7, "distance": 12},
        {"name": "Jupiter", "color": "orange", "size": 2.5, "distance": 16},
        {"name": "Saturn", "color": "goldenrod", "size": 2, "distance": 20},
        {"name": "Uranus", "color": "lightblue", "size": 1.5, "distance": 24},
        {"name": "Neptune", "color": "royalblue", "size": 1.4, "distance": 28},
        {"name": "Pluto", "color": "darkgray", "size": 0.4, "distance": 32}
    ]

    # Draw planets
    for body in celestial_bodies:
        ax.plot(body["distance"], 0, 'o', color=body["color"], markersize=body["size"]*10)
        ax.text(body["distance"], 0.5, body["name"], color=body["color"], ha='center')

    # Draw Callisto around Jupiter
    callisto_distance = 17.5
    ax.plot(callisto_distance, 0, 'o', color='lightgray', markersize=7)
    ax.text(callisto_distance, 0.5, 'Callisto', color='lightgray', ha='center')

    # Add signature
    ax.text(0.95, 0.05, "BR-01", fontsize=12, color='white', ha='right', transform=ax.transAxes)

    # Set limits and remove axis
    ax.set_xlim(0, 35)
    ax.set_ylim(-5, 5)
    ax.axis('off')
    
    ax.set_title("Solar System by BR-01", fontsize=16, color='white')
    plt.show()

draw_solar_system()
