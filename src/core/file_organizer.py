from src.core.mover import Mover
from src.core.undo_manager import UndoManager
from src.models.preview_record import PreviewRecord


class FileOrganizer:
    """Coordinates file organization."""

    def __init__(self) -> None:
        self.mover = Mover()
        self.undo_manager = UndoManager()

    def organize(
        self,
        records: list[PreviewRecord],
        dry_run: bool,
    ) -> list[str]:
        """
        Organize files.

        Returns log messages.
        """

        if dry_run:
            return self._dry_run(records)

        moved, messages = self.mover.move(records)

        if moved:
            self.undo_manager.save(moved)

        messages.append("")
        messages.append(
            f"Completed: {len(moved)} files moved."
        )

        return messages

    def _dry_run(
        self,
        records: list[PreviewRecord],
    ) -> list[str]:
        """Simulate organization."""

        messages: list[str] = []

        for record in records:
            messages.append(
                f"Would move: {record.source.name}"
            )
            messages.append(
                f"    -> {record.destination}"
            )

        messages.append("")
        messages.append(
            f"Dry Run completed ({len(records)} files)"
        )

        return messages