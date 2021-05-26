"""
Defines the Boid class
"""
import numpy as np
from parameters import neighbours_considered, limits, walls_param, collision_param


class Boid:
    """
    A Boid is an object defined by a spatial location, and which decides of a direction
    according to the information it perceives.
    """
    def __init__(self, x, y):
        self._location = np.array([x, y])
        self._direction = np.random.random() * 2 * np.pi - np.pi

    def decide(self, boids_distances, other_locations, other_directions):
        """
        Returns the direction (angle from the X-axis) that self should take according to
        the behavior rules.
        -- boids_distances: np array containing the distance with the OTHER boids;
        -- other_locations: 2D np array whose lines are the other boids' locations;
        -- other_directions: np array containing the directions of the other boids.
        """
        # First, filt1er the information to keep only the closest boids
        closest_boids = np.argpartition(boids_distances, 2)
        other_locations = other_locations[closest_boids[:neighbours_considered]]
        boids_distances = boids_distances[closest_boids[:neighbours_considered]]
        other_directions = other_directions[closest_boids[:neighbours_considered]]

        # Compute the closest boid itself
        closest = np.argmin(boids_distances)
        closest_distance = boids_distances[closest]

        group_angle, group_weight = self.grouping_steer(other_locations)
        avg_angle, avg_weight = self.average_direction(other_directions)
        opposite_angle, opp_weight = self.collision_avoiding_direction(other_locations[closest], closest_distance)
        walls_angles, walls_weights = self.wall_directions()

        # Normalize the weights so that their sum is 1
        total_weight = max(group_weight + avg_weight + opp_weight + np.sum(walls_weights), 1)
        group_weight /= total_weight
        avg_weight /= total_weight
        opp_weight /= total_weight
        walls_weights /= total_weight

        # Group the weights and angles together into an array to perform the weighted mean computation
        weights = np.array([group_weight, avg_weight, opp_weight] + list(walls_weights))
        angles = np.array([group_angle, avg_angle, opposite_angle] + list(walls_angles))

        # Compute the weighted angular average
        final_dir = np.arctan2(np.average(np.sin(angles), weights=weights), np.average(np.cos(angles), weights=weights))
        return final_dir

    # RUUUUUUULES ------------------------------------------------------------------------------------------------------
    def grouping_steer(self, other_locations):
        """
        -- boids_distances: Distances of the boids to take into account as a np array
        -- other_locations: 2D np array where the lines are the other boid's locations
        Returns (t, w) where t is the angle in radians between the X-axis and the mean position of those boids.
                    w is the weight to attribute to this direction (see parameters.py).
        """
        loc = np.mean(other_locations, axis=0)
        delta_x = loc[0] - self.location()[0]
        delta_y = self.location()[1] - loc[1]

        # Watchout for the computation float error
        if abs(delta_x) <= 1 and abs(delta_y) <= 1:
            return 0, 0

        # DO NOT use the arithmetic mean ! Use the angular average
        return np.arctan2(delta_y, delta_x), 1

    def average_direction(self, other_directions):
        """
        -- other_directions: numpy array containing the directions of the boids to take into account.
        returns a, w where:
        -- a is the average direction of the boids given;
        -- w is the weight to attribute to that direction (see parameters.py).
        """
        avg = np.arctan2(np.mean(np.sin(other_directions)), np.mean(np.cos(other_directions)))
        return avg, 0.2

    def collision_avoiding_direction(self, closest_boid_location, closest_dist):
        """
        -- closest_boid_location: Location of the closest boid (numpy array of 2 values)
        -- closest_dist: Distance to that boid
        Returns a, w where
        -- a is the direction to take in order to get away from the closest neighbour
        -- w is the importance of taking this direction, which increases as the neighbour gets closer
        """
        # Computes the opposite of the angle between self and the neighbour
        delta_x = closest_boid_location[0] - self.location()[0]
        delta_y = self.location()[1] - closest_boid_location[1]
        angle = np.arctan2(delta_y, delta_x)

        # The weight to attribute to this direction increases exponentially as the neighbour gets closer.
        weight = np.exp((10 - closest_dist) * collision_param)
        if angle <= 0:
            return angle + np.pi, weight
        else:
            return angle - np.pi, weight

    def wall_directions(self, limits=limits):
        """
        Returns (A, W) where:
        -- A is an array of 4 elements where each element is the direction perpendicular to one of the 4 walls
        -- Each w in W is the weight to attribute to this angle, which increases as the wall gets closer
        """
        self_loc = self._location
        distance_to_walls = np.array([
            abs(self_loc[0]),
            abs(self_loc[0] - limits),
            abs(self_loc[1]),
            abs(self_loc[1] - limits)
        ])
        directions = np.array([0, np.pi,  -np.pi / 2, np.pi / 2])

        # The importance of avoiding each wall increases exponentially as the boid gets closer to it
        weights = np.exp((limits / 25 - distance_to_walls) * walls_param)
        return directions, weights
    # END OF RUULES ----------------------------------------------------------------------------------------------------

    def update(self, boids_distances, other_boids, other_directions):
        """
        Updates the boid's location.
        """
        # The new direction is a weighted mean of the current dir and the ideal one
        # so that the boid's change of directions are smooth
        directions = np.array([self.decide(boids_distances, other_boids, other_directions),  # Ideal direction
                               self._direction])
        directional_weights = np.array([0.2, 0.8])  # Weight for the new and ancient directions

        # Angular weighted average between the ancient and current directions
        self._direction = np.arctan2(np.average(np.sin(directions), weights=directional_weights),
                                     np.average(np.cos(directions), weights=directional_weights))

        # Move slightly in the boid's new direction
        self._location[0] += np.cos(self._direction)
        self._location[1] -= np.sin(self._direction)

        # Make sure the boid does not get out of the window
        self._location = np.minimum(self._location, np.array([limits, limits]))
        self._location = np.maximum(self._location, np.array([0, 0]))

    def location(self):
        """
        :return: the boid's location
        """
        return self._location.copy()

    def direction(self):
        return self._direction
