# app_updater.py

import os
import sys
import requests
import zipfile
from PyQt6.QtCore import QThread, pyqtSignal
from version import VERSION

class AppUpdater(QThread):
    update_progress = pyqtSignal(str)
    update_complete = pyqtSignal(bool, str)
    update_available = pyqtSignal(str, str)  # New signal for update availability

    def __init__(self, localization):
        super().__init__()
        self.Localization = localization
        self.github_api_url = "https://api.github.com/repos/2Pz/Seamless-Co-op-Mod-Updater/releases/latest"
        self.current_version = VERSION
        self.should_update = False

    def run(self):
        try:
            self.update_progress.emit(self.Localization.translate("messages.update.checking"))
            response = requests.get(self.github_api_url)
            latest_release = response.json()
            latest_version = latest_release['tag_name']

            if latest_version > self.current_version:
                self.update_available.emit(self.current_version, latest_version)
                while not self.should_update:
                    self.msleep(100)
                
                if self.should_update:
                    self.perform_update(latest_release, latest_version)
            else:
                self.update_complete.emit(False, self.Localization.translate("messages.update.up_to_date"))
        except Exception as e:
            self.update_complete.emit(False, self.Localization.translate("messages.errors.update_error_check").format(str(e)))
            
    def perform_update(self, latest_release, latest_version):
        try:
            self.update_progress.emit(self.Localization.translate("messages.update.new_version_downloading").format(latest_version))
            asset = next(asset for asset in latest_release['assets'] if asset['name'] == 'SeamlessCo-opUpdater.zip')
            download_url = asset['browser_download_url']

            # Create a new folder for the update
            base_dir = os.path.dirname(sys.executable)
            new_folder_name = f'SeamlessCo-opUpdater_{latest_version}'
            new_folder_path = os.path.join(base_dir, new_folder_name)
            
            # Create the new folder if it doesn't exist
            os.makedirs(new_folder_path, exist_ok=True)

            # Download to the new folder
            zip_path = os.path.join(new_folder_path, "update.zip")
            response = requests.get(download_url)
            with open(zip_path, 'wb') as f:
                f.write(response.content)

            self.update_progress.emit(self.Localization.translate("messages.update.extracting_updates"))
            # Extract to the new folder
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(new_folder_path)

            # Clean up the zip file
            os.remove(zip_path)
            
            success_message = self.Localization.translate("messages.update.app_updated").format(
                latest_version) + f"\nExtracted to: {new_folder_path}"
            self.update_complete.emit(True, success_message)
        
        except Exception as e:
            self.update_complete.emit(False, self.Localization.translate("messages.errors.update_error_check").format(str(e)))

    def confirm_update(self):
        self.should_update = True
