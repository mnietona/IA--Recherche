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
    frontier_set = {start_state} # pour tester si un état est dans la frontière
    explored = set() # pour tester si un état a déjà été exploré
    path_to = {start_state: []}

    while frontier:
        current_state = frontier.popleft()
        frontier_set.remove(current_state) # on enlève l'état de la frontière
        
        if problem.is_goal_state(current_state):
            return Solution(actions=path_to[current_state])
        
        explored.add(current_state)

        for successor, actions, _ in problem.get_successors(current_state):
            if successor not in explored and successor not in frontier_set:
                frontier.append(successor) # on ajoute l'état à la frontière
                frontier_set.add(successor) # on ajoute l'état à la frontière
                path_to[successor] = path_to[current_state] + [actions]
    return None


def dfs(problem: SearchProblem) -> Optional[Solution]:
    start_state = problem.initial_state
    frontier = [start_state]
    explored = set()
    path_to = {start_state: []}

    while frontier:
        current_state = frontier.pop()  # Différence majeure ici: nous prenons le dernier élément
        
        if problem.is_goal_state(current_state):
            return Solution(actions=path_to[current_state])
        
        explored.add(current_state)

        for successor, actions, _ in problem.get_successors(current_state):
            if successor not in explored and successor not in frontier:
                frontier.append(successor)
                path_to[successor] = path_to[current_state] + [actions]
                
    return None



import heapq

def astar(problem: SearchProblem) -> Optional[Solution]:
    
    return None
