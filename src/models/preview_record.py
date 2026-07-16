from dataclasses import dataclass
from pathlib import Path


@dataclass(slots=True)
class PreviewRecord:
    """Represents one planned file operation."""

    source: Path
    destination: Path
    category: str