from dataclasses import dataclass
from typing import Optional
from lle import Action
from problem import SearchProblem



@dataclass
class Solution:
    actions: list[list[Action]]

    @property
    def n_steps(self) -> int:
        return len(self.actions)

    ...

def bfs(problem: SearchProblem) -> Optional[Solution]:
    
    return None


def dfs(problem: SearchProblem) -> Optional[Solution]:
   
    return None



def astar(problem: SearchProblem) -> Optional[Solution]:
   
    return None
