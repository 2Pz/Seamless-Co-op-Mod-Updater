from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, QTableWidget, 
                             QTableWidgetItem, QHeaderView, QDialog, QLabel, QGridLayout)
from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtGui import QFont
import requests
from dotenv import load_dotenv
import os

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


            value = stats.get(stat, 'N/A')  # Use 'N/A' if the stat is not found
            stats_table.setItem(row, 1, QTableWidgetItem(str(value)))

        stats_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        stats_table.setAlternatingRowColors(True)
        
        layout.addWidget(stats_table)
        self.setLayout(layout)

class GameSessionTab(QWidget):
    def __init__(self, localization, settings):
        super().__init__()
        self.Localization = localization
        self.settings = settings
        self.init_ui()
        self.sessions = []
        self.refresh_timer = QTimer()
        self.refresh_timer.timeout.connect(self.refresh_sessions)
        self.refresh_timer.start(60000)  # Refresh every 60 seconds
        self.refresh_sessions()  # Initial refresh

    def init_ui(self):
        layout = QVBoxLayout()

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

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.session_table.setColumnWidth(0, int(self.session_table.width() * 0.3))  # Username column
        self.session_table.setColumnWidth(1, int(self.session_table.width() * 0.5))  # Message column
        self.session_table.setColumnWidth(2, int(self.session_table.width() * 0.2))  # Password column
