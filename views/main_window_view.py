from pathlib import Path

from PySide6.QtCore import QFile, QIODevice
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import (
    QAbstractItemView,
    QComboBox,
    QGroupBox,
    QHeaderView,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QStackedWidget,
    QTableWidget,
    QTableWidgetItem,
    QWidget,
)


class MainWindowView:
    def __init__(self):
        project_root = Path(__file__).resolve().parent.parent
        candidate_paths = [
            project_root / "ui" / "main_window.ui",
            project_root / "main_window.ui",
        ]
        ui_path = next((p for p in candidate_paths if p.exists()), candidate_paths[0])
        loader = QUiLoader()
        ui_file = QFile(str(ui_path))
        if not ui_file.open(QIODevice.ReadOnly):
            raise RuntimeError(f"Cannot open UI file: {ui_path}")
        self.window = loader.load(ui_file)
        ui_file.close()

        if self.window is None:
            raise RuntimeError(f"Cannot load UI file: {ui_path}")

        self.role_combo = self.window.findChild(QComboBox, "roleCombo")
        self.username_edit = self.window.findChild(QLineEdit, "usernameEdit")
        self.password_edit = self.window.findChild(QLineEdit, "passwordEdit")
        self.login_button = self.window.findChild(QPushButton, "loginButton")
        self.logout_button = self.window.findChild(QPushButton, "logoutButton")
        self.content_stack = self.window.findChild(QStackedWidget, "contentStack")
        self.claim_id_edit = self.window.findChild(QLineEdit, "claimIdEdit")
        self.submit_button = self.window.findChild(QPushButton, "submitButton")
        self.view_list_button = self.window.findChild(QPushButton, "viewListButton")
        self.refresh_button = self.window.findChild(QPushButton, "refreshButton")
        self.back_to_submit_button = self.window.findChild(QPushButton, "backToSubmitButton")
        self.session_label = self.window.findChild(QLabel, "sessionLabel")
        self.submit_group = self.window.findChild(QGroupBox, "submitGroup")
        self.claims_table = self.window.findChild(QTableWidget, "claimsTable")
        self.submit_page = self.window.findChild(QWidget, "submitPage")
        self.list_page = self.window.findChild(QWidget, "listPage")

        required = [
            self.role_combo,
            self.username_edit,
            self.password_edit,
            self.login_button,
            self.logout_button,
            self.content_stack,
            self.claim_id_edit,
            self.submit_button,
            self.view_list_button,
            self.refresh_button,
            self.back_to_submit_button,
            self.session_label,
            self.submit_group,
            self.claims_table,
            self.submit_page,
            self.list_page,
        ]
        if any(w is None for w in required):
            raise RuntimeError("UI widgets are missing or misnamed.")

        self.claims_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.claims_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.claims_table.setAlternatingRowColors(True)
        self.claims_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

    def show(self):
        self.window.show()

    def set_session_text(self, text: str):
        self.session_label.setText(text)

    def set_submit_enabled(self, enabled: bool):
        self.submit_group.setEnabled(enabled)
        self.view_list_button.setEnabled(enabled)
        self.back_to_submit_button.setEnabled(enabled)

    def show_list_page(self):
        self.content_stack.setCurrentWidget(self.list_page)

    def show_submit_page(self):
        self.content_stack.setCurrentWidget(self.submit_page)

    def read_credentials(self):
        return (
            self.role_combo.currentText().strip(),
            self.username_edit.text().strip(),
            self.password_edit.text().strip(),
        )

    def clear_credentials(self):
        self.username_edit.clear()
        self.password_edit.clear()

    def read_claim_id(self):
        return self.claim_id_edit.text().strip()

    def clear_claim_id(self):
        self.claim_id_edit.clear()

    def show_info(self, message: str):
        QMessageBox.information(self.window, "Info", message)

    def show_error(self, message: str):
        QMessageBox.critical(self.window, "Error", message)

    def render_claims(self, claims, comp_lookup):
        self.claims_table.setRowCount(len(claims))
        for i, row in enumerate(claims):
            claim_id, claimant_id, submitted_date, status, fn, ln, income, ctype = row
            comp = comp_lookup.get(claim_id)
            comp_text = f"{comp['amount']} ({comp['date']})" if comp else "-"
            values = [
                claim_id,
                claimant_id,
                f"{fn} {ln}",
                str(income),
                ctype,
                status,
                comp_text,
                submitted_date,
            ]
            for j, value in enumerate(values):
                self.claims_table.setItem(i, j, QTableWidgetItem(value))
