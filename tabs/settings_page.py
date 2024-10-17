# settings_page.py
import os
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, 
                             QPushButton, QLineEdit, QLabel, QFileDialog, 
                             QMessageBox, QGridLayout,
                             QCheckBox, QSpinBox, QComboBox, QGroupBox, QScrollArea)
from configparser import ConfigParser
from language_selector import LanguageSelector
import aiohttp
from utility.worker import AsyncWorker

class SettingsPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.Localization = parent.Localization if parent else None
        self.main_window = parent
        self.init_ui()

        # Ensure language_selector is properly initialized with main_window
        self.language_selector = LanguageSelector(self.Localization, self.main_window)
        # Connect the language change event
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

        # Game Session settings
        self.game_session_group = QGroupBox(self.Localization.translate("ui.settings.game_session.title"))
        game_session_layout = QGridLayout()
        self.game_session_group.setLayout(game_session_layout)

        self.username_label = QLabel(self.Localization.translate("ui.settings.game_session.username"))
        game_session_layout.addWidget(self.username_label, 0, 0)
        self.username_input = QLineEdit()
        game_session_layout.addWidget(self.username_input, 0, 1)

        self.message_label = QLabel(self.Localization.translate("ui.settings.game_session.message"))
        game_session_layout.addWidget(self.message_label, 1, 0)
        self.message_input = QLineEdit()
        game_session_layout.addWidget(self.message_input, 1, 1)

        self.share_game_session = QCheckBox(self.Localization.translate("ui.settings.game_session.share"))
        game_session_layout.addWidget(self.share_game_session, 2, 0, 1, 2)

        self.share_game_session.stateChanged.connect(self.on_share_game_session_changed)
    
        scroll_layout.addWidget(self.game_session_group)

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
        self.overhead_player_display.addItems([self.Localization.translate("ui.settings.gameplay.display_options.normal"), 
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
            spinbox.setRange(0, 200)
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

        # Save button
        self.save_button = QPushButton(self.Localization.translate("ui.settings.save_button"))
        self.save_button.clicked.connect(self.save_settings)
        layout.addWidget(self.save_button)

        self.load_settings()

        # Update ersc.dll version
        self.path_input.textChanged.connect(self.parent().update_dll_version_label)

        

    async def share_game_session_data(self):
        settings = self.get_settings()
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post("https://seamless-co-op-game-sessions.onrender.com/api/add_session", 
                                        json={
                                            "username": settings['username'],
                                            "message": settings['message'],
                                            "password": settings['cooppassword']
                                        },
                                        timeout=5) as response:  # Add a 5-second timeout
                    if response.status == 200:
                        return True, "Game session shared successfully"
                    else:
                        return False, await response.text()
        except aiohttp.ClientError as e:
            return False, f"Error sharing game session: {str(e)}"
        except Exception as e:
            return False, f"Unexpected error sharing game session: {str(e)}"

    async def remove_game_session_data(self):
        settings = self.get_settings()
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post("https://seamless-co-op-game-sessions.onrender.com/api/remove_session", 
                                        json={
                                            "username": settings['username'],
                                            "action": "remove"
                                        },
                                        timeout=5) as response:  # Add a 5-second timeout
                    if response.status == 200:
                        return True, "Game session removed successfully"
                    else:
                        return False, await response.text()
        except aiohttp.ClientError as e:
            return False, f"Error removing game session: {str(e)}"
        except Exception as e:
            return False, f"Unexpected error removing game session: {str(e)}"

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
                'username': self.username_input.text(),
                'message': self.message_input.text(),
                'share_game_session': str(int(self.share_game_session.isChecked())),
                'preferred_language': self.Localization.language,
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

            # Now update the mod's settings file
            mod_settings_path = os.path.join(self.path_input.text(), "SeamlessCoop", "ersc_settings.ini")
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
            print(f"Error saving settings: {str(e)}")
            import traceback
            traceback.print_exc()

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

            # Other settings...
            preferred_language = settings.get('preferred_language', 'en')  # Default to 'English'
            self.language_selector.setCurrentText(preferred_language)  # Restore selected language

            self.username_input.setText(settings.get('username', ''))
            self.message_input.setText(settings.get('message', ''))
            self.share_game_session.setChecked(bool(int(settings.get('share_game_session', '0'))))
        else:
            # If the settings file doesn't exist, use default values
            self.set_default_values()


    def on_share_game_session_changed(self):
        if self.share_game_session.isChecked():
            self.worker = AsyncWorker(self.share_game_session_data)
            self.worker.finished.connect(self.on_share_game_session_complete)
            self.worker.start()
        else:
            self.worker = AsyncWorker(self.remove_game_session_data)
            self.worker.finished.connect(self.on_remove_game_session_complete)
            self.worker.start()

        # Disable the checkbox while the operation is in progress
        self.share_game_session.setEnabled(True)

    def on_share_game_session_complete(self, success, message):
        self.share_game_session.setEnabled(True)  # Re-enable the checkbox
        if not success:
            self.share_game_session.setChecked(False)
            QMessageBox.warning(self, self.Localization.translate("ui.settings.error"), "messages.errors.share_game_error")

    def on_remove_game_session_complete(self, success, message):
        self.share_game_session.setEnabled(True)  # Re-enable the checkbox
        if not success:
            self.share_game_session.setChecked(False)
            #QMessageBox.warning(self, self.Localization.translate("ui.settings.error"), "messages.errors.share_game_error")




    def set_default_values(self):
        # Set default values for all settings
        self.language_selector.setCurrentText('en')
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
        self.username_input.setText('')
        self.message_input.setText('')
        self.share_game_session.setChecked(False)


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
            "mod_language_override": self.mod_language_override.text(),
            "username": self.username_input.text(),
            "message": self.message_input.text(),
            "share_game_session": int(self.share_game_session.isChecked()),
            
        }
