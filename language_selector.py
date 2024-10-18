# language_selector.py

import os
import json
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QComboBox, QLabel
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

        selected_language = self.languages[index]['filename'].split('.')[0]
        self.localization.language = selected_language
        self.localization.load_localization()
        self.update_main_window_ui()
        self.update_settings_tab_ui()
        self.update_game_session_tab()
        self.set_layout_direction(selected_language)


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
        self.main_window.tab_widget.setTabText(0, self.localization.translate("ui.main_window.tabs.update"))
        self.main_window.tab_widget.setTabText(1, self.localization.translate("ui.main_window.tabs.settings"))
        self.main_window.tab_widget.setTabText(2, self.localization.translate("ui.main_window.tabs.game_session"))
        self.main_window.tab_widget.setTabText(3, self.localization.translate("ui.main_window.tabs.readme"))
        self.main_window.tab_widget.setTabText(4, self.localization.translate("ui.main_window.tabs.changlog"))
        
        # Update menu items
        help_menu = self.main_window.menu_bar.actions()[0]
        help_menu.setText(self.localization.translate("ui.main_window.menu.help"))
        help_menu.menu().actions()[0].setText(self.localization.translate("ui.main_window.menu.check_updates"))
        help_menu.menu().actions()[1].setText(self.localization.translate("ui.main_window.menu.about"))

        # Update status labels
        self.main_window.version_label.setText(
            self.localization.translate("ui.main_window.status.version.app").format(self.main_window.get_version())
        )
        self.main_window.dll_version_label.setText(
            self.localization.translate("ui.main_window.status.version.mod.unknown")
        )
        
        # Update other UI elements in the update tab
        self.main_window.status_label.setText(self.localization.translate("ui.main_window.status_ready"))
        self.main_window.update_button.setText(self.localization.translate("ui.main_window.update_button"))

        
        # Re-Call .dll version check function
        self.main_window.update_dll_version_label()

    def update_game_session_tab(self):
        game_session_tab = self.main_window.game_session_tab
        game_session_tab.search_input.setPlaceholderText(self.localization.translate("ui.game_session.search_placeholder"))
        
        game_session_tab.session_table.setHorizontalHeaderLabels([
        self.localization.translate("ui.game_session.username"),
        self.localization.translate("ui.game_session.message"),
        self.localization.translate("ui.game_session.password")
    ])

        game_session_tab.setWindowTitle(self.localization.translate("ui.game_session.stat.stat_for"))
        game_session_tab.setWindowTitle(self.localization.translate("ui.game_session.stat.level"))
        
        

    def update_settings_tab_ui(self):
        settings_tab = self.main_window.settings_tab
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
            label_item = settings_tab.scaling_group.layout().itemAtPosition(i, 0)
            if label_item and label_item.widget():
                label_widget = label_item.widget()
                if isinstance(label_widget, QLabel):
                    label_widget.setText(new_label_text)

        # Update group box titles
       

        # App language
        settings_tab.select_language.setText(self.localization.translate("ui.settings.language.select_language"))

        # Game Session 
        settings_tab.game_session_group.setTitle(self.localization.translate("ui.settings.game_session.title"))
        settings_tab.username_label.setText(self.localization.translate("ui.settings.game_session.username"))
        settings_tab.message_label.setText(self.localization.translate("ui.settings.game_session.message"))
        settings_tab.share_game_session.setText(self.localization.translate("ui.settings.game_session.share"))
        
        settings_tab.save_folder_label.setText(self.localization.translate("ui.settings.game_session.save_folder"))
        settings_tab.character_label.setText(self.localization.translate("ui.settings.game_session.character"))
        
        settings_tab.save_folder_combo.clear()
        settings_tab.save_folder_combo.addItem(self.localization.translate("ui.settings.game_session.save_folder_select"))
        settings_tab.save_folder_combo.addItems(get_save_folders())
        

        settings_tab.character_combo.clear()
        settings_tab.character_combo.addItem(self.localization.translate("ui.settings.game_session.character_select"))

        # Game Path
        settings_tab.game_path.setText(self.localization.translate("ui.settings.game_path.label"))

        # Update checkboxes
        settings_tab.allow_invaders.setText(self.localization.translate("ui.settings.gameplay.allow_invaders"))
        settings_tab.death_debuffs.setText(self.localization.translate("ui.settings.gameplay.death_debuffs"))
        settings_tab.allow_summons.setText(self.localization.translate("ui.settings.gameplay.allow_summons"))
        settings_tab.skip_splash_screens.setText(self.localization.translate("ui.settings.gameplay.skip_splash"))
        settings_tab.overhead_display.setText(self.localization.translate("ui.settings.gameplay.overhead_display"))
        settings_tab.master_volume.setText(self.localization.translate("ui.settings.gameplay.volume"))

        # Update ComboBox items
        current_index = settings_tab.overhead_player_display.currentIndex()
        settings_tab.overhead_player_display.clear()
        settings_tab.overhead_player_display.addItems([
            self.localization.translate("ui.settings.gameplay.display_options.normal"),
            self.localization.translate("ui.settings.gameplay.display_options.none"),
            self.localization.translate("ui.settings.gameplay.display_options.player_ping"),
            self.localization.translate("ui.settings.gameplay.display_options.player_soul_level"),
            self.localization.translate("ui.settings.gameplay.display_options.player_death_count"),
            self.localization.translate("ui.settings.gameplay.display_options.soul_level_and_ping")
        ])
        settings_tab.overhead_player_display.setCurrentIndex(current_index)
        
        # Update group box titles
        settings_tab.language_group1.setTitle(self.localization.translate("ui.settings.language.title"))
        settings_tab.language_group.setTitle(self.localization.translate("ui.settings.language.title"))
        settings_tab.path_group.setTitle(self.localization.translate("ui.settings.game_path.title"))
        settings_tab.gameplay_group.setTitle(self.localization.translate("ui.settings.gameplay.title"))
        settings_tab.scaling_group.setTitle(self.localization.translate("ui.settings.scaling.title"))
        settings_tab.password_group.setTitle(self.localization.translate("ui.settings.password.title"))
        settings_tab.save_group.setTitle(self.localization.translate("ui.settings.save.title"))
        
        # Update Password
        settings_tab.password.setText(self.localization.translate("ui.settings.password.coop_password"))

        # Update extension
        settings_tab.extension.setText(self.localization.translate("ui.settings.save.extension"))

        # Update Language override
        settings_tab.lang_override.setText(self.localization.translate("ui.settings.language.override"))


        # Update buttons
        settings_tab.browse_button.setText(self.localization.translate("ui.settings.game_path.browse_button"))
        settings_tab.save_button.setText(self.localization.translate("ui.settings.save_button"))

        

        # Refresh the UI to ensure all changes are visible
        self.main_window.update()
        
