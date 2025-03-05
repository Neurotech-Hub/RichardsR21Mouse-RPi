try:
    from gpiozero import Button, DigitalOutputDevice
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
        self.PIN_WATER = 25
        
        if not SIMULATION_MODE:
            try:
                # Setup I2C
                i2c = busio.I2C(SCL, SDA)
                
                # Try to initialize each display independently
                self.display_left = self._init_display(i2c, 0x3C, "left")
                self.display_right = self._init_display(i2c, 0x3D, "right")
                
                try:
                    # Setup GPIO inputs using gpiozero (pull_up=True by default)
                    self.lever_right = Button(self.PIN_LEVER_RIGHT)
                    self.lever_left = Button(self.PIN_LEVER_LEFT)
                    self.nose_poke = Button(self.PIN_NOSE_POKE)
                    
                    # Setup water port output
                    self.water_port = DigitalOutputDevice(self.PIN_WATER, initial_value=False)
                    
                    self._simulated_inputs = False
                    print("GPIO inputs and outputs initialized successfully")
                    
                except Exception as e:
                    print(f"Failed to initialize GPIO: {e}")
                    print("Switching to simulation mode for GPIO")
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
            'nose_poke': False,
            'water_port': False
        }
    
    def _init_simulation(self):
        """Initialize full simulation mode with dummy hardware"""
        self.display_left = DummyDisplay(128, 64)
        self.display_right = DummyDisplay(128, 64)
        self._init_simulated_inputs()
        
    def get_input_states(self):
        if not hasattr(self, '_simulated_inputs') or not self._simulated_inputs:
            return {
                'right_lever': self.lever_right.is_pressed,
                'left_lever': self.lever_left.is_pressed,
                'nose_poke': self.nose_poke.is_pressed,
                'water_port': self.water_port.value
            }
        else:
            return self._simulated_states
    
    def clear_displays(self):
        self.display_left.fill(0)
        self.display_right.fill(0)
        self.display_left.show()
        self.display_right.show()
    
    def set_water_port(self, state):
        """Control water port state"""
        if not hasattr(self, '_simulated_inputs') or not self._simulated_inputs:
            self.water_port.value = state
        else:
            self._simulated_states['water_port'] = state
    
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