import os
import shutil
import zipfile
from datetime import datetime
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                            QTableWidget, QTableWidgetItem, QHeaderView,
                            QLabel, QMessageBox)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QPixmap
from configparser import ConfigParser
import subprocess
import psutil
import threading
import time
import ctypes
from dotenv import load_dotenv
import os
load_dotenv()


class SaveBackupTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.Localization = parent.Localization if parent else None
        self.main_window = parent
        self.auto_backup_timer = None
        # GameMan pointer address
        self.GAME_MAN_PTR = int(os.getenv("GameMan"), 16)
        self.init_ui()
        self.load_settings()
        # Start game monitoring timer
        self.game_monitor_timer = QTimer()
        self.game_monitor_timer.timeout.connect(self.check_game_status)
        self.game_monitor_timer.start(5000)  # Check every 5 seconds

    def check_game_status(self):
        """Monitor game process and stop auto-backup if game exits"""
        if hasattr(self, 'backup_running') and self.backup_running:
            if not self.is_game_running():
                self.stop_auto_backup()

    def clean_old_backups(self):
        """Delete old backups if max limit is reached"""
        settings = self.get_settings()
        backup_dir = settings.get('backup_directory', '')
        max_backups = int(settings.get('max_backups', '20'))

        if not backup_dir or not os.path.exists(backup_dir):
            return

        # Get list of backup files with their timestamps
        backups = []
        for file in os.listdir(backup_dir):
            if file.endswith('.zip') and file.startswith('backup_'):
                file_path = os.path.join(backup_dir, file)
                timestamp = os.path.getmtime(file_path)
                backups.append((file_path, timestamp))

        # Sort by timestamp (oldest first)
        backups.sort(key=lambda x: x[1])

        # Remove oldest backups if we exceed the limit
        while len(backups) > max_backups:
            oldest_backup = backups.pop(0)  # Remove and get oldest backup
            try:
                os.remove(oldest_backup[0])
            except Exception as e:
                pass
                #print(f"Failed to remove old backup {oldest_backup[0]}: {e}")

    def request_save_file(self):
        """Request the game to create a save file by writing to memory"""
        try:
            # Define necessary Windows constants
            PROCESS_VM_READ = 0x0010
            PROCESS_VM_WRITE = 0x0020
            PROCESS_VM_OPERATION = 0x0008
            PROCESS_QUERY_INFORMATION = 0x0400

            # Get handle to the game process
            for proc in psutil.process_iter(['pid', 'name']):
                if proc.info['name'].lower() == 'eldenring.exe':
                    process_handle = ctypes.windll.kernel32.OpenProcess(
                        PROCESS_VM_READ | PROCESS_VM_WRITE | PROCESS_VM_OPERATION | PROCESS_QUERY_INFORMATION,
                        False,
                        proc.info['pid']
                    )
                    if process_handle:
                        try:
                            # Read the actual GameMan instance address from the pointer
                            game_man_value = ctypes.c_uint64()
                            bytes_read = ctypes.c_size_t()
                            
                            result = ctypes.windll.kernel32.ReadProcessMemory(
                                process_handle,
                                ctypes.c_uint64(self.GAME_MAN_PTR),
                                ctypes.byref(game_man_value),
                                ctypes.sizeof(game_man_value),
                                ctypes.byref(bytes_read)
                            )
                            
                            if not result:
                                error = ctypes.get_last_error()
                                #print(f"ReadProcessMemory failed with error: {error}")
                                return False
                                
                            # Calculate the final target address (GameMan instance + 0xB72)
                            target_address = game_man_value.value + 0xB72
                            
                            # Prepare the value to write (1 byte)
                            value = ctypes.c_ubyte(1)
                            bytes_written = ctypes.c_size_t()
                            
                            # Write to process memory
                            result = ctypes.windll.kernel32.WriteProcessMemory(
                                process_handle,
                                ctypes.c_uint64(target_address),
                                ctypes.byref(value),
                                ctypes.sizeof(value),
                                ctypes.byref(bytes_written)
                            )
                            
                            if result:
                                #print(f"Successfully wrote to memory at {hex(target_address)}")
                                return True
                            else:
                                error = ctypes.get_last_error()
                                #print(f"WriteProcessMemory failed with error: {error}")
                                return False
                        finally:
                            ctypes.windll.kernel32.CloseHandle(process_handle)
            return False
        except Exception as e:
            #print(f"Failed to request save file: {e}")
            return False

    def load_settings(self):
        """Load settings and setup auto backup if enabled"""
        settings = self.get_settings()

    def init_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Screenshot preview
        self.screenshot_label = QLabel()
        self.screenshot_label.setFixedSize(800, 450)  # 16:9 aspect ratio
        self.screenshot_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.screenshot_label.setStyleSheet("border: 1px solid gray;")
        layout.addWidget(self.screenshot_label)

        # Auto backup status
        self.auto_backup_status = QLabel(self.Localization.translate("ui.save_backup.auto_backup_not_running"))
        self.auto_backup_status.setStyleSheet("color: red;")
        layout.addWidget(self.auto_backup_status)

        # Backup table
        self.backup_table = QTableWidget(0, 2)
        self.backup_table.setHorizontalHeaderLabels([self.Localization.translate("ui.save_backup.backup_name"), self.Localization.translate("ui.save_backup.date")])
        self.backup_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.backup_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.backup_table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.backup_table.itemSelectionChanged.connect(self.on_backup_selected)
        # Make table cells read-only
        self.backup_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        layout.addWidget(self.backup_table)

        # Buttons
        button_layout = QHBoxLayout()
        
        self.save_button = QPushButton(self.Localization.translate("ui.save_backup.save_backup"))
    
        self.save_button.clicked.connect(self.save_backup)
        button_layout.addWidget(self.save_button)

        self.load_button = QPushButton(self.Localization.translate("ui.save_backup.load_backup"))
        self.load_button.clicked.connect(self.load_backup)
        self.load_button.setEnabled(False)
        button_layout.addWidget(self.load_button)

        self.refresh_button = QPushButton(self.Localization.translate("ui.game_session.refresh"))
        self.refresh_button.clicked.connect(self.refresh_backups)
        button_layout.addWidget(self.refresh_button)

        self.delete_button = QPushButton(self.Localization.translate("ui.save_backup.delete"))
        self.delete_button.clicked.connect(self.delete_backup)
        self.delete_button.setEnabled(False)
        button_layout.addWidget(self.delete_button)

        layout.addLayout(button_layout)

        # Auto backup buttons
        auto_backup_layout = QHBoxLayout()
        
        self.start_auto_backup_button = QPushButton(self.Localization.translate("ui.save_backup.start_auto_backup"))
        self.start_auto_backup_button.clicked.connect(self.start_auto_backup)
        auto_backup_layout.addWidget(self.start_auto_backup_button)

        self.stop_auto_backup_button = QPushButton(self.Localization.translate("ui.save_backup.stop_auto_backup"))
        self.stop_auto_backup_button.clicked.connect(self.stop_auto_backup)
        self.stop_auto_backup_button.setEnabled(False)
        auto_backup_layout.addWidget(self.stop_auto_backup_button)

        layout.addLayout(auto_backup_layout)

        # Load initial backups
        self.refresh_backups()

    def get_settings(self):
        config = ConfigParser()
        settings_path = os.path.join(os.environ['APPDATA'], 'SeamlessCo-opUpdater', 'settings.ini')
        if os.path.exists(settings_path):
            config.read(settings_path)
            return config['Settings']
        return {}

    def is_game_running(self):
        return "eldenring.exe" in (p.name().lower() for p in psutil.process_iter())

    def take_screenshot(self):
        try:
            import pyautogui
            screenshot = pyautogui.screenshot()
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            temp_path = f"temp_screenshot_{timestamp}.png"
            screenshot.save(temp_path)
            return temp_path
        except Exception as e:
            return None

    def save_backup(self):
        if not self.is_game_running():
            return

        # First request the game to create a save file
        if not self.request_save_file():
            QMessageBox.warning(self, self.Localization.translate('lables.error'), "Failed to request save file from game")
            return

        # Wait a short moment for the save file to be written
        time.sleep(0.5)

        settings = self.get_settings()
        save_type = settings.get('save_file_type', 'ER0000.co2')
        backup_dir = settings.get('backup_directory', '')
        steam_id = settings.get('steam_id', '')

        if not all([backup_dir, steam_id]):
            QMessageBox.warning(self, self.Localization.translate('lables.error'), self.Localization.translate('messages.errors.backup_settings'))
            return

        try:
            # Create backup directory if it doesn't exist
            if not os.path.exists(backup_dir):
                os.makedirs(backup_dir)

            # Clean up old backups if needed
            self.clean_old_backups()

            # Source save file path
            save_dir = os.path.join(os.environ['APPDATA'], 'EldenRing', steam_id)
            save_path = os.path.join(save_dir, save_type)

            if not os.path.exists(save_path):
                QMessageBox.warning(self, "Error", f"Save file not found: {save_path}")
                return

            # Take screenshot
            screenshot_path = self.take_screenshot()

            # Create backup with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_name = f"backup_{timestamp}.zip"
            backup_path = os.path.join(backup_dir, backup_name)

            # Create ZIP archive with save file and screenshot
            with zipfile.ZipFile(backup_path, 'w') as zipf:
                zipf.write(save_path, os.path.basename(save_path))
                if screenshot_path:
                    zipf.write(screenshot_path, f"screenshot_{timestamp}.png")
                    os.remove(screenshot_path)  # Clean up temporary screenshot

            # After successful save, refresh and select the new backup
            self.refresh_backups()
            self.backup_table.selectRow(0)  # Select the most recent backup

            # Play sound if enabled
            if bool(int(settings.get('enable_sounds', '0'))):
                sound_path = os.path.join("assets", "save_notification.wav")
                if os.path.exists(sound_path):
                    subprocess.run(['powershell', '-c', f'(New-Object Media.SoundPlayer "{sound_path}").PlaySync()'])
                else:
                    subprocess.run(['powershell', '-c', '(New-Object Media.SoundPlayer "C:\\Windows\\Media\\notify.wav").PlaySync()'])

            self.refresh_backups()

        except Exception as e:
            QMessageBox.critical(self, self.Localization.translate('lables.error'), self.Localization.translate('messages.errors.backup_create').format(str(e)))
            self.Localization.translate('messages.errors.backup_settings')

    def load_backup(self):
        selected_items = self.backup_table.selectedItems()
        if not selected_items:
            return

        settings = self.get_settings()
        save_type = settings.get('save_file_type', 'ER0000.co2')
        backup_dir = settings.get('backup_directory', '')
        steam_id = settings.get('steam_id', '')

        try:
            # Get selected backup
            backup_name = selected_items[0].text()
            backup_path = os.path.join(backup_dir, backup_name)

            # Target save file path
            save_dir = os.path.join(os.environ['APPDATA'], 'EldenRing', steam_id)
            save_path = os.path.join(save_dir, save_type)

            # Create backup of current save
            if os.path.exists(save_path):
                backup_current = save_path + '.backup'
                shutil.copy2(save_path, backup_current)

            # Extract save file from zip
            with zipfile.ZipFile(backup_path, 'r') as zipf:
                zipf.extract(save_type, save_dir)

            # Play sound if enabled
            if bool(int(settings.get('enable_sounds', '0'))):
                sound_path = os.path.join("assets", "load_notification.wav")
                if os.path.exists(sound_path):
                    subprocess.run(['powershell', '-c', f'(New-Object Media.SoundPlayer "{sound_path}").PlaySync()'])
                else:
                    subprocess.run(['powershell', '-c', '(New-Object Media.SoundPlayer "C:\\Windows\\Media\\notify.wav").PlaySync()'])

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load backup: {str(e)}")

    def refresh_backups(self):
        settings = self.get_settings()
        backup_dir = settings.get('backup_directory', '')
        if not backup_dir or not os.path.exists(backup_dir):
            return
        
        # Store the current selection if any
        current_row = self.backup_table.currentRow()
        
        self.backup_table.setRowCount(0)
        backups = []
        for file in os.listdir(backup_dir):
            if file.endswith('.zip') and file.startswith('backup_'):
                file_path = os.path.join(backup_dir, file)
                timestamp = os.path.getmtime(file_path)
                date_str = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
                backups.append((file, date_str))

        # Sort backups by date (newest first)
        backups.sort(key=lambda x: x[1], reverse=True)

        for i, (file, date) in enumerate(backups):
            self.backup_table.insertRow(i)
            self.backup_table.setItem(i, 0, QTableWidgetItem(file))
            self.backup_table.setItem(i, 1, QTableWidgetItem(date))

        # Select the most recent backup (row 0) if this is after a new save,
        # otherwise maintain the previous selection
        if current_row == -1 or current_row >= len(backups):
            self.backup_table.selectRow(0)
        else:
            self.backup_table.selectRow(current_row)

    def delete_backup(self):
        selected_items = self.backup_table.selectedItems()
        if not selected_items:
            return
        
        reply = QMessageBox.question(self, self.Localization.translate("ui.save_backup.confirm_delete_title"), 
                                   self.Localization.translate("ui.save_backup.confirm_delete?"),
                                   QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        
        if reply == QMessageBox.StandardButton.Yes:
            settings = self.get_settings()
            backup_dir = settings.get('backup_directory', '')
            backup_name = selected_items[0].text()
            backup_path = os.path.join(backup_dir, backup_name)

            try:
                os.remove(backup_path)
                self.refresh_backups()
                self.screenshot_label.clear()
            
                QMessageBox.information(self, self.Localization.translate('lables.success'), self.Localization.translate("ui.save_backup.backup_deleted"))
            except Exception as e:
                QMessageBox.critical(self, self.Localization.translate('lables.error'), self.Localization.translate("ui.save_backup.backup_not_deleted").format(str(e)))

    def on_backup_selected(self):
        selected_items = self.backup_table.selectedItems()
        has_selection = bool(selected_items)
        
        self.load_button.setEnabled(has_selection)
        self.delete_button.setEnabled(has_selection)

        if has_selection:
            settings = self.get_settings()
            backup_dir = settings.get('backup_directory', '')
            backup_name = selected_items[0].text()
            backup_path = os.path.join(backup_dir, backup_name)

            try:
                with zipfile.ZipFile(backup_path, 'r') as zipf:
                    screenshot_files = [f for f in zipf.namelist() if f.startswith('screenshot_')]
                    if screenshot_files:
                        screenshot_data = zipf.read(screenshot_files[0])
                        pixmap = QPixmap()
                        pixmap.loadFromData(screenshot_data)
                        scaled_pixmap = pixmap.scaled(self.screenshot_label.size(), 
                                                    Qt.AspectRatioMode.KeepAspectRatio,
                                                    Qt.TransformationMode.SmoothTransformation)
                        self.screenshot_label.setPixmap(scaled_pixmap)
                    else:
                        self.screenshot_label.clear()
            except Exception as e:
                self.screenshot_label.clear()

    def start_auto_backup(self):
        if not self.is_game_running():
            QMessageBox.warning(self, self.Localization.translate('lables.error'), 
                              "Game must be running to start auto-backup")
            return

        # Check if backup is already running
        if hasattr(self, 'backup_running') and self.backup_running:
            return  # Exit if backup is already running
            
        settings = self.get_settings()
        self.backup_interval = int(settings.get('auto_backup_interval', '5'))
        
        # Stop any existing backup thread (shouldn't be necessary with the check above, but just in case)
        self.stop_auto_backup_thread()
        
        # Create and start new backup thread
        self.backup_thread = threading.Thread(target=self.run_periodic_backup, daemon=True)
        self.backup_running = True
        self.backup_thread.start()
        
        self.auto_backup_status.setText(
            self.Localization.translate("ui.save_backup.backup_auto_backup_running").format(self.backup_interval)
        )
        self.auto_backup_status.setStyleSheet("color: green;")
        
        self.start_auto_backup_button.setEnabled(False)
        self.stop_auto_backup_button.setEnabled(True)

    def stop_auto_backup(self):
        self.stop_auto_backup_thread()
        
        self.auto_backup_status.setText(
            self.Localization.translate("ui.save_backup.backup_auto_backup_not_running")
        )
        self.auto_backup_status.setStyleSheet("color: red;")
        
        self.start_auto_backup_button.setEnabled(True)
        self.stop_auto_backup_button.setEnabled(False)

    def run_periodic_backup(self):
        """Run periodic backup in a separate thread"""
        while self.backup_running:
            try:
                if self.is_game_running():
                    self.save_backup()
                else:
                    # Game has exited, stop auto-backup
                    self.backup_running = False
                    break
            except Exception as e:
                pass
                #print(f"Backup error: {e}")
                
            # Sleep for the specified interval (in minutes)
            for _ in range(self.backup_interval * 60):
                if not self.backup_running:
                    break
                time.sleep(1)

        # If we exit the loop, make sure the UI is updated
        if hasattr(self, 'backup_running') and not self.backup_running:
            self.stop_auto_backup()

    def stop_auto_backup_thread(self):
        """Safely stop the backup thread"""
        if hasattr(self, 'backup_running'):
            self.backup_running = False
        if hasattr(self, 'backup_thread') and self.backup_thread and self.backup_thread.is_alive():
            self.backup_thread.join(timeout=1)
