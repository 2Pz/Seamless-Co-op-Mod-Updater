# readme_tab.py
import os
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTextBrowser
from PyQt6.QtGui import QPalette, QColor
from PyQt6.QtCore import Qt
import markdown
from utility.resource_ import resource_path

class ReadmeTab(QWidget):
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
        readme_path = os.path.join(current_dir, '..', 'utility', 'readme.md')

        # Replace relative image paths with absolute paths
        image1_path = resource_path('assets/1.png')
        image2_path = resource_path('assets/2.png')

        # Ensure the images exist
        if not os.path.exists(image1_path):
            print(f"Error: Image file not found: {image1_path}")
        if not os.path.exists(image2_path):
            print(f"Error: Image file not found: {image2_path}")


        # Update the paths in the Markdown content
        try:
            with open(readme_path, 'r', encoding='utf-8') as file:
                md_content = file.read()
                md_content = md_content.replace('assets/1.png', image1_path)
                md_content = md_content.replace('assets/2.png', image2_path)

            # Convert Markdown to HTML
            html_content = markdown.markdown(md_content, extensions=['extra'])

            # Display the HTML content in the QTextBrowser
            self.text_browser.setHtml(html_content)
        except FileNotFoundError:
            self.text_browser.setText("Error: readme.md file not found.")

        # Ensure the background of the widget itself is also dark
        self.setStyleSheet("background-color: #353535;")