"""
Defines the Boid class
"""
import numpy as np


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
        Decide must return an angle in radians indicating the direction taken.
        """
        # First, filter the information to keep only the 3 closest boids
        three_closest = np.argpartition(boids_distances, 2)
        other_locations = other_locations[three_closest[:3]]
        boids_distances = boids_distances[three_closest[:3]]
        other_directions = other_directions[three_closest[:3]]
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
#        weights = np.array([group_weight, avg_weight, opp_weight] + list(walls_weights))
#        angles = np.array([group_angle, avg_angle, opposite_angle] + list(walls_angles))
        weights = list(walls_weights)
        angles = list(walls_angles)

        # Compute the weighted angular average
        final_dir = np.arctan2(np.average(np.sin(angles), weights=weights), np.average(np.cos(angles), weights=weights))
        return final_dir

    def grouping_steer(self, other_locations):
        """
        Returns the angle needed to steer towards the mean location
        of the closest boids.
        :param boids_distances: Distances of the boids to take into account from self
        :param other_locations: Locations of those same boids
        :return: (t, w) where t is the angle in radians between the X-axis and the mean position of those boids.
                    w is the weight to attribute to this direction, which is always 1.
        """
        loc = np.mean(other_locations, axis=0)
        delta_x = loc[0] - self.location()[0]
        delta_y = self.location()[1] - loc[1]
        if abs(delta_x) <= 1 and abs(delta_y) <= 1:
            return 0, 0

        # DO NOT use the arithmetic mean ! Use the angular average
        return np.arctan2(delta_y, delta_x), 1

    def average_direction(self, other_directions):
        """
        Returns the average direction of the boids taken into account.
        :param other_directions: Directions of the boids to take into account, as a numpy array
        """
        avg = np.arctan2(np.mean(np.sin(other_directions)), np.mean(np.cos(other_directions)))
        return avg, 0.2

    def collision_avoiding_direction(self, closest_boid_location, closest_dist):
        """
        Returns the direction needed to avoid the closest boid
        """
        delta_x = closest_boid_location[0] - self.location()[0]
        delta_y = self.location()[1] - closest_boid_location[1]

        angle = np.arctan2(delta_y, delta_x)
        weight = np.exp((10 - closest_dist) / 100)
        if angle <= 0:
            return angle + np.pi, weight
        else:
            return angle - np.pi, weight

    def wall_directions(self, limits=800):
        """
        returns directions, weights where directions is an array of each direction perpendicular
        to the 4 walls, and weights are the weight to attribute to those directions.
        """
        self_loc = self._location
        distance_to_walls = np.array([
            abs(self_loc[0]),
            abs(self_loc[0] - limits),
            abs(self_loc[1]),
            abs(self_loc[1] - limits)
        ])
        directions = np.array([0, np.pi,  -np.pi / 2, np.pi / 2])
        weights = np.exp((limits / 25 - distance_to_walls) / 100)
        return directions, weights

    def update(self, boids_distances, other_boids, other_directions):
        """
        Updates the boid's location.
        """
        # The new direction is a weighted mean of the current dir and the ideal one
        directions = np.array([self.decide(boids_distances, other_boids, other_directions),  # Ideal direction
                               self._direction])
        directional_weights = np.array([0.2, 0.8])  # Weight for the new and ancient directions
        # Angular weighted average
        self._direction = np.arctan2(np.average(np.sin(directions), weights=directional_weights),
                                     np.average(np.cos(directions), weights=directional_weights))

        self._location[0] += np.cos(self._direction)
        self._location[1] -= np.sin(self._direction)
        self._location = np.minimum(self._location, np.array([800, 800]))
        self._location = np.maximum(self._location, np.array([0, 0]))

    def location(self):
        """
        :return: the boid's location
        """
        return self._location.copy()

    def direction(self):
        return self._direction
