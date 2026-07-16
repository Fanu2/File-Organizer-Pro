import sys

from PySide6.QtWidgets import QApplication

from src.core.config_manager import ConfigManager
from src.ui.main_window import MainWindow


def main() -> int:
    """Application entry point."""

    app = QApplication(sys.argv)

    # Ensure config.toml exists
    config = ConfigManager()
    config.load()

    window = MainWindow()
    window.show()

    return app.exec()


if __name__ == "__main__":
    sys.exit(main())