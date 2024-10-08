# changlog.py
import os
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, 
                             QTextBrowser)
from PyQt6.QtGui import QPalette, QColor
from PyQt6.QtCore import Qt
import os
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

        # Get the directory of the current script
        current_dir = os.path.dirname(os.path.abspath(__file__))

        html_content = f'''
<html>
<head>
    <title>Elden Ring Seamless Coop Mod Updater Changelog</title>
</head>
<body>
    <h1>Elden Ring Seamless Coop Mod Updater Changelog</h1>

    <p>Welcome to the changelog for the Elden Ring Seamless Coop Mod Updater! Here, you can find all the updates, enhancements, and fixes implemented in the latest versions of the tool.</p>

    <h2>Version 1.0.0 - Initial Release</h2>
    <ul>
        <li>Launched the Seamless Coop Mod Updater tool.</li>
        <li>Included automated mod downloading and installation functionality.</li>
        <li>Designed an intuitive interface for easy mod configuration.</li>
        <li>Enabled one-click updates to the latest mod version.</li>
        <li>User Interface Enhancements: Updated the UI for better readability and user experience.</li>
        <li>Version Information: Added labels to display the current version of the Seamless Co-op Mod and the application.</li>
        <li>Remote Updates: 
            <ul>
                <li>You can now update the app remotely. Simply check for updates under the “Help” menu.</li>
                <li>This feature will download the new release while retaining the old version.</li>
                <li>Currently, the tool will only receive remote updates because it is automatically quarantined with each update due to being an exe-based application. Please make sure to check for updates regularly. Any new releases for the tool will be announced in this post.</li>
            </ul>
        </li>
        <li>Initial Setup: If you’re using the app for the first time, please set the game path in the settings page.</li>
    </ul>

    <h2>Version 1.1.0 - Support for Localization</h2>
    <ul>
        <li>Enhanced Save Settings functionality to automatically update the "ersc_settings.ini" file.</li>
        <li>Introduced support for localization, allowing users to select their preferred language. Contributors can download the <a href="https://drive.google.com/file/d/1UcVp1lhmv8BjZhW3VCLILTQ6-aNJeGGW/view?usp=sharing">en.json</a> file, translate it into their desired languages, and send the completed files back for inclusion.</li>
        <li>Added a dedicated Changelog tab for easier access to update notes and version history.</li>
    </ul>

    <h2>Version 1.1.1 - Update on Packaging Method</h2>
    <ul>
        <li>Due to the app being flagged as malicious, I switched from PyInstaller to cx_Freeze. This method will eliminate false positives, but it will increase the file size.</li>
    </ul>

    <h2>Version 1.1.2 - Bug Fixes and new Localizations support</h2>
    <ul>
        <li>Resolved a critical bug where the text and app borders appeared pure white when the Windows theme was set to light mode, enhancing visual accessibility.</li>
        <li>Fixed the issue where the "Checking for Updates" message would become stuck in the app, improving user feedback during the update process.</li>
        <li>Added support for Simplified Chinese and Traditional Chinese localization, thanks to the contributions from B1adeOfMelina.</li>
    </ul>

    <h2>Need Help?</h2>
    <p>If you encounter any issues or have questions, please don't hesitate to visit the <a href="https://www.nexusmods.com/eldenring/mods/6624?tab=posts">Nexusmods Page</a> for support and the latest information.</p>

    <p>Made by 2Pz!</p>
</body>
</html>
'''



        self.text_browser.setHtml(html_content)

        # Ensure the background of the widget itself is also dark
        self.setStyleSheet("background-color: #353535;")
