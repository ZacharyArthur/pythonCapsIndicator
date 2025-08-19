# MIT License
# 
# Copyright (c) 2025 ZacharyArthur
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import argparse
import ctypes
import platform
import sys

from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont, QGuiApplication
from PyQt5.QtWidgets import QApplication, QLabel, QWidget

# Constants
CAPS_LOCK_VK = 0x14  # Virtual key code for Caps Lock
NUMLOCK_VK = 0x90  # Virtual key code for Num Lock
SCROLLLOCK_VK = 0x91  # Virtual key code for Scroll Lock

IS_WINDOWS = platform.system() == "Windows"

DEFAULT_POLLING_INTERVAL = 250  # milliseconds
DEFAULT_HIDE_TIME = 1500  # milliseconds
DEFAULT_WINDOW_WIDTH = 500  # pixels
DEFAULT_WINDOW_HEIGHT = 80  # pixels
DEFAULT_FONT_SIZE = 18  # points
BORDER_RADIUS = 8  # pixels
LABEL_PADDING = 12  # pixels


# Function to check the Caps Lock status using ctypes
def get_caps_lock_state() -> bool:
    """Get the current state of the Caps Lock key using Windows API."""
    if not IS_WINDOWS:
        return False  # Default state for non-Windows systems

    try:
        return ctypes.windll.user32.GetKeyState(CAPS_LOCK_VK) & 0x0001 != 0
    except (AttributeError, OSError):
        return False  # Fallback if Windows API is unavailable


# Function to check the Num Lock status using ctypes
def get_numlock_state() -> bool:
    """Get the current state of the Num Lock key using Windows API."""
    if not IS_WINDOWS:
        return False  # Default state for non-Windows systems

    try:
        return ctypes.windll.user32.GetKeyState(NUMLOCK_VK) & 0x0001 != 0
    except (AttributeError, OSError):
        return False  # Fallback if Windows API is unavailable


# Function to check the Scroll Lock status using ctypes
def get_scrolllock_state() -> bool:
    """Get the current state of the Scroll Lock key using Windows API."""
    if not IS_WINDOWS:
        return False  # Default state for non-Windows systems

    try:
        return ctypes.windll.user32.GetKeyState(SCROLLLOCK_VK) & 0x0001 != 0
    except (AttributeError, OSError):
        return False  # Fallback if Windows API is unavailable


# Create PyQt5 window
class CapsLockWindow(QWidget):
    """
    Main application window for displaying lock key status indicator.

    A translucent overlay window that monitors and displays the status of
    Caps Lock, Num Lock, and Scroll Lock keys with color-coded visual feedback.
    """

    def __init__(
        self, hide_time: int = 1000, polling_rate: int = DEFAULT_POLLING_INTERVAL
    ) -> None:
        super().__init__()
        self.hide_time = hide_time  # Time (milliseconds) after which to hide the window
        self.is_shown = False
        self.current_caps_state = None
        self.current_numlock_state = None
        self.current_scrolllock_state = None
        self.setWindowTitle("Lock Keys Status")

        primary_screen = QGuiApplication.primaryScreen().geometry()
        screen_width = primary_screen.width()
        screen_height = primary_screen.height()

        indicator_width = DEFAULT_WINDOW_WIDTH
        indicator_height = DEFAULT_WINDOW_HEIGHT

        # Center the window on screen
        self.setGeometry(
            (screen_width - indicator_width) // 2,
            (screen_height - indicator_height) // 2,
            indicator_width,
            indicator_height,
        )

        # Set window to be frameless, always on top, and persistent even when the application loses focus
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setStyleSheet("background: rgba(255, 255, 255, 0);")

        # Set initial label text based on platform
        if IS_WINDOWS:
            self.label = QLabel("CAPS: OFF | NUM: OFF | SCROLL: OFF", self)
        else:
            self.label = QLabel("Windows-only feature", self)
        # Modern, subtle but visible styling
        self.label.setStyleSheet(self._get_label_style(has_active_keys=False))
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setFont(QFont("Arial", DEFAULT_FONT_SIZE, QFont.Medium))
        self.label.resize(indicator_width, indicator_height)

        # Timer to update the lock key status
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_status)
        self.timer.start(polling_rate)

        # Timer to hide the window after specified time
        self.hide_timer = QTimer(self)
        self.hide_timer.timeout.connect(self.hide_window)

    def _get_label_style(self, has_active_keys: bool = False) -> str:
        """Get label styling CSS with color coding for key states."""
        if has_active_keys:
            # Green theme for when any keys are active
            return f"""
                color: #FFFFFF;
                background-color: #27AE60;
                border: 1px solid #2ECC71;
                border-radius: {BORDER_RADIUS}px;
                padding: {LABEL_PADDING}px;
                font-weight: 500;
            """
        else:
            # Gray theme for when all keys are off
            return f"""
                color: #FFFFFF;
                background-color: #2C3E50;
                border: 1px solid #34495E;
                border-radius: {BORDER_RADIUS}px;
                padding: {LABEL_PADDING}px;
                font-weight: 500;
            """

    def update_status(self) -> None:
        # On non-Windows systems, show platform message once and return
        if not IS_WINDOWS:
            if not self.is_shown:
                self.show()
                self.is_shown = True
            return

        caps_lock_active = get_caps_lock_state()
        num_lock_active = get_numlock_state()
        scroll_lock_active = get_scrolllock_state()

        # Show window only if any state has changed
        if (
            caps_lock_active != self.current_caps_state
            or num_lock_active != self.current_numlock_state
            or scroll_lock_active != self.current_scrolllock_state
        ):
            self.current_caps_state = caps_lock_active
            self.current_numlock_state = num_lock_active
            self.current_scrolllock_state = scroll_lock_active

            # Build status text
            caps_display_text = "ON" if caps_lock_active else "OFF"
            num_display_text = "ON" if num_lock_active else "OFF"
            scroll_display_text = "ON" if scroll_lock_active else "OFF"

            self.label.setText(
                f"CAPS: {caps_display_text} | NUM: {num_display_text} | SCROLL: {scroll_display_text}"
            )

            # Apply color-coded styling based on key states
            any_keys_active = caps_lock_active or num_lock_active or scroll_lock_active
            self.label.setStyleSheet(
                self._get_label_style(has_active_keys=any_keys_active)
            )

            self.show()
            self.is_shown = True
            self.hide_timer.start(self.hide_time)

    def hide_window(self) -> None:
        self.hide()
        self.is_shown = False
        self.hide_timer.stop()


def main() -> None:
    """Main application entry point with command line argument parsing."""
    parser = argparse.ArgumentParser(
        description="Python Caps Lock Indicator - Visual indicator for lock key states",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--hide-time",
        type=int,
        default=DEFAULT_HIDE_TIME,
        help="Time in milliseconds to display the indicator",
    )
    parser.add_argument(
        "--polling-rate",
        type=int,
        default=DEFAULT_POLLING_INTERVAL,
        help="Polling interval in milliseconds for checking key states",
    )

    args = parser.parse_args()

    app = QApplication(sys.argv)
    window = CapsLockWindow(args.hide_time, args.polling_rate)
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
