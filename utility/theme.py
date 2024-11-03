from PyQt6.QtGui import QPalette, QColor

def none(self):
        return

def modern_theme(self):
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




def stylized_silk_dark_theme(self):
        # Stylized dark palette with glowing effects
        WINDOW_BG = QColor(40, 40, 45)       # Dark gray background
        WIDGET_BG = QColor(45, 45, 50)       # Slightly lighter gray for widgets
        BUTTON_BG = QColor(20, 20, 20)       # Black for buttons
        TEXT_COLOR = QColor(255, 255, 255)   # White text
        BORDER_COLOR = QColor(70, 70, 75)    # Subtle gray borders
        HIGHLIGHT_COLOR = QColor(90, 90, 100) # Slightly lighter gray for highlights

        # Set up palette
        palette = QPalette()
        palette.setColor(QPalette.ColorRole.Window, WINDOW_BG)
        palette.setColor(QPalette.ColorRole.WindowText, TEXT_COLOR)
        palette.setColor(QPalette.ColorRole.Base, WIDGET_BG)
        palette.setColor(QPalette.ColorRole.AlternateBase, WINDOW_BG)
        palette.setColor(QPalette.ColorRole.ToolTipBase, WIDGET_BG)
        palette.setColor(QPalette.ColorRole.ToolTipText, TEXT_COLOR)
        palette.setColor(QPalette.ColorRole.Text, TEXT_COLOR)
        palette.setColor(QPalette.ColorRole.Button, BUTTON_BG)
        palette.setColor(QPalette.ColorRole.ButtonText, TEXT_COLOR)
        palette.setColor(QPalette.ColorRole.Link, TEXT_COLOR)
        palette.setColor(QPalette.ColorRole.Highlight, HIGHLIGHT_COLOR)
        palette.setColor(QPalette.ColorRole.HighlightedText, TEXT_COLOR)

        self.setPalette(palette)

        # Stylized comprehensive stylesheet
        self.setStyleSheet("""
            QMainWindow {
                background-color: #28282D;
                border: 1px solid #46464B;
                border-radius: 10px;
            }
            QWidget {
                font-size: 14px;
                font-family: 'Segoe UI', Tahoma, sans-serif;
            }
            QTabWidget::pane {
                border: 1px solid #5A5A63;
                border-radius: 8px;
            }
            QTabBar::tab {
                background-color: #323236;
                color: #FFFFFF;
                padding: 10px 20px;
                margin-right: 6px;
                border-top-left-radius: 10px;
                border-top-right-radius: 10px;
                transition: background-color 0.3s ease;
            }
            QTabBar::tab:selected {
                background-color: #505050;
                color: white;
                font-weight: bold;
            }
            QPushButton {
                background-color: #141414;
                color: #FFFFFF;
                border: 2px solid #5A5A63;
                padding: 12px 20px;
                border-radius: 10px;
                font-weight: bold;
                text-transform: uppercase;
                transition: background-color 0.3s ease, box-shadow 0.3s ease;
            }
            QPushButton:hover {
                background-color: #1A1A1A;
                box-shadow: 0 0 10px rgba(255, 255, 255, 0.2);
            }
            QPushButton:pressed {
                background-color: #333333;
                box-shadow: 0 0 5px rgba(255, 255, 255, 0.3);
            }
            QTextEdit {
                background-color: #323236;
                color: #FFFFFF;
                border: 1px solid #5A5A63;
                border-radius: 8px;
                padding: 10px;
                selection-background-color: #505050;
                selection-color: #FFFFFF;
            }
            QLabel {
                color: #FFFFFF;
            }
            QLineEdit {
                background-color: #323236;
                color: #FFFFFF;
                border: 1px solid #5A5A63;
                border-radius: 8px;
                padding: 10px;
                selection-background-color: #505050;
                selection-color: #FFFFFF;
            }
            QMessageBox {
                background-color: #28282D;
                border-radius: 10px;
            }
            QMessageBox QLabel {
                color: #FFFFFF;
            }
            QMenuBar {
                background-color: #28282D;
                color: #FFFFFF;
                border-bottom: 1px solid #5A5A63;
            }
            QMenuBar::item:selected {
                background-color: #5A5A63;
                border-radius: 5px;
            }
            QMenu {
                background-color: #323236;
                color: #FFFFFF;
                border: 1px solid #5A5A63;
                border-radius: 8px;
            }
            QMenu::item:selected {
                background-color: #505050;
                border-radius: 5px;
            }
            QScrollBar:vertical {
                border: none;
                background-color: #323236;
                width: 12px;
                margin: 0;
            }
            QScrollBar::handle:vertical {
                background-color: #505050;
                border-radius: 6px;
                min-height: 20px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0;
            }
        """)

def stylized_light_theme(self):
        # Light color palette
        WINDOW_BG = QColor(245, 245, 245)    # Soft light gray background
        WIDGET_BG = QColor(255, 255, 255)    # Pure white for widgets
        BUTTON_BG = QColor(220, 220, 220)    # Light gray buttons
        TEXT_COLOR = QColor(30, 30, 30)      # Dark text for good contrast
        BORDER_COLOR = QColor(200, 200, 200) # Subtle border color
        ACCENT_COLOR = QColor(100, 150, 255) # Gentle blue for accents
        HIGHLIGHT_COLOR = QColor(180, 220, 255) # Soft highlight color

        # Set up palette
        palette = QPalette()
        palette.setColor(QPalette.ColorRole.Window, WINDOW_BG)
        palette.setColor(QPalette.ColorRole.WindowText, TEXT_COLOR)
        palette.setColor(QPalette.ColorRole.Base, WIDGET_BG)
        palette.setColor(QPalette.ColorRole.AlternateBase, WINDOW_BG)
        palette.setColor(QPalette.ColorRole.ToolTipBase, WIDGET_BG)
        palette.setColor(QPalette.ColorRole.ToolTipText, TEXT_COLOR)
        palette.setColor(QPalette.ColorRole.Text, TEXT_COLOR)
        palette.setColor(QPalette.ColorRole.Button, BUTTON_BG)
        palette.setColor(QPalette.ColorRole.ButtonText, TEXT_COLOR)
        palette.setColor(QPalette.ColorRole.Link, ACCENT_COLOR)
        palette.setColor(QPalette.ColorRole.Highlight, ACCENT_COLOR)
        palette.setColor(QPalette.ColorRole.HighlightedText, TEXT_COLOR)

        self.setPalette(palette)

        # Stylized comprehensive stylesheet
        self.setStyleSheet("""
            QMainWindow {
                background-color: #F5F5F5;
                border-radius: 10px;
                border: 1px solid #DCDCDC;
            }
            QWidget {
                font-size: 14px;
                font-family: 'Segoe UI', Arial, sans-serif;
            }
            QTabWidget::pane {
                border: 1px solid #CCCCCC;
                border-radius: 8px;
            }
            QTabBar::tab {
                background-color: #FFFFFF;
                color: #1E1E1E;
                padding: 10px 20px;
                margin-right: 6px;
                border-top-left-radius: 10px;
                border-top-right-radius: 10px;
                transition: background-color 0.3s ease, color 0.3s ease;
            }
            QTabBar::tab:selected {
                background-color: #B4DCFF;
                color: #003366;
                font-weight: bold;
            }
            QPushButton {
                background-color: #DCDCDC;
                color: #1E1E1E;
                border: 2px solid #CCCCCC;
                padding: 10px 16px;
                border-radius: 10px;
                font-weight: bold;
                transition: background-color 0.3s ease, box-shadow 0.3s ease;
            }
            QPushButton:hover {
                background-color: #E6E6E6;
                box-shadow: 0 0 10px rgba(0, 0, 0, 0.15);
            }
            QPushButton:pressed {
                background-color: #CCCCCC;
                box-shadow: 0 0 5px rgba(0, 0, 0, 0.25);
            }
            QTextEdit {
                background-color: #FFFFFF;
                color: #1E1E1E;
                border: 1px solid #CCCCCC;
                border-radius: 8px;
                padding: 10px;
                selection-background-color: #B4DCFF;
                selection-color: #003366;
            }
            QLabel {
                color: #1E1E1E;
            }
            QLineEdit {
                background-color: #FFFFFF;
                color: #1E1E1E;
                border: 1px solid #CCCCCC;
                border-radius: 8px;
                padding: 10px;
                selection-background-color: #B4DCFF;
                selection-color: #003366;
            }
            QMessageBox {
                background-color: #F5F5F5;
                border-radius: 10px;
            }
            QMessageBox QLabel {
                color: #1E1E1E;
            }
            QMenuBar {
                background-color: #F5F5F5;
                color: #1E1E1E;
                border-bottom: 1px solid #CCCCCC;
            }
            QMenuBar::item:selected {
                background-color: #B4DCFF;
                border-radius: 5px;
            }
            QMenu {
                background-color: #FFFFFF;
                color: #1E1E1E;
                border: 1px solid #CCCCCC;
                border-radius: 8px;
            }
            QMenu::item:selected {
                background-color: #E6E6E6;
                border-radius: 5px;
            }
            QScrollBar:vertical {
                border: none;
                background-color: #F5F5F5;
                width: 12px;
                margin: 0;
            }
            QScrollBar::handle:vertical {
                background-color: #CCCCCC;
                border-radius: 6px;
                min-height: 20px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0;
            }
        """)