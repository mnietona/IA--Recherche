import cv2
from lle import World
from problem import SimpleSearchProblem, CornerSearchProblem, GemSearchProblem
import search
import argparse
from time import time

# Définition des problèmes disponibles
PROBLEMS = {
    "simple": SimpleSearchProblem,
    "corner": CornerSearchProblem,
    "gem": GemSearchProblem,
}

# Définition des algorithmes de recherche disponibles
ALGORITHMS = {
    "bfs": search.bfs,
    "dfs": search.dfs,
    "astar": search.astar,
}

# Configuration de l'analyseur d'arguments en ligne de commande
parser = argparse.ArgumentParser(description="AI Search Project")
parser.add_argument("problem", choices=PROBLEMS.keys(), help="Choose a problem: simple, corner, or gem")
parser.add_argument("algorithm", choices=ALGORITHMS.keys(), help="Choose an algorithm: bfs, dfs, or astar")

args = parser.parse_args()

# Charger le monde à partir d'un fichier (ajuster le chemin du fichier au besoin)
w = World.from_file("cartes/gems")

# Sélectionner le problème et l'algorithme en fonction des arguments
problem_class = PROBLEMS[args.problem]
algorithm = ALGORITHMS[args.algorithm]

problem = problem_class(w)

# Exécuter la recherche sans limite de temps
debut = time()
solution = algorithm(problem)
fin = time()

if solution is None:
    print("No solution found")
    exit(0)
else:
    print(f"Solution found in {fin - debut} seconds")
    print(f"Number of steps: {solution.n_steps}")
    print(f"{problem.nodes_expanded} nodes expanded")
    
    # Réinitialiser le monde
    w.reset()
    
    for actions in solution.actions:
        w.step(actions)
        img = w.get_image()
        cv2.imshow("Visualization", img)
        # Attendre que l'utilisateur appuie sur une touche pour passer à l'étape suivante
        key = cv2.waitKey(500)
# attend 1 sec et femre la fenetre
cv2.waitKey(1000)
cv2.destroyAllWindows()

