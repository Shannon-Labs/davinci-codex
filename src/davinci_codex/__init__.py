"""da Vinci Codex core package."""

from importlib.metadata import PackageNotFoundError, version

try:  # pragma: no cover - executed only in installed environment
    __version__ = version("davinci-codex")
except PackageNotFoundError:  # pragma: no cover - fallback for development
    __version__ = "0.1.0"

from . import renaissance_music

__all__ = [
    "__version__",
    "renaissance_music",
]
