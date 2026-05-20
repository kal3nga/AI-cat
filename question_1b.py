
"""
Finding the Shortest Path with A* 
"""

import heapq
import numpy as np
import matplotlib.pyplot as plt
from typing import List, Tuple, Dict, Set
import time

class MapSpot:
    def __init__(self, coordinates: Tuple[int, int], came_from=None):
        self.spot = coordinates
        self.parent = came_from
        self.cost_from_start = 0
        self.guess_to_goal = 0
        self.total_cost = 0
        
    def __lt__(self, other):
        return self.total_cost < other.total_cost

    def __eq__(self, other):
        return self.spot == other.spot

class PathFinder:
    def __init__(self, map_grid: np.ndarray):
        self.map = map_grid
        self.rows, self.cols = map_grid.shape

    def guess_distance(self, current: Tuple[int, int], destination: Tuple[int, int]) -> float:
        return np.sqrt((current[0] - destination[0])**2 + (current[1] - destination[1])**2)

    def find_walkable_neighbors(self, location: MapSpot) -> List[Tuple[int, int]]:
        possible_moves = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        good_neighbors = []

        for row_change, col_change in possible_moves:
            new_row = location.spot[0] + row_change
            new_col = location.spot[1] + col_change

            if (0 <= new_row < self.rows and 0 <= new_col < self.cols and
                self.map[new_row][new_col] == 0):
                good_neighbors.append((new_row, new_col))

        return good_neighbors

    def find_route(self, start: Tuple[int, int], goal: Tuple[int, int]) -> Tuple[List[Tuple[int, int]], Dict]:
        start_time = time.time()

        start_spot = MapSpot(start)
        goal_spot = MapSpot(goal)

        to_explore = []
        already_visited = set()
        spot_lookup = {}

        start_spot.cost_from_start = 0
        start_spot.guess_to_goal = self.guess_distance(start, goal)
        start_spot.total_cost = start_spot.cost_from_start + start_spot.guess_to_goal

        heapq.heappush(to_explore, start_spot)
        spot_lookup[start] = start_spot

        spots_considered = 0

        while to_explore:
            current_spot = heapq.heappop(to_explore)
            spots_considered += 1

            if current_spot.spot == goal:
                path = self.trace_back_path(current_spot)
                time_taken = time.time() - start_time
                
                stats = {
                    'path_length': len(path),
                    'path_cost': current_spot.cost_from_start,
                    'spots_considered': spots_considered,
                    'time_taken': time_taken,
                    'todo_list_size': len(to_explore),
                    'done_list_size': len(already_visited)
                }
                return path, stats

            already_visited.add(current_spot.spot)

            for neighbor_spot in self.find_walkable_neighbors(current_spot):
                if neighbor_spot in already_visited:
                    continue

                tentative_cost = current_spot.cost_from_start + 1
                neighbor = spot_lookup.get(neighbor_spot)

                if neighbor is None:
                    neighbor = MapSpot(neighbor_spot, current_spot)
                    neighbor.cost_from_start = tentative_cost
                    neighbor.guess_to_goal = self.guess_distance(neighbor_spot, goal)
                    neighbor.total_cost = neighbor.cost_from_start + neighbor.guess_to_goal
                    spot_lookup[neighbor_spot] = neighbor
                    heapq.heappush(to_explore, neighbor)

                elif tentative_cost < neighbor.cost_from_start:
                    neighbor.parent = current_spot
                    neighbor.cost_from_start = tentative_cost
                    neighbor.total_cost = neighbor.cost_from_start + neighbor.guess_to_goal

        return [], {'error': 'No path exists', 'spots_considered': spots_considered}

    def trace_back_path(self, spot: MapSpot) -> List[Tuple[int, int]]:
        full_path = []
        current = spot
        while current is not None:
            full_path.append(current.spot)
            current = current.parent
        return full_path[::-1]

def draw_map_with_path(map_grid: np.ndarray, route: List[Tuple[int, int]],
                       start: Tuple[int, int], goal: Tuple[int, int]):
    fig, ax = plt.subplots(figsize=(10, 8))

    color_map = plt.cm.colors.ListedColormap(['white', 'black', 'limegreen', 'red', 'dodgerblue'])
    bounds = [-0.5, 0.5, 1.5, 2.5, 3.5, 4.5]
    norm = plt.cm.colors.BoundaryNorm(bounds, color_map.N)

    viz_grid = map_grid.copy().astype(float)
    viz_grid[start] = 2
    viz_grid[goal] = 3

    for spot in route[1:-1]:
        viz_grid[spot] = 4

    ax.imshow(viz_grid, cmap=color_map, norm=norm, origin='upper')

    ax.set_xticks(np.arange(-0.5, map_grid.shape[1], 1), minor=True)
    ax.set_yticks(np.arange(-0.5, map_grid.shape[0], 1), minor=True)
    ax.grid(which='minor', color='gray', linestyle='-', linewidth=0.5)

    ax.set_title(f'Path Length: {len(route)} steps', fontsize=14)
    ax.set_xlabel('Columns')
    ax.set_ylabel('Rows')

    from matplotlib.patches import Patch
    legend_elements = [
        Patch(facecolor='white', label='Free Space'),
        Patch(facecolor='black', label='Obstacle'),
        Patch(facecolor='limegreen', label='Start'),
        Patch(facecolor='red', label='Goal'),
        Patch(facecolor='dodgerblue', label='Path')
    ]
    ax.legend(handles=legend_elements, loc='upper right')

    plt.tight_layout()
    plt.show()

def run_demo():
    scenarios = [
        {
            'name': 'Simple Open Grid',
            'grid': np.zeros((10, 10), dtype=int),
            'start': (0, 0),
            'goal': (9, 9)
        },
        {
            'name': 'Grid with Obstacles',
            'grid': np.zeros((12, 12), dtype=int),
            'start': (0, 0),
            'goal': (11, 11),
            'obstacles': [(3, 3), (3, 4), (4, 3), (4, 4), (5, 5), (5, 6), (6, 5), (6, 6),
                          (7, 2), (7, 3), (8, 2), (8, 3), (2, 7), (3, 7), (2, 8), (3, 8)]
        },
        {
            'name': 'Maze-like Environment',
            'grid': np.zeros((15, 15), dtype=int),
            'start': (0, 0),
            'goal': (14, 14),
            'obstacles': [(i, 7) for i in range(15) if i != 0 and i != 14] +
                         [(7, i) for i in range(15) if i != 7]
        }
    ]

    for scenario in scenarios:
        if 'obstacles' in scenario:
            for obs in scenario['obstacles']:
                scenario['grid'][obs] = 1

    for scenario in scenarios:
        print(f"\n{'='*60}")
        print(f"Scenario: {scenario['name']}")
        print(f"{'='*60}")

        finder = PathFinder(scenario['grid'])
        path, stats = finder.find_route(scenario['start'], scenario['goal'])

        if path:
            print(f"✓ Path found!")
            print(f"  Path length: {stats['path_length']} steps")
            print(f"  Total cost: {stats['path_cost']}")
            print(f"  Nodes explored: {stats['spots_considered']}")
            print(f"  Time taken: {stats['time_taken']:.5f} seconds")
            print(f"  Path: {path[:5]}...{path[-3:]}")

            draw_map_with_path(scenario['grid'], path, scenario['start'], scenario['goal'])
        else:
            print(f"✗ No path found: {stats.get('error', 'Unknown error')}")

if __name__ == "__main__":
    run_demo()
