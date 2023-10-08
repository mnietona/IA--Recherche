import cv2
from lle import World
from problem import SimpleSearchProblem, CornerSearchProblem, GemSearchProblem
import search
from time import time

w = World.from_file("cartes/gems")

#problem = SimpleSearchProblem(w)
#problem = CornerSearchProblem(w)
problem = GemSearchProblem(w)
debut = time()
#solution = search.bfs(problem)
#solution = search.dfs(problem)
solution = search.astar(problem)
fin = time()
print(f"Temps d'exécution : {fin - debut} secondes")


if solution is None:
    print("No solution found")
    exit(0)
else:
    print(solution.n_steps)
    print(solution.actions)
    w.reset()  # Réinitialisez le monde à son état initial
    for actions in solution.actions:
        w.step(actions)
        img = w.get_image()
        cv2.imshow("Visualisation", img)
        cv2.waitKey(500)  # Attend 500 ms entre chaque étape

print(f"{problem.nodes_expanded} nodes expanded")

cv2.waitKey(0)  # Attend que l'utilisateur appuie sur 'enter'
cv2.destroyAllWindows()  # Ferme toutes les fenêtres
