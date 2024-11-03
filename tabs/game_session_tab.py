from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, QTableWidget, 
                             QTableWidgetItem, QHeaderView, QDialog, QLabel, QGridLayout,
                             QComboBox, QCheckBox, QGroupBox, QMessageBox)
from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtGui import QFont
import requests
import aiohttp
from dotenv import load_dotenv
import os
from utility.worker import AsyncWorker
from configparser import ConfigParser

load_dotenv()

class UserStatsDialog(QDialog):
    def __init__(self, username, level, stats, parent=None):
        super().__init__(parent)
        self.Localization = parent.Localization if parent else None
        self.main_window = parent

        self.setWindowTitle(self.Localization.translate("ui.game_session.stat.stat_for").format(username))
        self.setModal(True)
        self.setMinimumSize(400, 320)

        layout = QVBoxLayout()

        title_font = QFont()
        title_font.setPointSize(14)
        title_font.setBold(True)

        level_label = QLabel(self.Localization.translate("ui.game_session.stat.level").format(level))
        level_label.setFont(title_font)
        layout.addWidget(level_label)

        # Define the desired order of stats
        stat_order = ['Vigor', 'Mind', 'Endurance', 'Strength', 'Dexterity', 'Intelligence', 'Faith', 'Arcane']

        stats_table = QTableWidget(len(stat_order), 2)
        stats_table.setHorizontalHeaderLabels([self.Localization.translate("ui.game_session.stat.stats"), self.Localization.translate("ui.game_session.stat.values")])
        stats_table.verticalHeader().setVisible(False)
        stats_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)

        for row, stat in enumerate(stat_order):
            if stat == "Vigor":
                stats_table.setItem(row, 0, QTableWidgetItem(self.Localization.translate("ui.game_session.stat.vigor")))
            elif stat == "Mind":
                stats_table.setItem(row, 0, QTableWidgetItem(self.Localization.translate("ui.game_session.stat.mind")))
            elif stat == "Endurance":
                stats_table.setItem(row, 0, QTableWidgetItem(self.Localization.translate("ui.game_session.stat.endurance")))
            elif stat == "Strength":
                stats_table.setItem(row, 0, QTableWidgetItem(self.Localization.translate("ui.game_session.stat.strength")))
            elif stat == "Dexterity":
                stats_table.setItem(row, 0, QTableWidgetItem(self.Localization.translate("ui.game_session.stat.dexterity"))) 
            elif stat == "Intelligence":
                stats_table.setItem(row, 0, QTableWidgetItem(self.Localization.translate("ui.game_session.stat.intelligence")))
            elif stat == "Faith":
                stats_table.setItem(row, 0, QTableWidgetItem(self.Localization.translate("ui.game_session.stat.faith")))
            elif stat == "Arcane":
                stats_table.setItem(row, 0, QTableWidgetItem(self.Localization.translate("ui.game_session.stat.arcane")))

            value = stats.get(stat, 'N/A')
            stats_table.setItem(row, 1, QTableWidgetItem(str(value)))

        stats_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        stats_table.setAlternatingRowColors(True)
        
        layout.addWidget(stats_table)
        self.setLayout(layout)

class GameSessionTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.Localization = parent.Localization if parent else None
        self.main_window = parent
        self.init_ui()
        self.sessions = []
        self.refresh_timer = QTimer()
        self.refresh_timer.timeout.connect(self.refresh_sessions)
        self.refresh_timer.start(60000)  # Refresh every 60 seconds
        self.refresh_sessions()  # Initial refresh

    def init_ui(self):
        layout = QVBoxLayout()

        # Game Session settings
        self.game_session_group = QGroupBox(self.Localization.translate("ui.settings.game_session.title"))
        game_session_layout = QGridLayout()
        self.game_session_group.setLayout(game_session_layout)

        # Character Selection group
        self.character_group = QGroupBox(self.Localization.translate("ui.settings.game_session.character"))
        character_layout = QGridLayout()
        self.character_group.setLayout(character_layout)

        self.character_label = QLabel(self.Localization.translate("ui.settings.game_session.character"))
        character_layout.addWidget(self.character_label, 0, 0)
        self.character_combo = QComboBox()
        self.character_combo.addItem(self.Localization.translate("ui.settings.game_session.character_select"))
        self.character_combo.currentIndexChanged.connect(self.check_game_session_fields)
        character_layout.addWidget(self.character_combo, 0, 1)

        layout.addWidget(self.character_group)
        

        self.username_label = QLabel(self.Localization.translate("ui.settings.game_session.username"))
        game_session_layout.addWidget(self.username_label, 0, 0)
        self.username_input = QLineEdit()
        self.username_input.textChanged.connect(self.check_game_session_fields)
        game_session_layout.addWidget(self.username_input, 0, 1)

        self.message_label = QLabel(self.Localization.translate("ui.settings.game_session.message"))
        game_session_layout.addWidget(self.message_label, 1, 0)
        self.message_input = QLineEdit()
        self.message_input.textChanged.connect(self.check_game_session_fields)
        game_session_layout.addWidget(self.message_input, 1, 1)

        self.share_game_session = QCheckBox(self.Localization.translate("ui.settings.game_session.share"))
        self.share_game_session.setChecked(False)
        self.share_game_session.setEnabled(False)
        game_session_layout.addWidget(self.share_game_session, 2, 0, 1, 2)

        self.share_game_session.stateChanged.connect(self.on_share_game_session_changed)

        layout.addWidget(self.game_session_group)

        # Search bar
        search_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText(self.Localization.translate("ui.game_session.search_placeholder"))
        self.search_input.textChanged.connect(self.filter_sessions)
        search_layout.addWidget(self.search_input)
        layout.addLayout(search_layout)

        # Session table
        self.session_table = QTableWidget(0, 3)
        self.session_table.setHorizontalHeaderLabels([
            self.Localization.translate("ui.game_session.username"),
            self.Localization.translate("ui.game_session.message"),
            self.Localization.translate("ui.game_session.password")
        ])
        self.session_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.session_table.cellClicked.connect(self.show_user_stats)
        
        # Make the table resize with the window
        self.session_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.session_table.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        
        layout.addWidget(self.session_table)

        # Refresh button
        self.refresh_button = QPushButton(self.Localization.translate("ui.game_session.refresh"))
        self.refresh_button.clicked.connect(self.refresh_sessions)
        layout.addWidget(self.refresh_button)

        self.setLayout(layout)
        self.load_settings()

    def show_user_stats(self, row, column):
        if column == 0:  # Username column
            item = self.session_table.item(row, column)
            if item:
                data = item.data(Qt.ItemDataRole.UserRole)
                if data:
                    dialog = UserStatsDialog(item.text(), data['level'], data['stats'], self)
                    dialog.exec()

    def refresh_sessions(self):
        try:
            response = requests.get(f"{os.getenv('API')}/sessions.json")
            if response.status_code == 200:
                self.sessions = response.json()
                self.update_session_table()
                self.filter_sessions()  # Apply current filter after refreshing
            else:
                print(f"Failed to fetch sessions. Status code: {response.status_code}")
        except Exception as e:
            print(f"Error fetching sessions: {str(e)}")

    def update_session_table(self):
        self.session_table.setRowCount(len(self.sessions))
        for row, session in enumerate(self.sessions):
            username_item = QTableWidgetItem(session.get('username', ''))
            username_item.setData(Qt.ItemDataRole.UserRole, {
                'level': session.get('level', 'N/A'),
                'stats': session.get('stats', {})
            })
            self.session_table.setItem(row, 0, username_item)
            self.session_table.setItem(row, 1, QTableWidgetItem(session.get('message', '')))
            self.session_table.setItem(row, 2, QTableWidgetItem(session.get('password', '')))

    def filter_sessions(self):
        search_text = self.search_input.text().lower()
        for row in range(self.session_table.rowCount()):
            show_row = False
            for col in range(self.session_table.columnCount()):
                item = self.session_table.item(row, col)
                if item and search_text in item.text().lower():
                    show_row = True
                    break
            self.session_table.setRowHidden(row, not show_row)

    def check_game_session_fields(self):
        username_filled = bool(self.username_input.text().strip())
        message_filled = bool(self.message_input.text().strip())
        character_selected = self.character_combo.currentIndex() > 0  # Check if a character is selected (index 0 is "Select Character")
        self.share_game_session.setEnabled(username_filled and message_filled and character_selected)


    def update_character_list(self, character_info):
        self.character_combo.clear()
        self.character_combo.addItem(self.Localization.translate("ui.settings.game_session.character"))
        for char in character_info:
            self.character_combo.addItem(f"{char['name']} (Level {char['level']})", char)

    # 3. Update the share_game_session_data method to use the character data:
    async def share_game_session_data(self):
        settings = self.get_settings()
        character_data = self.character_combo.currentData()
        
        if not character_data:
            return False, "No character selected"
            
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(f"{os.getenv('API')}/api/add_session", 
                                        json={
                                            "username": settings['username'],
                                            "message": settings['message'],
                                            "password": self.main_window.ersc_settings_tab.cooppassword.text(),
                                            "level": character_data['level'],
                                            "stats": character_data['stats']
                                        },
                                        timeout=5) as response:
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
                async with session.post(f"{os.getenv('API')}/api/remove_session", 
                                        json={
                                            "username": settings['username'],
                                            "action": "remove"
                                        },
                                        timeout=5) as response:
                    if response.status == 200:
                        return True, "Game session removed successfully"
                    else:
                        return False, await response.text()
        except aiohttp.ClientError as e:
            return False, f"Error removing game session: {str(e)}"
        except Exception as e:
            return False, f"Unexpected error removing game session: {str(e)}"

    def on_share_game_session_changed(self):
        if self.share_game_session.isChecked():
            if self.character_combo.currentIndex() == 0:  # No character selected
                QMessageBox.warning(
                    self,
                    self.Localization.translate("messages.errors.no_character_title"),
                    self.Localization.translate("messages.errors.no_character_message")
                )
                self.share_game_session.setChecked(False)
                return

            self.worker = AsyncWorker(self.share_game_session_data)
            self.worker.finished.connect(self.on_share_game_session_complete)
            self.worker.start()
        else:
            self.worker = AsyncWorker(self.remove_game_session_data)
            self.worker.finished.connect(self.on_remove_game_session_complete)
            self.worker.start()

        # Disable the checkbox while the operation is in progress
        self.share_game_session.setEnabled(False)

    def on_share_game_session_complete(self, success, message):
        self.share_game_session.setEnabled(True)  # Re-enable the checkbox
        if not success:
            self.share_game_session.setChecked(False)
            QMessageBox.warning(self, self.Localization.translate("messages.errors.share_game_error_title"), 
                              self.Localization.translate("messages.errors.share_game_error"))
        else:
            self.save_settings()  # Save settings after successful share

    def on_remove_game_session_complete(self, success, message):
        self.share_game_session.setEnabled(True)  # Re-enable the checkbox
        if not success:
            self.share_game_session.setChecked(True)
        else:
            self.save_settings()  # Save settings after successful removal

    def get_settings(self):
        return {
            "username": self.username_input.text(),
            "message": self.message_input.text(),
            "share_game_session": int(self.share_game_session.isChecked()),
        }

    def get_settings_path(self):
        app_data = os.path.join(os.environ['APPDATA'], 'SeamlessCo-opUpdater')
        if not os.path.exists(app_data):
            os.makedirs(app_data)
        return os.path.join(app_data, 'session_settings.ini')

    def save_settings(self):
        try:
            config = ConfigParser()
            config['GameSession'] = {
                'username': self.username_input.text(),
                'message': self.message_input.text(),
                'share_game_session': str(int(self.share_game_session.isChecked())),
            }

            settings_path = self.get_settings_path()
            with open(settings_path, 'w') as configfile:
                config.write(configfile)
        except Exception as e:
            print(f"Error saving session settings: {str(e)}")
            import traceback
            traceback.print_exc()

    def load_settings(self):
        config = ConfigParser()
        settings_path = self.get_settings_path()
        if os.path.exists(settings_path):
            config.read(settings_path)
            if 'GameSession' in config:
                settings = config['GameSession']
                self.username_input.setText(settings.get('username', ''))
                self.message_input.setText(settings.get('message', ''))
                if (self.username_input.text().strip() and
                    self.message_input.text().strip()):
                    self.share_game_session.setChecked(bool(int(settings.get('share_game_session', '0'))))
                else:
                    self.share_game_session.setChecked(False)
                    self.check_game_session_fields()

    def resizeEvent(self, event):
        super().resizeEvent(event)