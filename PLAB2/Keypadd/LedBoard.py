
import RPi.GPIO as GPIO
import time


class LedBoard:
    """interface to the physical, Charlieplexed LED board"""

    def __init__(self):
        self.pins = [12, 16, 20]
        self.pin_led_states = [
            [1, 0, -1],  # A
            [0, 1, -1],  # B
            [-1, 1, 0],  # C
            [-1, 0, 1],  # D
            [1, -1, 0],  # E
            [0, -1, 1],  # F
            [-1, -1, -1]
        ]
        GPIO.setmode(GPIO.BCM)

    def set_pin(self, pin_index, pin_state):
        if pin_state == -1:
            GPIO.setup(self.pins[pin_index], GPIO.IN)
        else:
            GPIO.setup(self.pins[pin_index], GPIO.OUT)
            GPIO.output(self.pins[pin_index], pin_state)

    def turn_on_led(self, led_number):  # Skru på lys
        for pin_index, pin_state in enumerate(self.pin_led_states[led_number - 1]):
            self.set_pin(pin_index, pin_state)

    def light_led(self, led_number, Ldur):
        """Turn on one of the 6 LEDs by making the appropriate combination of input and
        output declarations, and then making the appropriate HIGH / LOW settings on the output
        pins."""
        for pin_index, pin_state in enumerate(self.pin_led_states[led_number]):
            self.set_pin(pin_index, pin_state)
        self.turn_on_led(led_number)
        time.sleep(Ldur)
        self.turn_off_leds()

    def light_all(self, Ldur):  # Skru på alle lys
        timeout = time.time() + Ldur
        while time.time() <= timeout:
            for i in range(1, 7):
                self.turn_on_led(i)
        self.turn_off_leds()

    def flash_all_leds(self, k):
        """ Flash all 6 LEDs on and off for k seconds, where k is an argument of the
        method."""
        print("flashing leds")
        for i in range(0, 6):
            self.light_all(k)
            time.sleep(k)

        self.turn_off_leds()

    def turn_off_leds(self):
        """Turn off all leds"""
        for i in range(0, 3):
            self.set_pin(i, 0)

    def twinkle_all_leds(self, k):
        """Turn all LEDs on and off in sequence for k seconds, where k is an argument
        of the method."""
        print("twinkle leds")
        timeend = time.time() + k

        while time.time() < timeend:
            for i in range(0, 6):
                self.light_led(i, 0.2)
                time.sleep(0.1)
                self.turn_off_leds()

    def power_up(self):
        """A display of lights (Led0, Led2, Led4) that indicates ”powering up”.
        This should be performed when the user does the very first keystroke of a session."""
        print("powering up")
        self.light_led(0, 0.2)
        self.light_led(2, 0.2)
        self.light_led(4, 0.2)
        time.sleep(3)
        self.turn_off_leds()

    def power_down(self):
        """A display of lights (Led1, Led3, Led5) that indicates powering down"""
        print("powering down")
        self.light_led(1, 0.2)
        self.light_led(3, 0.2)
        self.light_led(5, 0.2)
        time.sleep(3)
        self.turn_off_leds()








