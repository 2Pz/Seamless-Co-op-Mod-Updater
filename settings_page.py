import os
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, 
                             QPushButton, QLineEdit, QLabel, QFileDialog, 
                             QMessageBox, QGridLayout,
                             QCheckBox, QSpinBox, QComboBox, QGroupBox, QScrollArea)
from configparser import ConfigParser
import os
from version_checker import check_for_updates
from config import APP_VERSION

class SettingsPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        layout.addWidget(scroll_area)

        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)

        # Game Path
        path_group = QGroupBox("Game Path")
        path_layout = QGridLayout()
        path_group.setLayout(path_layout)

        path_layout.addWidget(QLabel("Game Path:"), 0, 0)
        self.path_input = QLineEdit()
        path_layout.addWidget(self.path_input, 0, 1)
        browse_button = QPushButton("Browse")
        browse_button.clicked.connect(self.browse_path)
        path_layout.addWidget(browse_button, 0, 2)

        scroll_layout.addWidget(path_group)

        # Gameplay settings
        gameplay_group = QGroupBox("Gameplay")
        gameplay_layout = QGridLayout()
        gameplay_group.setLayout(gameplay_layout)

        self.allow_invaders = QCheckBox("Allow Invaders")
        gameplay_layout.addWidget(self.allow_invaders, 0, 0)

        self.death_debuffs = QCheckBox("Death Debuffs")
        gameplay_layout.addWidget(self.death_debuffs, 1, 0)

        self.allow_summons = QCheckBox("Allow Summons")
        gameplay_layout.addWidget(self.allow_summons, 2, 0)

        gameplay_layout.addWidget(QLabel("Overhead Player Display:"), 3, 0)
        self.overhead_player_display = QComboBox()
        self.overhead_player_display.addItems(["Normal", "None", "Player Ping", "Player Soul Level", "Player Death Count", "Soul Level AND Ping"])
        gameplay_layout.addWidget(self.overhead_player_display, 3, 1)

        self.skip_splash_screens = QCheckBox("Skip Splash Screens")
        gameplay_layout.addWidget(self.skip_splash_screens, 4, 0)

        gameplay_layout.addWidget(QLabel("Default Boot Master Volume:"), 5, 0)
        self.default_boot_master_volume = QSpinBox()
        self.default_boot_master_volume.setRange(0, 10)
        gameplay_layout.addWidget(self.default_boot_master_volume, 5, 1)

        scroll_layout.addWidget(gameplay_group)

        # Scaling settings
        scaling_group = QGroupBox("Scaling")
        scaling_layout = QGridLayout()
        scaling_group.setLayout(scaling_layout)

        scaling_settings = [
            ("enemy_health_scaling", "Enemy Health Scaling (%):"),
            ("enemy_damage_scaling", "Enemy Damage Scaling (%):"),
            ("enemy_posture_scaling", "Enemy Posture Scaling (%):"),
            ("boss_health_scaling", "Boss Health Scaling (%):"),
            ("boss_damage_scaling", "Boss Damage Scaling (%):"),
            ("boss_posture_scaling", "Boss Posture Scaling (%):"),
        ]

        for i, (key, label) in enumerate(scaling_settings):
            scaling_layout.addWidget(QLabel(label), i, 0)
            spinbox = QSpinBox()
            spinbox.setRange(0, 200)
            scaling_layout.addWidget(spinbox, i, 1)
            setattr(self, key, spinbox)

        scroll_layout.addWidget(scaling_group)

        # Password settings
        password_group = QGroupBox("Password")
        password_layout = QGridLayout()
        password_group.setLayout(password_layout)

        password_layout.addWidget(QLabel("Coop Password:"), 0, 0)
        self.cooppassword = QLineEdit()
        password_layout.addWidget(self.cooppassword, 0, 1)

        scroll_layout.addWidget(password_group)

        # Save settings
        save_group = QGroupBox("Save")
        save_layout = QGridLayout()
        save_group.setLayout(save_layout)

        save_layout.addWidget(QLabel("Save File Extension:"), 0, 0)
        self.save_file_extension = QLineEdit()
        save_layout.addWidget(self.save_file_extension, 0, 1)

        scroll_layout.addWidget(save_group)

        # Language settings
        language_group = QGroupBox("Language")
        language_layout = QGridLayout()
        language_group.setLayout(language_layout)

        language_layout.addWidget(QLabel("Mod Language Override:"), 0, 0)
        self.mod_language_override = QLineEdit()
        language_layout.addWidget(self.mod_language_override, 0, 1)

        scroll_layout.addWidget(language_group)

        scroll_area.setWidget(scroll_content)

        # Add Update group
        update_group = QGroupBox("Update")
        update_layout = QGridLayout()
        update_group.setLayout(update_layout)

        self.check_updates_button = QPushButton("Check for Updates")
        self.check_updates_button.clicked.connect(self.check_for_updates)
        update_layout.addWidget(self.check_updates_button, 0, 0)

        self.update_status_label = QLabel("No updates available")
        update_layout.addWidget(self.update_status_label, 0, 1)

        scroll_layout.addWidget(update_group)

        scroll_area.setWidget(scroll_content)

        # Save button
        save_button = QPushButton("Save Settings")
        save_button.clicked.connect(self.save_settings)
        layout.addWidget(save_button)

        self.load_settings()

    def check_for_updates(self):
        self.update_status_label.setText("Checking for updates...")
        update_available, latest_version, download_url = check_for_updates(APP_VERSION)
        
        if update_available:
            self.update_status_label.setText(f"Update available: v{latest_version}")
            reply = QMessageBox.question(self, 'Update Available', 
                                         f"A new version ({latest_version}) is available. Do you want to update?",
                                         QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, 
                                         QMessageBox.StandardButton.No)
            if reply == QMessageBox.StandardButton.Yes:
                self.parent().parent().update_application(download_url, latest_version)
        else:
            self.update_status_label.setText("No updates available")

    def browse_path(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Elden Ring Game Folder")
        if folder:
            self.path_input.setText(folder)

    def get_settings_path(self):
        app_data = os.path.join(os.environ['APPDATA'], 'EldenRingModUpdater')
        if not os.path.exists(app_data):
            os.makedirs(app_data)
        return os.path.join(app_data, 'settings.ini')

    def save_settings(self):
        config = ConfigParser()
        config['Settings'] = {
            'mod_path': self.path_input.text(),
            'allow_invaders': str(int(self.allow_invaders.isChecked())),
            'death_debuffs': str(int(self.death_debuffs.isChecked())),
            'allow_summons': str(int(self.allow_summons.isChecked())),
            'overhead_player_display': str(self.overhead_player_display.currentIndex()),
            'skip_splash_screens': str(int(self.skip_splash_screens.isChecked())),
            'default_boot_master_volume': str(self.default_boot_master_volume.value()),
            'enemy_health_scaling': str(self.enemy_health_scaling.value()),
            'enemy_damage_scaling': str(self.enemy_damage_scaling.value()),
            'enemy_posture_scaling': str(self.enemy_posture_scaling.value()),
            'boss_health_scaling': str(self.boss_health_scaling.value()),
            'boss_damage_scaling': str(self.boss_damage_scaling.value()),
            'boss_posture_scaling': str(self.boss_posture_scaling.value()),
            'cooppassword': self.cooppassword.text(),
            'save_file_extension': self.save_file_extension.text(),
            'mod_language_override': self.mod_language_override.text()
        }

        settings_path = self.get_settings_path()
        with open(settings_path, 'w') as configfile:
            config.write(configfile)

        QMessageBox.information(self, "Settings Saved", f"Your settings have been saved to {settings_path}")

    def load_settings(self):
        config = ConfigParser()
        settings_path = self.get_settings_path()
        if os.path.exists(settings_path):
            config.read(settings_path)
            settings = config['Settings']

            self.path_input.setText(settings.get('mod_path', ''))
            self.allow_invaders.setChecked(bool(int(settings.get('allow_invaders', '0'))))
            self.death_debuffs.setChecked(bool(int(settings.get('death_debuffs', '1'))))
            self.allow_summons.setChecked(bool(int(settings.get('allow_summons', '1'))))
            self.overhead_player_display.setCurrentIndex(int(settings.get('overhead_player_display', '3')))
            self.skip_splash_screens.setChecked(bool(int(settings.get('skip_splash_screens', '1'))))
            self.default_boot_master_volume.setValue(int(settings.get('default_boot_master_volume', '2')))

            self.enemy_health_scaling.setValue(int(settings.get('enemy_health_scaling', '35')))
            self.enemy_damage_scaling.setValue(int(settings.get('enemy_damage_scaling', '0')))
            self.enemy_posture_scaling.setValue(int(settings.get('enemy_posture_scaling', '15')))
            self.boss_health_scaling.setValue(int(settings.get('boss_health_scaling', '100')))
            self.boss_damage_scaling.setValue(int(settings.get('boss_damage_scaling', '0')))
            self.boss_posture_scaling.setValue(int(settings.get('boss_posture_scaling', '20')))

            self.cooppassword.setText(settings.get('cooppassword', '12345'))
            self.save_file_extension.setText(settings.get('save_file_extension', 'co2'))
            self.mod_language_override.setText(settings.get('mod_language_override', ''))
        else:
            # If the settings file doesn't exist, use default values
            self.set_default_values()

    def set_default_values(self):
        # Set default values for all settings
        self.path_input.setText('')
        self.allow_invaders.setChecked(True)
        self.death_debuffs.setChecked(True)
        self.allow_summons.setChecked(True)
        self.overhead_player_display.setCurrentIndex(0)
        self.skip_splash_screens.setChecked(False)
        self.default_boot_master_volume.setValue(5)
        self.enemy_health_scaling.setValue(35)
        self.enemy_damage_scaling.setValue(0)
        self.enemy_posture_scaling.setValue(15)
        self.boss_health_scaling.setValue(100)
        self.boss_damage_scaling.setValue(0)
        self.boss_posture_scaling.setValue(20)
        self.cooppassword.setText('12345')
        self.save_file_extension.setText('co2')
        self.mod_language_override.setText('')


    def get_settings(self):
        return {
            "allow_invaders": int(self.allow_invaders.isChecked()),
            "death_debuffs": int(self.death_debuffs.isChecked()),
            "allow_summons": int(self.allow_summons.isChecked()),
            "overhead_player_display": self.overhead_player_display.currentIndex(),
            "skip_splash_screens": int(self.skip_splash_screens.isChecked()),
            "default_boot_master_volume": self.default_boot_master_volume.value(),
            "enemy_health_scaling": self.enemy_health_scaling.value(),
            "enemy_damage_scaling": self.enemy_damage_scaling.value(),
            "enemy_posture_scaling": self.enemy_posture_scaling.value(),
            "boss_health_scaling": self.boss_health_scaling.value(),
            "boss_damage_scaling": self.boss_damage_scaling.value(),
            "boss_posture_scaling": self.boss_posture_scaling.value(),
            "cooppassword": self.cooppassword.text(),
            "save_file_extension": self.save_file_extension.text(),
            "mod_language_override": self.mod_language_override.text()
        }