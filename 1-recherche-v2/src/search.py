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


def bfs(problem: SearchProblem) -> Optional[Solution]:
    """ Recherche en largeur (Breadth-First Search) """
    
    start_state = problem.initial_state
    frontier = deque([start_state]) 
    explored = set([start_state]) 
    path_to = {start_state: []} # Dictionnaire pour mémoriser le chemin vers chaque état

    while frontier:
        current_state = frontier.popleft() # On récupère le premier état de la file

        if problem.is_goal_state(current_state):
            return Solution(actions=path_to[current_state])

        for successor, actions, _ in problem.get_successors(current_state):
            if successor not in explored:
                explored.add(successor)
                frontier.append(successor)
                path_to[successor] = path_to[current_state] + [actions]

    return None


def dfs(problem: SearchProblem) -> Optional[Solution]:
    """ Recherche en profondeur (Depth-First Search) """
    
    start_state = problem.initial_state
    frontier = [start_state] 
    explored = set([start_state])
    path_to = {start_state: []} # Dictionnaire pour mémoriser le chemin vers chaque état

    while frontier:
        current_state = frontier.pop() # On utilise pop() pour prendre le dernier élément de la liste

        if problem.is_goal_state(current_state):
            return Solution(actions=path_to[current_state])

        for successor, actions, _ in problem.get_successors(current_state):
            if successor not in explored:
                explored.add(successor)
                frontier.append(successor) 
                path_to[successor] = path_to[current_state] + [actions]

    return None


def astar(problem: SearchProblem) -> Optional[Solution]:
    """ Recherche A* """
    
    current_state = problem.initial_state
    frontier = PriorityQueue()
    frontier.push(current_state, problem.heuristic(current_state)) # On ajoute l'état initial à la file
    g_values = {current_state: 0} # g(n)
    path_to = {current_state: []} # Dictionnaire pour mémoriser le chemin vers chaque état
    explored = set()  

    while not frontier.isEmpty():
        current_state = frontier.pop()

        if current_state in explored: continue

        explored.add(current_state) 

        if problem.is_goal_state(current_state):
            return Solution(actions=path_to[current_state])

        for successor, action, action_cost in problem.get_successors(current_state):
            tentative_g_value = g_values[current_state] + action_cost # On calcule le coût du chemin jusqu'à l'état successeur

            if successor not in g_values or tentative_g_value < g_values[successor]:
                g_values[successor] = tentative_g_value # On met à jour le coût du chemin jusqu'à l'état successeur
                f_value = tentative_g_value + problem.heuristic(successor) # On calcule la valeur de f(n) = g(n) + h(n)
                if successor not in explored:
                    frontier.update(successor, f_value)
                path_to[successor] = path_to[current_state] + [action]

    return None
