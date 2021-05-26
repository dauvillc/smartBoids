"""
Defines the drawer class.
"""
import pygame
from pygame import draw
import numpy as np


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

            # Translate the direction between 0 and 2pi
            dir = -boid.direction()
            rot_matrix = np.array([[np.cos(dir), -np.sin(dir)],
                                   [np.sin(dir), np.cos(dir)]])

            # Compute the summits of the triangle
            # The triangle is isocele with angles (40, 70, 70)
            summits = np.array([
                [2.2506, 0],  # sin(55°) / tan(20°)
                [np.cos(2.18166), np.sin(2.18166)],  # 125 degrees in rads
                [np.cos(-2.18166), np.sin(-2.18166)]
            ])
            summits = np.dot(rot_matrix, summits.transpose()).transpose()
            summits *= 5
            summits += center
            pygame.draw.polygon(self._screen, (0, 0, 0), summits)
