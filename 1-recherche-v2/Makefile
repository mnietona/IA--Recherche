.PHONY: main t

main:
	python3 src/main.py

t:
	pytest tests/test_simple_problem.py tests/test_bfs.py tests/test_dfs.py tests/test_astar.py tests/test_corner_search.py tests/test_gem_search.py 
res:
	python3 src/res.py
clean:
	find . -name "__pycache__" -exec rm -rf {} \;