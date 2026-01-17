# Panspermia Simulation - Planning Document

## Overview
A 2D grid-based simulation modeling the spread of life through space via panspermia (the hypothesis that life can be distributed through space by asteroids/meteorites).

## Core Concepts

### Entities
1. **Stars** - Fixed points on the grid that can spawn planets
2. **Planets** - Orbit stars within a distance threshold, can spawn asteroids, can host life
3. **Asteroids** - Travel across the grid, may contain life, can seed planets
4. **Life** - Abstract property of planets that can grow, decline, and spread

### Simulation Mechanics
- **Grid**: 2D coordinate system (e.g., 100x100)
- **Tick-based**: Discrete time steps where all entities update
- **Probabilistic**: Most events governed by configurable probability parameters

## Data Structures

### Star
```
- position: (x, y)
- planets: list of Planet objects
- age: int (current age in ticks)
- lifetime: int (max age before death/supernova)
- is_alive: boolean
```

### Planet
```
- position: (x, y)
- parent_star: reference to Star
- has_life: boolean
- life_level: float (0.0 to 1.0, affects asteroid spawning probability)
- habitability: float (0.0 to 1.0, affects life seeding success and sustainability)
```

### Asteroid
```
- position: (x, y) - can be floating point
- velocity: (dx, dy) - direction vector
- contains_life: boolean
- in_transit: boolean (has left star system)
- life_viability: float (0.0 to 1.0, decreases each tick, life dies when reaches 0)
```

### Grid
```
- width: int
- height: int
- stars: list of Star objects
- asteroids: list of Asteroid objects
```

## Configuration Parameters

All of these should be adjustable:

```python
# Star/Planet Generation
GRID_SIZE = (100, 100)
NUM_STARS = 10
PLANET_SPAWN_CHANCE = 0.7  # per star
MAX_PLANETS_PER_STAR = 5
PLANET_ORBIT_RADIUS = 3  # max distance from star
INITIAL_LIFE_PLANETS = 3  # number of planets that start with life
STAR_MIN_LIFETIME = 500  # minimum ticks before star can die
STAR_MAX_LIFETIME = 2000  # maximum lifetime
PLANET_HABITABILITY_MIN = 0.2  # minimum habitability
PLANET_HABITABILITY_MAX = 1.0  # maximum habitability

# Asteroid Mechanics
ASTEROID_SPAWN_CHANCE = 0.01  # per planet per tick
ASTEROID_LIFE_BASE_CHANCE = 0.05  # base chance asteroid contains life
ASTEROID_LEAVE_SYSTEM_CHANCE = 0.1  # per asteroid per tick
ASTEROID_SPEED = 1.0  # units per tick
ASTEROID_LIFE_DECAY_RATE = 0.001  # viability lost per tick
ASTEROID_LIFE_INITIAL_VIABILITY = 1.0  # starting viability

# Life Mechanics
ASTEROID_SEED_BASE_SUCCESS = 0.3  # base chance when life-asteroid hits planet
LIFE_GROWTH_CHANCE = 0.05  # per tick for living planets
LIFE_DECLINE_CHANCE = 0.02  # per tick for living planets
LIFE_LEVEL_ASTEROID_MULTIPLIER = 2.0  # how much life level increases asteroid spawn chance
SPONTANEOUS_LIFE_CHANCE = 0.0001  # very low chance for life to spontaneously appear
HABITABILITY_SEEDING_MULTIPLIER = 1.5  # how much habitability affects seeding success
HABITABILITY_SUSTAIN_MULTIPLIER = 0.8  # how much habitability affects life decline

# Simulation
MAX_TICKS = 1000
```

## Implementation Design

### Class Structure

```
Simulation
├── Grid
│   ├── stars: List[Star]
│   └── asteroids: List[Asteroid]
├── Config (dataclass or dict)
├── Statistics (tracking spread of life)
└── TickBehaviors (list of behavior modules)

Star
├── position: Tuple[int, int]
├── planets: List[Planet]
├── age: int
├── lifetime: int
└── is_alive: bool

Planet
├── position: Tuple[int, int]
├── parent_star: Star
├── has_life: bool
├── life_level: float
└── habitability: float

Asteroid
├── position: Tuple[float, float]
├── velocity: Tuple[float, float]
├── contains_life: bool
├── in_transit: bool
└── life_viability: float
```

### Core Algorithm (per tick)

**Traditional Approach:**
```
1. For each star:
   a. Increment age
   b. Check if lifetime exceeded (trigger death/supernova)

2. For each planet:
   a. Check spontaneous life generation
   b. Check life growth/decline (modified by habitability)
   c. Attempt to spawn asteroid

3. For each asteroid:
   a. Decay life viability
   b. Check if life dies (viability reaches 0)
   c. If not in transit, check if leaving system
   d. Move asteroid along velocity vector
   e. Check collision with planets
   f. If collision and contains life, attempt seeding (modified by habitability)
   g. Remove if out of bounds

4. Update statistics
5. Render (if visualization enabled)
```

**Modular Approach (Recommended):**
See "Modular Architecture" section below for the plugin-based design.

### Initialization

```
1. Create empty grid
2. Spawn N stars at random positions
3. For each star:
   - Assign random lifetime (between MIN and MAX)
   - Set age to 0
   - Determine number of planets (random, up to MAX)
   - Place planets in orbit (random angle, random radius < MAX_RADIUS)
   - Assign each planet a random habitability score
4. Seed INITIAL_LIFE_PLANETS random planets with life (life_level = random 0.3-0.7)
```

### Output

The simulation should track and output:
- Number of living planets per tick
- Total life events (successful seedings)
- Asteroid statistics (total spawned, total with life)
- Final state: grid visualization showing stars, planets, life

## Modular Architecture

### Design Philosophy
To support easy addition of new behaviors and effects, the simulation uses a **modular tick behavior system**. Each behavior is a self-contained module that can be enabled/disabled independently.

### Behavior Plugin System

**Base Class:**
```python
class TickBehavior(ABC):
    """Base class for all tick behaviors"""

    def __init__(self, config):
        self.config = config
        self.enabled = True

    @abstractmethod
    def execute(self, grid, tick_number):
        """Execute this behavior for the current tick"""
        pass

    def get_stats(self):
        """Return statistics for this behavior"""
        return {}
```

**Example Behaviors:**
```python
class StarAgingBehavior(TickBehavior):
    def execute(self, grid, tick_number):
        for star in grid.stars:
            star.age += 1
            if star.age > star.lifetime:
                self.handle_star_death(star, grid)

class PlanetLifeBehavior(TickBehavior):
    def execute(self, grid, tick_number):
        for star in grid.stars:
            for planet in star.planets:
                self.check_spontaneous_life(planet)
                if planet.has_life:
                    self.update_life_level(planet)

class AsteroidMovementBehavior(TickBehavior):
    def execute(self, grid, tick_number):
        for asteroid in grid.asteroids:
            self.decay_life_viability(asteroid)
            self.move_asteroid(asteroid)
            self.check_collisions(asteroid, grid)

class AsteroidSpawnBehavior(TickBehavior):
    def execute(self, grid, tick_number):
        for star in grid.stars:
            for planet in star.planets:
                self.attempt_spawn_asteroid(planet, grid)
```

### Adding New Behaviors

To add a new effect (e.g., "Cosmic Radiation" that damages life):

1. Create new behavior class:
```python
class CosmicRadiationBehavior(TickBehavior):
    def execute(self, grid, tick_number):
        if tick_number % self.config.RADIATION_INTERVAL == 0:
            affected_zone = self.pick_random_zone(grid)
            for planet in self.get_planets_in_zone(affected_zone, grid):
                if planet.has_life:
                    planet.life_level *= self.config.RADIATION_DAMAGE
```

2. Add configuration:
```python
# In config.py
RADIATION_INTERVAL = 100
RADIATION_DAMAGE = 0.8  # reduce life level by 20%
```

3. Register behavior:
```python
# In simulation.py
simulation.add_behavior(CosmicRadiationBehavior(config))
```

### Execution Order

Behaviors execute in priority order each tick:
```python
class Simulation:
    def __init__(self):
        self.behaviors = [
            (1, StarAgingBehavior()),          # Phase 1: Environmental changes
            (2, PlanetLifeBehavior()),         # Phase 2: Life processes
            (3, AsteroidSpawnBehavior()),      # Phase 3: Asteroid generation
            (4, AsteroidMovementBehavior()),   # Phase 4: Movement & collision
            (5, StatisticsUpdateBehavior()),   # Phase 5: Bookkeeping
        ]

    def tick(self):
        sorted_behaviors = sorted(self.behaviors, key=lambda x: x[0])
        for priority, behavior in sorted_behaviors:
            if behavior.enabled:
                behavior.execute(self.grid, self.tick_number)
```

### Benefits of Modular Design

1. **Easy to extend**: Add new behaviors without modifying existing code
2. **Easy to test**: Test each behavior in isolation
3. **Easy to configure**: Enable/disable behaviors dynamically
4. **Easy to debug**: Isolate issues to specific behaviors
5. **Easy to experiment**: Try different combinations of behaviors
6. **Separation of concerns**: Each behavior has single responsibility

### Advanced Modularity: Event System

For even more flexibility, behaviors can emit/listen to events:

```python
class EventBus:
    def __init__(self):
        self.listeners = defaultdict(list)

    def emit(self, event_type, data):
        for listener in self.listeners[event_type]:
            listener(data)

    def on(self, event_type, callback):
        self.listeners[event_type].append(callback)

# Example usage
event_bus.on('planet_seeded', lambda data: print(f"Life seeded on {data['planet']}"))
event_bus.on('star_death', lambda data: trigger_supernova_effect(data['star']))
```

This allows behaviors to react to events from other behaviors without tight coupling.

## File Structure

```
panspermia-simulation/
├── PLANNING.md (this file)
├── README.md
├── requirements.txt
├── config.py (configuration parameters)
├── entities.py (Star, Planet, Asteroid classes)
├── grid.py (Grid class)
├── simulation.py (main Simulation class)
├── behaviors/ (modular tick behaviors)
│   ├── __init__.py
│   ├── base.py (TickBehavior base class)
│   ├── star_behaviors.py (StarAgingBehavior, etc.)
│   ├── planet_behaviors.py (PlanetLifeBehavior, etc.)
│   ├── asteroid_behaviors.py (AsteroidMovement, AsteroidSpawn, etc.)
│   └── event_bus.py (optional event system)
├── visualizer.py (ASCII or matplotlib visualization)
└── main.py (entry point)
```

## Initial Implementation (CLI + ASCII)

### Phase 1: Core Simulation
- Pure Python, no external dependencies
- ASCII visualization (optional per tick or final state)
- Configuration via config.py or CLI arguments
- Output statistics to console/file

### Visualization Options for Phase 1
```
. = empty space
* = star
o = planet (no life)
O = planet (with life)
+ = asteroid (no life)
# = asteroid (with life)
```

## Future Iterations & Alternatives

### 1. PyGame Visualization
**What it adds:**
- Real-time animated visualization
- Better visual distinction (colors, shapes, sizes)
- Interactive controls (pause, speed up, restart)
- Click on entities for info

**Implementation:**
- Star: yellow circles
- Planets: smaller circles, color-coded by life level (gray → green)
- Asteroids: small dots, trail effect
- Connect planets to stars with faint lines

**Complexity:** Medium - PyGame is relatively simple for 2D

---

### 2. 3D Simulation (matplotlib or PyVista)
**What it adds:**
- Z-axis for more realistic space
- Planets orbit in 3D
- Asteroids travel in 3D space
- More realistic collision detection

**Implementation approaches:**
- matplotlib 3D scatter plots (simple but limited interactivity)
- PyVista (more powerful, smooth rendering)
- Three.js via web interface

**Complexity:** High - 3D math, rendering complexity

---

### 3. Web-based Visualization (JavaScript + Canvas/WebGL)
**What it adds:**
- Shareable simulations (run in browser)
- Better UI/UX for configuration
- Easier distribution (no Python install needed)
- Could export simulation data from Python, visualize in browser

**Tech stack:**
- Python backend generates simulation data
- D3.js, Three.js, or P5.js for visualization
- Flask/FastAPI for serving

**Complexity:** Medium-High - requires web dev skills

---

### 4. Statistical Analysis Mode
**What it adds:**
- Run 1000s of simulations with varying parameters
- Generate charts showing parameter sensitivity
- Monte Carlo analysis
- Optimize parameters for maximum life spread

**Tools:**
- numpy for vectorization (speed up)
- pandas for data analysis
- matplotlib/seaborn for charts
- multiprocessing for parallel runs

**Complexity:** Medium - mostly about optimization and data handling

---

### 5. Cellular Automata Variant
**What it adds:**
- Grid cells themselves are the simulation units
- Life spreads via neighbor rules (like Conway's Game of Life)
- Asteroids = transient patterns that can jump cells
- More abstract but potentially faster

**Complexity:** Low-Medium - simpler model, different approach

**See "Cellular Automata Deep Dive" section below for detailed explanation**

---

### 6. Physics-Based (Orbital Mechanics)
**What it adds:**
- Real gravitational calculations
- Elliptical orbits
- N-body simulation
- More scientifically accurate

**Tools:**
- scipy for numerical integration
- Realistic orbital parameters

**Complexity:** High - requires physics knowledge

---

### 7. Network Graph Visualization
**What it adds:**
- View simulation as a graph
- Nodes = planets
- Edges = successful life transfers
- Track lineage of life

**Tools:**
- networkx for graph structure
- pyvis or gephi for interactive visualization

**Complexity:** Low-Medium - orthogonal visualization

---

## Recommended Progression

1. **Start:** CLI + ASCII (Phase 1) - proves the concept
2. **Next:** PyGame - makes it engaging and easier to debug
3. **Then:** Statistical analysis - understand parameter space
4. **Advanced:** Choose based on interest:
   - 3D for visual appeal
   - Web-based for sharing
   - Physics-based for accuracy

## Technical Considerations

### Performance
- Current design: O(n) per tick for n entities
- For large grids/many asteroids, consider:
  - Spatial hashing for collision detection
  - Quadtree for efficient neighbor queries
  - NumPy for vectorized operations

### Randomness
- Use `random.Random()` with seed for reproducibility
- Important for debugging and comparative runs

### Testing
- Unit tests for entity behaviors
- Integration tests for tick mechanics
- Statistical tests (run 100 times, verify distributions)

## Design Decisions

### Answered Questions

1. **Initial life seeding and spontaneous generation**
   - **Decision**: Both mechanisms exist
   - Simulation starts with N planets (configurable) that have life
   - Life can also spontaneously generate on any planet with very low probability per tick
   - This creates two pathways for life emergence

2. **Asteroid lifetime and life viability**
   - **Decision**: Asteroids travel indefinitely, but life inside decays
   - Asteroids persist until they exit the grid or collide
   - Life inside asteroids has a viability score (0.0-1.0) that decays each tick
   - When viability reaches 0, the asteroid no longer contains viable life
   - This creates a distance limit for panspermia naturally

3. **Star lifecycle**
   - **Decision**: Stars have finite lifetimes
   - Each star spawns with a random lifetime (configurable range)
   - Stars age each tick and can die/supernova when lifetime is exceeded
   - Star death can be expanded later (destroy planets, create new stars, etc.)

4. **Planetary habitability**
   - **Decision**: Each planet has a habitability score
   - Habitability is assigned at planet creation (random within range)
   - Higher habitability increases:
     - Success chance when asteroid with life collides
     - Life sustainability (reduces decline rate)
   - Lower habitability makes life harder to start and maintain
   - This adds realistic variation between planets

### Open for Future Iterations

5. Should there be different types of life (competitive)?
6. Should stars go supernova and affect nearby systems?
7. Should planet habitability change over time?
8. Should there be rare events (gamma ray bursts, passing comets, etc.)?

## Success Criteria

The simulation is successful if:
- Life can spread from one star system to another
- Parameters meaningfully affect outcomes
- Code is modular and extensible
- Visualization clearly shows the process
- Configuration is intuitive

---

## Cellular Automata Deep Dive

### What is Cellular Automata?

Cellular Automata (CA) is a discrete model where:
- Space is divided into a regular grid of cells
- Each cell has a **state** (e.g., empty, alive, dead)
- Time advances in discrete steps (ticks)
- Each cell's next state is determined by **rules** based on its current state and its **neighbors**

**Famous example:** Conway's Game of Life
- Cells are either alive or dead
- Rules:
  - Any live cell with 2-3 live neighbors survives
  - Any dead cell with exactly 3 live neighbors becomes alive
  - All other cells die or stay dead

### Cellular Automata for Panspermia

Instead of tracking individual Star/Planet/Asteroid objects, each grid cell has a state that represents what it contains.

### Cell States

Each cell in the grid has multiple properties (multi-state CA):

```python
class Cell:
    cell_type: CellType  # EMPTY, STAR, PLANET, ASTEROID_TRANSIT
    has_life: bool
    life_level: float  # 0.0 to 1.0
    habitability: float  # 0.0 to 1.0 (for planets)
    star_age: int  # (for stars)
    asteroid_direction: (dx, dy)  # velocity vector (for asteroids)
    asteroid_life_viability: float  # (for asteroids)
```

**Simplified visualization:**
```
State encoding per cell:
. = Empty space
* = Star (no planets with life nearby)
S = Star (with planets that have life nearby)
o = Planet (no life)
O = Planet (with life)
> = Asteroid moving right (no life)
# = Asteroid with life (direction encoded)
```

### Transition Rules

Instead of iterating over objects, we iterate over cells and apply rules based on neighborhood.

#### Rule 1: Star Aging and Death
```python
def update_star_cell(cell, neighbors):
    if cell.cell_type == STAR:
        cell.star_age += 1
        if cell.star_age > MAX_STAR_LIFETIME:
            # Star dies - convert to empty or supernova
            cell.cell_type = EMPTY
            # Could affect neighbors (supernova shockwave)
            for neighbor in neighbors:
                if neighbor.has_life:
                    neighbor.has_life = random.random() < 0.1  # 90% extinction
```

#### Rule 2: Planetary Life Dynamics
```python
def update_planet_cell(cell, neighbors):
    if cell.cell_type == PLANET:
        # Spontaneous generation
        if not cell.has_life:
            if random.random() < SPONTANEOUS_LIFE_CHANCE:
                cell.has_life = True
                cell.life_level = 0.1

        # Life growth/decline based on habitability
        if cell.has_life:
            growth_prob = LIFE_GROWTH_CHANCE * cell.habitability
            decline_prob = LIFE_DECLINE_CHANCE / cell.habitability

            if random.random() < growth_prob:
                cell.life_level = min(1.0, cell.life_level + 0.1)
            elif random.random() < decline_prob:
                cell.life_level = max(0.0, cell.life_level - 0.1)
                if cell.life_level == 0:
                    cell.has_life = False
```

#### Rule 3: Asteroid Spawning
```python
def spawn_asteroid_from_planet(cell, grid, x, y):
    if cell.cell_type == PLANET and cell.has_life:
        if random.random() < ASTEROID_SPAWN_CHANCE * cell.life_level:
            # Pick random direction
            direction = random.choice([
                (1, 0), (-1, 0), (0, 1), (0, -1),  # cardinal
                (1, 1), (1, -1), (-1, 1), (-1, -1)  # diagonal
            ])

            # Find next empty cell in that direction
            next_x, next_y = x + direction[0], y + direction[1]
            if grid.in_bounds(next_x, next_y):
                next_cell = grid[next_x][next_y]
                if next_cell.cell_type == EMPTY:
                    next_cell.cell_type = ASTEROID_TRANSIT
                    next_cell.asteroid_direction = direction
                    next_cell.contains_life = random.random() < ASTEROID_LIFE_BASE_CHANCE
                    next_cell.asteroid_life_viability = 1.0
```

#### Rule 4: Asteroid Movement (Most Interesting!)
```python
def update_asteroid_cell(cell, grid, x, y):
    if cell.cell_type == ASTEROID_TRANSIT:
        # Decay life viability
        if cell.contains_life:
            cell.asteroid_life_viability -= ASTEROID_LIFE_DECAY_RATE
            if cell.asteroid_life_viability <= 0:
                cell.contains_life = False

        # Calculate next position
        dx, dy = cell.asteroid_direction
        next_x, next_y = x + dx, y + dy

        # Check bounds
        if not grid.in_bounds(next_x, next_y):
            # Asteroid leaves grid - disappear
            cell.cell_type = EMPTY
            return

        next_cell = grid[next_x][next_y]

        # Check collision with planet
        if next_cell.cell_type == PLANET:
            # Collision! Attempt seeding
            if cell.contains_life and not next_cell.has_life:
                seed_success = ASTEROID_SEED_BASE_SUCCESS * next_cell.habitability
                if random.random() < seed_success:
                    next_cell.has_life = True
                    next_cell.life_level = 0.3

            # Asteroid is destroyed on impact
            cell.cell_type = EMPTY

        # If next cell is empty, move asteroid
        elif next_cell.cell_type == EMPTY:
            # Move asteroid to next cell
            next_cell.cell_type = ASTEROID_TRANSIT
            next_cell.asteroid_direction = cell.asteroid_direction
            next_cell.contains_life = cell.contains_life
            next_cell.asteroid_life_viability = cell.asteroid_life_viability

            # Clear current cell
            cell.cell_type = EMPTY

        # If next cell is occupied (star/another asteroid), asteroid bounces/disappears
        else:
            cell.cell_type = EMPTY
```

### Neighborhood Definitions

Different rules use different neighborhoods:

**Moore Neighborhood** (8 neighbors - all adjacent cells):
```
[NW][N][NE]
[W ][X][E ]
[SW][S][SE]
```
Good for: Life spread, local effects, resource sharing

**Von Neumann Neighborhood** (4 neighbors - cardinal directions):
```
   [N]
[W][X][E]
   [S]
```
Good for: Asteroid directions, radiation spread

**Extended Neighborhood** (radius 2 or more):
```
[ ][ ][ ][ ][ ]
[ ][x][x][x][ ]
[ ][x][X][x][ ]
[ ][x][x][x][ ]
[ ][ ][ ][ ][ ]
```
Good for: Planetary systems, gravitational effects

### Complete Update Algorithm (per tick)

```python
def tick(grid):
    # Create a copy to avoid conflicts (double buffering)
    new_grid = copy.deepcopy(grid)

    for y in range(grid.height):
        for x in range(grid.width):
            cell = grid[x][y]
            neighbors = grid.get_neighbors(x, y)

            # Apply rules based on cell type
            if cell.cell_type == STAR:
                update_star_cell(new_grid[x][y], neighbors)

            elif cell.cell_type == PLANET:
                update_planet_cell(new_grid[x][y], neighbors)
                spawn_asteroid_from_planet(new_grid[x][y], new_grid, x, y)

            elif cell.cell_type == ASTEROID_TRANSIT:
                update_asteroid_cell(new_grid[x][y], new_grid, x, y)

    return new_grid
```

**Important:** Double buffering prevents conflicts where updating one cell affects another being updated in the same tick.

### Representing Star Systems in CA

Since stars have planets orbiting them, we need to represent this spatially:

**Option 1: Star with Planet Neighbors**
```
. . . . . .
. o o o . .
. o * o . .
. o o o . .
. . . . . .
```
Star (*) at center, planets (o) in surrounding cells

**Option 2: Star Cell Contains Planet Count**
```
Cell state includes:
- is_star: bool
- planet_count: int
- planet_states: List[PlanetState]  # nested state for each planet
```

**Option 3: Hybrid - Regions**
Divide grid into regions, each region can be a star system:
```python
class Region:
    star_position: (x, y)
    planets: List[Planet]  # virtual planets not on grid
```

### Example CA Panspermia Rules Set

Here's a complete minimal rule set:

```python
# Rule 1: Stars age
if cell.is_star:
    cell.age += 1
    if cell.age > cell.lifetime:
        cell.is_star = False  # Star dies

# Rule 2: Planets near stars spawn asteroids
if cell.is_planet and cell.has_life:
    for direction in random_directions():
        if should_spawn_asteroid():
            spawn_asteroid(cell, direction)

# Rule 3: Asteroids move
if cell.is_asteroid:
    move_in_direction(cell)
    cell.life_viability *= 0.999  # decay
    if collides_with_planet():
        attempt_seed_life()

# Rule 4: Life spreads locally (bonus mechanic!)
if cell.is_planet and cell.has_life:
    for neighbor in get_neighbors(cell):
        if neighbor.is_planet and not neighbor.has_life:
            if random() < LOCAL_SPREAD_CHANCE:
                neighbor.has_life = True  # Direct spread
```

### Advantages of CA Approach

1. **Simpler Code**
   - No complex object hierarchies
   - Just grid + rules
   - Easier to understand

2. **Better Performance**
   - Grid iteration is cache-friendly
   - Can use NumPy for vectorization
   - Parallelizable (update chunks independently)

3. **Easier Visualization**
   - Grid maps directly to screen pixels
   - No coordinate conversion needed

4. **Natural Spatial Relationships**
   - Neighbor-based rules feel natural
   - Local effects emerge naturally

5. **Interesting Emergent Behavior**
   - Patterns can emerge from simple rules
   - Life "fronts" can form and spread
   - Asteroid "waves" can propagate

### Disadvantages of CA Approach

1. **Less Precise**
   - Asteroids move in discrete steps (cell to cell)
   - Can't have smooth trajectories
   - Distance is quantized

2. **Grid Artifacts**
   - Manhattan distance vs Euclidean
   - Diagonal bias in some neighborhoods
   - Hard to represent circular orbits

3. **Spatial Constraints**
   - One entity per cell (usually)
   - Hard to have multiple asteroids in same location
   - Star systems are spatially large

4. **Less Realistic**
   - Physics is simplified
   - No continuous motion
   - More abstract

### Hybrid Approach

Best of both worlds: **Object-oriented entities + CA-style rules**

```python
class Grid:
    cells: 2D array of Cell

    def get_entities_in_cell(x, y):
        # Multiple entities can exist at a cell
        return [e for e in all_entities if e.position == (x, y)]

    def get_neighbors(x, y):
        # Returns cells or entities in neighboring cells
        pass

# Entities move continuously but rules check discrete neighbors
```

This lets you have smooth asteroid motion while using neighbor-based rules for life spread, radiation, etc.

### When to Use CA vs Object-Oriented

**Use CA if:**
- Simplicity is priority
- You want emergent patterns
- Performance is critical (large grids)
- Spatial relationships are key
- You want easy visualization

**Use Object-Oriented if:**
- Precision is important
- You need complex entity behaviors
- Entities have unique properties
- You want realistic physics
- Fewer entities, larger space

**Use Hybrid if:**
- You want both precision and spatial rules
- Willing to handle extra complexity
- Want best of both worlds

### CA Implementation Example

```python
import numpy as np

# Cell states as integers for NumPy efficiency
EMPTY = 0
STAR = 1
PLANET = 2
ASTEROID = 3

class CASimulation:
    def __init__(self, width, height):
        self.width = width
        self.height = height

        # Multiple layers for different properties
        self.cell_type = np.zeros((height, width), dtype=int)
        self.has_life = np.zeros((height, width), dtype=bool)
        self.life_level = np.zeros((height, width), dtype=float)
        self.habitability = np.random.uniform(0.2, 1.0, (height, width))

    def tick(self):
        # Update all cells based on rules
        new_cell_type = self.cell_type.copy()
        new_has_life = self.has_life.copy()
        new_life_level = self.life_level.copy()

        # Vectorized operations where possible
        # Non-vectorized rules in loops

        for y in range(self.height):
            for x in range(self.width):
                self.apply_rules(x, y, new_cell_type, new_has_life, new_life_level)

        self.cell_type = new_cell_type
        self.has_life = new_has_life
        self.life_level = new_life_level
```

### Visualization Comparison

**CA Approach:**
```
Direct grid rendering - each cell is a pixel/character
* * . . . o . . > . .
* * . . O o . . . . .
. . . . o o . . . . #
. . . . . . . . . . .
```

**Object-Oriented Approach:**
```
Place entities on canvas at their (x, y) positions
Can have smooth positions between cells
```

### Conclusion

The Cellular Automata approach is **simpler and faster** but **less precise**. It's great for:
- Rapid prototyping
- Exploring rule-based emergence
- Large-scale simulations
- Educational demonstrations

The Object-Oriented approach (what we've designed) is **more flexible and realistic**. It's better for:
- Scientific accuracy
- Complex entity behaviors
- Detailed tracking
- Statistical analysis

For your panspermia simulation, **I recommend starting with the Object-Oriented design** (with modular behaviors) because:
1. More realistic representation of space
2. Easier to add complex features later
3. Better for scientific exploration
4. The modular behavior system gives you CA-like extensibility anyway

But you could **add a CA mode as an alternative visualization or a simplified "fast mode"** later!
