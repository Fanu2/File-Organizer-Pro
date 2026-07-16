from pathlib import Path

from src.core.categorizer import Categorizer
from src.core.scanner import Scanner
from src.models.preview_record import PreviewRecord
from src.models.scan_result import ScanResult
from src.models.settings import Settings
from src.core.file_organizer import FileOrganizer


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
        """
        Scan a folder and return the scan results.
        """

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
        """
        Generate a preview of the planned organization.

        No files are moved. A list of PreviewRecord objects is returned,
        describing what would happen during organization.
        """

        scan_result = self.scan(folder, settings)

        categorizer = Categorizer(categories)

        records: list[PreviewRecord] = []

        for file in scan_result.files:
            record = categorizer.categorize(
                file=file,
                root=folder,
            )
            records.append(record)

        return records
   
    def organize(
        self,
        records: list[PreviewRecord],
        dry_run: bool,
    ) -> list[str]:
        """
        Organize files.

        For this milestone only Dry Run is implemented.
        """

        if dry_run:
            return self.file_organizer.dry_run(records)

        return [
            "",
            "Real organization",
            "will be implemented",
            "in Version 0.6",
        ]