import sys
import os
from configparser import ConfigParser
from PyQt6.QtWidgets import QApplication
from tabs.main_window import MainWindow
from utility.Localization import Localization

class App(QApplication):
    def __init__(self, argv):
        super().__init__(argv)
        
        # Load preferred language from settings
        preferred_language = self.load_preferred_language()
        
        # Initialize Localization with preferred language
        self.localization = Localization(language=preferred_language, app=self)
        
        # Create main window with localization
        self.window = MainWindow(localization=self.localization)
        self.window.show()

    def load_preferred_language(self):
        config = ConfigParser()
        settings_path = os.path.join(os.environ['APPDATA'], 'SeamlessCo-opUpdater', 'settings.ini')
        
        if os.path.exists(settings_path):
            config.read(settings_path)
            if 'Settings' in config and 'preferred_language' in config['Settings']:
                return config['Settings']['preferred_language']
        
        return 'en'  # Default to English if no setting is found

if __name__ == "__main__":
    app = App(sys.argv)
    sys.exit(app.exec())