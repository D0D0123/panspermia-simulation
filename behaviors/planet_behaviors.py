"""
Planet-related behaviors for the Panspermia Simulation.
"""

import random
from .base import TickBehavior


class PlanetLifeBehavior(TickBehavior):
    """Handles life dynamics on planets (growth, decline, spontaneous generation)."""

    def __init__(self, config):
        super().__init__(config)
        self.stats = {
            'spontaneous_life_events': 0,
            'life_extinctions': 0,
        }

    def execute(self, grid, tick_number: int):
        """Update life on all planets."""
        for planet in grid.get_all_planets():
            # Only process planets whose parent star is alive
            if not planet.parent_star.is_alive:
                # Star is dead - life declines faster or dies immediately
                if planet.has_life:
                    planet.has_life = False
                    planet.life_level = 0.0
                    self.stats['life_extinctions'] += 1
                continue

            # Check for spontaneous life generation
            if not planet.has_life:
                self.check_spontaneous_life(planet)

            # Update existing life
            if planet.has_life:
                self.update_life_level(planet)

    def check_spontaneous_life(self, planet):
        """Check if life spontaneously appears on a planet."""
        # Higher habitability increases chance of spontaneous life
        adjusted_chance = self.config.SPONTANEOUS_LIFE_CHANCE * planet.habitability

        if random.random() < adjusted_chance:
            planet.has_life = True
            planet.life_level = random.uniform(0.1, 0.3)  # Start with low life level
            self.stats['spontaneous_life_events'] += 1

    def update_life_level(self, planet):
        """Update the life level on a planet (growth or decline)."""
        # Habitability affects growth and decline rates
        growth_chance = self.config.LIFE_GROWTH_CHANCE * planet.habitability
        decline_chance = self.config.LIFE_DECLINE_CHANCE * (
            2.0 - planet.habitability * self.config.HABITABILITY_SUSTAIN_MULTIPLIER
        )

        # Growth
        if random.random() < growth_chance:
            planet.life_level = min(1.0, planet.life_level + 0.1)

        # Decline
        if random.random() < decline_chance:
            planet.life_level = max(0.0, planet.life_level - 0.1)

            # Life goes extinct if level reaches 0
            if planet.life_level <= 0:
                planet.has_life = False
                self.stats['life_extinctions'] += 1
