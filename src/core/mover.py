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

        completed: list[MoveRecord] = []
        messages: list[str] = []

        for record in records:

            try:

                record.destination.parent.mkdir(
                    parents=True,
                    exist_ok=True,
                )

                if record.destination.exists():

                    messages.append(
                        f"Skipped (exists): {record.destination}"
                    )

                    continue

                shutil.move(
                    str(record.source),
                    str(record.destination),
                )

                completed.append(
                    MoveRecord(
                        source=record.source,
                        destination=record.destination,
                    )
                )

                messages.append(
                    f"Moved: {record.source.name}"
                )

            except Exception as exc:

                messages.append(
                    f"ERROR: {record.source.name}: {exc}"
                )

        return completed, messages