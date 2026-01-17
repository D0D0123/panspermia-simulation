"""
Asteroid-related behaviors for the Panspermia Simulation.
"""

import random
import math
from entities import Asteroid
from .base import TickBehavior


class AsteroidSpawnBehavior(TickBehavior):
    """Handles spawning of asteroids from planets."""

    def __init__(self, config):
        super().__init__(config)
        self.stats = {
            'asteroids_spawned': 0,
            'asteroids_with_life_spawned': 0,
        }

    def execute(self, grid, tick_number: int):
        """Attempt to spawn asteroids from planets with life."""
        for planet in grid.get_all_planets():
            # Only planets with life from alive stars can spawn asteroids
            if planet.has_life and planet.parent_star.is_alive:
                self.attempt_spawn_asteroid(planet, grid)

    def attempt_spawn_asteroid(self, planet, grid):
        """Attempt to spawn an asteroid from a planet."""
        # Life level increases spawn chance
        spawn_chance = (
            self.config.ASTEROID_SPAWN_CHANCE *
            (1 + planet.life_level * self.config.LIFE_LEVEL_ASTEROID_MULTIPLIER)
        )

        if random.random() < spawn_chance:
            # Generate random direction (8 directions: cardinal + diagonal)
            angle = random.uniform(0, 2 * math.pi)
            velocity = (
                math.cos(angle) * self.config.ASTEROID_SPEED,
                math.sin(angle) * self.config.ASTEROID_SPEED
            )

            # Start asteroid slightly offset from planet to avoid immediate collision
            offset_x = math.cos(angle) * 1.5
            offset_y = math.sin(angle) * 1.5
            position = (
                planet.position[0] + offset_x,
                planet.position[1] + offset_y
            )

            # Determine if asteroid contains life
            contains_life = random.random() < self.config.ASTEROID_LIFE_BASE_CHANCE

            asteroid = Asteroid(
                position=position,
                velocity=velocity,
                contains_life=contains_life,
                life_viability=self.config.ASTEROID_LIFE_INITIAL_VIABILITY if contains_life else 0.0
            )

            grid.add_asteroid(asteroid)
            self.stats['asteroids_spawned'] += 1
            if contains_life:
                self.stats['asteroids_with_life_spawned'] += 1


class AsteroidMovementBehavior(TickBehavior):
    """Handles asteroid movement, collisions, and life viability decay."""

    def __init__(self, config):
        super().__init__(config)
        self.stats = {
            'asteroids_exited_grid': 0,
            'asteroid_life_died': 0,
            'collisions': 0,
            'successful_seedings': 0,
        }

    def execute(self, grid, tick_number: int):
        """Update all asteroids: decay life, move, check collisions."""
        asteroids_to_remove = []

        for asteroid in grid.asteroids:
            # Decay life viability
            if asteroid.contains_life:
                asteroid.life_viability -= self.config.ASTEROID_LIFE_DECAY_RATE
                if asteroid.life_viability <= 0:
                    asteroid.contains_life = False
                    asteroid.life_viability = 0.0
                    self.stats['asteroid_life_died'] += 1

            # Check if asteroid should leave its star system (become in_transit)
            if not asteroid.in_transit:
                if random.random() < self.config.ASTEROID_LEAVE_SYSTEM_CHANCE:
                    asteroid.in_transit = True

            # Move asteroid
            asteroid.move()

            # Check if out of bounds
            if not grid.in_bounds(asteroid.position[0], asteroid.position[1]):
                asteroids_to_remove.append(asteroid)
                self.stats['asteroids_exited_grid'] += 1
                continue

            # Check for collision with planet
            collided_planet = grid.find_planet_at_position(asteroid.position, tolerance=1.0)
            if collided_planet:
                self.handle_collision(asteroid, collided_planet)
                asteroids_to_remove.append(asteroid)
                self.stats['collisions'] += 1

        # Remove asteroids that exited or collided
        for asteroid in asteroids_to_remove:
            grid.remove_asteroid(asteroid)

    def handle_collision(self, asteroid, planet):
        """Handle collision between an asteroid and a planet."""
        # Only attempt seeding if asteroid has life and planet doesn't
        if asteroid.contains_life and not planet.has_life:
            # Calculate seeding success based on habitability and life viability
            success_chance = (
                self.config.ASTEROID_SEED_BASE_SUCCESS *
                planet.habitability *
                self.config.HABITABILITY_SEEDING_MULTIPLIER *
                asteroid.life_viability  # Viability affects success
            )

            if random.random() < success_chance:
                # Successfully seed life on the planet
                planet.has_life = True
                planet.life_level = random.uniform(0.2, 0.5)  # Start with moderate life
                self.stats['successful_seedings'] += 1
