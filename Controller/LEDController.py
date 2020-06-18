import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)


class LEDController:
    def __init__(self):
        self.ledMap = [[16, 20, 21], [13, 19, 26]]

        for row in self.ledMap:
            for col in row:
                GPIO.setup(col, GPIO.OUT)

    def hintLed(self, row, col):
        GPIO.output(self.ledMap[row][col], 1)
        time.sleep(3)
        GPIO.output(self.ledMap[row][col], 0)

    def hintAllLed(self):
        for num in self.ledMap:
            GPIO.output(num, 1)
        time.sleep(3)
        for num in self.ledMap:
            GPIO.output(num, 0)


if __name__ == "__main__":
    ledController = LEDController()
    ledController.hintAllLed()
    #
    # for row in range(2):
    #     for col in range(3):
    #         ledController.hintLed(row, col)
