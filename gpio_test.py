import RPi.GPIO as GPIO
import time

def test_gpio():
    try:
        # Print GPIO version
        print(f"RPi.GPIO Version: {GPIO.VERSION}")
        
        # Set mode
        GPIO.setmode(GPIO.BCM)
        print("Mode set to BCM")
        
        # Test pin setup
        test_pin = 23
        GPIO.setup(test_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        print(f"Pin {test_pin} setup complete")
        
        # Read value
        value = GPIO.input(test_pin)
        print(f"Pin {test_pin} value: {value}")
        
        return True
        
    except Exception as e:
        print(f"GPIO Test Failed: {str(e)}")
        return False
    finally:
        GPIO.cleanup()

if __name__ == "__main__":
    test_gpio() 