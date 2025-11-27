from gpiozero import Button
from gpiozero import TonalBuzzer
from gpiozero.tones import Tone
from signal import pause
import time

# Initialize the button on BCM 6
# GPIO Zero automatically sets the internal Pull-Up resistor
button = Button(6, pull_up=True, bounce_time=0.05)
buzzer = TonalBuzzer(18)
hardware_available = {
    'buttons': False,
    'buzzer': False,
    'motion_sensors': False
}

def ring_buzzer():
    """Rings the buzzer for a specified duration."""
    if buzzer is not None:
        print("BUZZER: Ringing!")
        buzzer.play(Tone(880))
        time.sleep(0.1)
        buzzer.stop()
    else:
        print("BUZZER: Would ring (buzzer not available)")

try:
    #buzzer = Buzzer(18)
    hardware_available['buzzer'] = True
    #print(f"✓ Buzzer initialized (GPIO{PIN_BUZZER})")
except Exception as e:
    print(f"✗ Error initializing buzzer: {e}")
    print("  Running in software-only mode (buzzer disabled)")
    

def on_button_pressed():
    print("Button on BCM 6 was pressed!")
    ring_buzzer()

def on_button_released():
    print("Button released.")

print("Program is running. Press the button...")

# Assign functions to the events
button.when_pressed = on_button_pressed
button.when_released = on_button_released

# Keep the program running to listen for events
pause() 