PYTHON ?= python3
VENV ?= .venv
PYTHON_BIN := $(VENV)/bin/python3
ACTIVATE = . $(VENV)/bin/activate

setup:
	$(PYTHON) -m venv $(VENV)
	$(PYTHON_BIN) -m pip install --upgrade pip
	$(PYTHON_BIN) -m pip install -r requirements.txt
	$(PYTHON_BIN) -m pip install -e .

lint:
	$(ACTIVATE) && ruff check . && mypy src

test:
	$(ACTIVATE) && pytest -q

demo:
	$(ACTIVATE) && python -m davinci_codex.cli demo

build:
	$(ACTIVATE) && python -m davinci_codex.cli build --all
