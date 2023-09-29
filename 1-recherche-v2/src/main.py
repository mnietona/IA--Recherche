import cv2
from lle import World
from problem import SimpleSearchProblem, CornerSearchProblem
import search
liste_carte = ["cartes/1_agent/vide","cartes/1_agent/zigzag",
               "cartes/1_agent/impossible","cartes/2_agents/vide",
               "cartes/2_agents/zigzag","cartes/2_agents/impossible",
               "level3", "level4", "level5", "level6", "cartes/corners","cartes/gems"]

w = World.from_file(liste_carte[6])

problem = SimpleSearchProblem(w)
#problem = CornerSearchProblem(w)
solution = search.bfs(problem)
#solution = search.dfs(problem)
#solution = search.astar(problem)

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
