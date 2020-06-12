import RPi.GPIO as GPIO
import time
import smbus
import sys
from RPLCD.i2c import CharLCD

GPIO.setmode(GPIO.BCM)
sys.modules['smbus'] = smbus

class LCDController:
    def __init__(self):
        self.lcd = CharLCD('PCF8574', address=0x27, port=1, backlight_enabled=True)

    def writeLcd(self, firstStr, secondStr=""):
        self.lcd.clear()
        self.lcd.cursor_pos = (0, 0)
        self.lcd.write_string(firstStr)
        self.lcd.cursor_pos = (1, 0)
        self.lcd.write_string(secondStr)


if __name__ == "__main__":
    lcdController = LCDController()
    lcdController.writeLcd(firstStr="LCD Test", secondStr="Second Row Test")
    time.sleep(2)
    lcdController.writeLcd(firstStr="one line Test")pi
