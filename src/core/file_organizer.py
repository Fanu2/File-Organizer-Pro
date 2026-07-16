from src.core.mover import Mover
from src.core.undo_manager import UndoManager
from src.models.preview_record import PreviewRecord


class FileOrganizer:
    """Coordinates dry-run and real file organization."""

    def __init__(self) -> None:
        """Initialize organization services."""
        self.mover = Mover()
        self.undo_manager = UndoManager()

    def organize(
        self,
        records: list[PreviewRecord],
        dry_run: bool,
    ) -> list[str]:
        """
        Organize files.

        If dry_run is True, no files are moved.
        Otherwise, files are moved safely and the undo log is created.

        Returns:
            list[str]: Messages describing the completed operation.
        """

        if dry_run:
            return self._dry_run(records)

        moved_records, messages = self.mover.move(records)

        if moved_records:
            self.undo_manager.save(moved_records)

        messages.append("")
        messages.append("-" * 50)
        messages.append(
            f"Organization completed."
        )
        messages.append(
            f"Files moved : {len(moved_records)}"
        )

        return messages

    def _dry_run(
        self,
        records: list[PreviewRecord],
    ) -> list[str]:
        """
        Simulate file organization without making any changes.
        """

        messages: list[str] = []

        messages.append("=" * 50)
        messages.append("DRY RUN")
        messages.append("=" * 50)
        messages.append("")

        for record in records:
            messages.append(
                f"Would move : {record.source.name}"
            )
            messages.append(
                f"From       : {record.source}"
            )
            messages.append(
                f"To         : {record.destination}"
            )
            messages.append("")

        messages.append("-" * 50)
        messages.append(
            f"Dry Run completed."
        )
        messages.append(
            f"Files processed : {len(records)}"
        )

        return messages