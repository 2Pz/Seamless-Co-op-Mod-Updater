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

        markdown_content = '''
# Elden Ring Seamless Coop Mod Manager Changelog

Welcome to the changelog for the Elden Ring Seamless Coop Mod Manager! Here, you can find all the updates, enhancements, and fixes implemented in the latest versions of the tool.

## Version 1.0.0 - Initial Release
- Launched the Seamless Coop Mod Manager tool.
- Included automated mod downloading and installation functionality.
- Designed an intuitive interface for easy mod configuration.
- Enabled one-click updates to the latest mod version.
- **User Interface Enhancements:** Updated the UI for better readability and user experience.
- **Version Information:** Added labels to display the current version of the Seamless Co-op Mod and the application.
- **Remote Updates:**
    - You can now update the app remotely. Simply check for updates under the “Help” menu.
    - This feature will download the new release while retaining the old version.
    - Currently, the tool will only receive remote updates because it is automatically quarantined with each update due to being an exe-based application. Please make sure to check for updates regularly. Any new releases for the tool will be announced in this post.
- **Initial Setup:** If you’re using the app for the first time, please set the game path in the settings page.

## Version 1.1.0 - Support for Localization
- Enhanced Save Settings functionality to automatically update the "ersc_settings.ini" file.
- Introduced support for localization, allowing users to select their preferred language. Contributors can download the [en.json](https://drive.google.com/file/d/1UcVp1lhmv8BjZhW3VCLILTQ6-aNJeGGW/view?usp=sharing) file, translate it into their desired languages, and send the completed files back for inclusion.
- Added a dedicated Changelog tab for easier access to update notes and version history.

## Version 1.1.1 - Update on Packaging Method
- Due to the app being flagged as malicious, I switched from PyInstaller to cx_Freeze. This method will eliminate false positives, but it will increase the file size.

## Version 1.1.2 - Bug Fixes and New Localizations Support
- Resolved a critical bug where the text and app borders appeared pure white when the Windows theme was set to light mode, enhancing visual accessibility.
- Fixed the issue where the "Checking for Updates" message would become stuck in the app, improving user feedback during the update process.
- Added support for Simplified Chinese and Traditional Chinese localization, thanks to the contributions from [B1adeOfMelina](https://next.nexusmods.com/profile/B1adeOfMelina/about-me?gameId=4333).

## Version 1.1.3 - New Localizations Support
- Added support for Portuguese localization, thanks to the contributions from [Rakaels](https://next.nexusmods.com/profile/INinu/about-me?gameId=1704).

## Version 1.2.0 - Game Sessions
- Introduced a Game Sessions tab to allow players to share their co-op passwords with each other. Currently, this feature utilizes a free hosting API, so expect some errors.
- You can view the game sessions game sessions directly within this page [Seamless Co-op Game Sessions](https://2pz.github.io/Seamless-Co-op-Game-Sessions/)
- Users can set their username and a short message in the settings tab, this feature is optional.
- The tool name has been changed from **Seamless Coop Mod Updater** to **Seamless Coop Mod Manager** because it is no longer just a simple INI editor! :)

## Need Help?
If you encounter any issues or have questions, please don't hesitate to visit the [Nexusmods Page](https://www.nexusmods.com/eldenring/mods/6624?tab=posts) for support and the latest information.

Made by 2Pz!

'''

        self.text_browser.setMarkdown(markdown_content)

        # Ensure the background of the widget itself is also dark
        self.setStyleSheet("background-color: #353535;")
