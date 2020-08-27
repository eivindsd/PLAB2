

class KPC:
    """class to represent the agent"""

    def __init__(self, keypad, ledboard, pathname):
        self.keypad = keypad  # pointer to the keypad object
        self.ledboard = ledboard  # pointer to the ledboard
        self.passcode_buffer = ""
        self.pathname = pathname  # the complete pathname to the file holding the KPC's password
        self.overridesignal = None
        self.Lid = ""
        self.Ldur = ""
        self.signal = ""

    def exit_action(self):
        """Call the LED Board to initiate the ”power down” lighting sequence."""
        self.ledboard.power_down()

    def no_action(self):
        """this is a method for when we just want to change state in the fsm, and no action will be executed"""
        pass

    def init_passcode_entry(self):
        """Clear the passcode-buffer and initiate a ”power up” lighting sequence
        on the LED Board. This should be done when the user first presses the keypad."""
        self.passcode_buffer = ""
        self.ledboard.power_up()
        print("powering up")

    def get_next_signal(self):
        """Return the override-signal, if it is non-blank; otherwise query the keypad
        for the next pressed key."""
        if self.overridesignal is not None:
            temp = self.overridesignal
            self.overridesignal = None
            return temp
        # query the keypad for the next pressed key and adding the symbol to
        # the passcode buffer
        self.signal = self.keypad.get_next_signal()
        print("Input: " + self.signal)
        return self.signal

    def verify_login(self):
        """ Check that the password just entered via the keypad matches that in the password file.
        Store the result (Y or N) in the override-signal. Also, this should call the LED
        Board to initiate the appropriate lighting pattern for login success or failure"""
        f = open(self.pathname, "r")
        password = f.read()
        f.close()
        print("Temp password = " + self.passcode_buffer)
        if password == self.passcode_buffer:
            self.overridesignal = "Y"
            return True
        else:
            self.overridesignal = "N"
            return False

    def validate_passcode_change(self, password):
        """Check that the new password is legal. If so, write the new password in the password file.
        A legal password should be at least 4 digits long and should
        contain no symbols other than the digits 0-9. As in verify login, this should use the LED
        Board to signal success or failure in changing the password."""
        if len(password) > 3 and password.isdigit():
            return True
        return False

    def startup(self):  # Få lys til å blinke og reset password
        """startup"""
        self.clear_password()
        self.ledboard.startup_leds()

    def clear_password(self):
        """fjerner gammelt passord"""
        self.passcode_buffer = ""

    def login(self):  # Twinkle lights og verify login
        """logger inn"""
        self.verify_login()
        self.ledboard.rightPassword_leds()

    def write_password(self):
        if self.validate_passcode_change(self.passcode_buffer):
            try:
                f = open(self.pathname, "w")
                f.write(self.passcode_buffer)
                f.close()
                self.twinkle_leds(3)
            except IOError:
                print("Something went wrong when writing new password to file")
                self.flash_leds(3)

    #LYS

    def set_ledid(self):
        """Takes the signal pressed on keypad, and sets it as the instance variable Lid"""
        self.Lid = self.signal

    def set_ldur(self):
        """Takes the signal pressed on keypad, and sets this as the instance variable Ldur"""
        self.Ldur += self.signal

    def reset_led(self):
        """reset led"""
        self.Ldur = ""

    def light_one_led(self):
        """Using values stored in the Lid and Ldur slots, call the LED Board and request
        that LED # Lid be turned on for Ldur seconds."""
        self.ledboard.light_led(int(self.Lid), int(self.Ldur))

    def flash_leds(self, k):
        """Call the LED Board and request the flashing of all LEDs, for k seconds"""
        self.ledboard.flash_all_leds(k)

    def twinkle_leds(self, k):
        """Call the LED Board and request the twinkling of all LEDs."""
        self.ledboard.twinkle_all_leds(k)

    def add_symbol(self):
        """Adds the symbol pressed on the keypad to the passcode_buffer, if the symbol is a digit"""
        if self.signal.isdigit():
            self.passcode_buffer += self.signal

    def reset_password(self):
        """Resets the password"""
        self.passcode_buffer = ""




