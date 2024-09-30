from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QPushButton, QLabel, QTextEdit, QMessageBox, QTabWidget
from PyQt6.QtGui import QIcon, QPalette, QColor
from PyQt6.QtCore import Qt
from settings_page import SettingsPage
from readme_tab import ReadmeTab
from update_thread import UpdateThread
from resource import resource_path



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Seamless Co-op Mod Updater")
        self.setGeometry(100, 100, 800, 600)

        self.setWindowIcon(QIcon(resource_path("assets/update.png")))

        self.tab_widget = QTabWidget()
        self.setCentralWidget(self.tab_widget)

        self.update_tab = QWidget()
        self.settings_tab = SettingsPage()
        self.readme_tab = ReadmeTab()

        self.tab_widget.addTab(self.update_tab, "Update")
        self.tab_widget.addTab(self.settings_tab, "Settings")
        self.tab_widget.addTab(self.readme_tab, "README")

        self.init_update_tab()
        self.set_dark_theme()

    def init_update_tab(self):
        layout = QVBoxLayout()
        self.update_tab.setLayout(layout)

        update_button = QPushButton("Update Mod")
        update_button.clicked.connect(self.update_mod)
        layout.addWidget(update_button)

        self.status_label = QLabel("Ready")
        layout.addWidget(self.status_label)

        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        layout.addWidget(self.log_text)

        

    def set_dark_theme(self):
        palette = QPalette()
        palette.setColor(QPalette.ColorRole.Window, QColor(53, 53, 53))
        palette.setColor(QPalette.ColorRole.WindowText, Qt.GlobalColor.white)
        palette.setColor(QPalette.ColorRole.Base, QColor(25, 25, 25))
        palette.setColor(QPalette.ColorRole.AlternateBase, QColor(53, 53, 53))
        palette.setColor(QPalette.ColorRole.ToolTipBase, Qt.GlobalColor.white)
        palette.setColor(QPalette.ColorRole.ToolTipText, Qt.GlobalColor.white)
        palette.setColor(QPalette.ColorRole.Text, Qt.GlobalColor.white)
        palette.setColor(QPalette.ColorRole.Button, QColor(53, 53, 53))
        palette.setColor(QPalette.ColorRole.ButtonText, Qt.GlobalColor.white)
        palette.setColor(QPalette.ColorRole.BrightText, Qt.GlobalColor.red)
        palette.setColor(QPalette.ColorRole.Link, QColor(42, 130, 218))
        palette.setColor(QPalette.ColorRole.Highlight, QColor(42, 130, 218))
        palette.setColor(QPalette.ColorRole.HighlightedText, Qt.GlobalColor.black)
        self.setPalette(palette)

    def update_mod(self):
        install_path = self.settings_tab.path_input.text()
        if not install_path:
            QMessageBox.warning(self, "Error", "Please enter the Elden Ring mod installation path in the Settings tab.")
            return

        url = "https://github.com/LukeYui/EldenRingSeamlessCoopRelease/releases/latest/download/ersc.zip"
        settings = self.settings_tab.get_settings()
        self.update_thread = UpdateThread(url, install_path, settings)
        self.update_thread.update_progress.connect(self.update_status)
        self.update_thread.update_complete.connect(self.update_finished)
        self.update_thread.start()

    def update_status(self, message):
        self.status_label.setText(message)
        self.log_text.append(message)

    def update_finished(self, success, message):
        self.status_label.setText(message)
        self.log_text.append(message)
        if success:
            QMessageBox.information(self, "Success", message)
        else:
            QMessageBox.warning(self, "Error", message)
