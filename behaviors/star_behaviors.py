"""
Star-related behaviors for the Panspermia Simulation.
"""

from .base import TickBehavior


class StarAgingBehavior(TickBehavior):
    """Handles star aging and death."""

    def __init__(self, config):
        super().__init__(config)
        self.stats = {
            'stars_died': 0,
        }

    def execute(self, grid, tick_number: int):
        """Age all stars and handle death."""
        for star in grid.stars:
            if star.is_alive:
                star.age += 1

                # Check if star has exceeded its lifetime
                if star.age >= star.lifetime:
                    self.handle_star_death(star)
                    self.stats['stars_died'] += 1

    def handle_star_death(self, star):
        """
        Handle when a star dies.
        Currently just marks it as dead.
        Future: Could implement supernova effects, destroy planets, etc.
        """
        star.is_alive = False
        # Future enhancement: Add supernova effects
        # - Destroy nearby planets
        # - Create shockwave
        # - Spawn new asteroids
