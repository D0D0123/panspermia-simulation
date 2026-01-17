"""
Configuration parameters for the Panspermia Simulation.
All parameters can be adjusted to modify simulation behavior.
"""

from dataclasses import dataclass
from typing import Tuple


@dataclass
class SimulationConfig:
    """Configuration for the panspermia simulation."""

    # Grid Configuration
    GRID_SIZE: Tuple[int, int] = (100, 100)

    # Star/Planet Generation
    NUM_STARS: int = 10
    PLANET_SPAWN_CHANCE: float = 0.7  # per star
    MAX_PLANETS_PER_STAR: int = 5
    PLANET_ORBIT_RADIUS: int = 3  # max distance from star
    INITIAL_LIFE_PLANETS: int = 3  # number of planets that start with life

    # Star Lifecycle
    STAR_MIN_LIFETIME: int = 500  # minimum ticks before star can die
    STAR_MAX_LIFETIME: int = 2000  # maximum lifetime

    # Planet Properties
    PLANET_HABITABILITY_MIN: float = 0.2  # minimum habitability
    PLANET_HABITABILITY_MAX: float = 1.0  # maximum habitability

    # Asteroid Mechanics
    ASTEROID_SPAWN_CHANCE: float = 0.01  # per planet per tick
    ASTEROID_LIFE_BASE_CHANCE: float = 0.05  # base chance asteroid contains life
    ASTEROID_LEAVE_SYSTEM_CHANCE: float = 0.1  # per asteroid per tick
    ASTEROID_SPEED: float = 1.0  # units per tick
    ASTEROID_LIFE_DECAY_RATE: float = 0.001  # viability lost per tick
    ASTEROID_LIFE_INITIAL_VIABILITY: float = 1.0  # starting viability

    # Life Mechanics
    ASTEROID_SEED_BASE_SUCCESS: float = 0.3  # base chance when life-asteroid hits planet
    LIFE_GROWTH_CHANCE: float = 0.05  # per tick for living planets
    LIFE_DECLINE_CHANCE: float = 0.02  # per tick for living planets
    LIFE_LEVEL_ASTEROID_MULTIPLIER: float = 2.0  # how much life level increases asteroid spawn chance
    SPONTANEOUS_LIFE_CHANCE: float = 0.0001  # very low chance for life to spontaneously appear
    HABITABILITY_SEEDING_MULTIPLIER: float = 1.5  # how much habitability affects seeding success
    HABITABILITY_SUSTAIN_MULTIPLIER: float = 0.8  # how much habitability affects life decline

    # Simulation Control
    MAX_TICKS: int = 1000
    RANDOM_SEED: int = None  # Set to an integer for reproducible simulations

    # Visualization
    DISPLAY_EVERY_N_TICKS: int = 10  # How often to show visualization (0 = only final state)
    SHOW_STATS: bool = True  # Show statistics during simulation


# Default configuration instance
DEFAULT_CONFIG = SimulationConfig()
