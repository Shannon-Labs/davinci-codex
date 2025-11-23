"""Performance benchmarks for simulation engine."""

import os
import time

import pytest

try:  # pragma: no cover - optional dependency
    import psutil  # type: ignore
except ImportError:  # pragma: no cover - fallback for CI environments without psutil
    psutil = None

from davinci_codex.registry import get_invention, list_inventions


@pytest.fixture(autouse=True)
def _enable_fast_mode(monkeypatch):
    monkeypatch.setenv("DAVINCI_FAST_SIM", "1")
    yield


class TestSimulationPerformance:
    """Benchmark simulation performance across all inventions."""

    @pytest.fixture(scope="class")
    def all_inventions(self):
        """Get all available inventions for testing."""
        return list_inventions()

    def test_invention_loading_performance(self, benchmark, all_inventions):
        """Benchmark invention module loading times."""

        def load_all_inventions():
            loaded = []
            for spec in all_inventions:
                invention = get_invention(spec.slug)
                loaded.append(invention)
            return loaded

        result = benchmark(load_all_inventions)
        assert len(result) > 0

    @pytest.mark.parametrize("invention_slug", [
        "ornithopter", "parachute", "aerial_screw",
        "self_propelled_cart", "mechanical_odometer"
    ])
    def test_simulation_execution_performance(self, benchmark, invention_slug):
        """Benchmark individual simulation execution times."""

        invention = get_invention(invention_slug)

        def run_simulation():
            return invention.module.simulate(seed=42)

        result = benchmark(run_simulation)

        # Verify simulation produces valid results
        assert isinstance(result, dict)
        assert "status" in result or "performance" in result

    def test_bulk_simulation_performance(self, benchmark, all_inventions):
        """Benchmark running all simulations in sequence."""

        def run_all_simulations():
            results = {}
            for spec in all_inventions:
                start_time = time.perf_counter()
                result = spec.module.simulate(seed=42)
                execution_time = time.perf_counter() - start_time

                results[spec.slug] = {
                    "result": result,
                    "execution_time": execution_time
                }
            return results

        results = benchmark(run_all_simulations)

        # Verify all simulations completed
        assert len(results) == len(all_inventions)

        # Check for performance regressions
        for slug, data in results.items():
            execution_time = data["execution_time"]
            # Set reasonable performance expectations
            if slug in ["ornithopter", "parachute"]:
                assert execution_time < 5.0, f"{slug} simulation took too long: {execution_time}s"
            else:
                assert execution_time < 2.0, f"{slug} simulation took too long: {execution_time}s"

    def test_memory_usage_during_simulation(self, all_inventions):
        """Test memory usage during simulation execution."""
        if psutil is None:
            pytest.skip("psutil not available")

        process = psutil.Process(os.getpid())
        initial_memory = process.memory_info().rss / 1024 / 1024  # MB

        # Run simulations and track memory usage
        peak_memory = initial_memory
        for spec in all_inventions:
            spec.module.simulate(seed=42)
            current_memory = process.memory_info().rss / 1024 / 1024  # MB
            peak_memory = max(peak_memory, current_memory)

        memory_increase = peak_memory - initial_memory

        # Ensure memory usage is reasonable (adjust threshold as needed)
        assert memory_increase < 500, f"Memory usage increased by {memory_increase:.1f}MB"

    @pytest.mark.parametrize("seed", [0, 42, 12345])
    def test_simulation_reproducibility(self, seed):
        """Test that simulations produce consistent results with same seed."""

        invention = get_invention("ornithopter")  # Use most complex simulation

        # Run simulation multiple times with same seed
        results = []
        for _ in range(3):
            result = invention.module.simulate(seed=seed)
            results.append(result)

        # Verify all results are identical
        first_result = results[0]
        for result in results[1:]:
            assert result == first_result, "Simulation results not reproducible"

    def test_concurrent_simulation_performance(self, benchmark):
        """Test performance of concurrent simulations."""
        import concurrent.futures

        def run_concurrent_simulations():
            with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
                futures = []

                # Submit multiple simulation tasks
                inventions = ["ornithopter", "parachute", "aerial_screw", "mechanical_odometer"]
                for i, slug in enumerate(inventions):
                    invention = get_invention(slug)
                    future = executor.submit(invention.module.simulate, seed=i)
                    futures.append(future)

                # Wait for all to complete
                results = []
                for future in concurrent.futures.as_completed(futures):
                    results.append(future.result())

                return results

        results = benchmark(run_concurrent_simulations)
        assert len(results) == 4
