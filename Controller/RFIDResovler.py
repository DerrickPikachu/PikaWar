import RPi.GPIO as GPIO
import mfrc522
import time


class RFIDResovler:
    def __init__(self):
        self.reader = mfrc522.SimpleMFRC522()

    def readRFID(self):
        try:
            id, text = self.reader.read()
            return id
        finally:
            GPIO.cleanup()


if __name__ == "__main__":
    RFID = RFIDResovler()
    while True:
        id = RFID.readRFID()
        print("id = " + str(id))
        time.sleep(2)