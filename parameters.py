"""
Defines values for the simulation parameters
"""

limits = 800  # Size of the window
delay = 20  # Delay between each frame in ms

drawing_size = 5  # Size of the boids as drawed on screen. Default: 5

# Boids behavior
neighbours_considered = 3  # Neighbours to take into account for the direction
collision_param = 0.2  # Importance of avoiding collision. The higher, the more distant the boids will be. Default: 0.2
walls_param = 0.01  # Importance of avoiding walls. The higher, the more distant from the walls. Default: 0.01
