try:
    from board import SCL, SDA, D23, D24, D17
    import busio
    import digitalio
    import adafruit_ssd1306
    SIMULATION_MODE = False
except (ImportError, NotImplementedError):
    print("Hardware interfaces not available - running in simulation mode")
    SIMULATION_MODE = True

class IOController:
    def __init__(self):
        if not SIMULATION_MODE:
            # Setup I2C
            i2c = busio.I2C(SCL, SDA)
            
            # Setup displays
            self.display_left = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c, addr=0x3C)
            self.display_right = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c, addr=0x3D)
            
            # Setup GPIO inputs with pull-ups
            self.lever_right = digitalio.DigitalInOut(D23)
            self.lever_right.direction = digitalio.Direction.INPUT
            self.lever_right.pull = digitalio.Pull.UP
            
            self.lever_left = digitalio.DigitalInOut(D24)
            self.lever_left.direction = digitalio.Direction.INPUT
            self.lever_left.pull = digitalio.Pull.UP
            
            self.nose_poke = digitalio.DigitalInOut(D17)
            self.nose_poke.direction = digitalio.Direction.INPUT
            self.nose_poke.pull = digitalio.Pull.UP
        else:
            # Simulation mode - create dummy display objects
            self.display_left = DummyDisplay(128, 64)
            self.display_right = DummyDisplay(128, 64)
            # Initialize simulated input states
            self._simulated_states = {
                'right_lever': False,
                'left_lever': False,
                'nose_poke': False
            }
        
    def get_input_states(self):
        if not SIMULATION_MODE:
            return {
                'right_lever': not self.lever_right.value,
                'left_lever': not self.lever_left.value,
                'nose_poke': not self.nose_poke.value
            }
        else:
            return self._simulated_states
    
    def clear_displays(self):
        self.display_left.fill(0)
        self.display_right.fill(0)
        self.display_left.show()
        self.display_right.show()

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