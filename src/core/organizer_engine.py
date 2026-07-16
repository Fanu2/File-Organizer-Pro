from pathlib import Path

from src.core.categorizer import Categorizer
from src.core.file_organizer import FileOrganizer
from src.core.scanner import Scanner
from src.models.preview_record import PreviewRecord
from src.models.scan_result import ScanResult
from src.models.settings import Settings


class OrganizerEngine:
    """Coordinates all file organization operations."""

    def __init__(self) -> None:
        """Initialize application services."""

        self.scanner = Scanner()
        self.file_organizer = FileOrganizer()

    def scan(
        self,
        folder: Path,
        settings: Settings,
    ) -> ScanResult:
        """Scan a folder and return the scan results."""

        return self.scanner.scan(
            folder=folder,
            recursive=settings.recursive,
            ignore_hidden=settings.ignore_hidden,
        )

    def preview(
        self,
        folder: Path,
        settings: Settings,
        categories: dict[str, list[str]],
    ) -> list[PreviewRecord]:
        """Generate a preview without moving files."""

        scan_result = self.scan(folder, settings)

        categorizer = Categorizer(categories)

        records: list[PreviewRecord] = []

        for file in scan_result.files:
            records.append(
                categorizer.categorize(
                    file=file,
                    root=folder,
                )
            )

        return records

    def organize(
        self,
        records: list[PreviewRecord],
        dry_run: bool,
    ) -> list[str]:
        """Organize files or perform a dry run."""

        return self.file_organizer.organize(
            records=records,
            dry_run=dry_run,
        )