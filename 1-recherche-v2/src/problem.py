from abc import ABC, abstractmethod
from typing import Tuple, Iterable, Generic, TypeVar
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
        # Vérifier si tous les agents sont dans une position de sortie
        for agent_pos in state.agents_positions:
            if agent_pos not in self.world.exit_pos:
                return False
        return True

    def get_successors(self, state: WorldState) -> Iterable[Tuple[WorldState, Tuple[Action, ...], float]]:
        self.nodes_expanded += 1
        self.world.set_state(state)

        if self.world.done:
            return

        available_actions_per_agent = self.world.available_actions()
        visited_states = set()

        for joint_actions in product(*available_actions_per_agent):
            previous_state = self.world.get_state()
            reward = self.world.step(joint_actions)
            new_state = self.world.get_state()

            if new_state in visited_states:
                continue

            visited_states.add(new_state)
            self.world.set_state(previous_state)
            action_cost = -reward
            yield new_state, joint_actions, action_cost





    def heuristic(self, state: WorldState) -> float:
        """Manhattan distance for each agent to its goal"""
        return 0.0

class CornerProblemState:
    ...


class CornerSearchProblem(SearchProblem[CornerProblemState]):
    def __init__(self, world: World):
        super().__init__(world)
        self.corners = [(0, 0), (0, world.width - 1), (world.height - 1, 0), (world.height - 1, world.width - 1)]
        self.initial_state = ...

    def is_goal_state(self, state: CornerProblemState) -> bool:
        raise NotImplementedError()

    def heuristic(self, problem_state: CornerProblemState) -> float:
        raise NotImplementedError()

    def get_successors(self, state: CornerProblemState) -> Iterable[Tuple[CornerProblemState, Action, float]]:
        self.nodes_expanded += 1
        raise NotImplementedError()


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
