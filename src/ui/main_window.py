from pathlib import Path

from PySide6.QtWidgets import (
    QAbstractItemView,
    QCheckBox,
    QFileDialog,
    QGridLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPlainTextEdit,
    QPushButton,
    QStatusBar,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from src.core.config_manager import ConfigManager
from src.core.organizer_engine import OrganizerEngine
from src.core.undo_manager import UndoManager
from src.models.preview_record import PreviewRecord
from src.models.settings import Settings


class MainWindow(QMainWindow):
    """Main application window."""

    def __init__(self) -> None:
        super().__init__()

        self.selected_folder: Path | None = None
        self.preview_records: list[PreviewRecord] = []

        self.engine = OrganizerEngine()
        self.config = ConfigManager()
        self.config.load()

        self.undo_manager = UndoManager()

        self.settings = Settings()

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
        self.preview_table.setEditTriggers(
            QAbstractItemView.NoEditTriggers
        )
        self.preview_table.setSelectionBehavior(
            QAbstractItemView.SelectRows
        )
        self.preview_table.setSelectionMode(
            QAbstractItemView.SingleSelection
        )
        self.preview_table.horizontalHeader().setStretchLastSection(True)

        self.activity_log = QPlainTextEdit()
        self.activity_log.setReadOnly(True)
        self.activity_log.appendPlainText("Ready...")

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
        self.browse_button.clicked.connect(self._browse_folder)
        self.scan_button.clicked.connect(self._scan_folder)
        self.organize_button.clicked.connect(
            self._organize_files
        )

    def _browse_folder(self) -> None:
        """Open a folder selection dialog."""

        folder = QFileDialog.getExistingDirectory(
            self,
            "Select Folder",
            str(Path.home()),
        )

        if not folder:
            return

        self.selected_folder = Path(folder)

        self.folder_edit.setText(str(self.selected_folder))

        self.scan_button.setEnabled(True)

        self.activity_log.appendPlainText("")
        self.activity_log.appendPlainText(
            f"Selected folder: {self.selected_folder}"
        )

        self.statusBar().showMessage("Folder selected")

    def _scan_folder(self) -> None:
        """Scan the selected folder and generate an organization preview."""

        if self.selected_folder is None:
            return

        # Read current settings from the UI.
        self.settings.dry_run = self.dry_run_checkbox.isChecked()
        self.settings.recursive = (
            self.recursive_checkbox.isChecked()
        )
        self.settings.ignore_hidden = (
            self.hidden_checkbox.isChecked()
        )

        # Generate preview records.
        records = self.engine.preview(
            folder=self.selected_folder,
            settings=self.settings,
            categories=self.config.categories,
        )

        self.preview_records = records

        # Update the preview table.
        self._populate_preview_table(records)

        # Update the summary.
        self._update_summary(
            scanned=len(records),
            to_move=len(records),
            skipped=0,
        )

        # Enable or disable the Organize button.
        self.organize_button.setEnabled(bool(records))

        # Log the completed scan.
        self.activity_log.appendPlainText("")
        self.activity_log.appendPlainText(
            f"Preview generated for {len(records)} files."
        )

        self.statusBar().showMessage("Preview ready")

    def _populate_preview_table(
        self,
        records: list[PreviewRecord],
    ) -> None:
        """Populate the preview table."""

        self.preview_table.setRowCount(0)

        for record in records:

            row = self.preview_table.rowCount()

            self.preview_table.insertRow(row)

            self.preview_table.setItem(
                row,
                0,
                QTableWidgetItem(record.source.name),
            )

            self.preview_table.setItem(
                row,
                1,
                QTableWidgetItem(record.category),
            )

            self.preview_table.setItem(
                row,
                2,
                QTableWidgetItem(
                    str(
                        record.destination.relative_to(
                            self.selected_folder
                        )
                    )
                ),
            )

    def _reset_summary(self) -> None:
        """Reset summary labels."""

        self.files_scanned_label.setText(
            "Files Scanned : 0"
        )
        self.files_to_move_label.setText(
            "Files To Move : 0"
        )
        self.skipped_label.setText(
            "Skipped : 0"
        )


    def _update_summary(
        self,
        scanned: int,
        to_move: int,
        skipped: int,
    ) -> None:
        """Update summary labels."""

        self.files_scanned_label.setText(
            f"Files Scanned : {scanned}"
        )
        self.files_to_move_label.setText(
            f"Files To Move : {to_move}"
        )
        self.skipped_label.setText(
            f"Skipped : {skipped}"
        )

    def get_selected_folder(self) -> Path | None:
        """Return the currently selected folder."""

        return self.selected_folder
    
    def _organize_files(self) -> None:
        """Organize files or perform a dry run."""

        if not self.preview_records:
            return

        dry_run = self.dry_run_checkbox.isChecked()

        # Confirm before performing real file moves.
        if not dry_run:
            reply = QMessageBox.question(
                self,
                "Confirm Organization",
                (
                    "Files will be moved to their destination folders.\n\n"
                    "This operation can be undone.\n\n"
                    "Do you want to continue?"
                ),
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No,
            )

            if reply != QMessageBox.Yes:
                return

        # Execute the organization.
        messages = self.engine.organize(
            records=self.preview_records,
            dry_run=dry_run,
        )

        # Display log messages.
        self.activity_log.appendPlainText("")

        for message in messages:
            self.activity_log.appendPlainText(message)

        if dry_run:
            self.statusBar().showMessage(
                "Dry Run completed"
            )
            return

        # Refresh the interface after a successful organization.
        self.preview_table.setRowCount(0)

        self.preview_records.clear()

        self._reset_summary()

        self.scan_button.setEnabled(True)
        self.organize_button.setEnabled(False)

        self.undo_button.setEnabled(
            self.undo_manager.has_history()
        )

        self.statusBar().showMessage(
            "Organization completed"
        )