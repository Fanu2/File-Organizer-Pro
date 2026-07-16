import shutil
from pathlib import Path

from src.models.move_record import MoveRecord
from src.models.preview_record import PreviewRecord


class Mover:
    """Moves files safely."""

    def move(
        self,
        records: list[PreviewRecord],
    ) -> tuple[list[MoveRecord], list[str]]:
        """
        Move files described by the preview records.

        Returns:
            completed_moves : list[MoveRecord]
            log_messages    : list[str]
        """

        completed_moves: list[MoveRecord] = []
        log_messages: list[str] = []

        for record in records:
            try:
                # Create destination folder if necessary
                record.destination.parent.mkdir(
                    parents=True,
                    exist_ok=True,
                )

                # Never overwrite an existing file
                if record.destination.exists():
                    log_messages.append(
                        f"Skipped (already exists): {record.destination.name}"
                    )
                    continue

                shutil.move(
                    str(record.source),
                    str(record.destination),
                )

                completed_moves.append(
                    MoveRecord(
                        source=record.source,
                        destination=record.destination,
                    )
                )

                log_messages.append(
                    f"Moved: {record.source.name}"
                )

            except Exception as exc:
                log_messages.append(
                    f"Error moving '{record.source.name}': {exc}"
                )

        return completed_moves, log_messages