from src.models.preview_record import PreviewRecord


class FileOrganizer:
    """Simulates or performs file organization."""

    def dry_run(
        self,
        records: list[PreviewRecord],
    ) -> list[str]:
        """
        Simulate file organization.

        Returns a list of log messages.
        """

        messages: list[str] = []

        for record in records:
            messages.append(
                f"Would move:\n"
                f"{record.source}\n"
                f"    -> {record.destination}"
            )

        messages.append("")
        messages.append(
            f"Dry run completed ({len(records)} files)."
        )

        return messages