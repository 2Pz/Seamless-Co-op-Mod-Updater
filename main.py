import sys
from PyQt6.QtWidgets import QApplication
from main_window import MainWindow
from config import APP_VERSION

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.setWindowTitle(f"Seamless Co-op Mod Updater v{APP_VERSION}")
    window.show()
    sys.exit(app.exec())