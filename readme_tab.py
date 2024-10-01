# readme_tab.py
import os
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, 
                             QTextBrowser)
from PyQt6.QtGui import QPalette, QColor
from PyQt6.QtCore import Qt
import os
from resource_ import resource_path

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

        # Get the directory of the current script
        current_dir = os.path.dirname(os.path.abspath(__file__))

        html_content = f'''
<html>

</head>
    <body>
        <h1>Elden Ring Seamless Coop Mod Updater</h1>

        <p>Welcome to the Elden Ring Seamless Coop Mod Updater! This simpe tool streamlines the process of updating and configuring the Seamless Coop mod for Elden Ring, enhancing your cooperative gameplay experience.</p>

        <h2>Key Features</h2>
        <ul>
            <li>Automated mod downloading and installation</li>
            <li>Intuitive interface for easy mod configuration</li>
            <li>Effortless one-click updates to the latest version</li>
        </ul>

        <h2>Getting Started</h2>
        <p>Follow these simple steps to set up and use the Mod Updater:</p>
        <ol>
            <li><strong>Set the Game Path:</strong> In the Settings tab, ensure you select the correct Elden Ring game folder.</li>
            <p><img src="{resource_path('assets/2.png')}" alt="Configuration Guide"></p>
            <li><strong>Configure the Mod:</strong> Verify that "SeamlessCoop/ersc.dll" is properly set in the config_eldenring.toml file.</li>
            <p><img src="{resource_path('assets/1.png')}" alt="Configuration Guide"></p>
        </ol>

        
        

        <h2>Need Help?</h2>
        <p>If you encounter any issues or have questions, please don't hesitate to visit <a href=https://www.nexusmods.com/eldenring/mods/6624?tab=posts">Nexusmods Page</a> for support and the latest information.</p>

        <p>Made by 2Pz!</p>
    </body>
</html>
'''

        self.text_browser.setHtml(html_content)

        # Ensure the background of the widget itself is also dark
        self.setStyleSheet("background-color: #353535;")