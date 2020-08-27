# pylint: disable=C0103

from random import randint
import crypto_utils


class Cypher:
    """Superklasse med krypterings-algoritmer som subklasser"""

    alphabet = [chr(i) for i in range(32, 127)]

    def __init__(self):
        return

    """dummy-metoder"""

    def encode(self, key, message):
        """metode for å enkode en melding"""
        return

    def decode(self, key, message):
        """metode for å dekode en melding"""
        return

    def verify(self, key, message):
        """metode som verifiserer at teksten er uendret"""
        crypto = self.encode(key, message)
        return self.decode(key, crypto) == message

    def generate_keys(self):
        """metode som genererer krypteringsnøkler"""
        return


class Caesar(Cypher):
    """subklasse for å representere Caesar-chipheret"""

    def __init__(self):
        Cypher.__init__(self)

    def encode(self, key, message):
        """metode for å enkode melding"""
        encoded_message = ""
        for char in message:
            oldpos = self.alphabet.index(char)
            newpos = (oldpos + key) % 95
            encoded_message += self.alphabet[newpos]
        return encoded_message

    def decode(self, key, message):
        """metode for å dekode melding"""
        decrypted_message = ""
        for char in message:
            oldpos = self.alphabet.index(char)
            newpos = (oldpos - key) % 95
            decrypted_message += self.alphabet[newpos]

        return decrypted_message

    def generate_keys(self):
        """metode for å generere krypteringsnøkkel"""
        return randint(0, 95)


class Multiplicative(Cypher):
    """klasse for multiplikativ-cipher"""

    def __init__(self):
        Cypher.__init__(self)

    def generate_keys(self):
        """metode som genererer krypteringsnøkler"""
        senderkey = randint(0, 95)
        recieverkey = crypto_utils.modular_inverse(senderkey, 95)
        while not recieverkey:
            senderkey = randint(0, 95)
            recieverkey = crypto_utils.modular_inverse(senderkey, 95)
        return [senderkey, recieverkey]

    def encode(self, key, message):
        """metode for å enkode melding"""
        encodedmessage = ""
        new_key = key[0]
        for chr in message:
            oldpos = self.alphabet.index(chr)
            newpos = (oldpos * new_key) % 95
            encodedmessage += self.alphabet[newpos]
        return encodedmessage

    def decode(self, key, message):
        """metode for å dekode en melding"""
        decodedmessage = ""
        new_key = key[1]
        for chr in message:
            oldpos = self.alphabet.index(chr)
            newpos = (oldpos * new_key) % 95
            decodedmessage += self.alphabet[newpos]
        return decodedmessage


class Affine(Cypher):
    """klasse for affine-cipher"""

    def __init__(self):
        Cypher.__init__(self)

    def encode(self, key, message):
        """metode for å enkode melding"""
        key1 = key[-2:]
        key2 = key[0]
        first = Multiplicative().encode(key1, message)
        encoded = Caesar().encode(key2, first)
        return encoded

    def decode(self, key, message):
        """metode for å dekode en melding"""
        key1 = key[-2:]
        key2 = key[0]
        first = Caesar().decode(key2, message)
        decoded = Multiplicative().decode(key1, first)
        return decoded

    def generate_keys(self):
        """metode for å generere krypteringsnøkler for klassen Affine"""
        addkey = randint(0, 95)
        sendermultkey = randint(0, 95)
        recievermultkey = crypto_utils.modular_inverse(sendermultkey, 95)
        while not recievermultkey:
            sendermultkey = randint(0, 95)
            recievermultkey = crypto_utils.modular_inverse(sendermultkey, 95)
        keys = [addkey, sendermultkey, recievermultkey]
        return keys


class Unbreakable(Cypher):
    """klasse for 'ubrytbar' cipher"""

    def __init__(self):
        Cypher.__init__(self)

    def encode(self, key, message):
        """metode for å enkode melding"""
        encodedmessage = ""
        index = 0
        for char in message:
            verdi1 = self.alphabet.index(char)
            key_letter = key[index % len(key)]
            verdi2 = self.alphabet.index(key_letter)
            verdi3 = (verdi1 + verdi2) % 95
            encodedmessage += self.alphabet[verdi3]
            index += 1
        return encodedmessage

    def decode(self, key, message):
        """metode for å dekode en melding"""
        decodekey = ""
        for char in key:
            letter_index = self.alphabet.index(char)
            new_value = 95 - (letter_index % 95)
            decodekey += self.alphabet[new_value]
        return self.encode(decodekey, message)

    def generate_keys(self):
        """metode som genererer krypteringsnøkler"""
        key = input("Nøkkel: ")
        return key


class RSA(Cypher):
    """klasse for å representere RSA - cipher"""

    def __init__(self):
        Cypher.__init__(self)

    def encode(self, key, message):
        """metode for å enkode melding"""
        crypto = crypto_utils.blocks_from_text(message, 2)
        crypted = []
        for number in crypto:
            encoded_number = pow(number, key[1], key[0])
            crypted.append(encoded_number)
        return crypted

    def decode(self, key, message):
        """metode for å dekode en melding"""
        decoded = []
        for number in message:
            decoded_number = pow(number, key[1], key[0])
            decoded.append(decoded_number)
        return crypto_utils.text_from_blocks(decoded, 2)

    def generate_keys(self):
        """metode som genererer krypteringsnøkler"""
        p = crypto_utils.generate_random_prime(8)
        q = -1
        while q == -1 or q == p:
            q = crypto_utils.generate_random_prime(8)
        n = p * q
        phi = (p - 1) * (q - 1)
        e = randint(3, phi - 1)
        d = crypto_utils.modular_inverse(e, phi)
        while not d:
            p = crypto_utils.generate_random_prime(8)
            q = -1
            while q == -1 or q == p:
                q = crypto_utils.generate_random_prime(8)
            n = p * q
            phi = (p - 1) * (q - 1)
            e = randint(3, phi - 1)
            d = crypto_utils.modular_inverse(e, phi)
        encode_key = [n, e]
        decode_key = [n, d]
        return [encode_key, decode_key]

    def verify(self, key, message):
        """metode som verifiserer at teksten er uendret"""
        crypto = self.encode(key[0], message)
        return self.decode(key[1], crypto) == message


class Person:
    """klasse for å representere en person"""

    def __init__(self, cipher):
        self.key = None
        self.cipher = cipher

    def set_key(self, key):
        """metode for å sette nøkkel for denne personen"""
        self.key = key

    def get_key(self):
        """metode for å hente ut nøkkelen til denne personen"""
        return self.key

    def set_cipher(self, cipher):
        """metode for å sette cipher"""
        self.cipher = cipher

    def get_cipher(self):
        """metode for å hente ut cipher"""
        return self.cipher

    def operate_cipher(self, message):
        """metode for å operere cipher riktig mellom sender og mottaker"""


class Sender(Person):
    """klasse for å representere en avsender"""

    def __init__(self, cipher):
        Person.__init__(self, cipher)

    def generate_message(self):
        """metode for å bestemme melding"""
        return input("Melding: ")

    def operate_cipher(self, message):
        """metode for å operere cipher riktig mellom sender og mottaker"""
        return self.cipher.encode(self.key, message)


class Receiver(Person):
    """klasse for å representere en mottaker"""

    def __init__(self, cipher):
        Person.__init__(self, cipher)

    def operate_cipher(self, message):
        """metode for å operere cipher riktig mellom sender og mottaker"""
        return self.cipher.decode(self.key, message)


class Hacker(Receiver):
    """klasse for å representere en hacker"""

    def __init__(self, cipher=None):
        Receiver.__init__(self, cipher)
        file = open("english_words.txt", "r")
        words = file.read()
        self.englishwords = words.split("\n")
        file.close()

    def is_word(self, word):
        """hjelpemetode for å sjekke om et ord er i ordlisten"""
        return word in self.englishwords

    def is_hacked(self, message, cipher):
        """hackemetode"""

        if isinstance(cipher, Caesar):
            for i in range(0, 95):
                word = cipher.decode(i, message)
                if self.is_word(word):
                    return True

        elif isinstance(cipher, Multiplicative):
            for i in range(0, 95):
                invers = crypto_utils.modular_inverse(i, 95)
                key = [i, invers]
                word = cipher.decode(key, message)
                if self.is_word(word):
                    return True

        elif isinstance(cipher, Affine):
            for i in range(0, 95):
                for j in range(0, 95):
                    key = [i, j]
                    word = cipher.decode(key, message)
                    if self.is_word(word):
                        return True

        elif isinstance(cipher, Unbreakable):
            for word in self.englishwords:
                hacked = cipher.decode(word, message)
                if self.is_word(hacked):
                    return True
        return False


def caesar():
    """Testkode for caesar"""
    print("-------------- Caesar-Test -----------------")
    cae = Caesar()
    key = Caesar().generate_keys()
    sender = Sender(cae)
    receiver = Receiver(cae)
    sender.set_key(key)
    receiver.set_key(key)
    message = sender.generate_message()
    encodedmessage = sender.operate_cipher(message)
    print(encodedmessage)
    decodedmessage = receiver.operate_cipher(encodedmessage)
    print(decodedmessage)
    print(Caesar().verify(key, message))


def multi():
    """Testkode for multi"""
    print("---------- Multiplicative-Test -------------")
    mult = Multiplicative()
    key = Multiplicative().generate_keys()
    sender = Sender(mult)
    receiver = Receiver(mult)
    sender.set_key(key)
    receiver.set_key(key)
    message = sender.generate_message()
    encodedmessage = sender.operate_cipher(message)
    print(encodedmessage)
    decodedmessage = receiver.operate_cipher(encodedmessage)
    print(decodedmessage)
    print(Multiplicative().verify(key, message))


def affine():
    """Testkode for affine"""
    print("-------------- Affine-Test -----------------")
    aff = Affine()
    key = Affine().generate_keys()
    sender = Sender(aff)
    receiver = Receiver(aff)
    sender.set_key(key)
    receiver.set_key(key)
    message = sender.generate_message()
    encodedmessage = sender.operate_cipher(message)
    print(encodedmessage)
    decodedmessage = receiver.operate_cipher(encodedmessage)
    print(decodedmessage)
    print(Affine().verify(key, message))


def unbreakable():
    """testkode for unbreakable"""
    print("---------------- UNBREAKABLE - Test -----------------")
    unb = Unbreakable()
    key = unb.generate_keys()
    sender = Sender(unb)
    reciever = Receiver(unb)
    sender.set_key(key[0])
    reciever.set_key(key[1])
    message = sender.generate_message()
    encodedmessage = sender.operate_cipher(message)
    print(encodedmessage)
    decodedmessage = reciever.operate_cipher(encodedmessage)
    print(decodedmessage)
    print(Unbreakable().verify(key, message))


def rsa():
    """Testkode for rsa"""
    print("---------------- RSA-Test ------------------")
    rsa = RSA()
    key = rsa.generate_keys()
    sender = Sender(rsa)
    reciever = Receiver(rsa)
    sender.set_key(key[0])
    reciever.set_key(key[1])
    message = sender.generate_message()
    encodedmessage = sender.operate_cipher(message)
    print(encodedmessage)
    decodedmessage = reciever.operate_cipher(encodedmessage)
    print(decodedmessage)
    print(RSA().verify(key, message))


def hacked():
    """test hackerklasse"""
    print("---------------- Hacked-Test ----------------")
    hack = Hacker()
    cipher = Affine()
    sender = Sender(cipher)
    key = cipher.generate_keys()
    sender.set_key(key)
    message = sender.generate_message()
    text = sender.operate_cipher(message)
    print("Er meldingen hacked? : " + str(hack.is_hacked(text, cipher)))


class main():
    """metode for å sjekke at alt funker"""
    caesar()
    multi()
    affine()
    unbreakable()
    rsa()
    hacked()
