from dataclasses import dataclass


@dataclass(slots=True)
class Settings:
    """Application settings."""

    dry_run: bool = True
    recursive: bool = False
    ignore_hidden: bool = True