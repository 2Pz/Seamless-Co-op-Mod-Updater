# settings_page.py
import os
import subprocess
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, 
                             QPushButton, QLineEdit, QLabel, QFileDialog, 
                             QMessageBox, QGridLayout, QTextEdit,
                             QCheckBox, QComboBox, QGroupBox, QScrollArea, QColorDialog,
                             QSpinBox, QKeySequenceEdit)
from PyQt6.QtGui import QColor, QPalette
from PyQt6.QtCore import Qt
from configparser import ConfigParser
from language_selector import LanguageSelector
from utility.savefile_reader import get_save_folders, find_save_file, read_save_file
from dotenv import load_dotenv
load_dotenv()

class SettingsPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.Localization = parent.Localization if parent else None
        self.main_window = parent
        self.init_ui()
        self.language_selector = LanguageSelector(self.Localization, self.main_window)
        self.language_selector.currentIndexChanged.connect(self.language_selector.change_language)

    def init_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        layout.addWidget(scroll_area)

        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)

        # Language settings
        self.language_group1 = QGroupBox(self.Localization.translate("ui.settings.language.title"))
        language_layout = QGridLayout()
        self.language_group1.setLayout(language_layout)

        self.select_language = QLabel(self.Localization.translate("ui.settings.language.select_language"))
        language_layout.addWidget(self.select_language, 0, 0)
        self.language_selector = LanguageSelector(self.Localization, self.main_window)
        language_layout.addWidget(self.language_selector, 0, 1)

        scroll_layout.addWidget(self.language_group1)

        # Game Path
        self.path_group = QGroupBox(self.Localization.translate("ui.settings.game_path.title"))
        path_layout = QGridLayout()
        self.path_group.setLayout(path_layout)

        self.game_path = QLabel(self.Localization.translate("ui.settings.game_path.label"))
        path_layout.addWidget(self.game_path, 0, 0)
        self.path_input = QLineEdit()
        path_layout.addWidget(self.path_input, 0, 1)
        self.browse_button = QPushButton(self.Localization.translate("ui.settings.game_path.browse_button"))
        self.browse_button.clicked.connect(self.browse_path)
        path_layout.addWidget(self.browse_button, 0, 2)

        scroll_layout.addWidget(self.path_group)

        # Launcher Settings group
        self.launcher_group = QGroupBox(self.Localization.translate("ui.settings.launcher.title"))
        launcher_layout = QGridLayout()
        self.launcher_group.setLayout(launcher_layout)

        self.game_exe_label = QLabel(self.Localization.translate("ui.settings.launcher.game_exe"))
        launcher_layout.addWidget(self.game_exe_label, 0, 0)
        self.game_exe_input = QLineEdit()
        launcher_layout.addWidget(self.game_exe_input, 0, 1)
        self.browse_exe_button = QPushButton(self.Localization.translate("ui.settings.game_path.browse_button"))
        self.browse_exe_button.clicked.connect(self.browse_exe)
        launcher_layout.addWidget(self.browse_exe_button, 0, 2)

        self.auto_check_updates = QCheckBox(self.Localization.translate("ui.settings.launcher.auto_check_updates"))
        launcher_layout.addWidget(self.auto_check_updates, 1, 0, 1, 3)

        scroll_layout.addWidget(self.launcher_group)

        # Steam Settings group
        self.steam_group = QGroupBox(self.Localization.translate("ui.settings.steam.steam_settings"))
        steam_layout = QGridLayout()
        self.steam_group.setLayout(steam_layout)

        # Steam path input with auto-detect
        self.steam_exe_label = QLabel(self.Localization.translate("ui.settings.steam.steam_exe"))
        steam_layout.addWidget(self.steam_exe_label, 0, 0)
        self.steam_exe_input = QLineEdit()
        steam_layout.addWidget(self.steam_exe_input, 0, 1)
        
        steam_buttons_layout = QGridLayout()
        self.browse_steam_button = QPushButton(self.Localization.translate("ui.settings.game_path.browse_button"))
        self.browse_steam_button.clicked.connect(self.browse_steam)
        steam_buttons_layout.addWidget(self.browse_steam_button, 0, 0)

        self.auto_detect_steam = QPushButton(self.Localization.translate("ui.settings.steam.auto_detect"))
        self.auto_detect_steam.clicked.connect(self.auto_detect_steam_path)
        steam_buttons_layout.addWidget(self.auto_detect_steam, 0, 1)
        
        steam_layout.addLayout(steam_buttons_layout, 0, 2)

        # Steam status label
        self.steam_status_label = QLabel()
        self.update_steam_status()
        steam_layout.addWidget(self.steam_status_label, 1, 0, 1, 3)

        # Add Steam silent launch checkbox
        self.run_steam_silently = QCheckBox(self.Localization.translate("ui.settings.steam.run_steam_silently"))
        self.run_steam_silently.stateChanged.connect(self.on_steam_silent_changed)
        steam_layout.addWidget(self.run_steam_silently, 2, 0, 1, 3)

        # Steam ID and Character Selection
        
        self.save_folder_label = QLabel(self.Localization.translate("ui.settings.game_session.save_folder"))
        steam_layout.addWidget(self.save_folder_label, 3, 0)
        self.save_folder_combo = QComboBox()
        self.save_folder_combo.addItem(self.Localization.translate("ui.settings.game_session.save_folder_select"))
        self.save_folder_combo.addItems(get_save_folders())
        self.save_folder_combo.currentIndexChanged.connect(self.update_character_list)
        steam_layout.addWidget(self.save_folder_combo, 3, 1, 1, 2)

        scroll_layout.addWidget(self.steam_group)

        # Backup Settings group
        
        self.backup_group = QGroupBox(self.Localization.translate("ui.settings.backup.backup_settings"))
        backup_layout = QGridLayout()
        self.backup_group.setLayout(backup_layout)

        # Save File Selection
        self.save_file_label = QLabel(self.Localization.translate("ui.settings.backup.save_file_type"))
        backup_layout.addWidget(self.save_file_label, 0, 0)
        self.save_file_combo = QComboBox()
        self.save_file_combo.addItems(["ER0000.sl2", "ER0000.co2"])
        self.save_file_combo.setCurrentText("ER0000.co2")
        backup_layout.addWidget(self.save_file_combo, 0, 1)

        # Backup Directory
        self.backup_dir_label = QLabel(self.Localization.translate("ui.settings.backup.dir"))
        backup_layout.addWidget(self.backup_dir_label, 1, 0)
        self.backup_dir_input = QLineEdit()
        backup_layout.addWidget(self.backup_dir_input, 1, 1)
        self.browse_backup_button = QPushButton(self.Localization.translate("ui.settings.game_path.browse_button"))
        self.browse_backup_button.clicked.connect(self.browse_backup_dir)
        backup_layout.addWidget(self.browse_backup_button, 1, 2)

        # Auto Backup Interval
        self.auto_backup_label = QLabel(self.Localization.translate("ui.settings.backup.backup_Interval"))
        backup_layout.addWidget(self.auto_backup_label, 2, 0)
        self.auto_backup_interval = QSpinBox()
        self.auto_backup_interval.setRange(1, 60)
        self.auto_backup_interval.setValue(5)
        backup_layout.addWidget(self.auto_backup_interval, 2, 1)

        # Max Backups Setting
        self.max_backups_label = QLabel(self.Localization.translate("ui.settings.backup.max_backups"))
        backup_layout.addWidget(self.max_backups_label, 3, 0)
        self.max_backups = QSpinBox()
        self.max_backups.setRange(1, 100)
        self.max_backups.setValue(20)  # Default value
        backup_layout.addWidget(self.max_backups, 3, 1)

        # Notification Sound Settings
        self.enable_sounds = QCheckBox(self.Localization.translate("ui.settings.backup.backup_notify"))
        backup_layout.addWidget(self.enable_sounds, 4, 0)

        # Key Bindings
        self.key_bindings_group = QGroupBox(self.Localization.translate("ui.settings.backup.key_binds"))
        self.key_bindings_layout = QGridLayout()
        self.key_bindings_group.setLayout(self.key_bindings_layout)
        
        bindings = [
            (self.Localization.translate("ui.save_backup.save_backup"), "save_backup_key"),
            (self.Localization.translate("ui.save_backup.load_backup"), "load_backup_key"),
            (self.Localization.translate("ui.save_backup.start_auto_backup"), "start_auto_backup_key"),
            (self.Localization.translate("ui.save_backup.stop_auto_backup"), "stop_auto_backup_key"),
        ]
        
        for i, (label_text, key_name) in enumerate(bindings):
            label = QLabel(label_text)
            key_edit = QKeySequenceEdit()
            setattr(self, key_name, key_edit)
            self.key_bindings_layout.addWidget(label, i, 0)
            self.key_bindings_layout.addWidget(key_edit, i, 1)
            
        backup_layout.addWidget(self.key_bindings_group, 5, 0, 1, 3)

        scroll_layout.addWidget(self.backup_group)

        scroll_area.setWidget(scroll_content)

        # Save button
        self.save_button = QPushButton(self.Localization.translate("ui.settings.save_button"))
        self.save_button.clicked.connect(self.save_settings)
        layout.addWidget(self.save_button)

        self.load_settings()

        # Update ersc.dll version
        self.path_input.textChanged.connect(self.parent().update_dll_version_label)

    def browse_backup_dir(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Backup Directory")
        if folder:
            self.backup_dir_input.setText(folder)

    def update_character_list(self):
        folder = self.save_folder_combo.currentText()
        if folder != "Select Steam ID":
            folder_path = os.path.join(os.environ['APPDATA'], 'EldenRing', folder)
            save_file = find_save_file(folder_path)
            if save_file:
                self.character_info = read_save_file(save_file)
                # Notify game session tab to update its character list
                if hasattr(self.main_window, 'game_session_tab'):
                    self.main_window.game_session_tab.update_character_list(self.character_info)
        else:
            if hasattr(self.main_window, 'game_session_tab'):
                self.main_window.game_session_tab.update_character_list([])

    def find_steam_path(self):
        try:
            program_files_paths = [
                os.path.join(drive + ":\\Program Files (x86)\\Steam\\Steam.exe") 
                for drive in "CDEFGHIJKLMNOPQRSTUVWXYZ"
            ]
            program_files_paths.extend([
                os.path.join(drive + ":\\Program Files\\Steam\\Steam.exe") 
                for drive in "CDEFGHIJKLMNOPQRSTUVWXYZ"
            ])
            
            for path in program_files_paths:
                if os.path.exists(path):
                    return path
                    
            return None
        except Exception as e:
            return None

    def auto_detect_steam_path(self):
        try:
            steam_path = self.find_steam_path()
            if steam_path:
                self.steam_exe_input.setText(steam_path)
                QMessageBox.information(
                    self,
                    self.Localization.translate("lables.success"),
                    self.Localization.translate("ui.settings.steam.steam_found")
                )
            else:
                QMessageBox.warning(
                    self,
                    self.Localization.translate("lables.error"),
                    self.Localization.translate("ui.settings.steam.steam_not_found")
                )
        except Exception as e:
            QMessageBox.warning(
                self,
                self.Localization.translate("messages.error"),
                str(e)
            )

    def is_steam_running(self):
        try:
            cmd = 'tasklist /FI "IMAGENAME eq steam.exe" /FI "SESSIONNAME eq Console"'
            output = subprocess.check_output(cmd, shell=True, text=True)
            if "steam.exe" in output.lower():
                return True

            cmd = 'wmic process where "name=\'steam.exe\'" get processid'
            output = subprocess.check_output(cmd, shell=True, text=True)
            if len(output.strip().split('\n')) > 1:
                return True

            return False
        except Exception as e:
            return False

    def update_steam_status(self):
        is_running = self.is_steam_running()
        status_text = f"{self.Localization.translate('ui.settings.steam.steam_stauts')}: {self.Localization.translate('ui.settings.steam.running' if is_running else 'ui.settings.steam.not_running')}"
        self.steam_status_label.setText(status_text)
        self.steam_status_label.setStyleSheet("color: green;" if is_running else "color: red;")

    def on_steam_silent_changed(self, state):
        if state:
            if not self.steam_exe_input.text():
                self.auto_detect_steam_path()
            
            if not os.path.exists(self.steam_exe_input.text()):
                QMessageBox.warning(
                    self,
                    self.Localization.translate("lables.error"),
                    self.Localization.translate("ui.settings.steam.steam_path_required")
                )
                self.run_steam_silently.setChecked(False)

    def browse_steam(self):
        file_filter = "Steam Executable (Steam.exe);;All files (*.*)"
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            self.Localization.translate("ui.settings.launcher.select_steam_exe"),
            "",
            file_filter
        )
        if file_path:
            self.steam_exe_input.setText(file_path)

    def browse_exe(self):
        file_filter = "Executable files (*.exe *.bat);;All files (*.*)"
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            self.Localization.translate("ui.settings.launcher.select_game_exe"),
            "",
            file_filter
        )
        if file_path:
            self.game_exe_input.setText(file_path)

    def browse_path(self):
        folder = QFileDialog.getExistingDirectory(self, self.Localization.translate("ui.settings.game_path.select_game_folder"))
        if folder:
            self.path_input.setText(folder)

    def get_settings_path(self):
        app_data = os.path.join(os.environ['APPDATA'], 'SeamlessCo-opUpdater')
        if not os.path.exists(app_data):
            os.makedirs(app_data)
        return os.path.join(app_data, 'settings.ini')

    def save_settings(self):
        try:
            config = ConfigParser()
            config['Settings'] = {
                'preferred_language': self.Localization.language,
                'mod_path': self.path_input.text(),
                'game_exe_path': self.game_exe_input.text(),
                'steam_exe_path': self.steam_exe_input.text(),
                'auto_check_updates': str(int(self.auto_check_updates.isChecked())),
                'run_steam_silently': str(int(self.run_steam_silently.isChecked())),
                'steam_id': self.save_folder_combo.currentText(),
                'save_file_type': self.save_file_combo.currentText(),
                'backup_directory': self.backup_dir_input.text(),
                'enable_sounds': str(int(self.enable_sounds.isChecked())),
                'auto_backup_interval': str(self.auto_backup_interval.value()),
                'max_backups': str(self.max_backups.value()),
                'save_backup_key': self.save_backup_key.keySequence().toString(),
                'load_backup_key': self.load_backup_key.keySequence().toString(),
                'start_auto_backup_key': self.start_auto_backup_key.keySequence().toString(),
                'stop_auto_backup_key': self.stop_auto_backup_key.keySequence().toString(),
            }

            settings_path = self.get_settings_path()
            with open(settings_path, 'w') as configfile:
                config.write(configfile)

            QMessageBox.information(self, self.Localization.translate("ui.settings.settings_saved"), 
                                self.Localization.translate("ui.settings.saved_message").format(settings_path))
                
        except Exception as e:
            import traceback
            traceback.print_exc()

    def load_settings(self):
        config = ConfigParser()
        settings_path = self.get_settings_path()
        if os.path.exists(settings_path):
            config.read(settings_path)
            settings = config['Settings']

            self.path_input.setText(settings.get('mod_path', ''))
            self.game_exe_input.setText(settings.get('game_exe_path', ''))
            self.steam_exe_input.setText(settings.get('steam_exe_path', ''))
            self.auto_check_updates.setChecked(bool(int(settings.get('auto_check_updates', '0'))))
            self.run_steam_silently.setChecked(bool(int(settings.get('run_steam_silently', '0'))))
            
            # Load backup settings
            steam_id = settings.get('steam_id', '')
            if steam_id and steam_id in [self.save_folder_combo.itemText(i) for i in range(self.save_folder_combo.count())]:
                self.save_folder_combo.setCurrentText(steam_id)
            
            self.save_file_combo.setCurrentText(settings.get('save_file_type', 'ER0000.co2'))
            self.backup_dir_input.setText(settings.get('backup_directory', ''))
            self.enable_sounds.setChecked(bool(int(settings.get('enable_sounds', '0'))))
            self.auto_backup_interval.setValue(int(settings.get('auto_backup_interval', '5')))
            self.max_backups.setValue(int(settings.get('max_backups', '20')))
            
            # Load key bindings
            self.save_backup_key.setKeySequence(settings.get('save_backup_key', ''))
            self.load_backup_key.setKeySequence(settings.get('load_backup_key', ''))
            self.start_auto_backup_key.setKeySequence(settings.get('start_auto_backup_key', ''))
            self.stop_auto_backup_key.setKeySequence(settings.get('stop_auto_backup_key', ''))
            
            preferred_language = settings.get('preferred_language', 'en')
            self.language_selector.setCurrentText(preferred_language)

        else:
            self.set_default_values()

    def set_default_values(self):
        self.language_selector.setCurrentText('en')
        self.path_input.setText('')
        self.game_exe_input.setText('')
        self.steam_exe_input.setText('')
        self.auto_check_updates.setChecked(True)
        self.run_steam_silently.setChecked(False)
        self.save_file_combo.setCurrentText('ER0000.co2')
        self.auto_backup_interval.setValue(5)
        self.max_backups.setValue(20)
        self.enable_sounds.setChecked(True)
