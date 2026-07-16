from dataclasses import dataclass
from pathlib import Path


@dataclass(slots=True)
class MoveRecord:
    """Represents one completed file move."""

    source: Path
    destination: Path