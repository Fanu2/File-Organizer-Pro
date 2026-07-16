from pathlib import Path

from src.models.move_record import MoveRecord


class UndoManager:

    def __init__(
        self,
        file: Path = Path("logs/undo.log"),
    ) -> None:

        self.file = file

        self.file.parent.mkdir(
            exist_ok=True
        )

    def save(
        self,
        records: list[MoveRecord],
    ) -> None:

        with self.file.open(
            "w",
            encoding="utf-8",
        ) as f:

            for record in records:

                f.write(
                    f"{record.source}|{record.destination}\n"
                )