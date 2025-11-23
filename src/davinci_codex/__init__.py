"""da Vinci Codex core package."""

from importlib.metadata import PackageNotFoundError, version

try:  # pragma: no cover - executed only in installed environment
    __version__ = version("davinci-codex")
except PackageNotFoundError:  # pragma: no cover - fallback for development
    __version__ = "0.1.0"

_REN_MUSIC = None

__all__ = [
    "__version__",
    "renaissance_music",
]


def __getattr__(name):  # pragma: no cover - lazy import to avoid cycles
    global _REN_MUSIC
    if name == "renaissance_music":
        if _REN_MUSIC is None:
            from . import renaissance_music as _rm

            _REN_MUSIC = _rm
        return _REN_MUSIC
    raise AttributeError(name)
