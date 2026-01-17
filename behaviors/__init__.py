"""
Behavior module for the Panspermia Simulation.
Contains modular tick behaviors for different aspects of the simulation.
"""

from .base import TickBehavior
from .star_behaviors import StarAgingBehavior
from .planet_behaviors import PlanetLifeBehavior
from .asteroid_behaviors import AsteroidSpawnBehavior, AsteroidMovementBehavior

__all__ = [
    'TickBehavior',
    'StarAgingBehavior',
    'PlanetLifeBehavior',
    'AsteroidSpawnBehavior',
    'AsteroidMovementBehavior',
]
