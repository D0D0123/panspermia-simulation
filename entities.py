"""
Entity classes for the Panspermia Simulation.
Includes Star, Planet, and Asteroid classes.
"""

from typing import Tuple, List, Optional
import math


class Star:
    """Represents a star in the simulation."""

    def __init__(
        self,
        position: Tuple[int, int],
        lifetime: int,
    ):
        self.position = position
        self.lifetime = lifetime
        self.age = 0
        self.is_alive = True
        self.planets: List['Planet'] = []

    def add_planet(self, planet: 'Planet'):
        """Add a planet to this star system."""
        self.planets.append(planet)

    def __repr__(self):
        return f"Star(pos={self.position}, age={self.age}/{self.lifetime}, planets={len(self.planets)})"


class Planet:
    """Represents a planet orbiting a star."""

    def __init__(
        self,
        position: Tuple[int, int],
        parent_star: Star,
        habitability: float,
    ):
        self.position = position
        self.parent_star = parent_star
        self.habitability = habitability
        self.has_life = False
        self.life_level = 0.0  # 0.0 to 1.0

    def distance_to(self, other_position: Tuple[float, float]) -> float:
        """Calculate Euclidean distance to another position."""
        dx = self.position[0] - other_position[0]
        dy = self.position[1] - other_position[1]
        return math.sqrt(dx * dx + dy * dy)

    def __repr__(self):
        life_str = f"life={self.life_level:.2f}" if self.has_life else "no life"
        return f"Planet(pos={self.position}, hab={self.habitability:.2f}, {life_str})"


class Asteroid:
    """Represents an asteroid traveling through space."""

    def __init__(
        self,
        position: Tuple[float, float],
        velocity: Tuple[float, float],
        contains_life: bool = False,
        life_viability: float = 1.0,
    ):
        self.position = position
        self.velocity = velocity
        self.contains_life = contains_life
        self.life_viability = life_viability
        self.in_transit = False  # Whether it has left its star system

    def move(self):
        """Move the asteroid according to its velocity."""
        self.position = (
            self.position[0] + self.velocity[0],
            self.position[1] + self.velocity[1]
        )

    def distance_to(self, other_position: Tuple[float, float]) -> float:
        """Calculate Euclidean distance to another position."""
        dx = self.position[0] - other_position[0]
        dy = self.position[1] - other_position[1]
        return math.sqrt(dx * dx + dy * dy)

    def __repr__(self):
        life_str = f"life={self.life_viability:.2f}" if self.contains_life else "no life"
        return f"Asteroid(pos=({self.position[0]:.1f},{self.position[1]:.1f}), vel={self.velocity}, {life_str})"
