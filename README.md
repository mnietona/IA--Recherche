
# Projet d'Intelligence Artificielle - Recherche


## Introduction
Ce projet d'Intelligence Artificielle est axé sur la résolution de problèmes par des algorithmes de recherche. Il comprend plusieurs classes de problèmes, notamment la recherche dans un environnement de collecte de gemmes, la recherche de coins dans un environnement complexe, et la recherche dans un environnement de jeu de plateau. Les algorithmes de recherche implémentés sont la recherche en largeur (Breadth-First Search), la recherche en profondeur (Depth-First Search) et l'algorithme A*.

## Prérequis
- Python 3.10
- Poetry (pour l'installation des dépendances)

## Installation
1. Clonez ce dépôt sur votre machine locale.
2. Installez Poetry en suivant les instructions sur [le site officiel de Poetry](https://python-poetry.org/docs/#installation).
3. Ouvrez un terminal dans le répertoire du projet.

## Configuration de l'environnement
L'environnement de projet "Laser Learning Environment" est décrit comme suit :
- Entre 1 et 4 agents se déplacent et collectent des gemmes sur une grille.
- Des lasers de couleur bloquent le passage aux agents d'une autre couleur, mais un agent de la même couleur peut bloquer le rayon laser pour permettre à d'autres agents de passer.
- Les cases de départ sont représentées par des carrés de la couleur de l'agent qui commence (en haut, au milieu).
- Les cases de sortie sont indiquées par des cases encadrées en noir (en bas à droite).
- Le jeu est terminé quand tous les agents ont atteint la sortie.

## Structure du Projet
- `src/`: Le répertoire source contient toutes les implémentations des classes de problème et des algorithmes de recherche.
- `tests/`: Les tests unitaires pour les classes de problème et les algorithmes de recherche.
- `lle/`: Le code source de l'environnement "Laser Learning Environment".
- `main.py`: Un script pour exécuter les algorithmes de recherche sur les problèmes spécifiques.
- `res.py`: Un script pour générer des statistiques sur les performances des algorithmes.

## Utilisation
Pour exécuter le projet, ouvrez un terminal dans le répertoire du projet et utilisez les commandes suivantes :

- Pour exécuter le projet:
  ```shell
  poetry shell
  poetry install
  python3 src/main.py
  ```

- Pour exécuter les tests unitaires:
  ```shell
  pytest tests/test_simple_problem.py tests/test_bfs.py tests/test_dfs.py tests/test_astar.py tests/test_corner_search.py tests/test_gem_search.py
  ```

- Pour générer des statistiques sur les performances des algorithmes:
  ```shell
  python3 src/res.py
  ```
