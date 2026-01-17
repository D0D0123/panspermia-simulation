"""
Main simulation class for the Panspermia Simulation.
"""

import random
import math
from typing import List, Tuple
from config import SimulationConfig
from grid import Grid
from entities import Star, Planet
from behaviors import (
    StarAgingBehavior,
    PlanetLifeBehavior,
    AsteroidSpawnBehavior,
    AsteroidMovementBehavior,
)


class Simulation:
    """Main simulation class coordinating all behaviors and entities."""

    def __init__(self, config: SimulationConfig = None):
        """
        Initialize the simulation.

        Args:
            config: SimulationConfig instance. If None, uses default config.
        """
        if config is None:
            from config import DEFAULT_CONFIG
            config = DEFAULT_CONFIG

        self.config = config
        self.grid = Grid(config.GRID_SIZE[0], config.GRID_SIZE[1])
        self.tick_number = 0

        # Set random seed if specified
        if config.RANDOM_SEED is not None:
            random.seed(config.RANDOM_SEED)

        # Initialize behaviors in execution order
        self.behaviors = [
            (1, StarAgingBehavior(config)),          # Phase 1: Environmental changes
            (2, PlanetLifeBehavior(config)),         # Phase 2: Life processes
            (3, AsteroidSpawnBehavior(config)),      # Phase 3: Asteroid generation
            (4, AsteroidMovementBehavior(config)),   # Phase 4: Movement & collision
        ]

        # Initialize the world
        self._initialize_world()

    def _initialize_world(self):
        """Initialize the simulation world with stars and planets."""
        # Spawn stars at random positions
        for _ in range(self.config.NUM_STARS):
            # Find a position not too close to existing stars
            position = self._find_valid_star_position()

            # Random lifetime for this star
            lifetime = random.randint(
                self.config.STAR_MIN_LIFETIME,
                self.config.STAR_MAX_LIFETIME
            )

            star = Star(position=position, lifetime=lifetime)
            self.grid.add_star(star)

            # Spawn planets around this star
            self._spawn_planets_for_star(star)

        # Seed initial life on random planets
        self._seed_initial_life()

    def _find_valid_star_position(self) -> Tuple[int, int]:
        """Find a valid position for a star (not too close to others)."""
        min_distance = 10  # Minimum distance between stars

        for _ in range(100):  # Try up to 100 times
            x = random.randint(0, self.grid.width - 1)
            y = random.randint(0, self.grid.height - 1)

            # Check distance to other stars
            valid = True
            for star in self.grid.stars:
                dx = x - star.position[0]
                dy = y - star.position[1]
                distance = math.sqrt(dx * dx + dy * dy)
                if distance < min_distance:
                    valid = False
                    break

            if valid:
                return (x, y)

        # If we couldn't find a valid position, just return a random one
        return (
            random.randint(0, self.grid.width - 1),
            random.randint(0, self.grid.height - 1)
        )

    def _spawn_planets_for_star(self, star: Star):
        """Spawn planets orbiting a star."""
        # Determine number of planets
        num_planets = 0
        for _ in range(self.config.MAX_PLANETS_PER_STAR):
            if random.random() < self.config.PLANET_SPAWN_CHANCE:
                num_planets += 1

        # Create planets at random positions around the star
        for _ in range(num_planets):
            # Random angle and distance from star
            angle = random.uniform(0, 2 * math.pi)
            distance = random.uniform(1, self.config.PLANET_ORBIT_RADIUS)

            # Calculate position
            x = star.position[0] + int(math.cos(angle) * distance)
            y = star.position[1] + int(math.sin(angle) * distance)

            # Ensure position is within grid bounds
            x = max(0, min(self.grid.width - 1, x))
            y = max(0, min(self.grid.height - 1, y))

            # Random habitability
            habitability = random.uniform(
                self.config.PLANET_HABITABILITY_MIN,
                self.config.PLANET_HABITABILITY_MAX
            )

            planet = Planet(
                position=(x, y),
                parent_star=star,
                habitability=habitability
            )
            star.add_planet(planet)

    def _seed_initial_life(self):
        """Seed life on initial planets."""
        all_planets = self.grid.get_all_planets()
        if not all_planets:
            return

        # Randomly select planets to seed with life
        num_to_seed = min(self.config.INITIAL_LIFE_PLANETS, len(all_planets))
        seeded_planets = random.sample(all_planets, num_to_seed)

        for planet in seeded_planets:
            planet.has_life = True
            planet.life_level = random.uniform(0.3, 0.7)

    def tick(self):
        """Execute one tick of the simulation."""
        # Execute behaviors in priority order
        sorted_behaviors = sorted(self.behaviors, key=lambda x: x[0])
        for priority, behavior in sorted_behaviors:
            if behavior.enabled:
                behavior.execute(self.grid, self.tick_number)

        self.tick_number += 1

    def run(self, num_ticks: int = None, visualizer=None):
        """
        Run the simulation for a specified number of ticks.

        Args:
            num_ticks: Number of ticks to run. If None, uses config.MAX_TICKS
            visualizer: Optional visualizer instance for rendering
        """
        if num_ticks is None:
            num_ticks = self.config.MAX_TICKS

        for _ in range(num_ticks):
            self.tick()

            # Visualization
            if visualizer and self.config.DISPLAY_EVERY_N_TICKS > 0:
                if self.tick_number % self.config.DISPLAY_EVERY_N_TICKS == 0:
                    visualizer.render(self)

            # Show stats
            if self.config.SHOW_STATS and self.tick_number % 100 == 0:
                self.print_stats()

        # Final visualization
        if visualizer:
            print(f"\n=== Final State (Tick {self.tick_number}) ===")
            visualizer.render(self)

        # Final stats
        print(f"\n=== Final Statistics ===")
        self.print_stats()
        self.print_behavior_stats()

    def print_stats(self):
        """Print current simulation statistics."""
        living_planets = len(self.grid.get_living_planets())
        total_planets = len(self.grid.get_all_planets())
        asteroids_with_life = len(self.grid.get_asteroids_with_life())
        total_asteroids = len(self.grid.asteroids)
        alive_stars = sum(1 for s in self.grid.stars if s.is_alive)

        print(f"Tick {self.tick_number}: "
              f"Living Planets: {living_planets}/{total_planets}, "
              f"Asteroids: {total_asteroids} ({asteroids_with_life} with life), "
              f"Stars: {alive_stars}/{len(self.grid.stars)}")

    def print_behavior_stats(self):
        """Print statistics from all behaviors."""
        for priority, behavior in self.behaviors:
            stats = behavior.get_stats()
            if stats:
                print(f"\n{behavior.__class__.__name__}:")
                for key, value in stats.items():
                    print(f"  {key}: {value}")

    def get_stats(self) -> dict:
        """
        Get comprehensive statistics about the simulation.

        Returns:
            Dictionary containing various statistics
        """
        return {
            'tick': self.tick_number,
            'total_planets': len(self.grid.get_all_planets()),
            'living_planets': len(self.grid.get_living_planets()),
            'total_asteroids': len(self.grid.asteroids),
            'asteroids_with_life': len(self.grid.get_asteroids_with_life()),
            'alive_stars': sum(1 for s in self.grid.stars if s.is_alive),
            'total_stars': len(self.grid.stars),
        }
