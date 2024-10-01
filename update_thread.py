import os
import sys
import requests
import zipfile
import configparser
from PyQt6.QtCore import QThread, pyqtSignal

class UpdateThread(QThread):
    update_progress = pyqtSignal(str)
    update_complete = pyqtSignal(bool, str)
    download_progress = pyqtSignal(int, int)

    def __init__(self, url, install_path, settings, is_app_update=False, version=None):
        QThread.__init__(self)
        self.url = url
        self.install_path = install_path
        self.settings = settings
        self.is_app_update = is_app_update
        self.version = version

    def run(self):
        try:
            if self.is_app_update:
                self.update_application()
            else:
                self.update_mod()
        except Exception as e:
            self.update_complete.emit(False, f"Error during update: {str(e)}")

    def update_application(self):
        self.update_progress.emit(f"Downloading application update v{self.version}...")
        
        # Download the new version
        response = requests.get(self.url, stream=True)
        total_size = int(response.headers.get('content-length', 0))
        block_size = 1024  # 1 KB
        downloaded = 0

        app_update_path = os.path.join(os.path.dirname(sys.executable), f"app_update_v{self.version}.exe")
        with open(app_update_path, 'wb') as f:
            for data in response.iter_content(block_size):
                size = f.write(data)
                downloaded += size
                self.download_progress.emit(downloaded, total_size)

        self.update_progress.emit("Finalizing update...")

        # Create a batch script to replace the current executable
        current_executable = sys.executable
        batch_script = f"""
@echo off
timeout /t 2 /nobreak > NUL
move /y "{app_update_path}" "{current_executable}"
start "" "{current_executable}"
del "%~f0"
        """

        batch_path = os.path.join(os.path.dirname(sys.executable), "update.bat")
        with open(batch_path, 'w') as f:
            f.write(batch_script)

        # Execute the batch script and exit the current instance
        os.startfile(batch_path)
        self.update_complete.emit(True, f"Update to v{self.version} completed. Restarting application...")
        sys.exit()

    def update_mod(self):
        try:
            # Fetch the latest release information
            release_info = requests.get("https://api.github.com/repos/LukeYui/EldenRingSeamlessCoopRelease/releases/latest")
            release_data = release_info.json()
            release_name = release_data['tag_name']

            self.update_progress.emit(f"Downloading {release_name}...")
            
            response = requests.get(self.url, stream=True)
            total_size = int(response.headers.get('content-length', 0))
            block_size = 1024  # 1 KB
            downloaded = 0

            zip_path = os.path.join(self.install_path, "ersc.zip")
            with open(zip_path, 'wb') as f:
                for data in response.iter_content(block_size):
                    size = f.write(data)
                    downloaded += size
                    self.download_progress.emit(downloaded, total_size)

            self.update_progress.emit("Extracting files...")
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(self.install_path)

            self.update_progress.emit("Updating settings...")
            settings_path = os.path.join(self.install_path, "SeamlessCoop", "ersc_settings.ini")
            config = configparser.ConfigParser()
            config.read(settings_path)

            # Update GAMEPLAY section
            if 'GAMEPLAY' not in config:
                config['GAMEPLAY'] = {}
            for key in ['allow_invaders', 'death_debuffs', 'allow_summons', 'overhead_player_display', 'skip_splash_screens', 'default_boot_master_volume']:
                if key in self.settings:
                    config['GAMEPLAY'][key] = str(self.settings[key])

            # Update SCALING section
            if 'SCALING' not in config:
                config['SCALING'] = {}
            for key in ['enemy_health_scaling', 'enemy_damage_scaling', 'enemy_posture_scaling', 'boss_health_scaling', 'boss_damage_scaling', 'boss_posture_scaling']:
                if key in self.settings:
                    config['SCALING'][key] = str(self.settings[key])

            # Update PASSWORD section
            if 'PASSWORD' not in config:
                config['PASSWORD'] = {}
            if 'cooppassword' in self.settings:
                config['PASSWORD']['cooppassword'] = self.settings['cooppassword']

            # Update SAVE section
            if 'SAVE' not in config:
                config['SAVE'] = {}
            if 'save_file_extension' in self.settings:
                config['SAVE']['save_file_extension'] = self.settings['save_file_extension']

            # Update LANGUAGE section
            if 'LANGUAGE' not in config:
                config['LANGUAGE'] = {}
            if 'mod_language_override' in self.settings:
                config['LANGUAGE']['mod_language_override'] = self.settings['mod_language_override']

            with open(settings_path, 'w') as configfile:
                config.write(configfile)

            os.remove(zip_path)
            self.update_complete.emit(True, f"Update to {release_name} completed successfully!")
        except Exception as e:
            self.update_complete.emit(False, f"Error during update: {str(e)}")