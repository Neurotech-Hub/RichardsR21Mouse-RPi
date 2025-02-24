try:
    import lgpio
    from board import SCL, SDA
    import busio
    import adafruit_ssd1306
    SIMULATION_MODE = False
except (ImportError, NotImplementedError):
    print("Hardware interfaces not available - running in simulation mode")
    SIMULATION_MODE = True

class IOController:
    def __init__(self):
        # Define GPIO pins
        self.PIN_LEVER_RIGHT = 23
        self.PIN_LEVER_LEFT = 24
        self.PIN_NOSE_POKE = 17
        
        if not SIMULATION_MODE:
            try:
                # Setup I2C
                i2c = busio.I2C(SCL, SDA)
                
                # Try to initialize each display independently
                self.display_left = self._init_display(i2c, 0x3C, "left")
                self.display_right = self._init_display(i2c, 0x3D, "right")
                
                try:
                    # Setup GPIO using lgpio
                    self.gpio_handle = lgpio.gpiochip_open(0)
                    
                    # Configure pins as inputs with pull-ups
                    for pin in [self.PIN_LEVER_RIGHT, self.PIN_LEVER_LEFT, self.PIN_NOSE_POKE]:
                        lgpio.gpio_claim_input(self.gpio_handle, pin)
                        # Set internal pull-up
                        lgpio.gpio_pull_up(self.gpio_handle, pin)
                    
                    self._simulated_inputs = False
                    print("GPIO inputs initialized successfully")
                    
                except Exception as e:
                    print(f"Failed to initialize GPIO inputs: {e}")
                    print("Switching to simulation mode for inputs")
                    self._init_simulated_inputs()
                    
            except (ValueError, OSError) as e:
                print(f"Failed to initialize I2C bus: {e}")
                print("Switching to full simulation mode")
                self._init_simulation()
        else:
            self._init_simulation()
    
    def _init_display(self, i2c, address, name):
        """Initialize a single display, return DummyDisplay if fails"""
        try:
            display = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c, addr=address)
            print(f"Successfully initialized {name} display at address 0x{address:02X}")
            return display
        except (ValueError, OSError) as e:
            print(f"Failed to initialize {name} display at address 0x{address:02X}: {e}")
            print(f"Using simulation mode for {name} display")
            return DummyDisplay(128, 64)
    
    def _init_simulated_inputs(self):
        """Initialize just the input simulation"""
        self._simulated_inputs = True
        self._simulated_states = {
            'right_lever': False,
            'left_lever': False,
            'nose_poke': False
        }
    
    def _init_simulation(self):
        """Initialize full simulation mode with dummy hardware"""
        self.display_left = DummyDisplay(128, 64)
        self.display_right = DummyDisplay(128, 64)
        self._init_simulated_inputs()
        
    def get_input_states(self):
        if not hasattr(self, '_simulated_inputs') or not self._simulated_inputs:
            return {
                'right_lever': not lgpio.gpio_read(self.gpio_handle, self.PIN_LEVER_RIGHT),  # Inverted due to pull-up
                'left_lever': not lgpio.gpio_read(self.gpio_handle, self.PIN_LEVER_LEFT),
                'nose_poke': not lgpio.gpio_read(self.gpio_handle, self.PIN_NOSE_POKE)
            }
        else:
            return self._simulated_states
    
    def clear_displays(self):
        self.display_left.fill(0)
        self.display_right.fill(0)
        self.display_left.show()
        self.display_right.show()
    
    def __del__(self):
        """Cleanup GPIO on object destruction"""
        if not SIMULATION_MODE and not hasattr(self, '_simulated_inputs'):
            try:
                lgpio.gpiochip_close(self.gpio_handle)
            except:
                pass

class DummyDisplay:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        
    def fill(self, color):
        pass
        
    def show(self):
        pass
        
    def image(self, img):
        pass 