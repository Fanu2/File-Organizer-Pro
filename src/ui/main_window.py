from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QCheckBox,
    QGridLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QPlainTextEdit,
    QStatusBar,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)


class MainWindow(QMainWindow):
    """Main application window."""

    def __init__(self) -> None:
        super().__init__()

        self.setWindowTitle("File Organizer Pro")
        self.resize(1000, 700)

        self._create_widgets()
        self._create_layout()
        self._create_status_bar()
        self._connect_signals()

    def _create_widgets(self) -> None:
        self.folder_label = QLabel("Folder")

        self.folder_edit = QLineEdit()
        self.folder_edit.setReadOnly(True)
        self.folder_edit.setPlaceholderText("Select a folder...")

        self.browse_button = QPushButton("Browse")

        self.dry_run_checkbox = QCheckBox("Dry Run")
        self.dry_run_checkbox.setChecked(True)

        self.recursive_checkbox = QCheckBox("Include Subfolders")

        self.hidden_checkbox = QCheckBox("Ignore Hidden Files")
        self.hidden_checkbox.setChecked(True)

        self.preview_table = QTableWidget(0, 3)
        self.preview_table.setHorizontalHeaderLabels(
            ["File", "Category", "Destination"]
        )
        self.preview_table.verticalHeader().setVisible(False)
        self.preview_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.preview_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.preview_table.setSelectionMode(QTableWidget.SingleSelection)
        self.preview_table.horizontalHeader().setStretchLastSection(True)

        self.activity_log = QPlainTextEdit()
        self.activity_log.setReadOnly(True)
        self.activity_log.setPlainText("Ready...")

        self.files_scanned_label = QLabel("Files Scanned : 0")
        self.files_to_move_label = QLabel("Files To Move : 0")
        self.skipped_label = QLabel("Skipped : 0")

        self.scan_button = QPushButton("Scan")
        self.scan_button.setEnabled(False)

        self.organize_button = QPushButton("Organize")
        self.organize_button.setEnabled(False)

        self.undo_button = QPushButton("Undo")
        self.undo_button.setEnabled(False)

        self.exit_button = QPushButton("Exit")

    def _create_layout(self) -> None:
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)

        folder_layout = QGridLayout()
        folder_layout.addWidget(self.folder_label, 0, 0)
        folder_layout.addWidget(self.folder_edit, 0, 1)
        folder_layout.addWidget(self.browse_button, 0, 2)

        options_layout = QHBoxLayout()
        options_layout.addWidget(self.dry_run_checkbox)
        options_layout.addWidget(self.recursive_checkbox)
        options_layout.addWidget(self.hidden_checkbox)
        options_layout.addStretch()

        preview_group = QGroupBox("Preview")
        preview_layout = QVBoxLayout(preview_group)
        preview_layout.addWidget(self.preview_table)

        log_group = QGroupBox("Activity Log")
        log_layout = QVBoxLayout(log_group)
        log_layout.addWidget(self.activity_log)

        summary_group = QGroupBox("Summary")
        summary_layout = QHBoxLayout(summary_group)
        summary_layout.addWidget(self.files_scanned_label)
        summary_layout.addSpacing(20)
        summary_layout.addWidget(self.files_to_move_label)
        summary_layout.addSpacing(20)
        summary_layout.addWidget(self.skipped_label)
        summary_layout.addStretch()

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.scan_button)
        button_layout.addWidget(self.organize_button)
        button_layout.addWidget(self.undo_button)
        button_layout.addStretch()
        button_layout.addWidget(self.exit_button)

        main_layout.addLayout(folder_layout)
        main_layout.addLayout(options_layout)
        main_layout.addWidget(preview_group, 4)
        main_layout.addWidget(log_group, 2)
        main_layout.addWidget(summary_group)
        main_layout.addLayout(button_layout)

    def _create_status_bar(self) -> None:
        status_bar = QStatusBar()
        status_bar.showMessage("Ready")
        self.setStatusBar(status_bar)

    def _connect_signals(self) -> None:
        self.exit_button.clicked.connect(self.close)