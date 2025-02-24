# Behavioral System Test Interface

A test interface for a behavioral system using Raspberry Pi 5 with OLED displays and GPIO inputs.

## Hardware Setup

- 2x OLED displays (128x64, SSD1306)
  - Left display: I2C address 0x3C
  - Right display: I2C address 0x3D
- GPIO inputs (all with pull-up)
  - GPIO 23: Right lever
  - GPIO 24: Left lever
  - GPIO 17: Nose poke

## Initial Raspberry Pi Configuration

1. Enable required interfaces:
   ```bash
   sudo raspi-config
   # Navigate to: Interface Options -> I2C -> Enable -> Yes
   # Navigate to: Interface Options -> GPIO -> Enable -> Yes
   # Select: Finish
   ```

2. Add user to required groups:
   ```bash
   sudo usermod -aG gpio,i2c $USER
   ```

3. Enable and start GPIO system service:
   ```bash
   sudo systemctl enable pigpiod
   sudo systemctl start pigpiod
   ```

4. Verify services are running:
   ```bash
   # Check GPIO daemon status
   sudo systemctl status pigpiod
   
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
├── test_interface.py
└── hardware/
    ├── __init__.py
    ├── io_controller.py
    └── display_utils.py
```