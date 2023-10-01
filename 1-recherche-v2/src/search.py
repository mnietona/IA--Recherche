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
        current_state = frontier.popleft() # on prend le premier élément de la frontière
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
    path_to = {start_state: []} # stock le chemin vers un état

    while frontier:
        current_state = frontier.pop()  # prend le dernier élément
        
        if problem.is_goal_state(current_state):
            return Solution(actions=path_to[current_state])
        
        explored.add(current_state)

        for successor, actions, _ in problem.get_successors(current_state): # on parcourt les successeurs
            if successor not in explored and successor not in frontier:
                frontier.append(successor)
                path_to[successor] = path_to[current_state] + [actions]
                
    return None




def astar(problem: SearchProblem) -> Optional[Solution]:
    start_state = problem.initial_state
    frontier = PriorityQueue()  # La frontière est maintenant une file de priorité
    frontier.push(start_state, 0)  # On initialise avec un coût de 0

    path_to = {start_state: []}
    cost_so_far = {start_state: 0}

    while not frontier.isEmpty():
        current_state = frontier.pop()

        # Si l'état actuel est l'objectif, retournez la solution
        if problem.is_goal_state(current_state):
            return Solution(actions=path_to[current_state])

        for successor, actions, action_cost in problem.get_successors(current_state):
            new_cost = cost_so_far[current_state] + action_cost
            if successor not in cost_so_far or new_cost < cost_so_far[successor]:
                cost_so_far[successor] = new_cost
                priority = new_cost + problem.heuristic(successor)
                frontier.push(successor, priority)
                path_to[successor] = path_to[current_state] + [actions]

    return None 


