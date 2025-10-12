# =============================================================================
# da Vinci Codex - Professional Development Makefile
# =============================================================================

.PHONY: help setup clean install dev-install
.PHONY: lint format type-check security-check quality
.PHONY: test test-cov test-integration test-benchmarks test-all
.PHONY: build build-docs build-docker build-packages
.PHONY: demo simulate gallery validate
.PHONY: docker-dev docker-prod docker-test docker-clean
.PHONY: release pre-commit hooks

# =============================================================================
# Configuration
# =============================================================================

PYTHON ?= python
VENV ?= .venv
PROJECT_NAME := davinci-codex
VERSION := $(shell grep version pyproject.toml | head -1 | cut -d'"' -f2)

# Platform-specific paths
ifeq ($(OS),Windows_NT)
    PYTHON_BIN := $(VENV)/Scripts/python.exe
    ACTIVATE := $(VENV)/Scripts/activate
    PLATFORM := windows
else
    PYTHON_BIN := $(VENV)/bin/python3
    ACTIVATE := $(VENV)/bin/activate
    PLATFORM := unix
endif

# Colors for output
RED := \033[31m
GREEN := \033[32m
YELLOW := \033[33m
BLUE := \033[34m
RESET := \033[0m

# =============================================================================
# Help & Information
# =============================================================================

help: ## Show this help message
	@echo "$(BLUE)da Vinci Codex - Professional Development Tools$(RESET)"
	@echo "================================================="
	@echo ""
	@echo "$(GREEN)Setup & Installation:$(RESET)"
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## .*setup|install/ {printf "  $(BLUE)%-20s$(RESET) %s\n", $$1, $$2}' $(MAKEFILE_LIST)
	@echo ""
	@echo "$(GREEN)Code Quality:$(RESET)"
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## .*lint|format|quality|check/ {printf "  $(BLUE)%-20s$(RESET) %s\n", $$1, $$2}' $(MAKEFILE_LIST)
	@echo ""
	@echo "$(GREEN)Testing:$(RESET)"
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## .*test|benchmark/ {printf "  $(BLUE)%-20s$(RESET) %s\n", $$1, $$2}' $(MAKEFILE_LIST)
	@echo ""
	@echo "$(GREEN)Building & Deployment:$(RESET)"
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## .*build|deploy|docker|release/ {printf "  $(BLUE)%-20s$(RESET) %s\n", $$1, $$2}' $(MAKEFILE_LIST)
	@echo ""
	@echo "$(GREEN)Simulation & Demo:$(RESET)"
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## .*demo|simulate|gallery/ {printf "  $(BLUE)%-20s$(RESET) %s\n", $$1, $$2}' $(MAKEFILE_LIST)
	@echo ""

version: ## Show project version
	@echo "$(PROJECT_NAME) version $(VERSION)"

status: ## Show development environment status
	@echo "$(BLUE)Development Environment Status$(RESET)"
	@echo "=============================="
	@echo "Python: $(shell $(PYTHON) --version 2>/dev/null || echo 'Not found')"
	@echo "Virtual env: $(shell [ -d $(VENV) ] && echo 'Active ($(VENV))' || echo 'Not created')"
	@echo "Platform: $(PLATFORM)"
	@echo "Project: $(PROJECT_NAME) v$(VERSION)"

# =============================================================================
# Setup & Installation
# =============================================================================

setup: ## Setup development environment
	@echo "$(GREEN)Setting up development environment...$(RESET)"
	$(PYTHON) -m venv $(VENV)
	$(PYTHON_BIN) -m pip install --upgrade pip setuptools wheel
	$(PYTHON_BIN) -m pip install -r requirements.txt
	$(PYTHON_BIN) -m pip install -e .
	@echo "$(GREEN)✅ Development environment ready!$(RESET)"

install: setup ## Alias for setup

dev-install: setup hooks ## Full development setup with pre-commit hooks
	@echo "$(GREEN)Installing development dependencies...$(RESET)"
	$(PYTHON_BIN) -m pip install pre-commit pytest-cov pytest-xdist pytest-benchmark
	@echo "$(GREEN)✅ Development environment fully configured!$(RESET)"

clean: ## Clean up build artifacts and caches
	@echo "$(YELLOW)Cleaning up build artifacts...$(RESET)"
	rm -rf build/ dist/ *.egg-info/
	rm -rf .pytest_cache/ .coverage htmlcov/
	rm -rf .mypy_cache/ .ruff_cache/
	rm -rf docs/book/_build/
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	@echo "$(GREEN)✅ Cleanup complete!$(RESET)"

# =============================================================================
# Code Quality
# =============================================================================

lint: ## Run linting with ruff
	@echo "$(BLUE)Running Ruff linter...$(RESET)"
	$(PYTHON_BIN) -m ruff check .

format: ## Format code with ruff
	@echo "$(BLUE)Formatting code with Ruff...$(RESET)"
	$(PYTHON_BIN) -m ruff check --fix .
	$(PYTHON_BIN) -m ruff format .

type-check: ## Run type checking with mypy
	@echo "$(BLUE)Running MyPy type checker...$(RESET)"
	$(PYTHON_BIN) -m mypy src/

security-check: ## Run security checks with bandit
	@echo "$(BLUE)Running security checks...$(RESET)"
	$(PYTHON_BIN) -m pip install bandit safety > /dev/null 2>&1
	$(PYTHON_BIN) -m bandit -r src/ -f json || true
	$(PYTHON_BIN) -m safety check || true

quality: lint type-check security-check ## Run all quality checks

pre-commit-check: ## Run pre-commit checks
	@echo "$(BLUE)Running pre-commit checks...$(RESET)"
	$(PYTHON_BIN) -m pre_commit run --all-files

# =============================================================================
# Testing
# =============================================================================

test: ## Run basic test suite
	@echo "$(BLUE)Running test suite...$(RESET)"
	$(PYTHON_BIN) -m pytest -q --tb=short

test-cov: ## Run tests with coverage
	@echo "$(BLUE)Running tests with coverage...$(RESET)"
	$(PYTHON_BIN) -m pytest \
		--cov=src \
		--cov-report=xml \
		--cov-report=html \
		--cov-report=term-missing \
		--cov-fail-under=85

test-integration: ## Run integration tests
	@echo "$(BLUE)Running integration tests...$(RESET)"
	$(PYTHON_BIN) -m pytest tests/integration/ -v

test-benchmarks: ## Run performance benchmarks
	@echo "$(BLUE)Running performance benchmarks...$(RESET)"
	$(PYTHON_BIN) -m pytest tests/benchmarks/ --benchmark-only

test-all: test-cov test-integration test-benchmarks ## Run comprehensive test suite

# =============================================================================
# Building & Documentation
# =============================================================================

build: ## Build CAD models and artifacts
	@echo "$(BLUE)Building CAD models and artifacts...$(RESET)"
	$(PYTHON_BIN) -m davinci_codex.cli build --all

build-docs: ## Build documentation
	@echo "$(BLUE)Building documentation...$(RESET)"
	$(PYTHON_BIN) -m jupyter_book build docs/book

build-packages: ## Build distribution packages
	@echo "$(BLUE)Building distribution packages...$(RESET)"
	$(PYTHON_BIN) -m pip install build > /dev/null 2>&1
	$(PYTHON_BIN) -m build

build-all: build build-docs build-packages ## Build everything

# =============================================================================
# Simulation & Demo
# =============================================================================

demo: ## Run lightweight demonstration
	@echo "$(BLUE)Running da Vinci Codex demonstration...$(RESET)"
	$(PYTHON_BIN) -m davinci_codex.cli demo

simulate: ## Run simulations for specified invention
	@echo "$(BLUE)Running simulations...$(RESET)"
	@read -p "Enter invention slug (or 'all'): " slug; \
	if [ "$$slug" = "all" ]; then \
		$(PYTHON_BIN) -m davinci_codex.cli gallery; \
	else \
		$(PYTHON_BIN) -m davinci_codex.cli simulate --slug $$slug; \
	fi

gallery: ## Generate complete simulation gallery
	@echo "$(BLUE)Generating simulation gallery...$(RESET)"
	$(PYTHON_BIN) -m davinci_codex.cli gallery

validate: ## Run validation suite
	@echo "$(BLUE)Running validation suite...$(RESET)"
	$(PYTHON_BIN) -m davinci_codex.cli validate

# =============================================================================
# Docker Operations
# =============================================================================

docker-build: ## Build production Docker image
	@echo "$(BLUE)Building production Docker image...$(RESET)"
	docker build --target production -t $(PROJECT_NAME):latest .

docker-dev: ## Build and run development Docker environment
	@echo "$(BLUE)Starting development environment...$(RESET)"
	docker-compose --profile development up jupyter

docker-test: ## Run tests in Docker
	@echo "$(BLUE)Running tests in Docker...$(RESET)"
	docker-compose --profile test up test

docker-clean: ## Clean Docker images and containers
	@echo "$(YELLOW)Cleaning Docker resources...$(RESET)"
	docker-compose down --volumes --remove-orphans
	docker system prune -f

# =============================================================================
# Git Hooks & Pre-commit
# =============================================================================

hooks: ## Install pre-commit hooks
	@echo "$(BLUE)Installing pre-commit hooks...$(RESET)"
	$(PYTHON_BIN) -m pip install pre-commit > /dev/null 2>&1
	$(PYTHON_BIN) -m pre_commit install
	$(PYTHON_BIN) -m pre_commit install --hook-type commit-msg
	@echo "$(GREEN)✅ Pre-commit hooks installed!$(RESET)"

hooks-update: ## Update pre-commit hooks
	@echo "$(BLUE)Updating pre-commit hooks...$(RESET)"
	$(PYTHON_BIN) -m pre_commit autoupdate

# =============================================================================
# Release & Deployment
# =============================================================================

check-release: ## Check if ready for release
	@echo "$(BLUE)Checking release readiness...$(RESET)"
	$(PYTHON_BIN) -m pip install twine > /dev/null 2>&1
	$(PYTHON_BIN) -m build
	$(PYTHON_BIN) -m twine check dist/*
	@echo "$(GREEN)✅ Release check complete!$(RESET)"

release-test: build-packages ## Upload to test PyPI
	@echo "$(BLUE)Uploading to test PyPI...$(RESET)"
	$(PYTHON_BIN) -m twine upload --repository testpypi dist/*

release: build-packages ## Upload to PyPI
	@echo "$(BLUE)Uploading to PyPI...$(RESET)"
	$(PYTHON_BIN) -m twine upload dist/*

# =============================================================================
# Utility Functions
# =============================================================================

info: ## Display project information
	@echo "$(BLUE)Project Information$(RESET)"
	@echo "=================="
	@echo "Name: $(PROJECT_NAME)"
	@echo "Version: $(VERSION)"
	@echo "Python: $(shell $(PYTHON_BIN) --version 2>/dev/null || echo 'Not available')"
	@echo "Virtual env: $(VENV)"
	@echo "Platform: $(PLATFORM)"
	@echo ""
	@echo "$(GREEN)Available inventions:$(RESET)"
	@$(PYTHON_BIN) -m davinci_codex.cli list | head -5
	@echo "$(YELLOW)  ... (use 'make simulate' to see all)$(RESET)"

# =============================================================================
# Development Shortcuts
# =============================================================================

dev: dev-install ## Quick development environment setup
	@echo "$(GREEN)🚀 Development environment ready!$(RESET)"
	@echo "Run '$(BLUE)make demo$(RESET)' to test the installation"

fix: format lint ## Quick fix formatting and linting issues

check: quality test ## Quick quality and test check

all: clean dev-install quality test build ## Complete development cycle

# Make sure help is the default target
.DEFAULT_GOAL := help
