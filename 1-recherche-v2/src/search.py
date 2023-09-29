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
    frontier = deque([problem.initial_state])
    explored = set()
    path = {}

    while frontier:
        current_state = frontier.popleft()
        if problem.is_goal_state(current_state):
            actions = []
            while current_state in path:
                action, parent_state = path[current_state]
                actions.append(action)
                current_state = parent_state
            actions.reverse()
            return Solution(actions)

        explored.add(current_state)
        for successor, action, _ in problem.get_successors(current_state):
            if successor not in explored and successor not in frontier:
                frontier.append(successor)
                path[successor] = (action, current_state)

    return None


def dfs(problem: SearchProblem) -> Optional[Solution]:
    frontier = [problem.initial_state]
    explored = set()
    path = {}

    while frontier:
        current_state = frontier.pop()
        if problem.is_goal_state(current_state):
            actions = []
            while current_state in path:
                action, parent_state = path[current_state]
                actions.append(action)
                current_state = parent_state
            actions.reverse()
            return Solution(actions)

        explored.add(current_state)
        for successor, action, _ in problem.get_successors(current_state):
            if successor not in explored and successor not in frontier:
                frontier.append(successor)
                path[successor] = (action, current_state)

    return None



def astar(problem: SearchProblem) -> Optional[Solution]:
    """ A* search, using the Manhattan distance heuristic """
    frontier = PriorityQueue()
    frontier.push(problem.initial_state, 0)
    
    path = {}
    cost_so_far = {problem.initial_state: 0}
    
    while not frontier.isEmpty():
        current_state = frontier.pop()
        
        if problem.is_goal_state(current_state):
            actions = []
            while current_state in path:
                action, parent_state = path[current_state]
                actions.append(action)
                current_state = parent_state
            actions.reverse()
            return Solution(actions)
        
        for successor, action, cost in problem.get_successors(current_state):
            new_cost = cost_so_far[current_state] + cost
            if successor not in cost_so_far or new_cost < cost_so_far[successor]:
                cost_so_far[successor] = new_cost
                priority = new_cost + problem.heuristic(successor)
                frontier.push(successor, priority)
                path[successor] = (action, current_state)
    
    return None
