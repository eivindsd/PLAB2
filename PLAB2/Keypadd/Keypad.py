import RPi.GPIO as GPIO
import time


class Keypad:

    def __init__(self):
        self.symbols = {"nokey": "No key", "1817": "1", "1827": "2", "1822": "3", "2317": "4", "2327": "5", "2322": "6",
                        "2417": "7", "2427": "8", "2422": "9", "2517": '*', "2527": "0", "2522": '#'}
        GPIO.setmode(GPIO.BCM)
        self.cp=[17,27,22]
        self.rp=[18,23,24,25]
        for pins in self.cp:
            GPIO.setup(pins, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        for pins in self.rp:
            GPIO.setup(pins, GPIO.OUT)

    def polling(self):
        keystring = "nokey"
        for rpin in self.rp:
            GPIO.output(rpin, GPIO.HIGH)
            for cpin in self.cp:
                if GPIO.input(cpin) == GPIO.HIGH:
                    keystring = str(rpin) + str(cpin)

            GPIO.output(rpin, GPIO.LOW)

        return self.symbols[keystring]

    def get_next_signal(self):
        x = 0
        key = None
        last_key = "y"

        while x < 1:
            key = self.polling()
            if key != "No key":  # har funnet en nøkkel

                if last_key == "y":
                    last_key = key
                    x += 1
                elif key == last_key:  # Sjekker om det er samme signal som gis
                    x += 1
                else:   # hvis nøkkelen ikke er den samme som sist
                    last_key = "y"
                    x = 0
        time.sleep(4)
        print("key: " + key)
        return key


if __name__ == '__main__':
    print("test")
    keypad = Keypad()
    while True:
        sign = keypad.get_next_signal()
        print("Signal = ", sign)
