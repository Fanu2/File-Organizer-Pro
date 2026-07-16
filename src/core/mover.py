import shutil

from src.models.move_record import MoveRecord
from src.models.preview_record import PreviewRecord


class Mover:
    """Safely moves files to their destination."""

    def move(
        self,
        records: list[PreviewRecord],
    ) -> tuple[list[MoveRecord], list[str]]:
        """
        Move files described by the preview records.

        Returns:
            tuple containing:
                - list of successfully completed moves
                - list of log messages
        """

        completed_moves: list[MoveRecord] = []
        log_messages: list[str] = []

        moved_count = 0
        skipped_count = 0
        error_count = 0

        for record in records:
            try:
                # Skip if source and destination are identical.
                if record.source == record.destination:
                    skipped_count += 1
                    log_messages.append(
                        f"Skipped : {record.source.name} (already in destination)"
                    )
                    continue

                # Source must exist.
                if not record.source.exists():
                    error_count += 1
                    log_messages.append(
                        f"ERROR   : Source file not found: {record.source}"
                    )
                    continue

                # Ensure destination directory exists.
                record.destination.parent.mkdir(
                    parents=True,
                    exist_ok=True,
                )

                # Never overwrite an existing file.
                if record.destination.exists():
                    skipped_count += 1
                    log_messages.append(
                        f"Skipped : {record.destination.name} "
                        "(destination already exists)"
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

                moved_count += 1

                log_messages.append(
                    f"Moved   : {record.source.name}"
                )

            except Exception as exc:
                error_count += 1

                log_messages.append(
                    f"ERROR   : {record.source.name}"
                )
                log_messages.append(
                    f"          {exc}"
                )

        log_messages.append("")
        log_messages.append("-" * 60)
        log_messages.append(f"Moved   : {moved_count}")
        log_messages.append(f"Skipped : {skipped_count}")
        log_messages.append(f"Errors  : {error_count}")

        return completed_moves, log_messages