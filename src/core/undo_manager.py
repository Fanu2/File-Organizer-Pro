from pathlib import Path
import shutil

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

    def load(self) -> list[MoveRecord]:
        """Load the previous move history."""

        records: list[MoveRecord] = []

        if not self.undo_file.exists():
            return records

        with self.undo_file.open(
            "r",
            encoding="utf-8",
        ) as file:

            for line in file:

                line = line.strip()

                if not line:
                    continue

                source, destination = line.split("|", 1)

                records.append(
                    MoveRecord(
                        source=Path(source),
                        destination=Path(destination),
                    )
                )

        return records

    def undo(self) -> list[str]:
        """Restore the previous organization."""

        messages: list[str] = []

        records = self.load()

        if not records:
            return ["Nothing to undo."]

        restored = 0

        #
        # Restore in reverse order.
        #
        for record in reversed(records):

            try:

                record.source.parent.mkdir(
                    parents=True,
                    exist_ok=True,
                )

                shutil.move(
                    str(record.destination),
                    str(record.source),
                )

                restored += 1

                messages.append(
                    f"Restored : {record.source.name}"
                )

            except Exception as exc:

                messages.append(
                    f"ERROR : {record.source.name}: {exc}"
                )

        self.clear()

        messages.append("")
        messages.append("-" * 60)
        messages.append(
            f"Undo completed ({restored} files restored)"
        )

        return messages

    def has_history(self) -> bool:
        return (
            self.undo_file.exists()
            and self.undo_file.stat().st_size > 0
        )

    def clear(self) -> None:
        if self.undo_file.exists():
            self.undo_file.unlink()