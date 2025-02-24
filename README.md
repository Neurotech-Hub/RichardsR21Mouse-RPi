# Behavioral System Test Interface

A test interface for a behavioral system using Raspberry Pi 5 with OLED displays and GPIO inputs.

## Hardware Setup

- 2x OLED displays (128x64, SSD1306)
  - Left display: I2C address 0x3C
  - Right display: I2C address 0x3D (hardware modification)
- GPIO inputs (all with pull-up)
  - GPIO 23: Right lever
  - GPIO 24: Left lever
  - GPIO 17: Nose poke

## Initial Raspberry Pi Configuration

1. Enable required interfaces:
   ```bash
   sudo raspi-config
   # Navigate to: Interface Options -> I2C -> Enable -> Yes
   # Select: Finish
   ```

2. Install system packages:
   ```bash
   sudo apt-get update
   sudo apt-get install -y python3-gpiozero i2c-tools
   ```

3. Add user to I2C group:
   ```bash
   sudo usermod -aG i2c $USER
   ```

4. Verify setup (after reboot):
   ```bash
   # Test GPIO functionality
   python gpio_test.py
   
   # Check I2C devices
   i2cdetect -y 1
   ```

5. Reboot the Raspberry Pi:
   ```bash
   sudo reboot
   ```

## Software Setup

1. Create and activate virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Linux/Mac
   # or
   venv\Scripts\activate  # On Windows
   ```

2. Install requirements:
   ```bash
   pip install -r requirements.txt
   ```

   Note: When running on non-Raspberry Pi systems (macOS, Windows), the program will automatically run in simulation mode. Hardware-specific packages will only be installed on Raspberry Pi.

## Running the Test Interface

1. On Raspberry Pi:
   - Ensure all hardware is properly connected according to the hardware setup section
   - Run: `python test_interface.py`

2. On other systems (Simulation Mode):
   - Run: `python test_interface.py`
   - The interface will run in simulation mode with dummy hardware

## Features

The GUI interface provides:
- Real-time monitoring of input states (levers and nose poke)
- Display test patterns for both OLED screens
- Display clearing functionality

## Exit

- Press Ctrl+C in the terminal
- Or close the GUI window

## Project Structure
```
.
├── README.md
├── requirements.txt
├── gpio_test.py
├── test_interface.py
└── hardware/
    ├── __init__.py
    ├── io_controller.py
    └── display_utils.py
```