from dataclasses import dataclass, field
from pathlib import Path


@dataclass(slots=True)
class ScanResult:
    """Result returned by the scanner."""

    files: list[Path] = field(default_factory=list)
    skipped: list[Path] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)

    @property
    def total_files(self) -> int:
        return len(self.files)

    @property
    def skipped_files(self) -> int:
        return len(self.skipped)