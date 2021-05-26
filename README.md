# Boids simulation
Boids where introduced by Craig Reynolds in 1986 (https://en.wikipedia.org/wiki/Boids) and aim to simulate the auto-organization of groups of birds or fish.
The boids move around in a plane. Each of them follows 3 rules:
- A boid heads towards the center of mass of his neighbours;
- A boid must remain separated with another one;
- A boid tries to align its direction with it's neighbours'.

Finally, one last rule is applied for the sake of the simulation:
- A boid heading for the wall (space limit of the simulation) must turn to avoid it.

The well-known results of those simple rules are intriguing: while the original system seems chaotic, the boids progressively
organize themselves in groups in the way similar to a school of fish. The number of groups formed, the distance between the boids
or their direction depends on several parameters which define the rules more precisely (see parameters.py).

## Requirements
Python - Numpy; Pygame;
From a certain number of boids on, the application will start to slow down and may need too many ressources. The program is coded in Python and especially pygame
which makes it inevitably slow compared to C with the native SDL2 library.
