"""Namespace package exposing project modules for compatibility with tests."""

from importlib import import_module

__all__ = ["davinci_codex"]


def __getattr__(name):  # pragma: no cover - thin namespace shim
    if name == "davinci_codex":
        module = import_module("davinci_codex")
        globals()[name] = module
        return module
    raise AttributeError(name)
