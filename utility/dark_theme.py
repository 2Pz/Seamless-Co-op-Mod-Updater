from PyQt6.QtGui import QPalette, QColor

def set_dark_theme(self):
        # Modern color palette
        WINDOW_BG = QColor(32, 33, 36)       # Dark background
        WIDGET_BG = QColor(41, 42, 45)       # Slightly lighter for widgets
        TEXT_COLOR = QColor(237, 237, 240)   # Very light gray, easy to read
        ACCENT_COLOR = QColor(92, 119, 255)  # Blue accent
        BORDER_COLOR = QColor(55, 56, 59)    # Subtle borders
        
        # Set up palette
        palette = QPalette()
        palette.setColor(QPalette.ColorRole.Window, WINDOW_BG)
        palette.setColor(QPalette.ColorRole.WindowText, TEXT_COLOR)
        palette.setColor(QPalette.ColorRole.Base, WIDGET_BG)
        palette.setColor(QPalette.ColorRole.AlternateBase, WINDOW_BG)
        palette.setColor(QPalette.ColorRole.ToolTipBase, WIDGET_BG)
        palette.setColor(QPalette.ColorRole.ToolTipText, TEXT_COLOR)
        palette.setColor(QPalette.ColorRole.Text, TEXT_COLOR)
        palette.setColor(QPalette.ColorRole.Button, WIDGET_BG)
        palette.setColor(QPalette.ColorRole.ButtonText, TEXT_COLOR)
        palette.setColor(QPalette.ColorRole.Link, ACCENT_COLOR)
        palette.setColor(QPalette.ColorRole.Highlight, ACCENT_COLOR)
        palette.setColor(QPalette.ColorRole.HighlightedText, TEXT_COLOR)
        
        self.setPalette(palette)
        
        # Comprehensive stylesheet
        self.setStyleSheet("""
            QMainWindow {
                background-color: #202124;
            }
            QWidget {
                font-size: 14px;
            }
            QTabWidget::pane {
                border: 1px solid #373839;
                border-radius: 5px;
                top: -1px;
            }
            QTabBar::tab {
                background-color: #292A2D;
                color: #EDEDED;
                padding: 8px 16px;
                margin-right: 4px;
                border-top-left-radius: 5px;
                border-top-right-radius: 5px;
            }
            QTabBar::tab:selected {
                background-color: #5C77FF;
                color: white;
            }
            QPushButton {
                background-color: #5C77FF;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #6982FF;
            }
            QPushButton:pressed {
                background-color: #5166DD;
            }
            QTextEdit {
                background-color: #292A2D;
                color: #EDEDED;
                border: 1px solid #373839;
                border-radius: 5px;
                padding: 8px;
                selection-background-color: #5C77FF;
                selection-color: white;
            }
            QLabel {
                color: #EDEDED;
            }
            QLineEdit {
                background-color: #292A2D;
                color: #EDEDED;
                border: 1px solid #373839;
                border-radius: 5px;
                padding: 8px;
                selection-background-color: #5C77FF;
                selection-color: white;
            }
            QMessageBox {
                background-color: #202124;
            }
            QMessageBox QLabel {
                color: #EDEDED;
            }
            QMenuBar {
                background-color: #202124;
                color: #EDEDED;
                border-bottom: 1px solid #373839;
            }
            QMenuBar::item:selected {
                background-color: #373839;
            }
            QMenu {
                background-color: #292A2D;
                color: #EDEDED;
                border: 1px solid #373839;
            }
            QMenu::item:selected {
                background-color: #5C77FF;
            }
            QScrollBar:vertical {
                border: none;
                background-color: #292A2D;
                width: 10px;
                margin: 0;
            }
            QScrollBar::handle:vertical {
                background-color: #5C77FF;
                border-radius: 5px;
                min-height: 20px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0;
            }
        """)