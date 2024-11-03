# message_box_patch.py

from PyQt6.QtWidgets import QMessageBox, QPushButton
from PyQt6.QtCore import QTimer

original_question = QMessageBox.question
original_information = QMessageBox.information
original_warning = QMessageBox.warning
original_critical = QMessageBox.critical
original_about = QMessageBox.about
original_init = QMessageBox.__init__

def get_localization(parent):
    while parent:
        if hasattr(parent, 'Localization'):
            return parent.Localization
        parent = parent.parent()
    return None

def localize_buttons(msg_box, parent):
    localization = get_localization(parent)
    if not localization:
        return

    button_mapping = {
        QMessageBox.StandardButton.Ok: 'lables.ok',
        QMessageBox.StandardButton.Cancel: 'lables.cancel',
        QMessageBox.StandardButton.Yes: 'lables.yes',
        QMessageBox.StandardButton.No: 'lables.no',
        QMessageBox.StandardButton.Abort: 'lables.abort',
        QMessageBox.StandardButton.Retry: 'lables.retry',
        QMessageBox.StandardButton.Ignore: 'lables.ignore',
    }

    for button in msg_box.buttons():
        standard_button = msg_box.standardButton(button)
        if standard_button in button_mapping:
            button.setText(localization.translate(button_mapping[standard_button]))

def create_patched_method(original_method):
    def patched_method(parent, title, text, buttons=QMessageBox.StandardButton.Ok, defaultButton=QMessageBox.StandardButton.NoButton):
        msg_box = QMessageBox(parent)
        msg_box.setWindowTitle(title)
        msg_box.setText(text)
        msg_box.setStandardButtons(buttons)
        msg_box.setDefaultButton(defaultButton)
        
        if original_method == QMessageBox.question:
            msg_box.setIcon(QMessageBox.Icon.Question)
        elif original_method == QMessageBox.information:
            msg_box.setIcon(QMessageBox.Icon.Information)
        elif original_method == QMessageBox.warning:
            msg_box.setIcon(QMessageBox.Icon.Warning)
        elif original_method == QMessageBox.critical:
            msg_box.setIcon(QMessageBox.Icon.Critical)

        QTimer.singleShot(0, lambda: localize_buttons(msg_box, parent))
        
        return msg_box.exec()

    return patched_method

def patched_about(parent, title, text):
    msg_box = QMessageBox(parent)
    msg_box.setWindowTitle(title)
    msg_box.setText(text)
    msg_box.setIcon(QMessageBox.Icon.Information)
    msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
    
    QTimer.singleShot(0, lambda: localize_buttons(msg_box, parent))
    
    return msg_box.exec()

def apply_patches():
    QMessageBox.question = create_patched_method(QMessageBox.question)
    QMessageBox.information = create_patched_method(QMessageBox.information)
    QMessageBox.warning = create_patched_method(QMessageBox.warning)
    QMessageBox.critical = create_patched_method(QMessageBox.critical)
    QMessageBox.about = patched_about

    def patched_init(self, *args, **kwargs):
        original_init(self, *args, **kwargs)
        QTimer.singleShot(0, lambda: localize_buttons(self, self.parent()))
    QMessageBox.__init__ = patched_init

def revert_patches():
    QMessageBox.question = original_question
    QMessageBox.information = original_information
    QMessageBox.warning = original_warning
    QMessageBox.critical = original_critical
    QMessageBox.about = original_about
    QMessageBox.__init__ = original_init

# Optional: Add a context manager for temporary patching
from contextlib import contextmanager

@contextmanager
def localized_message_boxes():
    apply_patches()
    try:
        yield
    finally:
        revert_patches()