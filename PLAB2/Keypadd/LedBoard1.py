import RPi.GPIO as GPIO
import time

class Ledboard:
    """leadboard-klasse"""
    def __init__(self):  # Set the proper mode via: GPIO.setmode(GPIO.BCM).
        # Set the proper mode via: GPIO.setmode(GPIO.BCM).
        self.pins = [13, 19, 26]
        self.pin_led_states = [
            [1, 0, -1],  # 1
            [0, 1, -1],  # 2
            [1, -1, 0],  # 3
            [0, -1, 1],  # 4
            [-1, 1, 0],  # 5
            [-1, 0, 1],  # 6
            [-1, -1, -1]
        ]
        GPIO.setmode(GPIO.BCM)

    def set_pin(self, pin_index, pin_state):
        """setter pins"""

        if pin_state == -1:
            GPIO.setup(self.pins[pin_index], GPIO.IN)
        else:
            GPIO.setup(self.pins[pin_index], GPIO.OUT)
            GPIO.output(self.pins[pin_index], pin_state)

    def turn_on_led(self, Lid):  # Skru på lys
        for pin_index, pin_state in enumerate(self.pin_led_states[Lid - 1]):
            self.set_pin(pin_index, pin_state)

    def shut_off_lights(self):  # Skru av lys
        for i in range(0, 3):
            self.set_pin(i, 0)

    # Turn on one of the 6 LEDs by making the appropriate combination of input and output
    # declarations, and then making the appropriate HIGH / LOW settings on the
    # output pins.
    def light_led(self, Lid, Ldur):  # Lys opp ett lys
        for pin_index, pin_state in enumerate(self.pin_led_states[Lid]):
            self.set_pin(pin_index, pin_state)
        self.turn_on_led(Lid)
        print("Lights led", Lid, "for", Ldur, "sekunder")
        time.sleep(Ldur)
        self.shut_off_lights()

    def light_all(self, Led_duration):  # Skru på alle lys
        timeout = time.time() + Led_duration
        while time.time() <= timeout:
            for i in range(1, 7):
                self.turn_on_led(i)
        self.shut_off_lights()

    def flash_all_leds(self, flashes=5, dif=0.25):  # Flash alle lys
        print("All leds flashing")
        for i in range(0, flashes):
            self.light_all(dif)
            time.sleep(dif)

    def twinkle_all_leds(self, Led_duration):  # Twinkle lys
        timeout = time.time() + Led_duration
        print("All leds twinkle")
        while time.time() <= timeout:
            for i in range(1, 7):
                self.light_led(i, 0.2)
        self.shut_off_lights()

    def startup_leds(self):  # Start opp
        for i in range(1, 7):
            self.light_led(i, 0.2)
        self.flash_all_leds(3, 0.1)
        print("Power up animation")

    def rightPassword_leds(self):  # !Right pass
        for i in range(1, 7):
            self.light_led(i, 0.1)
        print("Tried password animation")

    def exit_leds(self):  # Slå av
        self.flash_all_leds(3, 0.1)
        for i in range(1, 7):
            self.light_led(i, 0.2)
        print("Power down animation")