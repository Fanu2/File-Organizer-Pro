import sys

from PySide6.QtWidgets import QApplication

from src.ui.main_window import MainWindow


def main() -> int:
    """Application entry point."""

    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    return app.exec()


if __name__ == "__main__":
    sys.exit(main())