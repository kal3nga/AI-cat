# -*- coding: utf-8 -*-
"""Vacuum Cleaner Agent"""

import random
import time
import matplotlib.pyplot as plt
import numpy as np
from enum import Enum
from typing import Tuple, List, Dict
import copy

class Action(Enum):
    MOVE_UP = "↑"
    MOVE_DOWN = "↓"
    MOVE_LEFT = "←"
    MOVE_RIGHT = "→"
    SUCK = "🧹"
    IDLE = "💤"

class LocationState(Enum):
    CLEAN = "●"
    DIRTY = "○"

class VacuumCleanerAgent:
    def __init__(self, rows: int = 5, cols: int = 5, dirt_probability: float = 0.4):
        self.rows = rows
        self.cols = cols
        self.dirt_probability = dirt_probability
        self.grid = self._initialize_grid()
        self.position = (0, 0)
        self.actions_taken = []
        self.total_dirt_cleaned = 0
        self.moves_made = 0
        self.suck_actions = 0
        self.idle_actions = 0
        self.initial_dirt_count = sum(cell == LocationState.DIRTY for row in self.grid for cell in row)
        self.current_dirt_count = self.initial_dirt_count
        self.visited = set()
        self.cleaning_history = []

    def _initialize_grid(self) -> List[List[LocationState]]:
        grid = []
        for i in range(self.rows):
            row = []
            for j in range(self.cols):
                if random.random() < self.dirt_probability:
                    row.append(LocationState.DIRTY)
                else:
                    row.append(LocationState.CLEAN)
            grid.append(row)
        return grid

    def sense(self) -> LocationState:
        x, y = self.position
        return self.grid[x][y]

    def act(self, action: Action) -> bool:
        x, y = self.position

        if action == Action.SUCK:
            if self.sense() == LocationState.DIRTY:
                self.grid[x][y] = LocationState.CLEAN
                self.total_dirt_cleaned += 1
                self.current_dirt_count -= 1
                self.suck_actions += 1
                self.cleaning_history.append(('SUCK', self.position))
                return True
            return False

        elif action == Action.MOVE_UP and x > 0:
            self.position = (x - 1, y)
            self.moves_made += 1
            self.cleaning_history.append(('MOVE_UP', self.position))
            return True

        elif action == Action.MOVE_DOWN and x < self.rows - 1:
            self.position = (x + 1, y)
            self.moves_made += 1
            self.cleaning_history.append(('MOVE_DOWN', self.position))
            return True

        elif action == Action.MOVE_LEFT and y > 0:
            self.position = (x, y - 1)
            self.moves_made += 1
            self.cleaning_history.append(('MOVE_LEFT', self.position))
            return True

        elif action == Action.MOVE_RIGHT and y < self.cols - 1:
            self.position = (x, y + 1)
            self.moves_made += 1
            self.cleaning_history.append(('MOVE_RIGHT', self.position))
            return True

        elif action == Action.IDLE:
            self.idle_actions += 1
            self.cleaning_history.append(('IDLE', self.position))
            return True

        return False

    def decide_action(self) -> Action:
        x, y = self.position

        if self.sense() == LocationState.DIRTY:
            return Action.SUCK

        target = self._find_target_cell()

        if target:
            tx, ty = target
            if tx < x:
                return Action.MOVE_UP
            elif tx > x:
                return Action.MOVE_DOWN
            elif ty < y:
                return Action.MOVE_LEFT
            elif ty > y:
                return Action.MOVE_RIGHT

        return self._spiral_next_move()

    def _find_target_cell(self) -> Tuple[int, int]:
        x, y = self.position
        min_distance = float('inf')
        target = None

        for i in range(self.rows):
            for j in range(self.cols):
                if self.grid[i][j] == LocationState.DIRTY:
                    distance = abs(i - x) + abs(j - y)
                    if distance < min_distance:
                        min_distance = distance
                        target = (i, j)

        if target is None:
            min_distance = float('inf')
            for i in range(self.rows):
                for j in range(self.cols):
                    if (i, j) not in self.visited:
                        distance = abs(i - x) + abs(j - y)
                        if distance < min_distance:
                            min_distance = distance
                            target = (i, j)

        return target if min_distance > 0 else None

    def _spiral_next_move(self) -> Action:
        x, y = self.position
        self.visited.add(self.position)

        if y < self.cols - 1 and (x, y + 1) not in self.visited:
            return Action.MOVE_RIGHT
        elif x < self.rows - 1 and (x + 1, y) not in self.visited:
            return Action.MOVE_DOWN
        elif y > 0 and (x, y - 1) not in self.visited:
            return Action.MOVE_LEFT
        elif x > 0 and (x - 1, y) not in self.visited:
            return Action.MOVE_UP
        else:
            return Action.IDLE

    def run(self, max_steps: int = 1000, visualize: bool = True) -> Dict:
        start_time = time.time()

        for step in range(max_steps):
            if self.current_dirt_count == 0:
                print(f"\n✓ Clean after {step + 1} steps!")
                break

            action = self.decide_action()
            self.act(action)
            self.actions_taken.append(action)
            self.visited.add(self.position)

            if visualize and step % 20 == 0:
                self.display_grid()
                time.sleep(0.1)

        elapsed_time = time.time() - start_time

        metrics = {
            'total_actions': len(self.actions_taken),
            'suck_actions': self.suck_actions,
            'move_actions': self.moves_made,
            'idle_actions': self.idle_actions,
            'total_dirt_cleaned': self.total_dirt_cleaned,
            'initial_dirt_count': self.initial_dirt_count,
            'remaining_dirt': self.current_dirt_count,
            'cleanliness_percentage': (1 - self.current_dirt_count / max(1, self.initial_dirt_count)) * 100,
            'time_taken': elapsed_time,
            'efficiency': self.total_dirt_cleaned / max(1, self.moves_made + self.suck_actions)
        }

        return metrics

    def display_grid(self):
        print(f"\nPosition: {self.position}")
        print(f"Dirt left: {self.current_dirt_count}/{self.initial_dirt_count}")
        print("+" + "---" * self.cols)

        for i in range(self.rows):
            row_str = "|"
            for j in range(self.cols):
                if self.position == (i, j):
                    row_str += " 🤖 "
                else:
                    row_str += f" {self.grid[i][j].value}  "
                row_str += "|"
            print(row_str)
            print("+" + "---" * self.cols)
        print()

    def plot_performance(self, metrics: Dict):
        fig, axes = plt.subplots(1, 2, figsize=(12, 5))

        actions = ['SUCK', 'MOVE', 'IDLE']
        counts = [metrics['suck_actions'], metrics['move_actions'], metrics['idle_actions']]
        colors = ['green', 'blue', 'gray']

        axes[0].bar(actions, counts, color=colors)
        axes[0].set_title('Actions')
        axes[0].set_ylabel('Count')

        axes[1].bar(['Initial', 'Left'],
                   [metrics['initial_dirt_count'], metrics['remaining_dirt']],
                   color=['red', 'green'])
        axes[1].set_title(f'{metrics["cleanliness_percentage"]:.1f}% Clean')

        plt.tight_layout()
        plt.show()

def run_multiple_scenarios():
    print("\n" + "="*60)
    print("VACUUM CLEANER - TESTING")
    print("="*60)

    scenarios = [
        {'name': 'Small', 'rows': 3, 'cols': 3, 'dirt': 0.5},
        {'name': 'Medium', 'rows': 5, 'cols': 5, 'dirt': 0.4},
        {'name': 'Large', 'rows': 7, 'cols': 7, 'dirt': 0.3},
    ]

    all_metrics = []

    for scenario in scenarios:
        print(f"\n📍 {scenario['name']} Room")
        print(f"   Grid: {scenario['rows']}x{scenario['cols']}, Dirt: {scenario['dirt']}")
        print("-" * 40)

        agent = VacuumCleanerAgent(
            rows=scenario['rows'],
            cols=scenario['cols'],
            dirt_probability=scenario['dirt']
        )

        print("Start:")
        agent.display_grid()

        metrics = agent.run(max_steps=500, visualize=False)
        all_metrics.append((scenario['name'], metrics))

        print(f"\nResults:")
        print(f"   Actions: {metrics['total_actions']}")
        print(f"   Cleaned: {metrics['total_dirt_cleaned']}")
        print(f"   Efficiency: {metrics['efficiency']:.2f} dirt/action")

        agent.display_grid()
        agent.plot_performance(metrics)

    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    print(f"{'Room':<10} {'Actions':<10} {'Cleaned':<10} {'Efficiency':<12}")
    print("-" * 50)
    for name, metrics in all_metrics:
        print(f"{name:<10} {metrics['total_actions']:<10} {metrics['total_dirt_cleaned']:<10} "
              f"{metrics['efficiency']:<12.2f}")

if __name__ == "__main__":
    run_multiple_scenarios()
    # print("ASSIGNMENT COMPLETED SUCCESSFULLY!")
    # print("="*60)
