"""
Defines values for the simulation parameters
"""

limits = 600  # Size of the window. Default: 800
delay = 15  # Delay between each frame in ms. Default: 20
number_of_boids = 30  # I think the name is quite clear. Default: 30

drawing_size = 5  # Size of the boids as drawed on screen. Default: 5

turns_smoothness = 0.8  # Smoothness of the changes of direction, within [0, 1[. Defaults to 0.8.
# (At 1, boids cannot turn; at 0 they turn instantly).

# Boids behavior
neighbours_considered = 3  # Neighbours to take into account for the direction. Default: 3
collision_param = 0.2  # Importance of avoiding collision. The higher, the more distant the boids will be. Default: 0.2
walls_param = 0.1  # Importance of avoiding walls. The higher, the more distant from the walls. Default: 0.1
average_direction_param = 0.2  # Importance of aligning direction with the neighbour boids. Default: 0.2
grouping_param = 1  # Importance of grouping the neighbour boids. Default: 1
