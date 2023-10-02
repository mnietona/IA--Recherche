from lle import World
from problem import SimpleSearchProblem, CornerSearchProblem, GemSearchProblem
from search import dfs, bfs, astar

from time import time
import sys

def select_problem(world, choice):
    if choice == '1':
        return SimpleSearchProblem(world)
    elif choice == '2':
        return CornerSearchProblem(world)
    elif choice == '3':
        return GemSearchProblem(world)
    else:
        print("Choix non reconnu!")
        sys.exit()

if __name__ == "__main__":
    carte = "level3"
    w = World.from_file(carte)
    
    print("Choix problème :")
    print("1 = Simple")
    print("2 = Corner")
    print("3 = Gems")
    choice = input("Entrez votre choix: ")

    

    algos = [(dfs, "dfs"), (bfs, "bfs"), (astar, "astar")]
    
    print("\033c")
    for algo, name in algos:
        problem = select_problem(w, choice)
        debut = time()
        solution = algo(problem)
        fin = time()
        
        problem_name = ""
        if choice == '1':
            problem_name = "SimpleSearchProblem"
        elif choice == '2':
            problem_name = "CornerSearchProblem"
        elif choice == '3':
            problem_name = "GemSearchProblem"
        
        if solution is None:
            print(f"{name}: No solution found")
        else:
            print("Carte : " + carte)
            print(f"Problem : {problem_name}")
            print(f"{name}: {len(solution.actions)} d'actions, {problem.nodes_expanded} nodes expanded en {fin - debut} secondes")
            print()
