# Panspermia Simulation

A Python simulation modeling the spread of life through space via panspermia - the hypothesis that life can be distributed throughout the universe by asteroids and meteorites.

## Overview

This simulation features:
- **Stars** that age and eventually die
- **Planets** orbiting stars with varying habitability
- **Asteroids** that spawn from living planets and travel through space
- **Life** that can spread between planets via asteroids
- **Modular behavior system** for easy extension

## Features

### Core Mechanics
- Life can start spontaneously on planets (very low probability)
- Planets with life spawn asteroids that may contain life
- Asteroids travel in straight lines across the grid
- Life in asteroids decays over time
- When asteroids collide with planets, they may seed life
- Planet habitability affects both seeding success and life sustainability
- Stars have finite lifetimes and eventually die

### Configurable Parameters
All simulation parameters are configurable in `config.py`:
- Grid size
- Number of stars
- Planet spawn rates and habitability ranges
- Asteroid spawn rates and life decay
- Life growth/decline rates
- Star lifetimes
- And more...

## Installation

### Prerequisites
- Python 3.7 or higher
- Git

### Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd panspermia-simulation
```

2. Create and activate a virtual environment (recommended):
```bash
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. No external dependencies required! The simulation uses only Python standard library.

4. Run the simulation:
```bash
python main.py
```

## Usage

### Basic Usage

Run with default settings:
```bash
python main.py
```

### Command Line Options

```bash
# Run for 500 ticks
python main.py --ticks 500

# Use a specific random seed for reproducibility
python main.py --seed 42

# Larger grid with more stars
python main.py --grid-size 200 200 --stars 20

# Start with more initial life
python main.py --initial-life 5

# ASCII visualization (shows the grid)
python main.py --visualizer ascii

# Detailed output showing entity information
python main.py --visualizer detailed

# Display every 50 ticks instead of 100
python main.py --display-interval 50

# No visualization (faster)
python main.py --visualizer none --no-stats
```

### Visualization Options

- **`compact`** (default): Shows summary statistics
- **`ascii`**: Shows grid with symbols representing entities
- **`detailed`**: Shows detailed information about entities
- **`none`**: No visualization (faster for large simulations)

### ASCII Visualization Legend

```
* = Living star     x = Dead star
O = High life       o = Medium life    ° = Low life    · = No life (planet)
# = Asteroid (life) + = Asteroid (no life)
. = Empty space
```

## Project Structure

```
panspermia-simulation/
├── main.py              # Entry point
├── config.py            # Configuration parameters
├── simulation.py        # Main simulation class
├── grid.py              # Grid and spatial management
├── entities.py          # Star, Planet, Asteroid classes
├── visualizer.py        # Visualization classes
├── behaviors/           # Modular tick behaviors
│   ├── __init__.py
│   ├── base.py          # Base behavior class
│   ├── star_behaviors.py
│   ├── planet_behaviors.py
│   └── asteroid_behaviors.py
├── PLANNING.md          # Detailed planning document
└── README.md            # This file
```

## Architecture

### Modular Behavior System

The simulation uses a plugin-based behavior system that makes it easy to add new mechanics:

1. **TickBehavior** - Base class for all behaviors
2. **StarAgingBehavior** - Handles star aging and death
3. **PlanetLifeBehavior** - Handles life growth/decline and spontaneous generation
4. **AsteroidSpawnBehavior** - Handles asteroid spawning from planets
5. **AsteroidMovementBehavior** - Handles asteroid movement and collisions

### Adding New Behaviors

To add a new behavior (e.g., cosmic radiation):

1. Create a new class inheriting from `TickBehavior`
2. Implement the `execute(grid, tick_number)` method
3. Add configuration parameters to `config.py`
4. Register the behavior in `simulation.py`

Example:
```python
class CosmicRadiationBehavior(TickBehavior):
    def execute(self, grid, tick_number):
        if tick_number % 100 == 0:  # Every 100 ticks
            # Damage random planets
            for planet in random.sample(grid.get_living_planets(), k=2):
                planet.life_level *= 0.8
```

## Example Output

```
============================================================
PANSPERMIA SIMULATION
============================================================
Grid Size: 100x100
Stars: 10
Initial Life Planets: 3
Max Ticks: 1000
============================================================

Initialized with 10 stars and 32 planets
Starting life planets: 3

Tick 100: Living Planets: 5/32, Asteroids: 12 (3 with life), Stars: 10/10
Tick 200: Living Planets: 8/32, Asteroids: 24 (7 with life), Stars: 10/10
Tick 300: Living Planets: 12/32, Asteroids: 31 (9 with life), Stars: 10/10
...
```

## Configuration Examples

### Fast Spread Scenario
Life spreads quickly across the galaxy:
```python
config = SimulationConfig(
    ASTEROID_SPAWN_CHANCE=0.05,  # More asteroids
    ASTEROID_LIFE_BASE_CHANCE=0.2,  # More likely to contain life
    ASTEROID_SEED_BASE_SUCCESS=0.6,  # Higher seeding success
    LIFE_GROWTH_CHANCE=0.1,  # Faster growth
)
```

### Harsh Universe Scenario
Life struggles to survive:
```python
config = SimulationConfig(
    PLANET_HABITABILITY_MAX=0.5,  # Lower max habitability
    SPONTANEOUS_LIFE_CHANCE=0.00001,  # Even rarer spontaneous life
    ASTEROID_LIFE_DECAY_RATE=0.01,  # Faster decay
    LIFE_DECLINE_CHANCE=0.05,  # More likely to decline
)
```

## Future Enhancements

See `PLANNING.md` for detailed future iteration ideas:
- PyGame real-time visualization
- 3D simulation
- Web-based interface
- Statistical analysis mode (run thousands of simulations)
- Physics-based orbital mechanics
- Cellular automata variant
- Network graph visualization of life spread

## Scientific Background

Panspermia is a hypothesis that life exists throughout the universe and is distributed by asteroids, meteorites, and other celestial bodies. This simulation explores:
- How quickly life could spread across a region of space
- The importance of habitability in sustaining life
- The role of asteroid frequency in life distribution
- Natural limits on panspermia due to time/distance

## License

This is a educational/research project. Feel free to use and modify as needed.
# panspermia-simulation
