from pathlib import Path
import tomllib

DEFAULT_CONFIG = """\
[general]
dry_run = true
recursive = false
ignore_hidden = true

[categories]
Images = ["jpg","jpeg","png","gif","bmp","webp"]
Videos = ["mp4","mkv","avi","mov"]
Documents = ["pdf","doc","docx","txt","xlsx","pptx"]
Music = ["mp3","wav","flac"]
Archives = ["zip","rar","7z","tar","gz"]
Others = []
"""


class ConfigManager:
    def __init__(self, config_file: Path = Path("config.toml")) -> None:
        self.config_file = config_file

    def load(self) -> dict:
        if not self.config_file.exists():
            self.create_default()

        with self.config_file.open("rb") as file:
            return tomllib.load(file)

    def create_default(self) -> None:
        self.config_file.write_text(DEFAULT_CONFIG, encoding="utf-8")

    @property
    def categories(self) -> dict[str, list[str]]:
        """Return configured categories."""

        return self.load()["categories"]