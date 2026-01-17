"""
Visualization for the Panspermia Simulation.
Provides ASCII-based rendering of the simulation state.
"""


class ASCIIVisualizer:
    """ASCII-based visualizer for the simulation."""

    def __init__(self, scale: int = 1):
        """
        Initialize the visualizer.

        Args:
            scale: Scaling factor for the visualization (1 = full grid, 2 = half size, etc.)
        """
        self.scale = scale

    def render(self, simulation):
        """
        Render the current state of the simulation.

        Args:
            simulation: Simulation instance to render
        """
        grid = simulation.grid
        width = grid.width // self.scale
        height = grid.height // self.scale

        # Create empty grid
        display = [['.' for _ in range(width)] for _ in range(height)]

        # Place stars and planets
        for star in grid.stars:
            sx, sy = self._scale_position(star.position)
            if 0 <= sx < width and 0 <= sy < height:
                if star.is_alive:
                    display[sy][sx] = '*'
                else:
                    display[sy][sx] = 'x'  # Dead star

            # Place planets
            for planet in star.planets:
                px, py = self._scale_position(planet.position)
                if 0 <= px < width and 0 <= py < height:
                    if planet.has_life:
                        # Use different symbols based on life level
                        if planet.life_level > 0.7:
                            display[py][px] = 'O'  # High life
                        elif planet.life_level > 0.3:
                            display[py][px] = 'o'  # Medium life
                        else:
                            display[py][px] = '°'  # Low life
                    else:
                        display[py][px] = '·'  # No life

        # Place asteroids (they render on top)
        for asteroid in grid.asteroids:
            ax, ay = self._scale_position(asteroid.position)
            if 0 <= ax < width and 0 <= ay < height:
                if asteroid.contains_life:
                    display[ay][ax] = '#'  # Asteroid with life
                else:
                    display[ay][ax] = '+'  # Asteroid without life

        # Print the grid
        print("+" + "-" * width + "+")
        for row in display:
            print("|" + "".join(row) + "|")
        print("+" + "-" * width + "+")

        # Print legend
        self._print_legend()

    def _scale_position(self, position):
        """Scale a position according to the scale factor."""
        return (int(position[0]) // self.scale, int(position[1]) // self.scale)

    def _print_legend(self):
        """Print the legend for the visualization."""
        print("\nLegend:")
        print("  * = Living star     x = Dead star")
        print("  O = High life       o = Medium life    ° = Low life    · = No life (planet)")
        print("  # = Asteroid (life) + = Asteroid (no life)")
        print("  . = Empty space")


class CompactVisualizer:
    """Compact visualizer showing only key statistics."""

    def render(self, simulation):
        """Render compact statistics."""
        stats = simulation.get_stats()

        print(f"\n--- Tick {stats['tick']} ---")
        print(f"Living Planets: {stats['living_planets']}/{stats['total_planets']}")
        print(f"Stars Alive: {stats['alive_stars']}/{stats['total_stars']}")
        print(f"Asteroids: {stats['total_asteroids']} ({stats['asteroids_with_life']} with life)")


class DetailedVisualizer:
    """Detailed visualizer showing individual entity information."""

    def render(self, simulation):
        """Render detailed entity information."""
        grid = simulation.grid

        print(f"\n=== Tick {simulation.tick_number} ===")

        # Stars
        print(f"\nStars ({len(grid.stars)}):")
        for i, star in enumerate(grid.stars[:5]):  # Show first 5
            status = "alive" if star.is_alive else "DEAD"
            print(f"  {i+1}. {star.position} - {status}, age {star.age}/{star.lifetime}, {len(star.planets)} planets")
        if len(grid.stars) > 5:
            print(f"  ... and {len(grid.stars) - 5} more")

        # Planets with life
        living_planets = grid.get_living_planets()
        print(f"\nLiving Planets ({len(living_planets)}):")
        for i, planet in enumerate(living_planets[:10]):  # Show first 10
            print(f"  {i+1}. {planet.position} - life={planet.life_level:.2f}, hab={planet.habitability:.2f}")
        if len(living_planets) > 10:
            print(f"  ... and {len(living_planets) - 10} more")

        # Asteroids
        asteroids_with_life = grid.get_asteroids_with_life()
        print(f"\nAsteroids with Life ({len(asteroids_with_life)}):")
        for i, asteroid in enumerate(asteroids_with_life[:10]):  # Show first 10
            print(f"  {i+1}. pos=({asteroid.position[0]:.1f},{asteroid.position[1]:.1f}), "
                  f"viability={asteroid.life_viability:.2f}")
        if len(asteroids_with_life) > 10:
            print(f"  ... and {len(asteroids_with_life) - 10} more")
