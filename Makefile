VENV_NAME = venv
PYTHON = ${VENV_NAME}/bin/python3


install:
	pip install -r requirements.txt

run:
	python3 a_maze_ing.py config.txt

debug:
	python3 -m pdb a_maze_ing.py config.txt

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	rm -rf .mypy_cache

lint:
	flake8 --exclude=./venv,mlx .
	${PYTHON} -m mypy . \
		--warn-return-any \
		--warn-unused-ignores \
		--ignore-missing-imports \
		--disallow-untyped-defs \
		--check-untyped-defs \
		--explicit-package-bases \
		--exclude '^(venv|\.venv|env|mlx)/'

lint-strict:
	flake8 --exclude=./venv,mlx .
	${PYTHON} -m mypy . \
		--strict \
		--explicit-package-bases \
		--exclude '^(venv|\.venv|env|mlx)/'
