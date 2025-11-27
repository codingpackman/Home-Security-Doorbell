#!/usr/bin/env python3
"""
Simple button test script to diagnose GPIO button issues
"""

import time
import sys

print("="*60)
print("Button Test Script")
print("="*60)

# Try to import gpiozero
try:
    from gpiozero import Button
    print("✓ gpiozero imported successfully")
except ImportError as e:
    print(f"✗ Failed to import gpiozero: {e}")
    sys.exit(1)

# Button configuration
PIN = 6  # GPIO 6
print(f"\nTesting button on GPIO{PIN}")
print("="*60)

# Test 1: Try to initialize button
print("\nTest 1: Initializing button...")
try:
    button = Button(PIN, pull_up=True, bounce_time=0.1)
    print(f"✓ Button initialized successfully")
    print(f"  Current state: {'PRESSED' if button.is_pressed else 'NOT PRESSED'}")
except Exception as e:
    print(f"✗ Failed to initialize button: {e}")
    print(f"  Error type: {type(e).__name__}")
    import traceback
    traceback.print_exc()
    print("\n" + "="*60)
    print("TROUBLESHOOTING:")
    print("1. Install lgpio: sudo apt-get install -y python3-lgpio")
    print("2. Add user to gpio group: sudo usermod -a -G gpio $USER")
    print("3. Reboot: sudo reboot")
    print("4. Or run with sudo: sudo python3 test_button.py")
    print("="*60)
    sys.exit(1)

# Test 2: Check if button is currently pressed
print("\nTest 2: Checking button state...")
print(f"  Button is: {'PRESSED' if button.is_pressed else 'NOT PRESSED'}")
print("  (If button is pressed but shows NOT PRESSED, wiring might be reversed)")

# Test 3: Set up callback
print("\nTest 3: Setting up callback...")
button_press_count = 0

def button_pressed():
    global button_press_count
    button_press_count += 1
    print(f"\n🔔 BUTTON PRESSED! (Count: {button_press_count})")
    print(f"   Time: {time.strftime('%H:%M:%S')}")

def button_released():
    print(f"   Button released")

try:
    button.when_pressed = button_pressed
    button.when_released = button_released
    print("✓ Callback assigned successfully")
except Exception as e:
    print(f"✗ Failed to assign callback: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test 4: Wait for button presses
print("\n" + "="*60)
print("Test 4: Waiting for button presses...")
print("="*60)
print("\nPress the button to test!")
print("(Press Ctrl+C to exit)\n")

try:
    while True:
        time.sleep(0.1)
except KeyboardInterrupt:
    print("\n\n" + "="*60)
    print("Test Complete!")
    print("="*60)
    print(f"Total button presses detected: {button_press_count}")
    print("\nIf button didn't work:")
    print("1. Check wiring: Button should connect GPIO6 to GND")
    print("2. Try reversing the wiring (connect to 3.3V instead)")
    print("3. Check for loose connections")
    print("4. Verify button works with multimeter")
    print("="*60)

