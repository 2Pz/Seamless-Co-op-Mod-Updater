# main_window.py
from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QPushButton, QLabel, QTextEdit, QMessageBox, QTabWidget, QApplication
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QMainWindow, QMenu, QMenuBar
from updater.app_updater import AppUpdater
from PyQt6.QtGui import QAction
from PyQt6.QtCore import Qt
from tabs.settings_page import SettingsPage
import requests
import os
from tabs.readme_tab import ReadmeTab
from tabs.changlog import Changelongtab
from updater.update_thread import UpdateThread
from version import VERSION
from utility.version_checker import extract_version_after_marker  # Import the version checker
from utility.resource_ import resource_path
from utility.Localization import Localization
from utility.message_box_patch import apply_patches
from tabs.game_session_tab import GameSessionTab



apply_patches()

class MainWindow(QMainWindow):
    def __init__(self, localization=None):
        super().__init__()
        self.Localization = localization or Localization(language='en', app=QApplication.instance())

        
        
        self.setWindowTitle(self.Localization.translate("ui.main_window.title"))
        self.setGeometry(100, 100, 800, 600)


        self.setWindowIcon(QIcon(resource_path("assets/update.ico")))

        self.tab_widget = QTabWidget()
        self.setCentralWidget(self.tab_widget)

        self.update_tab = QWidget()
        self.settings_tab = SettingsPage(self)
        self.game_session_tab = GameSessionTab(self.Localization, self.settings_tab.get_settings())
        self.readme_tab = ReadmeTab()
        self.changelog_tab = Changelongtab()

        self.tab_widget.addTab(self.update_tab, self.Localization.translate("ui.main_window.tabs.update"))
        self.tab_widget.addTab(self.settings_tab, self.Localization.translate("ui.main_window.tabs.settings"))
        self.tab_widget.addTab(self.game_session_tab, self.Localization.translate("ui.main_window.tabs.game_session"))
        self.tab_widget.addTab(self.readme_tab, self.Localization.translate("ui.main_window.tabs.readme"))
        self.tab_widget.addTab(self.changelog_tab, self.Localization.translate("ui.main_window.tabs.changlog"))

        self.init_update_tab()
       
        # Add menu bar
        self.menu_bar = QMenuBar()
        self.setMenuBar(self.menu_bar)

        # Add Help menu
        help_menu = QMenu(self.Localization.translate("ui.main_window.menu.help"), self)
        self.menu_bar.addMenu(help_menu)

        # Add Check for Updates action
        check_updates_action = QAction(self.Localization.translate("ui.main_window.menu.check_updates"), self)
        check_updates_action.triggered.connect(self.check_for_updates)
        help_menu.addAction(check_updates_action)

        # Add About action
        about_action = QAction(self.Localization.translate("ui.main_window.menu.about"), self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)

        # Add version label
        
        self.dll_version_label = QLabel(self.Localization.translate("ui.main_window.status.version.mod.unknown"))
        self.version_label = QLabel(self.Localization.translate('ui.main_window.status.version.app').format(VERSION))

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
                self.dll_version_label.setText(self.Localization.translate("ui.main_window.status.version.mod.found").format(current_version))
            else:
                self.dll_version_label.setText(self.Localization.translate("ui.main_window.status.version.mod.unknown"))
        else:
            self.dll_version_label.setText(self.Localization.translate("ui.main_window.status.version.mod.not_found"))


    def check_for_updates(self):
        self.updater = AppUpdater(self.Localization)
        self.updater.update_progress.connect(self.show_update_progress)
        self.updater.update_complete.connect(self.update_complete)
        self.updater.update_available.connect(self.confirm_update)
        self.updater.start()

    def show_update_progress(self, message):
        # Show temporary status message for 3000ms (3 seconds)
        self.statusBar().showMessage(message, 3000)

    def update_complete(self, success, message):
        # Clear any temporary status message
        self.statusBar().clearMessage()
        # Update the DLL version label
        self.update_dll_version_label()
        
        if success:
            QMessageBox.information(self, self.Localization.translate('messages.update.update_complete'), message)
        else:
            QMessageBox.information(self, self.Localization.translate('messages.update.update_status'), message)

    def confirm_update(self, current_version, latest_version):
        reply = QMessageBox.question(
            self,
            self.Localization.translate('messages.update.update_available'),
            self.Localization.translate('messages.update.download?').format(current_version, latest_version),
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            self.updater.confirm_update()
        else:
            # Show cancelled message temporarily and restore DLL version
            self.statusBar().showMessage(self.Localization.translate('messages.update.update_cancelled'), 3000)
            self.updater.update_complete.emit(False, self.Localization.translate('messages.update.update_cancelled'))
            self.update_dll_version_label()
    
    
    def show_about(self):
        author = "2Pz"
        about_text = self.Localization.translate('messages.update.show_about').format(VERSION, author)
        QMessageBox.about(self, self.Localization.translate('ui.main_window.menu.about'), about_text)

    def get_version(self):
        return VERSION

    def init_update_tab(self):
        layout = QVBoxLayout()
        self.update_tab.setLayout(layout)

        self.update_button = QPushButton(self.Localization.translate('ui.main_window.update_button'))
        self.update_button.clicked.connect(self.update_mod)
        layout.addWidget(self.update_button)

        self.status_label = QLabel(self.Localization.translate('ui.main_window.status_ready'))
        layout.addWidget(self.status_label)

        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        layout.addWidget(self.log_text)

    def update_mod(self):
        install_path = self.settings_tab.path_input.text()
        if not install_path:
            QMessageBox.warning(self, self.Localization.translate('messages.update.error'), self.Localization.translate('messages.errors.path_required'))
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
            QMessageBox.warning(self, self.Localization.translate('messages.update.error'), self.Localization.translate('messages.errors.path_required').format(str(e)))
            return

        # Compare current version with latest version
        if current_version == latest_version:
            reply = QMessageBox.question(
                self,
                self.Localization.translate('messages.update.last_version_installed'),
                self.Localization.translate('messages.update.latest_installed').format(current_version),
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No
            )

            if reply != QMessageBox.StandardButton.Yes:
                return

        elif current_version:
            reply = QMessageBox.question(
                self,
                self.Localization.translate('messages.update.update_available'),
                self.Localization.translate('messages.update.download?').format(current_version, latest_version),
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No
            )

            if reply != QMessageBox.StandardButton.Yes:
                return

        # Check if session sharing is enabled and share the session
        settings = self.settings_tab.get_settings()
        if settings['share_game_session']:
            self.share_game_session(settings)
        # Proceed with updating
        url = "https://github.com/LukeYui/EldenRingSeamlessCoopRelease/releases/latest/download/ersc.zip"
        settings = self.settings_tab.get_settings()
        self.update_thread = UpdateThread(url, install_path, settings, self.Localization)
        self.update_thread.update_progress.connect(self.update_status)
        self.update_thread.update_complete.connect(self.update_finished)
        self.update_thread.start()

    def share_game_session(self, settings):
        session_data = {
            "username": settings['username'],
            "message": settings['message'],
            "password": settings['cooppassword']
        }
        try:
            response = requests.post("http://localhost:8001/add_session", json=session_data)
            if response.status_code != 200:
                print(f"Failed to share game session. Status code: {response.status_code}")
        except Exception as e:
            print(f"Error sharing game session: {str(e)}")

    def update_status(self, message):
        self.status_label.setText(message)
        self.log_text.append(message)

    def update_finished(self, success, message):
        self.status_label.setText(message)
        self.log_text.append(message)
        if success:
            QMessageBox.information(self, self.Localization.translate('lables.success'), message)
        else:
            QMessageBox.warning(self, self.Localization.translate('lables.error'), message)

        # Refresh the game session tab after update
        self.game_session_tab.refresh_sessions()


    def closeEvent(self, event):
        settings = self.settings_tab.get_settings()
        if settings['share_game_session']:
            try:
                session_data = {
                    "username": settings['username'],
                    "action": "remove"
                }
                requests.post("https://seamless-co-op-game-sessions.onrender.com/api/remove_session", json=session_data)
            except Exception as e:
                print(f"Error removing game session: {str(e)}")
        event.accept()
