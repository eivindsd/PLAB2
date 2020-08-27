from KPC import KPC
from Keypad import Keypad
from LedBoard import LedBoard


class FSM:
    """class to represent the Finite state machine"""

    def __init__(self, kpc):
        self.state = None
        self.rulelist = []
        self.kpc = kpc

    def add_rule(self, state1, state2, signal, action):
        """method to add rule"""
        self.rulelist.append(Rule(state1, state2, signal, action))

    def get_next_signal(self):
        """query the agent for the next signal"""
        return self.kpc.get_next_signal()

    def run_rule(self, input):
        """go through the rule set, in order, applying each rule until one of the rules is fired"""
        for rule in self.rulelist:
            if self.apply_rule(rule, input):
                print("apply rule")
                break #found the rule that was fired, stop iteration

    def apply_rule(self, rule, input):
        """check whether the conditions of a rule are met"""
        if self.state == rule.state1 and (input in rule.triggersignal):  #hmm
            print(rule.state1)
            print(rule.triggersignal)
            print(rule.state2)
            self.fire_rule(rule)
            return True
        return False

    def fire_rule(self, rule):
        """use the consequent of a rule to a) set the next state of the FSM, and b) call the
        appropriate agent action method."""
        self.state = rule.state2
        rule.action()

    def main_loop(self):
        """begin in the FSM’s default initial state and then repeatedly call get next signal
        and run rules until the FSM enters its default final state."""
        pass


def signal_is_digit(signal):
    """check if a signal is digit"""
    return 48 <= ord(signal) <= 57


class Rule:
    """class to represent a Finite state machine rule"""

    def __init__(self, state1, state2, trigger, action):
        self.state1 = state1
        self.state2 = state2
        self.triggersignal = trigger
        self.action = action


class FSMRules(FSM):

    def __init__(self, kpc):
        FSM.__init__(self, kpc)
        legal_inputs = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '*', '#']
        legal_numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

        led_numbers = ['0', '1', '2', '3', '4', '5']
        not_led_numbers = ['6', '7', '8', '9']


        #Regler login

        self.add_rule("S-INIT", "S-READ", legal_inputs, self.kpc.init_passcode_entry)
        #starte opp og blinke lys
        self.add_rule("S-READ", "S-READ", legal_numbers, self.kpc.add_symbol)
        #legger til et tall i temp-passord
        self.add_rule("S-READ", "S-VERIFY", ["*"], self.kpc.verify_login)
        #logger inn når hele passordet er skrevet
        self.add_rule("S-READ", "S-INIT", ["#"], self.kpc.no_action)
        #reseter systemet når man skriver #
        self.add_rule("S-VERIFY", "S-INIT", ["N"], self.kpc.no_action)
        #ved feil passord
        self.add_rule("S-VERIFY", "S-ACTIVE", ["Y"], self.kpc.no_action)
        #ved riktig passord

        #Regler endre passord

        self.add_rule("S-ACTIVE", "S-READ-2", ["*"], self.kpc.reset_password)
        #reset gammelt passord
        self.add_rule("S-READ-2", "S-ACTIVE", ["#"], self.kpc.no_action)
        #gå tilbake til active-state ved press #
        self.add_rule("S-READ-2", "S-READ-2", legal_numbers, self.kpc.add_symbol)
        #legger til symbol til nytt passord
        self.add_rule("S-READ-2", "S-ACTIVE", ["*"], self.kpc.write_password)
        #endrer til nytt passord

        #Regler logoff
        self.add_rule("S-ACTIVE", "S-INIT", ["#"], self.kpc.exit_action)
        #logger av og går tilbake til init-state

        #Regler lys

        self.add_rule("S-ACTIVE", "S-LED", led_numbers, self.kpc.set_ledid)
        #velge en led (0-5)
        self.add_rule("S-ACTIVE", "S-ACTIVE", not_led_numbers, self.kpc.no_action)
        #trykker på et tall som ikke er koblet til noen led
        self.add_rule("S-LED", "S-LED", legal_numbers, self.kpc.set_ldur)
        #sette tiden den valgte led skal lyse
        self.add_rule("S-LED", "S-TIME", ["*"], self.kpc.light_one_led)
        #sette sekunder led skal lyse, og utføre lys
        self.add_rule("S-TIME", "S-ACTIVE", ["*"], self.kpc.exit_action)
        #gå tilbake til active-state, og tilbakestille leds

    def main_loop(self):
        """kjører"""
        self.state = "S-INIT"
        while True:
            print("Button pushed")
            print("State: " + self.state)
            input = str(self.kpc.get_next_signal())
            self.run_rule(input)

            if self.state == "S-ACTIVE" and input == "#":
                print("Finito")
                break


if __name__ == "__main__":
    print("run")
    keypad = Keypad()
    ledboard = LedBoard()

    kpc = KPC(keypad, ledboard, "password.txt")
    fsm = FSMRules(kpc)
    fsm.main_loop()




