"""
Defines the drawer class.
"""
import pygame
import numpy as np
from parameters import drawing_size


class Drawer:
    """
    The Drawer is the tool used to draw the boids and every other features
    on screen.
    """
    def __init__(self, screen):
        """
        -- screen: Screen surface used by pygame
        """
        self._screen = screen

    def draw_boids(self, boids):
        """
        Draws the boids.
        -- boids: list of boids to draw
        """
        for boid in boids:
            center = boid.location()

            # Compute the summits of the triangle
            # The triangle is isocele with angles (40, 70, 70)
            summits = np.array([
                [2.2506, 0],  # sin(55°) / tan(20°)
                [np.cos(2.18166), np.sin(2.18166)],  # 125 degrees in rads
                [np.cos(-2.18166), np.sin(-2.18166)]
            ])

            # Rotate the triangle according to the direction of the boid
            dir = -boid.direction()
            rot_matrix = np.array([[np.cos(dir), -np.sin(dir)],
                                   [np.sin(dir), np.cos(dir)]])
            summits = np.dot(rot_matrix, summits.transpose()).transpose()

            # Give its size and translate it to the boid's location
            summits *= drawing_size
            summits += center
            pygame.draw.polygon(self._screen, (0, 0, 0), summits)
