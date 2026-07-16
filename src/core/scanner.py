from pathlib import Path

from src.models.scan_result import ScanResult


class Scanner:
    """Scans folders for files."""

    def scan(
        self,
        folder: Path,
        recursive: bool,
        ignore_hidden: bool,
    ) -> ScanResult:

        result = ScanResult()

        if recursive:
            iterator = folder.rglob("*")
        else:
            iterator = folder.iterdir()

        for item in iterator:

            try:

                if not item.is_file():
                    continue

                if ignore_hidden and item.name.startswith("."):
                    result.skipped.append(item)
                    continue

                result.files.append(item)

            except Exception as exc:
                result.errors.append(str(exc))

        return result