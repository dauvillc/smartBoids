import pygame
import sys
from pygame import locals
from boid import Boid
import numpy as np
from drawer import Drawer


if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption("Smart boids")
    screen = pygame.display.set_mode((800, 800))
    screen.fill((255, 255, 255))
    pygame.display.update()
    drawer = Drawer(screen)

    boids = [Boid(*(np.random.random(2) * 800)) for _ in range(30)]

    while True:
        for event in pygame.event.get():
            if event.type == locals.QUIT:
                sys.exit(0)
            elif event.type == locals.KEYUP:
                if event.key == locals.K_ESCAPE:
                    sys.exit(0)

        # UPDATE
        locations = np.stack([b.location() for b in boids])
        directions = np.array([b.direction() for b in boids])
        for i, boid in enumerate(boids):
            other_locations = locations[[k != i for k in range(len(boids))]]
            other_directions = directions[[k != i for k in range(len(boids))]]
            distances = np.linalg.norm(other_locations - locations[i], axis=1)
            boid.update(distances, other_locations, other_directions)

        # DRAWING
        screen.fill((255, 255, 255))
        drawer.draw_boids(boids)

        pygame.display.update()
        pygame.time.delay(20)
