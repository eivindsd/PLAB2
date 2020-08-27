"""Keypadd"""

from inspect import isfunction
import RPi.GPIO as GPIO


class FSM:
    """class to represent the Finite state machine"""

    def __init__(self, kpc):
        self.state = "S-INIT"
        self.signal = ""
        self.rulelist = []
        self.CP = ""   #current password
        self.CUMP = "" #cumulative password
        self.kpc = kpc

    def add_rule(self, state1, state2, signal, action):
        """method to add rule"""
        self.rulelist.append(Rule(state1, state2, signal, action))

    def get_next_signal(self):
        """query the agent for the next signal"""
        return self.kpc.get_next_signal() #kpc must be a KPC-object

    def run_rule(self):
        """go through the rule set, in order, applying each rule until one of the rules is fired"""
        for rule in self.rulelist:
            if self.apply_rule(rule):
                break

    def apply_rule(self, rule):
        """check whether the conditions of a rule are met"""
        pass

    def fire_rule(self):
        """use the consequent of a rule to a) set the next state of the FSM, and b) call the
        appropriate agent action method."""
        pass

    def main_loop(self):
        """begin in the FSM’s default initial state and then repeatedly call get next signal
        and run rules until the FSM enters its default final state."""
        pass


def signal_is_digit(signal):
    """check if a signal is digit"""
    return 48 <= ord(signal) <= 57


class Rule:
    """class to represent a Finite state machine rule"""

    def __init__(self, state1, state2, signal, action):
        self.state1 = state1
        self.state2 = state2
        self.triggersignal = signal
        self.action = action


class KPC:
    """class to represent the agent"""

    def __init__(self):
        self.overridesignal = ""
        self.keypad = "" #keypad object
        self.ledboard = "" #ledboard object

    def init_passcode_entry(self):
        """Clear the passcode-buffer and initiate a ”power up” lighting sequence
        on the LED Board. This should be done when the user first presses the keypad."""
        pass

    def get_next_signal(self):
        """Return the override-signal, if it is non-blank; otherwise query the keypad
        for the next pressed key."""
        if len(self.overridesignal) != 0:
            return self.overridesignal
        #query the keypad for the next pressed key

    def verify_login(self):
        """ Check that the password just entered via the keypad matches that in the password file.
        Store the result (Y or N) in the override-signal. Also, this should call the LED
        Board to initiate the appropriate lighting pattern for login success or failure"""
        pass

    def validate_passcode_change(self):
        """Check that the new password is legal. If so, write the new password in the password file.
        A legal password should be at least 4 digits long and should
        contain no symbols other than the digits 0-9. As in verify login, this should use the LED
        Board to signal success or failure in changing the password."""
        pass

    def light_one_led(self):
        """Using values stored in the Lid and Ldur slots, call the LED Board and request
        that LED # Lid be turned on for Ldur seconds."""
        pass

    def flash_leds(self):
        """Call the LED Board and request the flashing of all LEDs"""
        pass

    def twinkle_leds(self):
        """Call the LED Board and request the twinkling of all LEDs."""
        pass

    def exit_action(self):
        """Call the LED Board to initiate the ”power down” lighting sequence."""
        pass


class LedBoard:
    """interface to the physical, Charlieplexed LED board"""

    pins = [13, 19, 26]

    pin_led_states = [
        [1, 0, - 1],
        [0, 1, - 1],
        [-1, 1, 0],
        [-1, 0, 1],
        [1, -1, 0],
        [0, -1, 1],
        [-1, -1, -1]
    ]

    def setup(self):
        # Set the proper mode via: GPIO.setmode(GPIO.BCM).
        GPIO.setmode(GPIO.BCM)  # Use physical pin numbering

    @staticmethod
    def set_pin(pin_index, pin_state):
        if pin_state == -1:
            GPIO.setup(LedBoard.pins[pin_index], GPIO.IN)
        else:
            GPIO.setup(LedBoard.pins[pin_index], GPIO.OUT)
            GPIO.output(LedBoard.pins[pin_index], pin_state)

    def light_led(self, led_number):
        for pin_index, pin_state in enumerate(LedBoard.pin_led_states[led_number]):
            LedBoard.set_pin(pin_index, pin_state)




