import sys
import os
import subprocess
from configparser import ConfigParser
from PyQt6.QtWidgets import QApplication
from tabs.main_window import MainWindow
from tabs.settings_page import SettingsPage
from utility.Localization import Localization
from utility.theme import stylized_silk_dark_theme, modern_theme
class App(QApplication):
    def __init__(self, argv):
        super().__init__(argv)
        modern_theme(self)
        
        # Load settings
        settings = self.load_settings()
        
        # Initialize Localization with preferred language
        self.localization = Localization(language=settings.get('preferred_language', 'en'), app=self)
        
        # Handle Steam silent launch if enabled
        if settings.get('run_steam_silently') == '1':
            self.launch_steam_silently(settings.get('steam_exe_path', ''))
        
        # Create main window with localization
        self.window = MainWindow(localization=self.localization)
        self.window.show()

    def load_settings(self):
        config = ConfigParser()
        settings_path = os.path.join(os.environ['APPDATA'], 'SeamlessCo-opUpdater', 'settings.ini')
        
        if os.path.exists(settings_path):
            config.read(settings_path)
            if 'Settings' in config:
                return config['Settings']
        
        return {'preferred_language': 'en', 'run_steam_silently': '0'}

    def launch_steam_silently(self, steam_path):
        """Launch Steam in silent mode if it's not already running"""
        try:
            # Check if Steam is already running
            if not  SettingsPage.is_steam_running(self):
                # If no steam path provided, try to find it
                if not steam_path:
                    steam_path =  SettingsPage.find_steam_path()
                
                if steam_path and os.path.exists(steam_path):
                    # Launch Steam with -silent parameter
                    subprocess.Popen([steam_path, "-silent"], 
                                  stdout=subprocess.DEVNULL, 
                                  stderr=subprocess.DEVNULL,
                                  creationflags=subprocess.CREATE_NO_WINDOW)
                else:
                    pass
                    print("Steam executable path not found or invalid")
        except Exception as e:
            pass
            print(f"Error launching Steam: {str(e)}")

    
if __name__ == "__main__":
    app = App(sys.argv)
    sys.exit(app.exec())
