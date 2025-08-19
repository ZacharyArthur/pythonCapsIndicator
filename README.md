# Python Caps Lock Indicator

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.6+](https://img.shields.io/badge/python-3.6+-blue.svg)](https://www.python.org/downloads/)
[![PyQt5](https://img.shields.io/badge/PyQt5-5.15.10+-green.svg)](https://pypi.org/project/PyQt5/)
[![Platform](https://img.shields.io/badge/platform-Windows-lightgrey.svg)](https://www.microsoft.com/windows)

A lightweight PyQt5-based visual indicator that displays real-time status of Caps Lock, Num Lock, and Scroll Lock keys on Windows systems. Features a modern translucent overlay with color-coded display and configurable auto-hide functionality.

## Quick Start

```bash
# Clone and run
git clone https://github.com/ZacharyArthur/pythonCapsIndicator.git
cd pythonCapsIndicator
pip install -r requirements.txt
python caps_indicator.py
```

## Features

- Real-time monitoring of Caps Lock, Num Lock, and Scroll Lock states
- Modern, translucent overlay window with color-coded display
- Auto-hide functionality (configurable timeout)
- Always-on-top display
- Frameless, centered window design
- Command line argument support for easy configuration
- Cross-platform compatibility (optimized for Windows)

## Installation

### Prerequisites
- Windows operating system
- Python 3.6+

### Setup
```bash
# Clone the repository
git clone https://github.com/ZacharyArthur/pythonCapsIndicator.git
cd pythonCapsIndicator

# Create and activate virtual environment (recommended)
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/macOS

# Install dependencies
pip install -r requirements.txt
```

## Usage

### Basic Usage
```bash
python caps_indicator.py
```

The application runs in the background and displays a translucent indicator whenever you toggle lock keys. The indicator shows status in the format: **"CAPS: ON | NUM: OFF | SCROLL: OFF"**

### Command Line Options
```bash
python caps_indicator.py --help
```

| Option | Description | Default |
|--------|-------------|---------|
| `--hide-time` | Display duration in milliseconds | 1500 |
| `--polling-rate` | Key state check interval in milliseconds | 250 |

### Examples
```bash
# Extended display with faster polling
python caps_indicator.py --hide-time 3000 --polling-rate 100

# Quick display
python caps_indicator.py --hide-time 1000
```

## Technical Notes

- **Platform**: Windows-optimized using `ctypes` for Windows API access
- **Performance**: Configurable polling (default 250ms) for responsive updates  
- **Display**: Color-coded translucent overlay with auto-hide functionality
- **Compatibility**: Graceful handling of non-Windows platforms

### Limitations
- Primary support for Windows systems
- Requires GUI environment (not suitable for headless systems)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

> **Note**: This application uses PyQt5 (GPL v3). For commercial distribution, consider PyQt5's commercial licensing options.