from PySide6.QtWidgets import QMainWindow


class MainWindow(QMainWindow):
    """Main application window."""

    def __init__(self) -> None:
        super().__init__()

        self.setWindowTitle("File Organizer Pro")
        self.resize(1000, 700)