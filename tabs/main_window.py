from PyQt6.QtWidgets import (QMainWindow, QVBoxLayout, QWidget, QPushButton, 
                           QLabel, QMessageBox, QApplication, QHBoxLayout, 
                           QStackedWidget, QSizePolicy)
from PyQt6.QtGui import QIcon, QAction, QFont, QKeySequence, QShortcut
from PyQt6.QtCore import Qt, QSize
import subprocess
from updater.app_updater import AppUpdater
from configparser import ConfigParser
from tabs.settings_page import SettingsPage
from tabs.ersc_settings_tab import ERSCSettingsTab
from tabs.save_backup_tab import SaveBackupTab
import requests
import os
from time import sleep
from tabs.readme_tab import ReadmeTab
from tabs.changlog import Changelongtab
from updater.update_thread import UpdateThread
from version import VERSION
from utility.version_checker import extract_version_after_marker
from utility.resource_ import resource_path
from utility.Localization import Localization
from utility.message_box_patch import apply_patches
from tabs.game_session_tab import GameSessionTab
from dotenv import load_dotenv
load_dotenv()

apply_patches()

class SidebarButton(QPushButton):
    def __init__(self, icon_path, text, parent=None):
        super().__init__(parent)
        self.setIcon(QIcon(icon_path))
        self.setText(text)
        self.setFixedHeight(50)
        self.setCheckable(True)
        self.setIconSize(QSize(24, 24))  # Larger icons
        self.setFont(QFont("Segoe UI", 10))  # Modern font
        self.setStyleSheet("""
            QPushButton {
                border: none;
                padding: 10px 10px;
                text-align: left;
                border-radius: 8px;
                margin: 5px 10px;
                color: #E2E8F0;
                background-color: transparent;
            }
            QPushButton:checked {
                background-color: #4A5568;
                color: white;
            }
            QPushButton:hover:!checked {
                background-color: #2D3748;
            }
            QPushButton:pressed {
                background-color: #4A5568;
            }
        """)

class Sidebar(QWidget):
    def __init__(self, parent=None, localization=None):
        super().__init__(parent)
        self.localization = localization
        self.buttons = []
        self.setFixedWidth(240)
        self.init_ui()

    def init_ui(self):
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(5)
        
        self.setStyleSheet("""
            Sidebar {
                background-color: #2D3748;
                border-right: 1px solid #4A5568;
            }
        """)

    def set_button_connections(self, stack):
        for i, button in enumerate(self.buttons):
            button.clicked.connect(lambda checked, index=i: self.handle_button_click(index, stack))
            
    def handle_button_click(self, index, stack):
        stack.setCurrentIndex(index)
        for i, button in enumerate(self.buttons):
            button.setChecked(i == index)

class MainWindow(QMainWindow):
    def __init__(self, localization=None):
        super().__init__()
        self.Localization = localization or Localization(language='en', app=QApplication.instance())
        
        self.setWindowTitle(self.Localization.translate("ui.main_window.title"))
        self.setGeometry(100, 100, 1000, 700)
        self.setWindowIcon(QIcon(resource_path("assets/icon.ico")))

        # Create main layout
        self.central_widget = QWidget()
        self.main_layout = QHBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        self.setCentralWidget(self.central_widget)

        # Create sidebar
        self.sidebar = Sidebar(self)
        self.main_layout.addWidget(self.sidebar)

        # Create stacked widget for content
        self.stack = QStackedWidget()
        self.main_layout.addWidget(self.stack)

        # Create pages
        self.update_tab = QWidget()
        self.ersc_settings_tab = ERSCSettingsTab(self)
        self.game_session_tab = GameSessionTab(self)
        self.save_backup_tab = SaveBackupTab(self)
        self.settings_tab = SettingsPage(self)

        # Initialize update tab
        self.init_update_tab()

        # Add pages to stack
        self.stack.addWidget(self.update_tab)
        self.stack.addWidget(self.ersc_settings_tab)
        self.stack.addWidget(self.game_session_tab)
        self.stack.addWidget(self.save_backup_tab)
        self.stack.addWidget(self.settings_tab)

        # Create sidebar buttons
        self.create_sidebar_buttons()

        # Create menu bar
        self.create_menu_bar()

        # Create status bar items
        self.create_status_bar()

        # Setup keyboard shortcuts and auto-backup
        self.setup_shortcuts()
        self.setup_auto_backup()

        QApplication.instance().processEvents()
        self.check_auto_updates()

    def setup_auto_backup(self):
        """Initialize auto-backup on startup if enabled in settings"""
        config = ConfigParser()
        settings_path = self.settings_tab.get_settings_path()
        if os.path.exists(settings_path):
            config.read(settings_path)
            settings = config['Settings']
  
    def setup_shortcuts(self):
        import keyboard 
        
        config = ConfigParser()
        settings_path = self.settings_tab.get_settings_path()
        if os.path.exists(settings_path):
            config.read(settings_path)
            settings = config['Settings']

            # Save backup shortcut
            save_key = settings.get('save_backup_key', '')
            if save_key:
                keyboard.add_hotkey(save_key, self.save_backup_tab.save_backup)

            # Load backup shortcut
            load_key = settings.get('load_backup_key', '')
            if load_key:
                keyboard.add_hotkey(load_key, self.save_backup_tab.load_backup)

            # Start Auto Backup
            start_auto_backup_key = settings.get('start_auto_backup_key', '')
            if start_auto_backup_key:
                keyboard.add_hotkey(start_auto_backup_key, self.save_backup_tab.start_auto_backup)

            # Stop Auto Backup
            stop_auto_backup_key = settings.get('stop_auto_backup_key', '')
            if stop_auto_backup_key:
                keyboard.add_hotkey(stop_auto_backup_key, self.save_backup_tab.stop_auto_backup)

        # Optional: Add cleanup method to remove hotkeys when closing the application
        def cleanup_hotkeys(self):
            keyboard.unhook_all()

                
    def create_sidebar_buttons(self):
        # Create buttons for each section
        buttons = [
            (resource_path("assets/home.png"), self.Localization.translate("ui.main_window.tabs.main")),
            (resource_path("assets/seamless.png"), self.Localization.translate("ui.main_window.tabs.ersc_settings")),
            (resource_path("assets/game_session.png"), self.Localization.translate("ui.main_window.tabs.game_session")),
            (resource_path("assets/backup.png"), self.Localization.translate("ui.main_window.tabs.save_backup")),  # New Save Backup tab
            (resource_path("assets/settings.png"), self.Localization.translate("ui.main_window.tabs.settings"))
        ]

        self.button_group = []
        for i, (icon, text) in enumerate(buttons):
            btn = SidebarButton(resource_path(icon), text)
            btn.clicked.connect(lambda checked, index=i: self.change_page(index))
            self.sidebar.layout.addWidget(btn)
            self.button_group.append(btn)

        # Add spacer to push buttons to the top
        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        self.sidebar.layout.addWidget(spacer)

    def change_page(self, index):
        # Uncheck all buttons except the clicked one
        for i, btn in enumerate(self.button_group):
            btn.setChecked(i == index)
        self.stack.setCurrentIndex(index)

    def create_menu_bar(self):
        self.menu_bar = self.menuBar()
        help_menu = self.menu_bar.addMenu(self.Localization.translate("ui.main_window.menu.help"))

        # Create readme and changelog tabs
        self.readme_tab = ReadmeTab()
        self.changelog_tab = Changelongtab()

        # Add menu actions
        actions = [
            (self.Localization.translate("ui.main_window.menu.check_app_updates"), self.check_for_updates),
            (self.Localization.translate('ui.main_window.menu.check_mod_updates'), self.update_mod),
            (self.Localization.translate("ui.main_window.tabs.readme"), self.show_readme),
            (self.Localization.translate("ui.main_window.tabs.changlog"), self.show_changelog),
            (self.Localization.translate("ui.main_window.menu.about"), self.show_about)
        ]

        for text, slot in actions:
            action = QAction(text, self)
            action.triggered.connect(slot)
            help_menu.addAction(action)

    def create_status_bar(self):
        self.dll_version_label = QLabel(self.Localization.translate("ui.main_window.status.version.mod.unknown"))
        self.version_label = QLabel(self.Localization.translate('ui.main_window.status.version.app').format(VERSION))
        self.version_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignBottom)
        
        self.statusBar().addWidget(self.dll_version_label)
        self.statusBar().addPermanentWidget(self.version_label)
        
        self.update_dll_version_label()

    def get_current_settings(self):
        """Get current settings from ersc_settings_tab and existing ini file"""
        install_path = self.settings_tab.path_input.text()
        settings_path = os.path.join(install_path, "SeamlessCoop", "ersc_settings.ini")
        
        # Initialize with default settings
        settings = {
            # GAMEPLAY settings
            'allow_invaders': 1,
            'death_debuffs': 1,
            'allow_summons': 1,
            'overhead_player_display': 0,
            'skip_splash_screens': 0,
            'default_boot_master_volume': 5,
            
            # SCALING settings
            'enemy_health_scaling': 35,
            'enemy_damage_scaling': 0,
            'enemy_posture_scaling': 15,
            'boss_health_scaling': 100,
            'boss_damage_scaling': 0,
            'boss_posture_scaling': 20,
            
            # PASSWORD settings
            'cooppassword': '',
            
            # SAVE settings
            'save_file_extension': '.co2',
            
            # LANGUAGE settings
            'mod_language_override': ''
        }
        
        # Try to read existing settings from file
        if os.path.exists(settings_path):
            try:
                config = ConfigParser()
                config.read(settings_path)
                
                if 'GAMEPLAY' in config:
                    for key in ['allow_invaders', 'death_debuffs', 'allow_summons', 
                              'overhead_player_display', 'skip_splash_screens']:
                        if key in config['GAMEPLAY']:
                            settings[key] = int(config['GAMEPLAY'][key])
                    if 'default_boot_master_volume' in config['GAMEPLAY']:
                        settings['default_boot_master_volume'] = int(config['GAMEPLAY']['default_boot_master_volume'])
                
                if 'SCALING' in config:
                    for key in ['enemy_health_scaling', 'enemy_damage_scaling', 'enemy_posture_scaling',
                              'boss_health_scaling', 'boss_damage_scaling', 'boss_posture_scaling']:
                        if key in config['SCALING']:
                            settings[key] = int(config['SCALING'][key])
                
                if 'PASSWORD' in config and 'cooppassword' in config['PASSWORD']:
                    settings['cooppassword'] = config['PASSWORD']['cooppassword']
                
                if 'SAVE' in config and 'save_file_extension' in config['SAVE']:
                    settings['save_file_extension'] = config['SAVE']['save_file_extension']
                
                if 'LANGUAGE' in config and 'mod_language_override' in config['LANGUAGE']:
                    settings['mod_language_override'] = config['LANGUAGE']['mod_language_override']
            except Exception as e:
                print(f"Error reading existing settings: {str(e)}")
        
        return settings

    def check_auto_updates(self):
        """
        Check for both app and mod updates on startup if enabled
        """
        settings = ConfigParser()
        settings_path = self.settings_tab.get_settings_path()
        
        if os.path.exists(settings_path):
            settings.read(settings_path)
            if bool(int(settings.get('Settings', 'auto_check_updates', fallback='0'))):
                self.check_all_updates(silent=True)
                self.check_mod_updates(silent=True)
    
    def check_all_updates(self, silent=False):
        """
        Check for both app and mod updates in sequence
        """
        # First check app updates
        self.updater = AppUpdater(self.Localization, silent=silent)
        self.updater.update_progress.connect(self.show_update_progress)
        self.updater.update_complete.connect(self.handle_app_update_complete)
        self.updater.update_available.connect(self.confirm_update)
        self.updater.start()
                
    def handle_app_update_complete(self, success, message):
        """
        Handle app update completion and then check mod updates
        """
        if "up to date" not in message.lower():
            self.update_complete(success, message)
        
    def check_mod_updates(self, silent=False):
        """
        Check for mod updates with consistent behavior for both automatic and manual checks
        """
        install_path = self.settings_tab.path_input.text()
        if not install_path:
            return

        ersc_dll_path = os.path.join(install_path, "SeamlessCoop", "ersc.dll")
        current_marker = "SteamMatchMaking009"

        if not os.path.exists(ersc_dll_path):
            if not silent:
                QMessageBox.warning(
                    self,
                    self.Localization.translate('messages.update.update_error'),
                    self.Localization.translate("ui.main_window.status.version.mod.not_found")
                )
            return

        try:
            # Get current version
            current_version = extract_version_after_marker(ersc_dll_path, current_marker)
            current_version = f"v{current_version}" if current_version else None

            # Get latest version from GitHub
            release_info = requests.get("https://api.github.com/repos/LukeYui/EldenRingSeamlessCoopRelease/releases/latest")
            release_data = release_info.json()
            latest_version = release_data['tag_name']

            # Compare versions and show update prompt if needed
            if current_version and current_version != latest_version:
                # Always show the update prompt, regardless of silent mode
                reply = QMessageBox.question(
                    self,
                    self.Localization.translate('messages.update.update_available'),
                    self.Localization.translate('messages.update.download_mod?').format(current_version, latest_version),
                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                    QMessageBox.StandardButton.No
                )

                if reply == QMessageBox.StandardButton.Yes:
                    self.perform_mod_update()
            elif not silent:
                # Only show "up to date" message for manual checks
                QMessageBox.information(
                    self,
                    self.Localization.translate('messages.update.last_version_installed'),
                    self.Localization.translate('messages.update.latest_installed').format(current_version)
                )

        except Exception as e:
            if not silent:
                if isinstance(e, KeyError):
                    QMessageBox.warning(
                        self,
                        self.Localization.translate('messages.update.update_error'),
                        self.Localization.translate('messages.errors.Api_limit').format(str(e))
                    )
                else:
                    QMessageBox.warning(
                        self,
                        self.Localization.translate('messages.update.update_error'),
                        self.Localization.translate('messages.errors.check_failed').format(str(e))
                    )
                    
    def perform_mod_update(self):
        """
        Perform the actual mod update
        """
        url = "https://github.com/LukeYui/EldenRingSeamlessCoopRelease/releases/latest/download/ersc.zip"
        install_path = self.settings_tab.path_input.text()
        
        # Check if session sharing is enabled and share the session
        if self.game_session_tab.share_game_session.isChecked():
            self.share_game_session()
            
        # Get current settings before update
        current_settings = self.get_current_settings()
            
        self.update_thread = UpdateThread(url, install_path, current_settings, self.Localization)
        self.update_thread.update_progress.connect(self.update_status)
        self.update_thread.update_complete.connect(self.update_finished)
        self.update_thread.start()

    def silent_update_check(self):
        """
        Perform a silent check for updates but still show download progress
        """
        self.updater = AppUpdater(self.Localization, silent=True)
        # Still connect the update_progress and update_complete for download status
        self.updater.update_progress.connect(self.show_update_progress)
        self.updater.update_complete.connect(self.show_download_complete)
        self.updater.update_available.connect(self.confirm_update)
        self.updater.start()

    def show_download_complete(self, success, message):
        """
        Show download completion message but skip 'up to date' messages in silent mode
        """
        if "up to date" not in message.lower():
            self.update_complete(success, message)

    def check_for_updates(self, silent=False):
        """
        Check for updates with optional silent mode
        """
        self.updater = AppUpdater(self.Localization, silent=silent)
        if not silent:
            self.updater.update_progress.connect(self.show_update_progress)
            self.updater.update_complete.connect(self.update_complete)
        self.updater.update_available.connect(self.confirm_update)
        self.updater.start()

    def launch_game(self):
        try:
            settings = ConfigParser()
            settings_path = self.settings_tab.get_settings_path()
            settings.read(settings_path)
            game_exe = settings.get('Settings', 'game_exe_path', fallback='')
            run_steam_silent = bool(int(settings.get('Settings', 'run_steam_silent', fallback='0')))

            if not game_exe:
                QMessageBox.warning(
                    self,
                    self.Localization.translate("messages.errors.launch_error_title"),
                    self.Localization.translate("messages.errors.no_game_exe")
                )
                return

            if not os.path.exists(game_exe):
                QMessageBox.warning(
                    self,
                    self.Localization.translate("messages.errors.launch_error_title"),
                    self.Localization.translate("messages.errors.game_exe_not_found")
                )
                return

            # Get the directory of the script
            script_dir = os.path.dirname(os.path.abspath(__file__))
            
            # Construct the path to config_eldenring.toml
            config_path = os.path.join(script_dir, 'config_eldenring.toml')

            # Construct the command
            command = [
                game_exe,
                '-t', 'er',
                '-c', config_path,
                '-p', game_exe
            ]

            # Add silent flag if enabled
            if run_steam_silent:
                command.extend(['-s'])

            # Change the working directory to the game directory before running the command
            game_dir = os.path.dirname(game_exe)
            os.chdir(game_dir)
            
            process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = process.communicate()

            if process.returncode != 0:
                error_message = f"Command failed with return code {process.returncode}\n"
                error_message += f"STDOUT: {stdout.decode('utf-8')}\n"
                error_message += f"STDERR: {stderr.decode('utf-8')}"
                raise Exception(error_message)

        except Exception as e:
            QMessageBox.critical(
                self,
                self.Localization.translate("messages.errors.launch_error_title"),
                self.Localization.translate("messages.errors.launch_error").format(str(e))
            )

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
        """
        Show update confirmation dialog and handle response
        """
        reply = QMessageBox.question(
            self,
            self.Localization.translate('messages.update.update_available'),
            self.Localization.translate('messages.update.download_app?').format(current_version, latest_version),
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            self.updater.confirm_update()
        else:
            self.statusBar().showMessage(self.Localization.translate('messages.update.update_cancelled'), 3000)
            self.updater.update_complete.emit(False, self.Localization.translate('messages.update.update_cancelled'))
            self.update_dll_version_label()
    
    def show_readme(self):
        """Show readme in a new window"""
        readme_window = QMainWindow(self)
        readme_window.setWindowTitle(self.Localization.translate("ui.main_window.tabs.readme"))
        
        # Set the window size using resize() instead of setGeometry()
        readme_window.resize(800, 600)  # Set the preferred size of the window

        readme_window.setCentralWidget(self.readme_tab)
        readme_window.show()

    def show_changelog(self):
        """Show changelog in a new window"""
        changelog_window = QMainWindow(self)
        changelog_window.setWindowTitle(self.Localization.translate("ui.main_window.tabs.changlog"))
        
        # Set the window size using resize() instead of setGeometry()
        changelog_window.resize(800, 600)  # Set the preferred size of the window

        changelog_window.setCentralWidget(self.changelog_tab)
        changelog_window.show()

    def show_about(self):
        author = "2Pz"
        about_text = self.Localization.translate('messages.update.show_about').format(VERSION, author)
        QMessageBox.about(self, self.Localization.translate('ui.main_window.menu.about'), about_text)

    def get_version(self):
        return VERSION

    def init_update_tab(self):
        layout = QVBoxLayout()
        self.update_tab.setLayout(layout)

        # Add launch button
        self.launch_button = QPushButton(self.Localization.translate("ui.main.launch_button"))
        self.launch_button.clicked.connect(self.launch_game)
        layout.addWidget(self.launch_button)

    def update_mod(self):
        install_path = self.settings_tab.path_input.text()
        if not install_path:
            QMessageBox.warning(self, self.Localization.translate('messages.update.update_error'), self.Localization.translate('messages.errors.path_required'))
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
            if KeyError:
                QMessageBox.warning(self, self.Localization.translate('messages.update.update_error'), self.Localization.translate('messages.errors.Api_limit').format(str(e)))
                return
            QMessageBox.warning(self, self.Localization.translate('messages.update.update_error'), self.Localization.translate('messages.errors.path_required').format(str(e)))
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
                self.Localization.translate('messages.update.download_mod?').format(current_version, latest_version),
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No
            )

            if reply != QMessageBox.StandardButton.Yes:
                return

        # Check if session sharing is enabled and share the session
        if self.game_session_tab.share_game_session.isChecked():
            self.share_game_session()

        # Get current settings before update
        current_settings = self.get_current_settings()

        # Proceed with updating
        url = "https://github.com/LukeYui/EldenRingSeamlessCoopRelease/releases/latest/download/ersc.zip"
        self.update_thread = UpdateThread(url, install_path, current_settings, self.Localization)
        self.update_thread.update_progress.connect(self.update_status)
        self.update_thread.update_complete.connect(self.update_finished)
        self.update_thread.start()

    def share_game_session(self):
        character_data = self.game_session_tab.character_combo.currentData()
        session_data = {
            "username": self.game_session_tab.username_input.text(),
            "message": self.game_session_tab.message_input.text(),
            "password": self.ersc_settings_tab.cooppassword.text(),
            "level": character_data['level'],
            "stats": character_data['stats']
        }
        try:
            response = requests.post(f"{os.getenv('API')}/api/add_session", json=session_data)
            if response.status_code != 200:
                print(f"Failed to share game session. Status code: {response.status_code}")
        except Exception as e:
            print(f"Error sharing game session: {str(e)}")

    def update_status(self, message):
        # Show temporary status message for 3000ms (3 seconds)
        self.statusBar().showMessage(message, 3000)

    def update_finished(self, success, message):
        # Show temporary status message for 3000ms (3 seconds)
        self.statusBar().showMessage(message, 3000)
        
        if success:
            QMessageBox.information(self, self.Localization.translate('lables.success'), message)
        else:
            QMessageBox.warning(self, self.Localization.translate('lables.error'), message)

        self.update_dll_version_label()
        # Refresh the game session tab after update
        self.game_session_tab.refresh_sessions()

    def closeEvent(self, event):
        if self.game_session_tab.share_game_session.isChecked():
            try:
                session_data = {
                    "username": self.game_session_tab.username_input.text(),
                    "action": "remove"
                }
                requests.post(f"{os.getenv('API')}/api/remove_session", json=session_data)
            except Exception as e:
                print(f"Error removing game session: {str(e)}")
        event.accept()
