# =============================================================================
# Multi-stage Dockerfile for da Vinci Codex
# =============================================================================

# -----------------------------------------------------------------------------
# Build Stage: Dependencies and Testing
# -----------------------------------------------------------------------------
FROM python:3.11-slim as builder

LABEL maintainer="Hunter Bown <hunter@shannon-labs.com>"
LABEL description="da Vinci Codex - Computational Archaeology Framework"
LABEL version="1.0.0"

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    curl \
    libgl1 \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgomp1 \
    libfontconfig1 \
    && rm -rf /var/lib/apt/lists/*

# Create working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt pyproject.toml ./
COPY src/ ./src/

# Install Python dependencies
RUN pip install --upgrade pip && \
    pip install -r requirements.txt && \
    pip install -e .

# Run tests during build to ensure everything works
COPY tests/ ./tests/
RUN python -m pytest tests/ -q --tb=short

# -----------------------------------------------------------------------------
# Production Stage: Minimal Runtime
# -----------------------------------------------------------------------------
FROM python:3.11-slim as production

# Copy environment variables from builder
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PATH="/app/.venv/bin:$PATH"

# Install minimal runtime dependencies
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Create non-root user for security
RUN groupadd -r davinci && useradd -r -g davinci davinci

# Set working directory
WORKDIR /app

# Copy application from builder stage
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin
COPY --from=builder /app/src /app/src

# Copy additional files
COPY . .

# Create directories and set permissions
RUN mkdir -p /app/artifacts /app/data && \
    chown -R davinci:davinci /app

# Switch to non-root user
USER davinci

# Expose port for web interface (future)
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD python -c "import davinci_codex; print('OK')" || exit 1

# Default command
CMD ["python", "-m", "davinci_codex.cli", "--help"]

# -----------------------------------------------------------------------------
# Development Stage: Full Development Environment
# -----------------------------------------------------------------------------
FROM builder as development

# Install additional development tools
RUN pip install \
    jupyter \
    jupyterlab \
    notebook \
    ipykernel \
    pre-commit \
    black \
    isort

# Copy pre-commit configuration
COPY .pre-commit-config.yaml ./

# Set up pre-commit hooks
RUN git init && pre-commit install || true

# Switch to non-root user
USER davinci

# Expose Jupyter port
EXPOSE 8888

# Default command for development
CMD ["jupyter", "lab", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--allow-root"]

# =============================================================================
# Build Instructions
# =============================================================================
# 
# Production build:
#   docker build --target production -t davinci-codex:latest .
#
# Development build:
#   docker build --target development -t davinci-codex:dev .
#
# Run production container:
#   docker run -it --rm -v $(pwd)/artifacts:/app/artifacts davinci-codex:latest
#
# Run development container:
#   docker run -it --rm -p 8888:8888 -v $(pwd):/app davinci-codex:dev
#
# =============================================================================