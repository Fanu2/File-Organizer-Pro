from pathlib import Path

from src.models.move_record import MoveRecord


class UndoManager:
    """Manages undo information for the most recent organization."""

    def __init__(
        self,
        undo_file: Path = Path("logs/undo.log"),
    ) -> None:
        self.undo_file = undo_file

        self.undo_file.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

    def save(
        self,
        records: list[MoveRecord],
    ) -> None:
        """Save move history."""

        with self.undo_file.open(
            "w",
            encoding="utf-8",
        ) as file:

            for record in records:
                file.write(
                    f"{record.source}|{record.destination}\n"
                )

    def has_history(self) -> bool:
        """Return True if undo information exists."""

        return (
            self.undo_file.exists()
            and self.undo_file.stat().st_size > 0
        )

    def clear(self) -> None:
        """Remove undo history."""

        if self.undo_file.exists():
            self.undo_file.unlink()