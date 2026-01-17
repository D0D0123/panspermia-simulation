"""
Grid class for the Panspermia Simulation.
Manages the simulation space and entities.
"""

from typing import List, Tuple
from entities import Star, Planet, Asteroid


class Grid:
    """Represents the simulation grid containing stars and asteroids."""

    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.stars: List[Star] = []
        self.asteroids: List[Asteroid] = []

    def add_star(self, star: Star):
        """Add a star to the grid."""
        self.stars.append(star)

    def add_asteroid(self, asteroid: Asteroid):
        """Add an asteroid to the grid."""
        self.asteroids.append(asteroid)

    def remove_asteroid(self, asteroid: Asteroid):
        """Remove an asteroid from the grid."""
        if asteroid in self.asteroids:
            self.asteroids.remove(asteroid)

    def in_bounds(self, x: float, y: float) -> bool:
        """Check if a position is within grid bounds."""
        return 0 <= x < self.width and 0 <= y < self.height

    def get_all_planets(self) -> List[Planet]:
        """Get all planets from all star systems."""
        planets = []
        for star in self.stars:
            planets.extend(star.planets)
        return planets

    def get_living_planets(self) -> List[Planet]:
        """Get all planets that currently have life."""
        return [p for p in self.get_all_planets() if p.has_life]

    def get_asteroids_with_life(self) -> List[Asteroid]:
        """Get all asteroids that contain life."""
        return [a for a in self.asteroids if a.contains_life]

    def find_planet_at_position(self, position: Tuple[float, float], tolerance: float = 1.0) -> Planet:
        """Find a planet at or near a given position within tolerance distance."""
        for planet in self.get_all_planets():
            if planet.distance_to(position) <= tolerance:
                return planet
        return None

    def __repr__(self):
        return f"Grid({self.width}x{self.height}, stars={len(self.stars)}, asteroids={len(self.asteroids)})"
