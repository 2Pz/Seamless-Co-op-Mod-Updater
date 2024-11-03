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

## Version 1.2.1 - Bug Fixes & API Update for Game sessions
- Increased the limits of scaling% Enemy & Boss from 200 to 1000
- Steam ID and Character Dropdowns: New dropdown menus let you select your Steam ID and in-game character. The tool now reads your save file to automatically display your character’s name, level, and stats.
- Game Sessions Tab Improvements: You can now click on a user's name in the game sessions tab to inspect their character’s level and stats. This feature is also available on the corresponding webpage.


## Version 1.2.2 - Bug Fixes & Launch Seamless Co-op button
- Added new settings for Seamless Co-op launcher, allowing selection between .exe or .bat files.
- Introduced a "Launch Seamless Co-op" button on the main window for easier game startup with Seamless Co-op enabled.
- Added an "Auto-Update" checkbox to automatically update both the app and mod at startup.
- Removed the Seamless Co-op update button; now you can manually check for mod/app updates in the "Help" menu.

## Need Help?
If you encounter any issues or have questions, please don't hesitate to visit the [Nexusmods Page](https://www.nexusmods.com/eldenring/mods/6624?tab=posts) for support and the latest information.

Made by 2Pz!