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

    def __init__(self):
        super().__init__()
        self.github_api_url = "https://api.github.com/repos/2Pz/Seamless-Co-op-Mod-Updater/releases/latest"
        self.current_version = VERSION
        self.should_update = False

    def run(self):
        try:
            self.update_progress.emit("Checking for updates...")
            response = requests.get(self.github_api_url)
            latest_release = response.json()
            latest_version = latest_release['tag_name']

            if latest_version > self.current_version:
                self.update_available.emit(self.current_version, latest_version)
                # Wait for user confirmation
                while not self.should_update:
                    self.msleep(100)
                
                if self.should_update:
                    self.perform_update(latest_release, latest_version)
            else:
                self.update_complete.emit(False, "You are already using the latest version.")
        except Exception as e:
            self.update_complete.emit(False, f"Error during update check: {str(e)}")

    def perform_update(self, latest_release, latest_version):
        try:
            self.update_progress.emit(f"New version {latest_version} available. Downloading...")
            asset = next(asset for asset in latest_release['assets'] if asset['name'] == 'SeamlessCo-opUpdater.zip')
            download_url = asset['browser_download_url']

            zip_path = os.path.join(os.path.dirname(sys.executable), "update.zip")
            response = requests.get(download_url)
            with open(zip_path, 'wb') as f:
                f.write(response.content)

            self.update_progress.emit("Extracting update...")
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(os.path.dirname(sys.executable))

            os.remove(zip_path)
            self.update_complete.emit(True, f"New Update version SeamlessCo-opUpdater_{latest_version}.exe downloaded. \nYou can delete this version.")
        except Exception as e:
            self.update_complete.emit(False, f"Error during update: {str(e)}")

    def confirm_update(self):
        self.should_update = True