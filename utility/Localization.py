# Localization.py

import json
import os
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt
from utility.resource_ import resource_path

RTL_LANGUAGES = {'ar', 'arc', 'dv', 'fa', 'ha', 'he', 'khw', 'ks', 'ku', 'ps', 'ur', 'yi'}

class Localization:
    def __init__(self, language='en', app=None):
        self.language = language
        self.localization_data = {}
        self.app = app  # Reference to the QApplication
        self.load_localization()

    def has_key(self, key):
        """Check if a translation key exists in the current language."""
        try:
            keys = key.split('.')
            current = self.translations
            for k in keys:
                current = current[k]
            return True
        except (KeyError, TypeError):
            return False

    def load_localization(self):
        file_path = resource_path(os.path.join('localization', f'{self.language}.json'))
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                self.localization_data = json.load(f)
            self.set_layout_direction()  # Set layout direction based on language
        except FileNotFoundError:
            print(f"Localization file not found: {file_path}")
        except json.JSONDecodeError:
            print("Error decoding the localization JSON file.")

    def translate(self, key):
        """Translate a given key."""
        if key in self.localization_data:
            return self.localization_data[key]

        keys = key.split('.')
        data = self.localization_data
        for k in keys:
            data = data.get(k, None)
            if data is None:
                return key  # Return the key itself if not found
        return data

    def set_layout_direction(self):
        """Set the layout direction of the application based on the language."""
        if self.app:
            if self.language in RTL_LANGUAGES:
                self.app.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
            else:
                self.app.setLayoutDirection(Qt.LayoutDirection.LeftToRight)


# Usage example:
app = QApplication([])  # Initialize your PyQt application
localization = Localization(language='en', app=app)  # Example with LTR language
