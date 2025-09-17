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
	@if [ -d "$(VENV)/bin" ]; then . "$(VENV)/bin/activate"; fi; ruff check . && mypy src

test:
	@if [ -d "$(VENV)/bin" ]; then . "$(VENV)/bin/activate"; fi; pytest -q

demo:
	@if [ -d "$(VENV)/bin" ]; then . "$(VENV)/bin/activate"; fi; python -m davinci_codex.cli demo

build:
	@if [ -d "$(VENV)/bin" ]; then . "$(VENV)/bin/activate"; fi; python -m davinci_codex.cli build --all

book:
	@if [ -d "$(VENV)/bin" ]; then . "$(VENV)/bin/activate"; fi; jupyter-book build docs/book
