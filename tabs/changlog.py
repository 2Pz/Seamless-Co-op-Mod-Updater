import os
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, 
                             QTextBrowser)
from PyQt6.QtGui import QPalette, QColor
from PyQt6.QtCore import Qt
from utility.resource_ import resource_path

class Changelongtab(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)

        self.text_browser = QTextBrowser()
        self.text_browser.setOpenExternalLinks(True)
        layout.addWidget(self.text_browser)

        # Set the color scheme to match the dark theme
        palette = self.text_browser.palette()
        palette.setColor(QPalette.ColorRole.Base, QColor(53, 53, 53))
        palette.setColor(QPalette.ColorRole.Text, Qt.GlobalColor.white)
        self.text_browser.setPalette(palette)

        # Get the correct path to the readme.md file
        current_dir = os.path.dirname(os.path.abspath(__file__))
        changelog_path = os.path.join(current_dir, '..', 'utility', 'changelogs.md')


        # Read the markdown content from the changelog.md file
        try:
            with open(changelog_path, 'r', encoding='utf-8') as file:
                markdown_content = file.read()
                self.text_browser.setMarkdown(markdown_content)
        except FileNotFoundError:
            self.text_browser.setText("Changelog file not found.")
        except Exception as e:
            self.text_browser.setText(f"Error loading changelog: {str(e)}")

        # Ensure the background of the widget itself is also dark
        self.setStyleSheet("background-color: #353535;")
