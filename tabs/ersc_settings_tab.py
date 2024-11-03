from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QLineEdit, QLabel, 
                             QGridLayout, QCheckBox, QSpinBox, QComboBox, 
                             QGroupBox, QScrollArea, QPushButton, QMessageBox)
from configparser import ConfigParser
import os

class ERSCSettingsTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.Localization = parent.Localization if parent else None
        self.main_window = parent
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        layout.addWidget(scroll_area)

        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)

        # Gameplay settings
        self.gameplay_group = QGroupBox(self.Localization.translate("ui.settings.gameplay.title"))
        gameplay_layout = QGridLayout()
        self.gameplay_group.setLayout(gameplay_layout)

        self.allow_invaders = QCheckBox(self.Localization.translate("ui.settings.gameplay.allow_invaders"))
        gameplay_layout.addWidget(self.allow_invaders, 0, 0)

        self.death_debuffs = QCheckBox(self.Localization.translate("ui.settings.gameplay.death_debuffs"))
        gameplay_layout.addWidget(self.death_debuffs, 1, 0)
        
        self.allow_summons = QCheckBox(self.Localization.translate("ui.settings.gameplay.allow_summons"))
        gameplay_layout.addWidget(self.allow_summons, 2, 0)

        self.overhead_display = QLabel(self.Localization.translate("ui.settings.gameplay.overhead_display"))
        gameplay_layout.addWidget(self.overhead_display, 3, 0)
        self.overhead_player_display = QComboBox()
        self.overhead_player_display.addItems([
            self.Localization.translate("ui.settings.gameplay.display_options.normal"), 
            self.Localization.translate("ui.settings.gameplay.display_options.none"), 
            self.Localization.translate("ui.settings.gameplay.display_options.player_ping"), 
            self.Localization.translate("ui.settings.gameplay.display_options.player_soul_level"), 
            self.Localization.translate("ui.settings.gameplay.display_options.player_death_count"), 
            self.Localization.translate("ui.settings.gameplay.display_options.soul_level_and_ping")
        ])
        gameplay_layout.addWidget(self.overhead_player_display, 3, 1)

        self.skip_splash_screens = QCheckBox(self.Localization.translate("ui.settings.gameplay.skip_splash"))
        gameplay_layout.addWidget(self.skip_splash_screens, 4, 0)

        self.master_volume = QLabel(self.Localization.translate("ui.settings.gameplay.volume"))
        gameplay_layout.addWidget(self.master_volume, 5, 0)
        self.default_boot_master_volume = QSpinBox()
        self.default_boot_master_volume.setRange(0, 10)
        gameplay_layout.addWidget(self.default_boot_master_volume, 5, 1)

        scroll_layout.addWidget(self.gameplay_group)

        # Scaling settings
        self.scaling_group = QGroupBox(self.Localization.translate("ui.settings.scaling.title"))
        scaling_layout = QGridLayout()
        self.scaling_group.setLayout(scaling_layout)

        scaling_settings = [
            ("enemy_health_scaling", self.Localization.translate("ui.settings.scaling.enemy_health")),
            ("enemy_damage_scaling", self.Localization.translate("ui.settings.scaling.enemy_damage")),
            ("enemy_posture_scaling", self.Localization.translate("ui.settings.scaling.enemy_posture")),
            ("boss_health_scaling", self.Localization.translate("ui.settings.scaling.boss_health")),
            ("boss_damage_scaling", self.Localization.translate("ui.settings.scaling.boss_damage")),
            ("boss_posture_scaling", self.Localization.translate("ui.settings.scaling.boss_posture")),
        ]

        for i, (key, label) in enumerate(scaling_settings):
            scaling_layout.addWidget(QLabel(label), i, 0)
            spinbox = QSpinBox()
            spinbox.setRange(0, 1000)
            scaling_layout.addWidget(spinbox, i, 1)
            setattr(self, key, spinbox)

        scroll_layout.addWidget(self.scaling_group)

        # Password settings
        self.password_group = QGroupBox(self.Localization.translate("ui.settings.password.title"))
        password_layout = QGridLayout()
        self.password_group.setLayout(password_layout)

        self.password = QLabel(self.Localization.translate("ui.settings.password.coop_password"))
        password_layout.addWidget(self.password, 0, 0)
        self.cooppassword = QLineEdit()
        password_layout.addWidget(self.cooppassword, 0, 1)

        scroll_layout.addWidget(self.password_group)

        # Save settings
        self.save_group = QGroupBox(self.Localization.translate("ui.settings.save.title"))
        save_layout = QGridLayout()
        self.save_group.setLayout(save_layout)
        
        self.extension = QLabel(self.Localization.translate("ui.settings.save.extension"))
        save_layout.addWidget(self.extension, 0, 0)
        self.save_file_extension = QLineEdit()
        save_layout.addWidget(self.save_file_extension, 0, 1)

        scroll_layout.addWidget(self.save_group)

        # Language settings
        self.language_group = QGroupBox(self.Localization.translate("ui.settings.language.title"))
        language_layout = QGridLayout()
        self.language_group.setLayout(language_layout)

        self.lang_override = QLabel(self.Localization.translate("ui.settings.language.override"))
        language_layout.addWidget(self.lang_override, 0, 0)
        self.mod_language_override = QLineEdit()
        language_layout.addWidget(self.mod_language_override, 0, 1)

        scroll_layout.addWidget(self.language_group)

        scroll_area.setWidget(scroll_content)

        # Buttons layout
        buttons_layout = QVBoxLayout()
        
        # Save button
        self.save_button = QPushButton(self.Localization.translate("ui.settings.save_button"))
        self.save_button.clicked.connect(self.save_settings)
        buttons_layout.addWidget(self.save_button)

        # Reset button
        self.reset_button = QPushButton(self.Localization.translate("ui.settings.reset_button"))
        self.reset_button.clicked.connect(self.reset_settings)
        buttons_layout.addWidget(self.reset_button)

        layout.addLayout(buttons_layout)

        # Set default values first, then try to load saved settings
        self.set_default_values()
        self.load_settings()

    def get_settings(self):
        return {
            "allow_invaders": str(int(self.allow_invaders.isChecked())),
            "death_debuffs": str(int(self.death_debuffs.isChecked())),
            "allow_summons": str(int(self.allow_summons.isChecked())),
            "overhead_player_display": str(self.overhead_player_display.currentIndex()),
            "skip_splash_screens": str(int(self.skip_splash_screens.isChecked())),
            "default_boot_master_volume": str(self.default_boot_master_volume.value()),
            "enemy_health_scaling": str(self.enemy_health_scaling.value()),
            "enemy_damage_scaling": str(self.enemy_damage_scaling.value()),
            "enemy_posture_scaling": str(self.enemy_posture_scaling.value()),
            "boss_health_scaling": str(self.boss_health_scaling.value()),
            "boss_damage_scaling": str(self.boss_damage_scaling.value()),
            "boss_posture_scaling": str(self.boss_posture_scaling.value()),
            "cooppassword": self.cooppassword.text(),
            "save_file_extension": self.save_file_extension.text(),
            "mod_language_override": self.mod_language_override.text(),
        }

    def get_game_path(self):
        """Get the game path from the settings tab"""
        if hasattr(self.main_window, 'settings_tab') and self.main_window.settings_tab:
            return self.main_window.settings_tab.path_input.text()
        return None

    def get_settings_path(self):
        app_data = os.path.join(os.environ['APPDATA'], 'SeamlessCo-opUpdater')
        if not os.path.exists(app_data):
            os.makedirs(app_data)
        return os.path.join(app_data, 'ersc_settings.ini')

    def save_settings(self):
        try:
            settings_path = self.get_settings_path()
            if not settings_path:
                return

            config = ConfigParser()
            config['Settings'] = self.get_settings()

            with open(settings_path, 'w') as configfile:
                config.write(configfile)


            # Now update the mod's settings file
            
            mod_settings_path = os.path.join(self.get_game_path(), "SeamlessCoop", "ersc_settings.ini")
            if os.path.exists(os.path.dirname(mod_settings_path)):
                mod_config = ConfigParser()
                if os.path.exists(mod_settings_path):
                    mod_config.read(mod_settings_path)

                # Update GAMEPLAY section
                if 'GAMEPLAY' not in mod_config:
                    mod_config['GAMEPLAY'] = {}
                mod_config['GAMEPLAY']['allow_invaders'] = str(int(self.allow_invaders.isChecked()))
                mod_config['GAMEPLAY']['death_debuffs'] = str(int(self.death_debuffs.isChecked()))
                mod_config['GAMEPLAY']['allow_summons'] = str(int(self.allow_summons.isChecked()))
                mod_config['GAMEPLAY']['overhead_player_display'] = str(self.overhead_player_display.currentIndex())
                mod_config['GAMEPLAY']['skip_splash_screens'] = str(int(self.skip_splash_screens.isChecked()))
                mod_config['GAMEPLAY']['default_boot_master_volume'] = str(self.default_boot_master_volume.value())

                # Update SCALING section
                if 'SCALING' not in mod_config:
                    mod_config['SCALING'] = {}
                mod_config['SCALING']['enemy_health_scaling'] = str(self.enemy_health_scaling.value())
                mod_config['SCALING']['enemy_damage_scaling'] = str(self.enemy_damage_scaling.value())
                mod_config['SCALING']['enemy_posture_scaling'] = str(self.enemy_posture_scaling.value())
                mod_config['SCALING']['boss_health_scaling'] = str(self.boss_health_scaling.value())
                mod_config['SCALING']['boss_damage_scaling'] = str(self.boss_damage_scaling.value())
                mod_config['SCALING']['boss_posture_scaling'] = str(self.boss_posture_scaling.value())

                # Update PASSWORD section
                if 'PASSWORD' not in mod_config:
                    mod_config['PASSWORD'] = {}
                mod_config['PASSWORD']['cooppassword'] = self.cooppassword.text()

                # Update SAVE section
                if 'SAVE' not in mod_config:
                    mod_config['SAVE'] = {}
                mod_config['SAVE']['save_file_extension'] = self.save_file_extension.text()

                # Update LANGUAGE section
                if 'LANGUAGE' not in mod_config:
                    mod_config['LANGUAGE'] = {}
                mod_config['LANGUAGE']['mod_language_override'] = self.mod_language_override.text()

            
                try:
                    with open(mod_settings_path, 'w') as configfile:
                        mod_config.write(configfile)
                    QMessageBox.information(self, self.Localization.translate("ui.settings.settings_saved"), 
                                        self.Localization.translate("ui.settings.saved_message").format(f"{settings_path}\n{mod_settings_path}"))
                except Exception as e:
                    QMessageBox.warning(self, self.Localization.translate("ui.settings.settings_error"), 
                                    self.Localization.translate("ui.settings.mod_settings_error").format(str(e)))
            else:
                QMessageBox.warning(self, self.Localization.translate("ui.settings.settings_error"), 
                                self.Localization.translate("ui.settings.mod_path_error"))
                
        except Exception as e:
            #print(f"Error saving settings: {str(e)}")
            import traceback
            traceback.print_exc()
            QMessageBox.critical(self, "Error", f"Failed to save settings: {str(e)}")

    def load_settings(self):
        try:
            settings_path = self.get_settings_path()
            if not settings_path or not os.path.exists(settings_path):
                return

            config = ConfigParser()
            config.read(settings_path)
            
            if 'Settings' not in config:
                return

            settings = config['Settings']

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

        except Exception as e:
            #print(f"Error loading settings: {str(e)}")
            import traceback
            traceback.print_exc()

    def reset_settings(self):
        reply = QMessageBox.question(self, self.Localization.translate("ui.settings.reset_settings"), 
                                   self.Localization.translate("ui.settings.rest_confirmation"),
                                   QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        
        if reply == QMessageBox.StandardButton.Yes:
            self.set_default_values()
            self.save_settings()

    def set_default_values(self):
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
