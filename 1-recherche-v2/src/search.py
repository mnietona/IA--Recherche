from dataclasses import dataclass
from typing import Optional
from lle import Action
from problem import SearchProblem

from collections import deque
from priority_queue import PriorityQueue


@dataclass
class Solution:
    actions: list[list[Action]]

    @property
    def n_steps(self) -> int:
        return len(self.actions)

    ...


def bfs(problem: SearchProblem) -> Optional[Solution]:
    start_state = problem.initial_state
    frontier = deque([start_state])
    explored = set([start_state])
    path_to = {start_state: []}

    while frontier:
        current_state = frontier.popleft()

        if problem.is_goal_state(current_state):
            return Solution(actions=path_to[current_state])

        for successor, actions, _ in problem.get_successors(current_state):
            if successor not in explored:
                explored.add(successor)
                frontier.append(successor)
                path_to[successor] = path_to[current_state] + [actions]

    return None


def dfs(problem: SearchProblem) -> Optional[Solution]:
    start_state = problem.initial_state
    frontier = [start_state]  # utilisation d'une liste comme une pile
    explored = set([start_state])
    path_to = {start_state: []}

    while frontier:
        current_state = frontier.pop()  # utilisation de pop() pour un comportement de pile

        if problem.is_goal_state(current_state):
            return Solution(actions=path_to[current_state])

        for successor, actions, _ in problem.get_successors(current_state):
            if successor not in explored:
                explored.add(successor)
                frontier.append(successor)  # on utilise append pour ajouter à la fin
                path_to[successor] = path_to[current_state] + [actions]

    return None


def astar(problem: SearchProblem) -> Optional[Solution]:
    current_state = problem.initial_state
    frontier = PriorityQueue()
    # utilisation de la valeur heuristique comme priorité initiale
    frontier.push(current_state, problem.heuristic(current_state))

    g_values = {current_state: 0}
    path_to = {current_state: []}

    explored = set()  # renommé pour uniformité

    while not frontier.isEmpty():
        current_state = frontier.pop()

        if current_state in explored:
            continue

        explored.add(current_state)

        if problem.is_goal_state(current_state):
            return Solution(actions=path_to[current_state])

        for successor, action, action_cost in problem.get_successors(current_state):
            tentative_g_value = g_values[current_state] + action_cost

            if successor not in g_values or tentative_g_value < g_values[successor]:
                g_values[successor] = tentative_g_value
                f_value = tentative_g_value + problem.heuristic(successor)
                # vérification avant d'ajouter à la frontière
                if successor not in explored:
                    frontier.update(successor, f_value)
                path_to[successor] = path_to[current_state] + [action]

    return None
