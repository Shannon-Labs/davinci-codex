"""Project-wide pytest fixtures."""

from __future__ import annotations

import pytest

try:  # pragma: no cover - exercised implicitly when plugin is available
    import pytest_benchmark.plugin  # type: ignore  # noqa: F401
except ImportError:
    @pytest.fixture
    def benchmark():
        """Fallback benchmark fixture emulating pytest-benchmark when plugin is absent."""

        def _benchmark(func, *args, **kwargs):
            return func(*args, **kwargs)

        return _benchmark
