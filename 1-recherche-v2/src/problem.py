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






    # def heuristic(self, state: WorldState) -> float:
    #     """Manhattan distance for each agent to its goal"""
    
    #     pos_agents = state.agents_positions
    #     pos_goals = self.world.exit_pos.copy()  # Copie pour ne pas modifier la liste originale
        
    #     total_distance = 0
        
    #     for agent_position in pos_agents:
    #         # Calcule la distance de Manhattan à toutes les sorties pour cet agent
    #         distances = [abs(x1 - x2) + abs(y1 - y2) for x1, y1 in [agent_position] for x2, y2 in pos_goals]
            
    #         # Trouve la sortie la plus proche et ajouter sa distance à la distance totale
    #         nearest_exit_distance = min(distances)
    #         total_distance += nearest_exit_distance
            
    #         # Enleve cette sortie de la liste pour qu'elle ne soit pas considérée pour les autres agents
    #         nearest_exit_index = distances.index(nearest_exit_distance)
    #         del pos_goals[nearest_exit_index]

    #     return total_distance
    
    def heuristic(self, state: WorldState) -> float:
        """Manhattan distance for each agent to its goal"""
        total_distance = 0
        for agent_pos in state.agents_positions:
            distances = [abs(agent_pos[0] - exit[0]) + abs(agent_pos[1] - exit[1]) for exit in self.world.exit_pos]
            total_distance += min(distances)
        return total_distance




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
