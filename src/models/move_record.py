from dataclasses import dataclass
from pathlib import Path


@dataclass(slots=True)
class MoveRecord:
    """Represents a successfully moved file."""

    source: Path
    destination: Path