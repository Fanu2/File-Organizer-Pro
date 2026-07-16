from pathlib import Path

from src.models.preview_record import PreviewRecord


class Categorizer:
    """Categorizes files according to extension."""

    def __init__(self, categories: dict[str, list[str]]) -> None:
        self._extension_map: dict[str, str] = {}

        for category, extensions in categories.items():
            for extension in extensions:
                self._extension_map[extension.lower()] = category

    def categorize(
        self,
        file: Path,
        root: Path,
    ) -> PreviewRecord:

        extension = file.suffix.lower().lstrip(".")

        category = self._extension_map.get(
            extension,
            "Others",
        )

        destination = root / category / file.name

        return PreviewRecord(
            source=file,
            destination=destination,
            category=category,
        )