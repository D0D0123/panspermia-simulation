#!/usr/bin/env python3
"""
Main entry point for the Panspermia Simulation.

This simulation models the spread of life through space via panspermia,
where asteroids carrying microbial life can seed other planets.
"""

import argparse
from config import SimulationConfig
from simulation import Simulation
from visualizer import ASCIIVisualizer, CompactVisualizer, DetailedVisualizer


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Panspermia Simulation - Model the spread of life through space'
    )

    # Simulation parameters
    parser.add_argument(
        '--ticks',
        type=int,
        default=None,
        help='Number of ticks to run (default: from config)'
    )
    parser.add_argument(
        '--seed',
        type=int,
        default=None,
        help='Random seed for reproducible simulations'
    )
    parser.add_argument(
        '--stars',
        type=int,
        default=10,
        help='Number of stars to spawn (default: 10)'
    )
    parser.add_argument(
        '--grid-size',
        type=int,
        nargs=2,
        default=[100, 100],
        metavar=('WIDTH', 'HEIGHT'),
        help='Grid size (default: 100 100)'
    )
    parser.add_argument(
        '--initial-life',
        type=int,
        default=3,
        help='Number of planets starting with life (default: 3)'
    )

    # Visualization options
    parser.add_argument(
        '--visualizer',
        choices=['ascii', 'compact', 'detailed', 'none'],
        default='compact',
        help='Visualization style (default: compact)'
    )
    parser.add_argument(
        '--display-interval',
        type=int,
        default=100,
        help='Display every N ticks (0 = only final state, default: 100)'
    )
    parser.add_argument(
        '--scale',
        type=int,
        default=1,
        help='ASCII visualizer scale factor (default: 1)'
    )
    parser.add_argument(
        '--no-stats',
        action='store_true',
        help='Disable statistics output'
    )

    args = parser.parse_args()

    # Create configuration
    config = SimulationConfig(
        GRID_SIZE=(args.grid_size[0], args.grid_size[1]),
        NUM_STARS=args.stars,
        INITIAL_LIFE_PLANETS=args.initial_life,
        RANDOM_SEED=args.seed,
        DISPLAY_EVERY_N_TICKS=args.display_interval,
        SHOW_STATS=not args.no_stats,
    )

    # Create visualizer
    if args.visualizer == 'ascii':
        visualizer = ASCIIVisualizer(scale=args.scale)
    elif args.visualizer == 'compact':
        visualizer = CompactVisualizer()
    elif args.visualizer == 'detailed':
        visualizer = DetailedVisualizer()
    else:
        visualizer = None

    # Print configuration
    print("=" * 60)
    print("PANSPERMIA SIMULATION")
    print("=" * 60)
    print(f"Grid Size: {config.GRID_SIZE[0]}x{config.GRID_SIZE[1]}")
    print(f"Stars: {config.NUM_STARS}")
    print(f"Initial Life Planets: {config.INITIAL_LIFE_PLANETS}")
    print(f"Max Ticks: {args.ticks if args.ticks else config.MAX_TICKS}")
    if config.RANDOM_SEED is not None:
        print(f"Random Seed: {config.RANDOM_SEED}")
    print("=" * 60)

    # Create and run simulation
    sim = Simulation(config)

    print(f"\nInitialized with {len(sim.grid.stars)} stars and "
          f"{len(sim.grid.get_all_planets())} planets")
    print(f"Starting life planets: {len(sim.grid.get_living_planets())}\n")

    # Run simulation
    try:
        sim.run(num_ticks=args.ticks, visualizer=visualizer)
    except KeyboardInterrupt:
        print("\n\nSimulation interrupted by user.")
        print(f"\n=== State at Tick {sim.tick_number} ===")
        if visualizer:
            visualizer.render(sim)
        sim.print_stats()
        sim.print_behavior_stats()

    print("\n" + "=" * 60)
    print("SIMULATION COMPLETE")
    print("=" * 60)


if __name__ == '__main__':
    main()
