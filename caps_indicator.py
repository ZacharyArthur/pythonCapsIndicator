import ctypes
import sys

from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont, QGuiApplication
from PyQt5.QtWidgets import QApplication, QLabel, QWidget


# Function to check the Caps Lock status using ctypes
def get_caps_lock_state():
    # Get the current state of the Caps Lock key using ctypes (Windows API)
    return ctypes.windll.user32.GetKeyState(0x14) & 0x0001 != 0


# Function to check the Num Lock status using ctypes
def get_numlock_state():
    # Get the current state of the Num Lock key using ctypes (Windows API)
    return ctypes.windll.user32.GetKeyState(0x90) & 0x0001 != 0


# Create PyQt5 window
class CapsLockWindow(QWidget):
    def __init__(self, hide_time=1000):
        super().__init__()
        self.hide_time = hide_time  # Time (milliseconds) after which to hide the window
        self.is_shown = False
        self.current_caps_state = None
        self.current_numlock_state = None
        self.setWindowTitle("Lock Keys Status")

        screen_geometry = QGuiApplication.primaryScreen().geometry()
        screen_width = screen_geometry.width()
        screen_height = screen_geometry.height()

        window_width = 400  # Increased width for longer text
        window_height = 80  # Keep same height

        # Center the window on screen
        self.setGeometry(
            (screen_width - window_width) // 2,
            (screen_height - window_height) // 2,
            window_width,
            window_height,
        )

        # Set window to be frameless, always on top, and persistent even when the application loses focus
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setStyleSheet("background: rgba(255, 255, 255, 0);")

        self.label = QLabel("CAPS: OFF | NUM: OFF", self)
        # Modern, subtle but visible styling
        self.label.setStyleSheet("""
            color: #FFFFFF;
            background-color: #2C3E50;
            border: 1px solid #34495E;
            border-radius: 8px;
            padding: 12px;
            font-weight: 500;
        """)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setFont(QFont("Arial", 18, QFont.Medium))
        self.label.resize(window_width, window_height)

        # Timer to update the Caps Lock status every 100ms
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_status)
        self.timer.start(100)

        # Timer to hide the window after specified time
        self.hide_timer = QTimer(self)
        self.hide_timer.timeout.connect(self.hide_window)

    def update_status(self):
        current_caps_state = get_caps_lock_state()
        current_numlock_state = get_numlock_state()

        # Show window only if either state has changed
        if (
            current_caps_state != self.current_caps_state
            or current_numlock_state != self.current_numlock_state
        ):
            self.current_caps_state = current_caps_state
            self.current_numlock_state = current_numlock_state

            # Build status text
            caps_text = "ON" if current_caps_state else "OFF"
            num_text = "ON" if current_numlock_state else "OFF"

            self.label.setText(f"CAPS: {caps_text} | NUM: {num_text}")

            # Same modern styling for all states
            self.label.setStyleSheet("""
                color: #FFFFFF;
                background-color: #2C3E50;
                border: 1px solid #34495E;
                border-radius: 8px;
                padding: 12px;
                font-weight: 500;
            """)

            self.show()
            self.is_shown = True
            self.hide_timer.start(self.hide_time)

    def hide_window(self):
        self.hide()
        self.is_shown = False
        self.hide_timer.stop()


def main():
    app = QApplication(sys.argv)
    hide_time = 1500  # Set how long the window stays visible after Caps Lock is toggled (milliseconds)
    window = CapsLockWindow(hide_time)
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()