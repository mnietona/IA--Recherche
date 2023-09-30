from abc import ABC, abstractmethod
from typing import Tuple, Iterable, Generic, TypeVar, Set
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

        # Sauvegardons l'état courant du monde pour le restaurer plus tard
        current_state = self.world.get_state()

        # Mettons le monde à l'état que nous examinons
        self.world.set_state(state)

        # Générer toutes les combinaisons possibles d'actions pour tous les agents
        all_actions_combinations = product(*self.world.available_actions())

        visited_states = set()

        for actions in all_actions_combinations:
            if not self.world.done:
                self.world.step(actions)
                # Une fois que vous avez effectué l'action, capturez le nouvel état du monde
                new_state = self.world.get_state()
                # Ajoutez le nouvel état, l'action et le coût à vos successeurs
                if new_state not in visited_states:
                    visited_states.add(new_state)
                    yield (new_state, actions, 1.0)  # J'ai utilisé un coût fixe de 1.0, mais vous pouvez le changer selon vos besoins.
                # Restaurer le monde à l'état précédent pour tester la prochaine action
                self.world.set_state(state)

        # Restaurer l'état original du monde une fois que nous avons terminé
        self.world.set_state(current_state)
    
    def heuristic(self, state: WorldState) -> float:
        """Manhattan distance for each agent to its goal"""
        total_distance = 0
        for agent_pos in state.agents_positions:
            distances = [abs(agent_pos[0] - exit[0]) + abs(agent_pos[1] - exit[1]) for exit in self.world.exit_pos]
            total_distance += min(distances)
        return total_distance




class CornerProblemState:
    def __init__(self, position: Tuple[int, int], visited_corners: Set[Tuple[int, int]]):
        self.position = position
        self.visited_corners = visited_corners

    def __eq__(self, other):
        return isinstance(other, CornerProblemState) and self.position == other.position and self.visited_corners == other.visited_corners

    def __hash__(self):
        return hash((self.position, frozenset(self.visited_corners)))


class CornerSearchProblem(SearchProblem[CornerProblemState]):
    def __init__(self, world: World):
        super().__init__(world)
        self.corners = [(0, 0), (0, world.width - 1), (world.height - 1, 0), (world.height - 1, world.width - 1)]
        # Utilisation de agents_positions pour obtenir la position initiale de l'agent
        self.initial_state = CornerProblemState(world.agents_positions[0], set())

    def is_goal_state(self, state: CornerProblemState) -> bool:
        return len(state.visited_corners) == 4 and state.position in self.world.exit_pos

    
    def get_successors(self, state: CornerProblemState) -> Iterable[Tuple[CornerProblemState, Tuple[Action, ...], float]]:
        self.nodes_expanded += 1

        # Sauvegardons l'état courant du monde pour le restaurer plus tard
        current_state = self.world.get_state()

        # Convertissons le CornerProblemState en WorldState
        other_agents_positions = self.world.agents_positions.copy()
        other_agents_positions[0] = state.position
        gem_status = [False] * self.world.n_gems
        world_state = WorldState(other_agents_positions, gem_status)
        
        # Mettons le monde à l'état que nous examinons
        self.world.set_state(world_state)

        # Générer toutes les actions possibles pour l'agent
        available_actions_for_agent = self.world.available_actions()[0]

        visited_states = set()

        for action in available_actions_for_agent:
            # Prenez les actions pour tous les agents (supposez que les autres agents restent immobiles)
            actions_for_all_agents = (action,) + tuple([Action.STAY for _ in range(self.world.n_agents - 1)])

            if not self.world.done:
                self.world.step(actions_for_all_agents)
                
                # Une fois l'action effectuée, capturez la nouvelle position de l'agent
                new_position = self.world.agents_positions[0]
                visited_corners = state.visited_corners.copy()
                
                # Si la nouvelle position est un coin, ajoutez-la aux coins visités
                if new_position in self.corners:
                    visited_corners.add(new_position)

                # Créez un nouvel état pour ce scénario
                new_state = CornerProblemState(new_position, visited_corners)
                
                if new_state not in visited_states:
                    visited_states.add(new_state)
                    yield (new_state, actions_for_all_agents, 1.0)
                
                # Restaurer le monde à l'état précédent pour tester la prochaine action
                self.world.set_state(world_state)

        # Restaurer l'état original du monde une fois que nous avons terminé
        self.world.set_state(current_state)


        


    def heuristic(self, problem_state: CornerProblemState) -> float:
        remaining_corners = [corner for corner in self.corners if corner not in problem_state.visited_corners]
        if not remaining_corners:
            return min(self.manhattan_distance(problem_state.position, exit) for exit in self.world.exit_pos)
        return min(self.manhattan_distance(problem_state.position, corner) for corner in remaining_corners)

    def manhattan_distance(self,p1: Tuple[int, int], p2: Tuple[int, int]) -> int:
        return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])




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
