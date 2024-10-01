# main_window.py
from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QPushButton, QLabel, QTextEdit, QMessageBox, QTabWidget
from PyQt6.QtGui import QIcon, QPalette, QColor
from PyQt6.QtWidgets import QMainWindow, QMenu, QMenuBar
from app_updater import AppUpdater
from PyQt6.QtGui import QAction
from PyQt6.QtCore import Qt
from settings_page import SettingsPage
import requests
import os
from readme_tab import ReadmeTab
from update_thread import UpdateThread
from version import VERSION
from version_checker import extract_version_after_marker  # Import the version checker
from resource_ import resource_path

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Seamless Co-op Mod Updater")
        self.setGeometry(100, 100, 800, 600)

        self.setWindowIcon(QIcon(resource_path("assets/update.ico")))

        self.tab_widget = QTabWidget()
        self.setCentralWidget(self.tab_widget)

        self.update_tab = QWidget()
        self.settings_tab = SettingsPage(self)
        self.readme_tab = ReadmeTab()

        self.tab_widget.addTab(self.update_tab, "Update")
        self.tab_widget.addTab(self.settings_tab, "Settings")
        self.tab_widget.addTab(self.readme_tab, "README")

        self.init_update_tab()
        self.set_dark_theme()

        # Add menu bar
        self.menu_bar = QMenuBar()
        self.setMenuBar(self.menu_bar)

        # Add Help menu
        help_menu = QMenu("Help", self)
        self.menu_bar.addMenu(help_menu)

        # Add Check for Updates action
        check_updates_action = QAction("Check for Updates", self)
        check_updates_action.triggered.connect(self.check_for_updates)
        help_menu.addAction(check_updates_action)

        # Add About action
        about_action = QAction("About", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)

        # Add version label
        
        self.dll_version_label = QLabel("Seamless Co-op Version: Unknown")
        self.version_label = QLabel(f"App Version: {VERSION}")
        self.version_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignBottom)

        self.statusBar().addWidget(self.dll_version_label)
        self.statusBar().addPermanentWidget(self.version_label)

        self.update_dll_version_label()

        # Add the update_dll_version_label method
    def update_dll_version_label(self):
        install_path = self.settings_tab.path_input.text()
        ersc_dll_path = os.path.join(install_path, "SeamlessCoop", "ersc.dll")
        marker = "SteamMatchMaking009"

        if os.path.exists(ersc_dll_path):
            current_version = extract_version_after_marker(ersc_dll_path, marker)
            if current_version:
                self.dll_version_label.setText(f"Seamless Co-op Version: {current_version}")
            else:
                self.dll_version_label.setText("Seamless Co-op Version: Unknown")
        else:
            self.dll_version_label.setText("Seamless Co-op Version: Not Found")


    def check_for_updates(self):
        self.updater = AppUpdater()
        self.updater.update_progress.connect(self.show_update_progress)
        self.updater.update_complete.connect(self.update_complete)
        self.updater.update_available.connect(self.confirm_update)
        self.updater.start()

    def show_update_progress(self, message):
        self.statusBar().showMessage(message)

    def update_complete(self, success, message):
        if success:
            QMessageBox.information(self, "Update Complete", message)
        else:
            QMessageBox.information(self, "Update Status", message)

    def confirm_update(self, current_version, latest_version):
        reply = QMessageBox.question(
            self,
            'Update Available',
            f'A new version is available!\n\nCurrent version: {current_version}\nLatest version: {latest_version}\n\nDo you want to update now?',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            self.updater.confirm_update()
        else:
            self.statusBar().showMessage("Update cancelled", 3000)
            self.updater.update_complete.emit(False, "Update cancelled")

    def show_about(self):
        about_text = f"""
        Seamless Co-op Mod Updater
        Version: {VERSION}
        
        This application helps you update and manage Seamless 
        Co-op Mod for Elden Ring.
        
        Created by 2Pz
        """
        QMessageBox.about(self, "About", about_text)

    def get_version(self):
        return VERSION

    def init_update_tab(self):
        layout = QVBoxLayout()
        self.update_tab.setLayout(layout)

        update_button = QPushButton("Update Seamless Co-op Mod")
        update_button.clicked.connect(self.update_mod)
        layout.addWidget(update_button)

        self.status_label = QLabel("Ready")
        layout.addWidget(self.status_label)

        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        layout.addWidget(self.log_text)

    def set_dark_theme(self):
        # Modern color palette
        WINDOW_BG = QColor(32, 33, 36)       # Dark background
        WIDGET_BG = QColor(41, 42, 45)       # Slightly lighter for widgets
        TEXT_COLOR = QColor(237, 237, 240)   # Very light gray, easy to read
        ACCENT_COLOR = QColor(92, 119, 255)  # Blue accent
        BORDER_COLOR = QColor(55, 56, 59)    # Subtle borders
        
        # Set up palette
        palette = QPalette()
        palette.setColor(QPalette.ColorRole.Window, WINDOW_BG)
        palette.setColor(QPalette.ColorRole.WindowText, TEXT_COLOR)
        palette.setColor(QPalette.ColorRole.Base, WIDGET_BG)
        palette.setColor(QPalette.ColorRole.AlternateBase, WINDOW_BG)
        palette.setColor(QPalette.ColorRole.ToolTipBase, WIDGET_BG)
        palette.setColor(QPalette.ColorRole.ToolTipText, TEXT_COLOR)
        palette.setColor(QPalette.ColorRole.Text, TEXT_COLOR)
        palette.setColor(QPalette.ColorRole.Button, WIDGET_BG)
        palette.setColor(QPalette.ColorRole.ButtonText, TEXT_COLOR)
        palette.setColor(QPalette.ColorRole.Link, ACCENT_COLOR)
        palette.setColor(QPalette.ColorRole.Highlight, ACCENT_COLOR)
        palette.setColor(QPalette.ColorRole.HighlightedText, TEXT_COLOR)
        
        self.setPalette(palette)
        
        # Comprehensive stylesheet
        self.setStyleSheet("""
            QMainWindow {
                background-color: #202124;
            }
            QWidget {
                font-size: 14px;
            }
            QTabWidget::pane {
                border: 1px solid #373839;
                border-radius: 5px;
                top: -1px;
            }
            QTabBar::tab {
                background-color: #292A2D;
                color: #EDEDED;
                padding: 8px 16px;
                margin-right: 4px;
                border-top-left-radius: 5px;
                border-top-right-radius: 5px;
            }
            QTabBar::tab:selected {
                background-color: #5C77FF;
                color: white;
            }
            QPushButton {
                background-color: #5C77FF;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #6982FF;
            }
            QPushButton:pressed {
                background-color: #5166DD;
            }
            QTextEdit {
                background-color: #292A2D;
                color: #EDEDED;
                border: 1px solid #373839;
                border-radius: 5px;
                padding: 8px;
                selection-background-color: #5C77FF;
                selection-color: white;
            }
            QLabel {
                color: #EDEDED;
            }
            QLineEdit {
                background-color: #292A2D;
                color: #EDEDED;
                border: 1px solid #373839;
                border-radius: 5px;
                padding: 8px;
                selection-background-color: #5C77FF;
                selection-color: white;
            }
            QMessageBox {
                background-color: #202124;
            }
            QMessageBox QLabel {
                color: #EDEDED;
            }
            QMenuBar {
                background-color: #202124;
                color: #EDEDED;
                border-bottom: 1px solid #373839;
            }
            QMenuBar::item:selected {
                background-color: #373839;
            }
            QMenu {
                background-color: #292A2D;
                color: #EDEDED;
                border: 1px solid #373839;
            }
            QMenu::item:selected {
                background-color: #5C77FF;
            }
            QScrollBar:vertical {
                border: none;
                background-color: #292A2D;
                width: 10px;
                margin: 0;
            }
            QScrollBar::handle:vertical {
                background-color: #5C77FF;
                border-radius: 5px;
                min-height: 20px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0;
            }
        """)

    def update_mod(self):
        install_path = self.settings_tab.path_input.text()
        if not install_path:
            QMessageBox.warning(self, "Error", "Please enter the Elden Ring mod installation path in the Settings tab.")
            return

        ersc_dll_path = os.path.join(install_path, "SeamlessCoop", "ersc.dll")
        current_marker = "SteamMatchMaking009"

        # Check the current DLL version if the file exists
        if os.path.exists(ersc_dll_path):
            current_version = extract_version_after_marker(ersc_dll_path, current_marker)
            current_version = f"v{current_version}"
        else:
            current_version = None

        # Fetch latest version from GitHub
        try:
            release_info = requests.get("https://api.github.com/repos/LukeYui/EldenRingSeamlessCoopRelease/releases/latest")
            release_data = release_info.json()
            latest_version = release_data['tag_name']
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Unable to fetch the latest version: {str(e)}")
            return

        # Compare current version with latest version
        if current_version == latest_version:
            reply = QMessageBox.question(
                self,
                "Latest Version Installed",
                f"You already have the latest version: {current_version}.\nDo you want to reinstall it?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No
            )

            if reply != QMessageBox.StandardButton.Yes:
                return

        elif current_version:
            reply = QMessageBox.question(
                self,
                "Update Available",
                f"A new version is available!\n\nCurrent version: {current_version}\nLatest version: {latest_version}\n\nDo you want to update now?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No
            )

            if reply != QMessageBox.StandardButton.Yes:
                return

        # Proceed with updating
        url = "https://github.com/LukeYui/EldenRingSeamlessCoopRelease/releases/latest/download/ersc.zip"
        settings = self.settings_tab.get_settings()
        self.update_thread = UpdateThread(url, install_path, settings)
        self.update_thread.update_progress.connect(self.update_status)
        self.update_thread.update_complete.connect(self.update_finished)
        self.update_thread.start()

    def update_status(self, message):
        self.status_label.setText(message)
        self.log_text.append(message)

    def update_finished(self, success, message):
        self.status_label.setText(message)
        self.log_text.append(message)
        if success:
            QMessageBox.information(self, "Success", message)
        else:
            QMessageBox.warning(self, "Error", message)