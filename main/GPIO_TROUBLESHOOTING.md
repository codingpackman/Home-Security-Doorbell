# GPIO Troubleshooting Guide

## 🔧 Common GPIO Errors and Solutions

### Error: "Failed to add edge detection"

This error occurs when the GPIO pins cannot be initialized. Here are the solutions:

---

## ✅ Solution 1: Install lgpio (Recommended)

The `lgpio` library is the modern GPIO library for Raspberry Pi.

```bash
# Install lgpio
sudo apt-get update
sudo apt-get install -y python3-lgpio

# Or install via pip
pip3 install lgpio
```

After installation, try running your script again:
```bash
python3 main_system.py
```

---

## ✅ Solution 2: Force gpiozero to use RPi.GPIO

If lgpio doesn't work, you can force gpiozero to use the RPi.GPIO library:

```bash
# Set environment variable before running
export GPIOZERO_PIN_FACTORY=rpigpio
python3 main_system.py
```

Or add this to the top of your script (already in requirements.txt):
```python
import os
os.environ['GPIOZERO_PIN_FACTORY'] = 'rpigpio'
```

---

## ✅ Solution 3: Run with sudo (Permission Issue)

Sometimes GPIO access requires root permissions:

```bash
sudo python3 main_system.py
```

**Note:** If using a virtual environment, use:
```bash
sudo /path/to/your/venv/bin/python3 main_system.py
```

---

## ✅ Solution 4: Add User to GPIO Group

Add your user to the `gpio` group to access GPIO without sudo:

```bash
# Add user to gpio group
sudo usermod -a -G gpio $USER

# Log out and log back in for changes to take effect
# Or reboot
sudo reboot
```

After reboot, try running without sudo:
```bash
python3 main_system.py
```

---

## ✅ Solution 5: Software-Only Mode (Updated!)

The system has been updated to run in software-only mode if GPIO hardware fails. This is useful for:
- Testing on non-Raspberry Pi systems
- Development without GPIO access
- Systems where GPIO isn't needed

When running in software-only mode:
- The system will display warnings but continue running
- Use `test_doorbell.py` to trigger events manually
- Camera and database features still work

```bash
# System will run without GPIO
python3 main_system.py

# In another terminal, trigger events:
python3 test_doorbell.py button
```

---

## 🔍 Diagnostic Commands

### Check Python Version
```bash
python3 --version
# Should be 3.7 or higher
```

### Check Installed GPIO Libraries
```bash
pip3 list | grep -i gpio
# Look for: gpiozero, RPi.GPIO, lgpio
```

### Check GPIO Group Membership
```bash
groups $USER
# Should include 'gpio'
```

### Test GPIO Access
```bash
# Try to read GPIO chip info
cat /dev/gpiochip0
# If this fails with permission denied, you need to:
# - Add user to gpio group (Solution 4)
# - Or run with sudo (Solution 3)
```

### Check if Running on Raspberry Pi
```bash
cat /proc/device-tree/model
# Should show "Raspberry Pi" if on actual Pi hardware
```

---

## 📊 Understanding the Warnings

### "PinFactoryFallback: Falling back from lgpio"
- **Severity:** Warning (not critical)
- **Meaning:** lgpio not installed, using fallback library
- **Fix:** Install lgpio (Solution 1)

### "Failed to add edge detection"
- **Severity:** Critical (hardware won't work)
- **Meaning:** Cannot set up GPIO interrupt detection
- **Fix:** Try solutions 1-4 in order

### "name 'doorbell_button' is not defined"
- **Severity:** Critical (but now fixed!)
- **Meaning:** Hardware initialization failed, objects not created
- **Fix:** This is now handled gracefully in the updated code

---

## 🎯 Recommended Setup

For a production Raspberry Pi system:

```bash
# 1. Install lgpio
sudo apt-get install -y python3-lgpio

# 2. Add user to gpio group
sudo usermod -a -G gpio $USER

# 3. Reboot
sudo reboot

# 4. After reboot, test without sudo
python3 main_system.py
```

---

## 🧪 Testing GPIO

Create a simple test script to verify GPIO works:

```python
# test_gpio.py
from gpiozero import LED
import time

# Test with an LED on GPIO18 (or any free pin)
led = LED(18)

print("Blinking LED...")
for i in range(5):
    led.on()
    time.sleep(0.5)
    led.off()
    time.sleep(0.5)

print("GPIO test successful!")
```

Run it:
```bash
python3 test_gpio.py
```

If this works, your GPIO is properly configured!

---

## 🚨 Still Not Working?

### Option A: Use Software-Only Mode
The updated `main_system.py` now handles GPIO failures gracefully. You can:
1. Run the system anyway (it will work without GPIO)
2. Use `test_doorbell.py` to trigger events manually
3. Camera recording and database features work fine

### Option B: Check Hardware Connections
- Verify wiring is correct
- Check for loose connections
- Ensure no short circuits
- Verify pin numbers match your configuration

### Option C: Fresh Install
If all else fails, try a fresh OS install:
```bash
# Backup your code first!
sudo apt-get update
sudo apt-get dist-upgrade
sudo apt-get install -y python3-lgpio python3-rpi.gpio
sudo reboot
```

---

## 📝 Quick Command Reference

```bash
# Install lgpio
sudo apt-get install -y python3-lgpio

# Install RPi.GPIO
pip3 install RPi.GPIO

# Add to gpio group
sudo usermod -a -G gpio $USER

# Run with specific pin factory
GPIOZERO_PIN_FACTORY=rpigpio python3 main_system.py

# Run with sudo
sudo python3 main_system.py

# Test manually (no GPIO needed)
python3 test_doorbell.py button
```

---

## ✅ Success Indicators

You'll know GPIO is working when you see:
```
✓ Buttons initialized (Doorbell: GPIO14, Stop: GPIO15)
✓ Buzzer initialized (GPIO18)
✓ Motion sensors initialized.
✓ Doorbell button callback assigned
✓ Stop button callback assigned
✓ PIR motion sensor callbacks assigned
```

No ✗ marks or error messages!

---

## 💡 Pro Tips

1. **Always test with a simple LED first** before complex sensors
2. **Check your wiring** - wrong pins are the #1 cause of issues
3. **Use software-only mode** for development and testing
4. **Add logging** to see what's happening
5. **Test one component at a time** - don't try to initialize everything at once

---

## 🆘 Need More Help?

If you're still stuck:
1. Check the output of diagnostic commands above
2. Verify you're on actual Raspberry Pi hardware
3. Make sure Python version is 3.7+
4. Try running `test_doorbell.py` to bypass GPIO entirely
5. Post the full error message for more specific help

---

**Remember:** The system now works in software-only mode, so you can still test camera recording and database features even if GPIO isn't working!

