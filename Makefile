VENV = venv
PYTHON = $(VENV)/bin/python3
PACKAGE = mazegen-1.0.0.tar.gz  # name of the mazegen tar file
EXTRACT_DIR = mazegen-1.0.0
PIP = $(VENV)/bin/pip

.PHONY: install run lint lint-strict clean debug unpack

# unpack:
# ifeq ("$(wildcard $(EXTRACT_DIR))", "")
# 	@echo "Extracting $(PACKAGE)"
# 	tar -xzf $(PACKAGE)
# else
# 	@echo "$(EXTRACT_DIR) already exists"
# endif

install:
ifeq ("$(wildcard $(VENV))", "")
	@echo "Virtual enviroment not found. Creating $(VENV)"
	@python -m venv $(VENV)
else
	@echo "Virtual enviroment already exists"
endif
	@$(PIP) install -r requirements.txt
	@echo "Dependencies and mazegen installed"

run:
ifeq ("$(wildcard $(VENV))", "")
	@echo "No virtual enviroment detected running make install"
	@make install
endif
	@$(PYTHON) a_maze_ing.py config.txt

debug:
	@$(PYTHON) -m pdb a_maze_ing.py config.txt

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	rm -rf .mypy_cache

lint:
	python3 -m flake8 . \
		--exclude ./$(VENV)
	python3 -m mypy . \
		--warn-return-any \
		--warn-unused-ignores \
		--ignore-missing-imports \
		--disallow-untyped-defs \
		--check-untyped-defs \
		--explicit-package-bases \
		--exclude '^(venv|\.venv|env|mlx)/'

lint-strict:
	python3 -m flake8 . \
		--exclude ./$(VENV)
	python3 -m mypy . \
		--strict \
		--explicit-package-bases \
		--ignore-missing-imports \
		--exclude '^(venv|\.venv|env|mlx)/'
