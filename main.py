import pygame
import sys
from pygame import locals
from boid import Boid
import numpy as np
from drawer import Drawer
from parameters import limits, delay, number_of_boids, draw_trajectories


if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption("Smart boids")
    screen = pygame.display.set_mode((limits, limits))
    screen.fill((255, 255, 255))
    pygame.display.update()
    drawer = Drawer(screen)

    boids = [Boid(*(np.random.random(2) * limits)) for _ in range(number_of_boids)]

    while True:
        for event in pygame.event.get():
            if event.type == locals.QUIT:
                sys.exit(0)
            elif event.type == locals.KEYUP:
                if event.key == locals.K_ESCAPE:
                    sys.exit(0)

        # UPDATE
        # Creates an array containing the locations of the boids as lines
        locations = np.stack([b.location() for b in boids])
        directions = np.array([b.direction() for b in boids])
        for i, boid in enumerate(boids):
            # Furnishes the boid.update method with arrays containing the OTHER boids' locations
            # and directions
            other_locations = locations[[k != i for k in range(len(boids))]]
            other_directions = directions[[k != i for k in range(len(boids))]]
            distances = np.linalg.norm(other_locations - locations[i], axis=1)
            boid.update(distances, other_locations, other_directions)

        # DRAWING
        screen.fill((255, 255, 255))
        drawer.draw_boids(boids)

        pygame.display.update()
        pygame.time.delay(delay)
