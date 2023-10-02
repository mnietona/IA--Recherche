from abc import ABC, abstractmethod
from typing import Tuple, Iterable, Generic, TypeVar, Set, List
from lle import World, Action, WorldState
from itertools import product


T = TypeVar("T")


class SearchProblem(ABC, Generic[T]):
    """
    A Search Problem is a problem that can be solved by a search algorithm.

    The generic parameter T is the type of the problem state, which must inherit from WorldState.
    """

    def __init__(self, world: World):
        self.world = world
        world.reset()
        self.initial_state = world.get_state()
        self.nodes_expanded = 0

    @abstractmethod
    def is_goal_state(self, problem_state: T) -> bool:
        """Whether the given state is the goal state"""

    @abstractmethod
    def get_successors(self, state: T) -> Iterable[Tuple[T, Tuple[Action, ...], float]]:
        """
        Yield all possible states that can be reached from the given world state.
        Returns
            - the new problem state
            - the joint action that was taken to reach it
            - the cost of taking the action
        """

    def heuristic(self, problem_state: T) -> float:
        return 0.0

class SimpleSearchProblem(SearchProblem[WorldState]):

    def is_goal_state(self, state: WorldState) -> bool:
        return all(agent_pos in self.world.exit_pos for agent_pos in state.agents_positions)


    def get_successors(self, state: WorldState) -> Iterable[Tuple[WorldState, Tuple[Action, ...], float]]:
        self.nodes_expanded += 1
        self.world.set_state(state)
        
        if self.world.done:
            return []
        
        all_actions_combinations = product(*self.world.available_actions())

        for actions in all_actions_combinations:
           
            self.world.step(actions)
            new_state = self.world.get_state()
            self.world.set_state(state)
            cost = 1.0
            
            yield (new_state, actions, cost)  
        
    
    def heuristic(self, state: WorldState) -> float:
        """Manhattan distance for each agent to its goal"""
        total_distance = 0
        for agent_pos in state.agents_positions:
            distances = [abs(agent_pos[0] - exit[0]) + abs(agent_pos[1] - exit[1]) for exit in self.world.exit_pos]
            total_distance += min(distances)
        return total_distance


class CornerProblemState:
    def __init__(self, world_state, positions: List[Tuple[int, int]], visited_corners: Set[Tuple[int, int]]):
        self.world_state = world_state
        self.positions = positions  # Liste des positions des agents
        self.visited_corners = visited_corners

    
    def __eq__(self, other):
        return isinstance(other, CornerProblemState) and self.world_state == other.world_state and self.positions == other.positions and self.visited_corners == other.visited_corners

    def __hash__(self):
        return hash((self.world_state, tuple(self.positions), frozenset(self.visited_corners)))

    def get_new_state(self, new_world_state, corners):
        new_positions = new_world_state.agents_positions
        visited_corners = self.visited_corners.copy()
        for position in new_positions:
            if position in corners:
                visited_corners.add(position)
        return CornerProblemState(new_world_state, new_positions, visited_corners)



class CornerSearchProblem(SearchProblem[CornerProblemState]):
    def __init__(self, world: World):
        super().__init__(world)
        self.corners = [(0, 0), (0, world.width - 1), (world.height - 1, 0), (world.height - 1, world.width - 1)]
        self.initial_state = CornerProblemState(world.get_state(), world.agents_positions, set())

    def is_goal_state(self, state: CornerProblemState) -> bool:
        all_in_exit = all(pos in self.world.exit_pos for pos in state.positions)
        return len(state.visited_corners) == len(self.corners) and all_in_exit

    def get_successors(self, state: CornerProblemState) -> Iterable[Tuple[CornerProblemState, Action, float]]:
        self.nodes_expanded += 1
        self.world.set_state(state.world_state)
        
        if self.world.done:
            return []

        all_actions_combinations = product(*self.world.available_actions())
        for actions in all_actions_combinations:
            self.world.set_state(state.world_state)
            cost = self.world.step(actions)  + 1.0
            new_state = self.world.get_state()
            
            yield (state.get_new_state(new_state, self.corners), actions, cost)


    def manhattan_distance(self,p1, p2):
        """Retourne la distance de Manhattan entre deux points."""
        return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

    def heuristic(self, problem_state: CornerProblemState) -> float:
        unvisited_corners = set(self.corners) - problem_state.visited_corners
        if not unvisited_corners:
            return 0
        
        max_distance = -float('inf')
        for agent_position in problem_state.positions:
            distances = [self.manhattan_distance(agent_position, corner) for corner in unvisited_corners]
            if distances:
                max_distance = max(max_distance, max(distances))
        return max_distance




class GemProblemState:
    def __init__(self, world_state: WorldState, gems_collected: int):
        self.world_state = world_state
        self.gems_collected = gems_collected

    def __eq__(self, other):
        return isinstance(other, GemProblemState) and self.world_state == other.world_state and self.gems_collected == other.gems_collected

    def __hash__(self):
        return hash((self.world_state, self.gems_collected))


class GemSearchProblem(SearchProblem[GemProblemState]):
    def __init__(self, world: World):
        super().__init__(world)
        initial_world_state = world.get_state()
        self.initial_state = GemProblemState(initial_world_state, world.gems_collected)

    def is_goal_state(self, state: GemProblemState) -> bool:
        # Le but est atteint lorsque toutes les gemmes sont collectées
        # et que tous les agents sont sur la case exit.
        all_gems_collected = state.gems_collected == self.world.n_gems
        all_agents_on_exit = all(agent_pos in self.world.exit_pos for agent_pos in state.world_state.agents_positions)
        return all_gems_collected and all_agents_on_exit

    def heuristic(self, state: GemProblemState) -> float:
        # Le nombre de gemmes non collectées
        return self.world.n_gems - state.gems_collected

    def get_successors(self, state: GemProblemState) -> Iterable[Tuple[GemProblemState, Action, float]]:
        self.nodes_expanded += 1
        self.world.set_state(state.world_state)
        
        if self.world.done:
            return []

        all_actions_combinations = product(*self.world.available_actions())
        for actions in all_actions_combinations:
            self.world.set_state(state.world_state)  # Restauration de l'état précédent
            cost = self.world.step(actions)  # Coût d'effectuer ces actions
            new_world_state = self.world.get_state()
            new_state = GemProblemState(new_world_state, self.world.gems_collected)
            
            yield (new_state, actions, cost)
