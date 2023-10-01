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
        current_state = self.world.get_state()
        self.world.set_state(state)
        all_actions_combinations = product(*self.world.available_actions())

        for actions in all_actions_combinations:
            if not self.world.done:
                self.world.step(actions)
                new_state = self.world.get_state()
                yield (new_state, actions, 1.0)  
                self.world.set_state(state)

        self.world.set_state(current_state)

    
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

    def get_new_state(self, new_world_state, corners):
        new_positions = new_world_state.agents_positions
        visited_corners = self.visited_corners.copy()
        for position in new_positions:
            if position in corners:
                visited_corners.add(position)
        return CornerProblemState(new_world_state, new_positions, visited_corners)

    def __eq__(self, other):
        return isinstance(other, CornerProblemState) and self.world_state == other.world_state and self.positions == other.positions and self.visited_corners == other.visited_corners

    def __hash__(self):
        return hash((self.world_state, tuple(self.positions), frozenset(self.visited_corners)))


class CornerSearchProblem(SearchProblem[CornerProblemState]):
    def __init__(self, world: World):
        super().__init__(world)
        self.corners = [(0, 0), (0, world.width - 1), (world.height - 1, 0), (world.height - 1, world.width - 1)]
        self.initial_state = CornerProblemState(world.get_state(), world.agents_positions, set())

    def is_goal_state(self, state: CornerProblemState) -> bool:
        # Vérifier que chaque agent est dans une sortie
        all_in_exit = all(pos in self.world.exit_pos for pos in state.positions)
        return len(state.visited_corners) == 4 and all_in_exit

    # Le reste du code est similaire
    def get_successors(self, state: CornerProblemState) -> Iterable[Tuple[CornerProblemState, Action, float]]:
        self.world.set_state(state.world_state)
        
        if self.world.done:
            return []
        
        all_actions_combinations = product(*self.world.available_actions())
        
        for actions in all_actions_combinations:
            self.world.set_state(state.world_state)
            
            cost = self.world.step(actions)  
            new_state = self.world.get_state()
            
            yield (state.get_new_state(new_state, self.corners), actions, cost)
        self.nodes_expanded += 1


    def heuristic(self, problem_state: CornerProblemState) -> float:
        # Etape 1 : Trouver la distance minimale de l'agent actuel à chaque coin non visité
        remaining_corners = [corner for corner in self.corners if corner not in problem_state.visited_corners]
        if not remaining_corners:
            return min(self.manhattan_distance(problem_state.positions[0], exit) for exit in self.world.exit_pos)
        
        min_distances_from_agent = [self.manhattan_distance(problem_state.positions[0], corner) for corner in remaining_corners]

        # Etape 2 : Estimation de la distance pour visiter tous les coins restants (approximation du TSP)
        distances_between_corners = {}
        for i, corner1 in enumerate(remaining_corners):
            for j, corner2 in enumerate(remaining_corners):
                if i != j:
                    distances_between_corners[(corner1, corner2)] = self.manhattan_distance(corner1, corner2)

        # Pour simplifier, prenons la distance minimale parmi les coins restants comme approximation
        approximated_tsp_distance = sum(sorted(distances_between_corners.values())[:len(remaining_corners)-1])
        
        # Etape 3 : Calculer la distance du dernier coin à la sortie la plus proche
        distances_to_exit = [min(self.manhattan_distance(corner, exit) for exit in self.world.exit_pos) for corner in remaining_corners]
        min_distance_to_exit = min(distances_to_exit)

        # Etape 4 : Somme de toutes les distances
        return min(min_distances_from_agent) + approximated_tsp_distance + min_distance_to_exit


        
    def manhattan_distance(self, pos1, pos2):
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])




class GemProblemState:
    ...


class GemSearchProblem(SearchProblem[GemProblemState]):
    def __init__(self, world: World):
        super().__init__(world)
        self.initial_state = ...

    def is_goal_state(self, state: GemProblemState) -> bool:
        raise NotImplementedError()

    def heuristic(self, state: GemProblemState) -> float:
        """The number of uncollected gems"""
        raise NotImplementedError()

    def get_successors(self, state: GemProblemState) -> Iterable[Tuple[GemProblemState, Action, float]]:
        self.nodes_expanded += 1
        raise NotImplementedError()
