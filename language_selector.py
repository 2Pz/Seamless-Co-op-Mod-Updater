# language_selector.py

import os
import json
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QComboBox, QLabel, QMessageBox
from utility.resource_ import resource_path
from utility.savefile_reader import get_save_folders


RTL_LANGUAGES = {'ar', 'arc', 'dv', 'fa', 'ha', 'he', 'khw', 'ks', 'ku', 'ps', 'ur', 'yi'}

class LanguageSelector(QComboBox):
    def __init__(self, localization, main_window):
        super().__init__()
        self.localization = localization
        self.main_window = main_window
        self.languages = self.load_languages()
        self.addItems([lang['language_name'] for lang in self.languages])
        self.setCurrentText(self.get_current_language_name())
        self.currentIndexChanged.connect(self.change_language)
        
    def load_languages(self):
        languages = []
        localization_path = resource_path('localization')
        for filename in os.listdir(localization_path):
            if filename.endswith('.json'):
                file_path = os.path.join(localization_path, filename)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        languages.append({
                            'filename': filename,
                            'language_name': data.get('language_name', filename.split('.')[0])
                        })
                except (FileNotFoundError, json.JSONDecodeError):
                    print(f"Error loading localization file: {file_path}")
        return languages

    def get_current_language_name(self):
        current_language = self.localization.language
        for lang in self.languages:
            if lang['filename'].startswith(current_language):
                return lang['language_name']
        return 'English'  # This fallback might be the issue if the language is not found

    
    def change_language(self, index):
        try:
            selected_language = self.languages[index]['filename'].split('.')[0]
            self.localization.language = selected_language
            self.localization.load_localization()
            self.update_main_window_ui()
            self.update_settings_tab_ui()
            self.update_ersc_settings_tab_ui()
            self.update_save_backup_tab()
            self.update_game_session_tab()
            
            self.set_layout_direction(selected_language)
        except Exception as e:
            print(e)


    def set_layout_direction(self, language):
        """Set the layout direction dynamically based on the language."""
        if language in RTL_LANGUAGES:
            self.main_window.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        else:
            self.main_window.setLayoutDirection(Qt.LayoutDirection.LeftToRight)

    def update_main_window_ui(self):
        # Update window title
        self.main_window.setWindowTitle(self.localization.translate("ui.main_window.title"))
        
        # Update tab names
        self.main_window.button_group[0].setText(self.localization.translate("ui.main_window.tabs.main"))
        self.main_window.button_group[1].setText(self.localization.translate("ui.main_window.tabs.ersc_settings"))
        self.main_window.button_group[2].setText(self.localization.translate("ui.main_window.tabs.game_session"))
        self.main_window.button_group[3].setText(self.localization.translate("ui.main_window.tabs.save_backup"))
        self.main_window.button_group[4].setText(self.localization.translate("ui.main_window.tabs.settings"))
        
        # Update menu items
        help_menu = self.main_window.menu_bar.actions()[0]
        help_menu.setText(self.localization.translate("ui.main_window.menu.help"))
        help_menu.menu().actions()[0].setText(self.localization.translate("ui.main_window.menu.check_app_updates"))
        help_menu.menu().actions()[1].setText(self.localization.translate("ui.main_window.menu.check_mod_updates"))
        help_menu.menu().actions()[2].setText(self.localization.translate("ui.main_window.tabs.readme"))
        help_menu.menu().actions()[3].setText(self.localization.translate("ui.main_window.tabs.changlog"))
        help_menu.menu().actions()[4].setText(self.localization.translate("ui.main_window.menu.about"))

        # Update Seamless Co-op Launche button
        self.main_window.launch_button.setText(self.localization.translate("ui.main.launch_button"))

        # Update status labels
        self.main_window.version_label.setText(
            self.localization.translate("ui.main_window.status.version.app").format(self.main_window.get_version())
        )
        self.main_window.dll_version_label.setText(
            self.localization.translate("ui.main_window.status.version.mod.unknown")
        )
        
        # Re-Call .dll version check function
        self.main_window.update_dll_version_label()

    def update_game_session_tab(self):
        game_session_tab = self.main_window.game_session_tab
        
        # Store current character data and selection
        current_characters = []
        for i in range(game_session_tab.character_combo.count()):
            data = game_session_tab.character_combo.itemData(i)
            if data:  # Skip the first item (select character) which has no data
                current_characters.append(data)
        
        # Update UI elements
        game_session_tab.search_input.setPlaceholderText(self.localization.translate("ui.game_session.search_placeholder"))
        game_session_tab.session_table.setHorizontalHeaderLabels([
            self.localization.translate("ui.game_session.username"),
            self.localization.translate("ui.game_session.message"),
            self.localization.translate("ui.game_session.password")
        ])
        
        game_session_tab.game_session_group.setTitle(self.localization.translate("ui.settings.game_session.title"))
        game_session_tab.username_label.setText(self.localization.translate("ui.settings.game_session.username"))
        game_session_tab.message_label.setText(self.localization.translate("ui.settings.game_session.message"))
        game_session_tab.share_game_session.setText(self.localization.translate("ui.settings.game_session.share"))
        
        game_session_tab.character_group.setTitle(self.localization.translate("ui.settings.game_session.character"))
        game_session_tab.character_label.setText(self.localization.translate("ui.settings.game_session.character"))
        
        # Store currently selected index
        current_index = game_session_tab.character_combo.currentIndex()
        
        # Clear and update character combo box with stored data
        if current_characters:
            game_session_tab.update_character_list(current_characters)
            # Restore the previous selection if valid
            if current_index < game_session_tab.character_combo.count():
                game_session_tab.character_combo.setCurrentIndex(current_index)
        
        game_session_tab.refresh_button.setText(self.localization.translate("ui.game_session.refresh"))

    def update_settings_tab_ui(self):
        settings_tab = self.main_window.settings_tab

        # App language
        settings_tab.language_group1.setTitle(self.localization.translate("ui.settings.language.title"))
        settings_tab.select_language.setText(self.localization.translate("ui.settings.language.select_language"))

        # Game Path
        settings_tab.game_path.setText(self.localization.translate("ui.settings.game_path.label"))

        # Seamless Co-op launcher
        settings_tab.launcher_group.setTitle(self.localization.translate("ui.settings.launcher.title"))
        settings_tab.game_exe_label.setText(self.localization.translate("ui.settings.launcher.game_exe"))
        settings_tab.browse_exe_button.setText(self.localization.translate("ui.settings.game_path.browse_button"))
        settings_tab.auto_check_updates.setText(self.localization.translate("ui.settings.launcher.auto_check_updates"))
        
        # Update group box titles
        settings_tab.path_group.setTitle(self.localization.translate("ui.settings.game_path.title"))

        # Update Steam Settings
        settings_tab.steam_group.setTitle(self.localization.translate("ui.settings.steam.steam_settings"))
        settings_tab.auto_detect_steam.setText(self.localization.translate("ui.settings.steam.auto_detect"))
        settings_tab.run_steam_silently.setText(self.localization.translate("ui.settings.steam.run_steam_silently"))
        settings_tab.steam_exe_label.setText(self.localization.translate("ui.settings.steam.steam_exe"))
        is_running = settings_tab.is_steam_running()
        status_text = f"{self.localization.translate('ui.settings.steam.steam_stauts')}: {self.localization.translate('ui.settings.steam.running' if is_running else 'ui.settings.steam.not_running')}"
        settings_tab.steam_status_label.setStyleSheet("color: green;" if is_running else "color: red;")
        settings_tab.steam_status_label.setText(status_text)
        settings_tab.browse_steam_button.setText(self.localization.translate("ui.settings.game_path.browse_button"))

        settings_tab.save_folder_label.setText(self.localization.translate("ui.settings.game_session.save_folder"))
        settings_tab.save_folder_combo.addItem(self.localization.translate("ui.settings.game_session.save_folder_select"))

        settings_tab.backup_group.setTitle(self.localization.translate("ui.settings.backup.backup_settings"))
        settings_tab.save_file_label.setText(self.localization.translate("ui.settings.backup.save_file_type"))
        settings_tab.backup_dir_label.setText(self.localization.translate("ui.settings.backup.dir"))
        settings_tab.auto_backup_label.setText(self.localization.translate("ui.settings.backup.backup_Interval"))
        settings_tab.max_backups_label.setText(self.localization.translate("ui.settings.backup.max_backups"))
        settings_tab.enable_sounds.setText(self.localization.translate("ui.settings.backup.backup_notify"))

        # Update key bindings group title without clearing the layout
        settings_tab.key_bindings_group.setTitle(self.localization.translate("ui.settings.backup.key_binds"))

        # Instead of clearing and recreating the layout, just update the existing labels
        bindings = [
            (self.localization.translate("ui.save_backup.save_backup"), "save_backup_key"),
            (self.localization.translate("ui.save_backup.load_backup"), "load_backup_key"),
            (self.localization.translate("ui.save_backup.start_auto_backup"), "start_auto_backup_key"),
            (self.localization.translate("ui.save_backup.stop_auto_backup"), "stop_auto_backup_key"),
        ]

        # Update existing labels without recreating the widgets
        for i, (label_text, key_name) in enumerate(bindings):
            # Get the label widget from the layout at position (i, 0)
            label_item = settings_tab.key_bindings_layout.itemAtPosition(i, 0)
            if label_item and label_item.widget():
                label = label_item.widget()
                if isinstance(label, QLabel):
                    label.setText(label_text)
            else:
                # Only create new widgets if they don't exist
                label = QLabel(label_text)
                key_edit = getattr(settings_tab, key_name)
                settings_tab.key_bindings_layout.addWidget(label, i, 0)
                settings_tab.key_bindings_layout.addWidget(key_edit, i, 1)

        # No need to call updateGeometry() as we're not recreating the layout
        settings_tab.key_bindings_group.update()

        # Update buttons
        settings_tab.browse_button.setText(self.localization.translate("ui.settings.game_path.browse_button"))
        settings_tab.browse_backup_button.setText(self.localization.translate("ui.settings.game_path.browse_button"))
        settings_tab.save_button.setText(self.localization.translate("ui.settings.save_button"))

        # Refresh the UI to ensure all changes are visible
        self.main_window.update()

    def update_ersc_settings_tab_ui(self):
        ersc_settings_tab = self.main_window.ersc_settings_tab
        # Add this to the update_settings_tab_ui method
        scaling_settings = [
            ("enemy_health_scaling", self.localization.translate("ui.settings.scaling.enemy_health")),
            ("enemy_damage_scaling", self.localization.translate("ui.settings.scaling.enemy_damage")),
            ("enemy_posture_scaling", self.localization.translate("ui.settings.scaling.enemy_posture")),
            ("boss_health_scaling", self.localization.translate("ui.settings.scaling.boss_health")),
            ("boss_damage_scaling", self.localization.translate("ui.settings.scaling.boss_damage")),
            ("boss_posture_scaling", self.localization.translate("ui.settings.scaling.boss_posture")),
        ]

        # Now update the labels in the scaling layout
        for i, (key, new_label_text) in enumerate(scaling_settings):
            # Find the QLabel in the scaling layout at row i, column 0
            label_item = ersc_settings_tab.scaling_group.layout().itemAtPosition(i, 0)
            if label_item and label_item.widget():
                label_widget = label_item.widget()
                if isinstance(label_widget, QLabel):
                    label_widget.setText(new_label_text)

        # Update checkboxes
        ersc_settings_tab.allow_invaders.setText(self.localization.translate("ui.settings.gameplay.allow_invaders"))
        ersc_settings_tab.death_debuffs.setText(self.localization.translate("ui.settings.gameplay.death_debuffs"))
        ersc_settings_tab.allow_summons.setText(self.localization.translate("ui.settings.gameplay.allow_summons"))
        ersc_settings_tab.skip_splash_screens.setText(self.localization.translate("ui.settings.gameplay.skip_splash"))
        ersc_settings_tab.overhead_display.setText(self.localization.translate("ui.settings.gameplay.overhead_display"))
        ersc_settings_tab.master_volume.setText(self.localization.translate("ui.settings.gameplay.volume"))

        # Update ComboBox items
        current_index = ersc_settings_tab.overhead_player_display.currentIndex()
        ersc_settings_tab.overhead_player_display.clear()
        ersc_settings_tab.overhead_player_display.addItems([
            self.localization.translate("ui.settings.gameplay.display_options.normal"),
            self.localization.translate("ui.settings.gameplay.display_options.none"),
            self.localization.translate("ui.settings.gameplay.display_options.player_ping"),
            self.localization.translate("ui.settings.gameplay.display_options.player_soul_level"),
            self.localization.translate("ui.settings.gameplay.display_options.player_death_count"),
            self.localization.translate("ui.settings.gameplay.display_options.soul_level_and_ping")
        ])
        ersc_settings_tab.overhead_player_display.setCurrentIndex(current_index)

        # Update group box titles
        ersc_settings_tab.gameplay_group.setTitle(self.localization.translate("ui.settings.gameplay.title"))
        ersc_settings_tab.scaling_group.setTitle(self.localization.translate("ui.settings.scaling.title"))
        ersc_settings_tab.password_group.setTitle(self.localization.translate("ui.settings.password.title"))
        ersc_settings_tab.save_group.setTitle(self.localization.translate("ui.settings.save.title"))
        
        # Update Password
        ersc_settings_tab.password.setText(self.localization.translate("ui.settings.password.coop_password"))

        # Update extension
        ersc_settings_tab.extension.setText(self.localization.translate("ui.settings.save.extension"))

        # Update Language override
        ersc_settings_tab.language_group.setTitle(self.localization.translate("ui.settings.language.title"))
        ersc_settings_tab.lang_override.setText(self.localization.translate("ui.settings.language.override"))

        # Update buttons
        ersc_settings_tab.save_button.setText(self.localization.translate("ui.settings.save_button"))
        ersc_settings_tab.reset_button.setText(self.localization.translate("ui.settings.reset_button"))

    def update_save_backup_tab(self):
        """Update the save backup tab UI with translated text"""
        backup_tab = self.main_window.save_backup_tab
        
        # Update table headers
        backup_tab.backup_table.setHorizontalHeaderLabels([
            self.localization.translate("ui.save_backup.backup_name"),
            self.localization.translate("ui.save_backup.date")
        ])
        
        # Update auto backup status
        if backup_tab.auto_backup_timer and backup_tab.auto_backup_timer.isActive():
            interval = int(self.main_window.get_settings().get('auto_backup_interval', '5'))
            backup_tab.auto_backup_status.setText(
                self.localization.translate("ui.save_backup.auto_backup_running").format(interval)
            )
        else:
            backup_tab.auto_backup_status.setText(
                self.localization.translate("ui.save_backup.auto_backup_not_running")
            )
        
        # Update buttons
        backup_tab.save_button.setText(self.localization.translate("ui.save_backup.save_backup"))
        backup_tab.load_button.setText(self.localization.translate("ui.save_backup.load_backup"))
        backup_tab.delete_button.setText(self.localization.translate("ui.save_backup.delete"))
        backup_tab.refresh_button.setText(self.localization.translate("ui.game_session.refresh"))
        backup_tab.start_auto_backup_button.setText(self.localization.translate("ui.save_backup.start_auto_backup"))
        backup_tab.stop_auto_backup_button.setText(self.localization.translate("ui.save_backup.stop_auto_backup"))
