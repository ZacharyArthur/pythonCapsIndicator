# Python Caps Lock Indicator

A PyQt5-based visual indicator for Caps Lock and Num Lock status on Windows systems.

## Description

This application provides a translucent overlay that appears whenever you toggle Caps Lock or Num Lock keys. The indicator shows the current status of both keys and automatically disappears after a configurable timeout.

## Features

- Real-time monitoring of Caps Lock and Num Lock states
- Modern, translucent overlay window
- Auto-hide functionality (configurable timeout)
- Always-on-top display
- Frameless, centered window design

## Requirements

- Windows operating system (uses Windows API via ctypes)
- Python 3.6+
- PyQt5

## Installation

1. Clone this repository or download the files
2. Create a virtual environment:
   ```bash
   python -m venv venv
   ```
3. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - Linux/macOS: `source venv/bin/activate`
4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the application:
```bash
python caps_indicator.py
```

The application will run in the background and show a visual indicator whenever you toggle Caps Lock or Num Lock.

## Configuration

You can modify the `hide_time` parameter in the `main()` function to change how long the indicator stays visible (in milliseconds). Default is 1500ms (1.5 seconds).

## Technical Details

- Uses Windows API calls through `ctypes` to monitor key states
- Polls key states every 100ms for responsive updates
- Window styling uses modern CSS-like properties for a clean appearance

## Limitations

- Currently Windows-only due to platform-specific API usage
- Requires GUI environment (won't work in headless systems)

## Development

This project is developed in WSL2 Ubuntu for a Windows target environment.