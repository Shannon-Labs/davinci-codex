PYTHON ?= python
VENV ?= .venv

ifeq ($(OS),Windows_NT)
PYTHON_BIN := $(VENV)/Scripts/python.exe
ACTIVATE := $(VENV)/Scripts/activate
else
PYTHON_BIN := $(VENV)/bin/python3
ACTIVATE := $(VENV)/bin/activate
endif

setup:
	$(PYTHON) -m venv $(VENV)
	$(PYTHON_BIN) -m pip install --upgrade pip
	$(PYTHON_BIN) -m pip install -r requirements.txt
	$(PYTHON_BIN) -m pip install -e .

lint:
	$(PYTHON_BIN) -m ruff check .
	$(PYTHON_BIN) -m mypy src

test:
	$(PYTHON_BIN) -m pytest -q

demo:
	$(PYTHON_BIN) -m davinci_codex.cli demo

build:
	$(PYTHON_BIN) -m davinci_codex.cli build --all

book:
	$(PYTHON_BIN) -m jupyter_book build docs/book
