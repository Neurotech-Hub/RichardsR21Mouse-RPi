import lgpio
import time

def test_gpio():
    try:
        # Open GPIO chip
        h = lgpio.gpiochip_open(0)
        print("GPIO chip opened successfully")
        
        # Configure test pin
        test_pin = 23
        lgpio.gpio_claim_input(h, test_pin)
        print(f"Pin {test_pin} configured as input")
        
        # Read value
        value = lgpio.gpio_read(h, test_pin)
        print(f"Pin {test_pin} value: {value}")
        
        return True
        
    except Exception as e:
        print(f"GPIO Test Failed: {str(e)}")
        return False
    finally:
        try:
            lgpio.gpiochip_close(h)
        except:
            pass

if __name__ == "__main__":
    test_gpio() 