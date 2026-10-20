*This project has been created as part of the 42 curriculum by* **MAGRAM**.

# FLY-IN — Drone Simulation System

---

## Description

FLY-IN is a drone simulation system that models the movement of multiple drones through a weighted zone graph from a start hub to an end hub.

The goal is to route all drones from the start zone to the end zone in the minimum number of turns, respecting zone capacities, connection capacities, and zone type constraints (normal, priority, restricted, blocked).

### Overview

The project is structured as a multi-stage pipeline:

```
Input file
    ↓
Read_file       — reads and validates raw file structure
    ↓
RegEx_line      — parses and validates each line with regex
    ↓
Json_file       — builds the graph + runs reverse Dijkstra
    ↓
Simulation      — runs turn-based drone movement
    ↓
Terminal output — turn-by-turn drone positions
```

### Zone types

| Zone | Movement cost | Effect |
|---|---|---|
| `normal` | 1 | standard movement |
| `priority` | 1 | drones prefer these |
| `restricted` | 2 | costs extra turn to cross |
| `blocked` | 151 | effectively impassable |

---

## Algorithm Choices and Implementation Strategy

### Reverse Dijkstra — Gradient Field

Instead of running Dijkstra per drone per turn, FLY-IN runs **one reverse Dijkstra from the goal** before the simulation starts. This builds a gradient field — every zone knows its cost to reach the goal.

```
goal:  0
A:     1   (priority zone)
B:     3   (restricted zone)
start: 4   (normal + A cost)
```

Drones then follow the gradient downhill each turn — no pathfinding per drone needed. This is O(n log n) once vs O(n log n × drones × turns).

### Priority Queue (Min Heap)

Dijkstra uses Python's `heapq` — a min heap that always pops the lowest cost zone next. This guarantees the shortest path is found first without revisiting zones.

```python
heapq.heappush(heap, (cost, zone))
current_cost, current = heapq.heappop(heap)  # always minimum
```

### Turn-based Simulation

Each turn:
1. Every drone checks its gradient — finds the lowest cost neighbor
2. Skips full zones (`holde >= max_drones`)
3. Skips saturated connections (`holde >= capacity`)
4. Restricted zones add 1 extra wait turn
5. Connection `holde` resets after each turn (flow model)
6. Simulation ends when all drones reach goal

### Parser Pipeline

- `Read_file` — validates file structure (sections, keywords, comments)
- `RegEx_line` — validates each line format with named capture groups
- `Json_file` — assembles adjacency list graph with per-zone and per-edge state

### Visual Representation

The simulation outputs a turn-by-turn terminal trace showing each drone's movement:

```
TTurn 1: D1-d3  D2-d1  D3-d2  D5-d1  D8-d1  D11-d1 
Turn 2: D1-m3  D2-m2  D3-m2  D4-d3  D5-d1-m1  D6-d2  D7-d1  D9-d1 
Turn 3: D1-c2  D2-c3  D3-c2  D4-m3  D5-m1  D6-m2  D7-m2  D8-d1-m1  D10-d3  D12-d2  D13-d1  D14-d1 
Turn 4: D1-c2-merge1  D2-c3-merge2  D4-c3  D5-c1  D6-c2  D7-c3  D8-m1  D9-m2  D10-m3  D11-d1-m1  D12-m2  D15-d3  D16-d2  D17-d1  D18-d1 
Turn 5: D1-merge1  D2-merge2  D3-c2-merge1  D4-c3-merge2  D5-c1-merge1  D8-c1  D9-c2  D10-c3  D11-m1  D13-m2  D14-d1-m1  D15-m3  D16-m3  D19-d3  D20-d2 
Turn 6: D1-end  D2-end  D3-merge1  D4-merge2  D5-merge1  D6-c2-merge1  D7-c3-merge2  D11-c1  D12-c2  D13-c3  D14-m1  D17-m2  D18-d1-m1  D19-d3-m4  D20-m2 
Turn 7: D3-end  D4-end  D6-merge1  D7-merge2  D8-c1-merge1  D10-c3-merge2  D14-c1  D15-c3  D18-m1  D19-m4 
Turn 8: D5-end  D7-end  D8-merge1  D9-c2-merge1  D10-merge2  D13-c3-merge2  D16-c2  D17-c3  D19-c4 
Turn 9: D6-end  D9-merge1  D10-end  D11-c1-merge1  D13-merge2  D15-c3-merge2  D18-c1  D19-c4-merge2  D20-c3 
Turn 10: D8-end  D11-merge1  D12-c2-merge1  D13-end  D15-merge2  D17-c3-merge2  D19-merge2 
Turn 11: D9-end  D12-merge1  D14-c1-merge1  D15-end  D17-merge2  D20-c3-merge2 
Turn 12: D11-end  D14-merge1  D16-c2-merge1  D17-end  D20-merge2 
Turn 13: D12-end  D16-merge1  D18-c1-merge1  D19-end 
Turn 14: D14-end  D18-merge1  D20-end 
Turn 15: D16-end 
Turn 16: D18-end 

Total turns: 16
```

Each line shows: turn number + drone ID + destination zone. This lets the user trace every drone's path through the graph and verify routing decisions, capacity constraints, and zone interactions at each step.

---

## Instructions

### Requirements

- Python 3.11+
- `flake8`
- `mypy`

### Installation

```bash
# clone the project
git clone <repo_url>
cd FLY-IN

# create and activate virtual environment
python3 -m venv fly_env
source fly_env/bin/activate

# install dependencies
make install
```

### Running

```bash
# run simulation (uses test.txt by default)
make run

# or directly
python3 route_all.py <map.txt>
```

### Debug

```bash
make debug
```

### Lint

```bash
# mandatory flags
make lint

```

### Clean

```bash
make clean
```

### Input file format

Example input 
```
nb_drones: 20

start_hub: start 0 0 [color=green max_drones=20 zone=priority]
end_hub: end 14 0 [color=green max_drones=20 zone=priority]

# Layer 1 (Distribution)
hub: d1 2 4 [color=blue max_drones=4 zone=normal]
hub: d2 2 0 [color=blue max_drones=4 zone=normal]
hub: d3 2 -4 [color=blue max_drones=4 zone=priority]

# Layer 2 (Middle)
hub: m1 5 4 [color=yellow max_drones=2 zone=restricted]
hub: m2 5 1 [color=yellow max_drones=2 zone=normal]
hub: m3 5 -1 [color=yellow max_drones=2 zone=normal]
hub: m4 5 -4 [color=yellow max_drones=2 zone=restricted]

# Layer 3 (Connecting)
hub: c1 8 4 [color=orange max_drones=2 zone=normal]
hub: c2 8 1 [color=orange max_drones=2 zone=normal]
hub: c3 8 -1 [color=orange max_drones=2 zone=normal]
hub: c4 8 -4 [color=orange max_drones=2 zone=normal]

# Layer 4 (Merge)
hub: merge1 11 2 [color=red max_drones=3 zone=restricted]
hub: merge2 11 -2 [color=red max_drones=3 zone=restricted]

# Connections - Layer 1 to Layer 2
connection: start-d1 [max_link_capacity=5]
connection: start-d2
connection: start-d3

connection: d1-m1
connection: d1-m2
connection: d2-m2
connection: d2-m3
connection: d3-m3
connection: d3-m4

# Connections - Layer 2 to Layer 3
connection: m1-c1
connection: m1-c2
connection: m2-c2
connection: m2-c3
connection: m3-c2
connection: m3-c3
connection: m4-c3
connection: m4-c4

# Connections - Layer 3 to Layer 4
connection: c1-merge1
connection: c2-merge1
connection: c3-merge2
connection: c4-merge2

# Connections - Layer 4 to End
connection: merge1-end
connection: merge2-end
```

**Sections must appear in this order:**
1. `nb_drones` — first non-comment line
2. `start_hub` — exactly one
3. `end_hub` — exactly one
4. `hub` — zero or more
5. `connection` — one or more

---

## Resources

### Documentation

- [Python `re` module](https://docs.python.org/3/library/re.html) — regex engine used for parsing
- [Python `heapq` module](https://docs.python.org/3/library/heapq.html) — min heap for Dijkstra
- [mypy documentation](https://mypy.readthedocs.io/en/stable/) — static type checking
- [flake8 documentation](https://flake8.pycqa.org/en/latest/) — linting

### Articles

- [Dijkstra's algorithm — Wikipedia](https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm)
- [Adjacency list — Wikipedia](https://en.wikipedia.org/wiki/Adjacency_list)
- [Graph theory — Wikipedia](https://en.wikipedia.org/wiki/Graph_theory)
- [Priority queue — Wikipedia](https://en.wikipedia.org/wiki/Priority_queue)

### AI Usage

ai was used for the following tasks:

| Task | Parts of project |
|---|---|
| Type hint fixes | `Read_file.py`, `RegEx_line.py`, `Json_file.py`, `Simulation.py` |
| mypy and flake8 compliance | all `.py` files |
| Test pipeline setup | `Makefile`, `test_parser.sh`, `tests/` |

AI was used as a learning and debugging tool — all logic, algorithm choices, and architecture decisions were made by the me.