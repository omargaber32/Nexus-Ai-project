# Nexus Air Traffic Conflict Resolver

Nexus is an air traffic conflict resolution system that uses game tree search algorithms—**Alpha-Beta Pruning** and **Minimax**—to compute optimal flight paths for two aircraft and determine whether mid-air conflicts can be avoided. The system analyzes different altitude adjustment strategies, visualizes the results, and compares algorithmic performance in real time through an interactive GUI.

## What It Does

- **Simulates two-aircraft conflicts** at altitude levels 1–10
- **Computes optimal paths** using both Alpha-Beta Pruning and Minimax algorithms
- **Detects conflicts** (aircraft occupying the same altitude)
- **Measures deviations** from planned descent/ascent paths
- **Visualizes results** with interactive charts, node evaluations, and summary tables
- **Exports reports** to PDF for analysis

## Stack

- **Language:** Python 3
- **GUI Framework:** PySide6 (Qt-based)
- **Visualization:** Matplotlib
- **Utilities:** tabulate (formatted terminal tables)

## How It's Organized

```
.
├── main.py              Entry point; initializes simulations and launches GUI
├── config.py            Config class for running simulations; manages results storage
├── algorithms.py        Alpha-Beta Pruning and Minimax search implementations
├── state.py             Aircraft and State classes; game tree logic, conflict detection, evaluation
├── gui.py               PySide6 GUI: tabbed interface, charts, tables, PDF export
├── requirements.txt     Python dependencies
└── .gitignore
```

### Architecture

**Simulation Flow:**

1. **Initialization** (`main.py`): Creates multiple `Config` objects, each with two aircraft starting/target altitudes.
2. **Game Tree Search** (`config.py` + `algorithms.py`): 
   - Runs Alpha-Beta Pruning to find the optimal path (with alpha-beta cutoffs)
   - Runs Minimax to evaluate all nodes without pruning
   - Stores results: paths, node counts, conflicts, deviations
3. **State Management** (`state.py`):
   - Maintains aircraft positions and targets (altitude levels)
   - Detects conflicts (both aircraft at same altitude = -10,000 penalty)
   - Evaluates board positions based on distance to targets
   - Generates next possible moves (-1, 0, +1 altitude change)
   - Computes path deviations from planned descent/ascent
4. **Visualization** (`gui.py`):
   - Displays per-config tabs with altitude trajectory charts
   - Shows algorithm performance comparison (nodes evaluated)
   - Provides summary table across all configs
   - Exports summary to PDF

## Getting Started

### Prerequisites
- Python 3.7 or higher
- pip

### Installation & Run

```bash
# Clone or download the repository
cd Nexus-Ai-project

# Install dependencies
pip install -r requirements.txt

# Run the application
python main.py
```

### What Happens When You Run It

1. **Terminal Output**: Four test configurations are simulated. For each:
   - Path decisions for both aircraft
   - Conflict status (Avoided / Happened / Cannot Happen)
   - Deviation from planned routes
   - Alpha-Beta vs. Minimax node evaluation count (formatted table)
   - Global summary table comparing all configs

2. **GUI Window**: A multi-tab interface opens with:
   - **Config 1–4 Tabs**: Each shows:
     - Altitude trajectory chart (actual vs. planned paths)
     - Outcome summary (paths, deviations, conflict status)
     - Node evaluation comparison table (Alpha-Beta vs. Minimax)
     - "Show All Nodes" button for full evaluation history
   - **Summary Tab**:
     - Cross-config comparison table
     - "Save to PDF" button to export results

## Configuration

Modify aircraft parameters in `main.py`:

```python
config1 = Config(a_start, a_target, b_start, b_target)
```

Where:
- `a_start`, `a_target`: Aircraft A starting altitude and target altitude (1–10)
- `b_start`, `b_target`: Aircraft B starting altitude and target altitude (1–10)

Additional parameters (in `Config.__init__`):
- `depth`: Search tree depth (default 6, max 6)
- `maximising`: Boolean for whose turn it is (true = Aircraft A's turn)
- `alpha`, `beta`: Initial bounds for Alpha-Beta pruning (defaults: -∞, +∞)

## Key Concepts

### Aircraft Roles (Game Theory)
- **Maximizer (Aircraft A)**: Tries to maximize the evaluation score (get closer to target)
- **Minimizer (Aircraft B)**: Tries to minimize the score (push Aircraft A away from target)

### Evaluation Function
```
Score = -distance(A to target) + distance(B to target)
Conflict penalty = -10,000
```

### Algorithms
- **Alpha-Beta Pruning**: Optimizes Minimax by cutting off branches that won't affect the final decision
- **Minimax**: Exhaustively evaluates all possible game states down to a given depth

## Example Output

```
Decision sequence for the first plane: [5, 6, 7, 8, 8, 8]
Decision sequence for the second plane: [3, 2, 2, 2, 2, 2]
Is conflict avoided: Conflict avoided
Deviation for the first plane: 3
Deviation for the second plane: 1
┌─────────────────────────┬──────────────────────────┬──────────────────────────┐
│                         │ Nodes evaluated alphabeta│ Nodes evaluated minimax  │
├─────────────────────────┼──────────────────────────┼──────────────────────────┤
│ Nodes                   │ [[5, 3], [6, 3], [7, 2]..│ [[5, 3], [6, 3], [7, 2]..│
│ Count                   │ 42                       │ 89                       │
└─────────────────────────┴──────────────────────────┴──────────────────────────┘
```

## Project Structure

| File | Purpose |
|------|---------|
| `main.py` | Bootstrap entry point; instantiates test configs and launches GUI |
| `config.py` | `Config` class; orchestrates algorithm runs and result storage |
| `algorithms.py` | `alpha_beta()` and `minimax()` game tree search functions |
| `state.py` | `Aircraft` & `State` classes; conflict detection, move generation, evaluation |
| `gui.py` | PySide6 GUI; tabs, charts, tables, PDF export functionality |

## Contributing & Future Work

- [ ] Add AI agents (minimax player can be human vs. AI)
- [ ] Extend depth/complexity beyond 6 levels
- [ ] Implement additional heuristics for evaluation function
- [ ] Add real-world air traffic data integration
- [ ] Performance profiling for large search trees

## License

This project is open source. See `LICENSE` for details (if applicable).

## Questions?

- **Why does Alpha-Beta evaluate fewer nodes?** Branch pruning eliminates subtrees that don't affect the best move.
- **What counts as a "conflict"?** Two aircraft at the same altitude level at the same step.
- **How is deviation calculated?** Sum of absolute differences between planned and actual positions across all steps.
