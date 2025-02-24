from gpiozero import Button
import time

def test_gpio():
    try:
        # Test pin setup
        test_pin = 23
        button = Button(test_pin)
        print(f"Pin {test_pin} configured as input with pull-up")
        
        # Read value a few times
        for i in range(3):
            value = button.is_pressed
            print(f"Pin {test_pin} value: {value}")
            time.sleep(1)
            
        print("GPIO test successful!")
        return True
        
    except Exception as e:
        print(f"GPIO Test Failed: {str(e)}")
        return False

if __name__ == "__main__":
    test_gpio() 