# main.py

import sys
from PyQt6.QtWidgets import QApplication
from main_window import MainWindow

class App(QApplication):
    def __init__(self, argv):
        super().__init__(argv)
        self.window = MainWindow()
        self.window.show()

if __name__ == "__main__":
    app = App(sys.argv)
    sys.exit(app.exec())