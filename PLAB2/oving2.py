"""stein, saks, papir"""
import random
import statistics
import matplotlib.pyplot as plt


class Spiller:
    """klasse som representerer en spiller"""

    aksjoner = ["stein", "saks", "papir"]

    def __init__(self, navn):
        self.navn = navn
        self.poeng = 0
        self.spilt = []
        self.motstanderspilt = []

    def velg_aksjon(self):
        """abstrakt metode som arves av de ulike spillertypene"""

    def motta_resultat(self, egenaksjon, motstanderaksjon):
        """mottar aksjonene fra både spiller og motstander"""
        self.spilt.append(egenaksjon)
        self.motstanderspilt.append(motstanderaksjon)

    def har_spilt(self):
        """returnerer en liste med trekkene spilleren har spilt"""
        return self.spilt

    def oppgi_navn(self):
        """oppgir navnet til spilleren"""
        return str(self.navn)

    def legg_til_poeng(self, poeng):
        """legger til poeng"""
        self.poeng += poeng

    def hent_poeng(self):
        """henter poengene spilleren har"""
        return self.poeng


class Tilfeldig(Spiller):
    """spillertype som spiller et tilfeldig trekk"""

    def __init__(self, navn):
        Spiller.__init__(self, navn)

    def velg_aksjon(self):
        return self.aksjoner[random.randint(0, 2)]

    def motta_navn(self):
        """mottar navnet spiller har skrevet til konsoll"""
        return self.navn


class Sekvensiell(Spiller):
    """spillertype som spiller trekkene stein, saks, papir sekvensielt"""

    def __init__(self, navn):
        Spiller.__init__(self, navn)

    teller = 1

    def velg_aksjon(self):
        aksjon = ""
        if self.teller % 3 == 1:
            aksjon = "stein"
        elif self.teller % 3 == 2:
            aksjon = "saks"
        elif self.teller % 3 == 0:
            aksjon = "papir"

        self.teller += 1
        return aksjon

    def motta_navn(self):
        """mottar navnet bruker har skrevet til konsoll"""
        return self.navn


class MestVanlig(Spiller):
    """klasse for å representere spillertypen mestVanlig"""

    def __init__(self, navn):
        Spiller.__init__(self, navn)

    def motta_navn(self):
        """mottar navnet bruker har skrevet inn til konsoll"""
        return self.navn

    def velg_aksjon(self):
        aksjon = ""
        try:
            mestvanlig = statistics.mode(self.motstanderspilt)
            if mestvanlig == "stein":
                aksjon = self.aksjoner[2]
            elif mestvanlig == "saks":
                aksjon = self.aksjoner[0]
            elif mestvanlig == "papir":
                aksjon = self.aksjoner[1]
            return aksjon

        except statistics.StatisticsError:
            return self.aksjoner[random.randint(0, 2)]


class Historiker(Spiller):
    """spillertype som baserer seg på historikk fra tidligere spilte trekk"""

    def __init__(self, navn):
        Spiller.__init__(self, navn)
        self.husk = int(input("Hvor mange trekk skal huskes? "))

    def motta_navn(self):
        """mottar navnet bruker har skrevet til konsollen"""
        return self.navn

    def velg_aksjon(self):
        sekvens = []
        flest = []
        if self.husk >= len(self.motstanderspilt):
            aksjon = self.aksjoner[random.randint(0, 2)]
        else:
            for i in range(len(self.motstanderspilt) - self.husk,
                           len(self.motstanderspilt)):
                sekvens.append(self.motstanderspilt[i])
            for i in range(0, len(self.motstanderspilt) - self.husk):
                # sjekker sekvens i listen av resultater
                if self.motstanderspilt[i:i + self.husk] == sekvens:
                    flest.append(self.motstanderspilt[i + self.husk])

            stein = flest.count("stein")
            saks = flest.count("saks")
            papir = flest.count("papir")

            dic = {
                "count_stein": stein,
                "count_saks": saks,
                "count_papir": papir}
            if dic.get("count_stein") > dic.get("count_saks") \
                    and dic.get("count_stein") > dic.get("count_papir"):
                aksjon = "papir"
            elif dic.get("count_papir") > dic.get("count_saks") \
                    and dic.get("count_papir") > dic.get("count_stein"):
                aksjon = "saks"
            elif dic.get("count_saks") > dic.get("count_stein") \
                    and dic.get("count_saks") > dic.get("count_papir"):
                aksjon = "stein"
            else:
                aksjon = self.aksjoner[random.randint(0, 2)]

        return aksjon


class Aksjon:

    """klasse for å vite om en aksjon slår en annen"""

    aksjon = {"stein": 0, "saks": 1, "papir": 2}

    def __init__(self, aksjon):
        if isinstance(aksjon, str):
            aksjon = {"stein": 0, "saks": 1, "papir": 2}[aksjon]
        assert isinstance(aksjon, int) & (aksjon >= 0) & (aksjon < 3)
        self.aksjon = aksjon

    def __eq__(self, other):
        return self.aksjon == other.aksjon

    def __gt__(self, other):
        return (3 + other.aksjon - self.aksjon) % 3 == 1

    def __str__(self):
        return {0: "Stein", 1: "Saks", 2: "Papir"}[self.aksjon]

    def who_beats_me(self):
        """sier hvilke metoder som slår hvilke"""
        return (self.aksjon - 1) % 3


class EnkeltSpill:
    """klasse for å gjennomføre et enkelt slag mellom 2 spillere"""

    def __init__(self, spiller1, spiller2):
        self.spiller1 = spiller1
        self.spiller2 = spiller2

    def gjennomfoer_spill(self):
        """gjennomfører et enkelt slag stein, saks, papir"""
        spiller1aksjon = self.spiller1.velg_aksjon()
        spiller2aksjon = self.spiller2.velg_aksjon()

        aksjon1 = Aksjon(spiller1aksjon)
        aksjon2 = Aksjon(spiller2aksjon)

        if aksjon1.__eq__(aksjon2):
            self.spiller1.legg_til_poeng(0.5)
            self.spiller2.legg_til_poeng(0.5)
            print(
                self.spiller1.motta_navn() +
                " spilte " +
                spiller1aksjon +
                ", og fikk 0.5 poeng, og " +
                self.spiller2.motta_navn() +
                " spilte " +
                spiller2aksjon +
                " og fikk 0.5 poeng")

        elif aksjon1.__gt__(aksjon2):
            self.spiller1.legg_til_poeng(1)
            print(
                self.spiller1.motta_navn() +
                " spilte " +
                spiller1aksjon +
                ", og vant dermed over " +
                self.spiller2.motta_navn() +
                " som spilte " +
                spiller2aksjon +
                ". " +
                self.spiller1.motta_navn() +
                " fikk dermed 1 poeng! ")
        else:
            self.spiller2.legg_til_poeng(1)
            print(
                self.spiller2.motta_navn() +
                " spilte " +
                spiller2aksjon +
                ", og vant dermed over " +
                self.spiller1.motta_navn() +
                " som spilte " +
                spiller1aksjon +
                ". " +
                self.spiller2.motta_navn() +
                " fikk dermed 1 poeng! ")

        self.spiller1.motta_resultat(spiller1aksjon, spiller2aksjon)
        self.spiller2.motta_resultat(spiller2aksjon, spiller1aksjon)

    def __str__(self):
        print("halla")


class MangeSpill:

    """klasse for å gjennomføre mange spill av stein, saks, papir"""

    spilt = 0

    def __init__(self, spiller1, spiller2, antall_spill):
        self.spiller1 = spiller1
        self.spiller2 = spiller2
        self.antall_spill = antall_spill

    def arranger_enkeltspill(self):
        """arrangerer enkeltspill av stein, saks, papir"""
        EnkeltSpill(self.spiller1, self.spiller2).gjennomfoer_spill()

    def arranger_turnering(self):
        """arrangerer turnering av stein, saks, papir"""
        prosentspiller1 = []
        prosentspiller2 = []
        for _ in range(self.antall_spill):
            self.arranger_enkeltspill()
            self.spilt += 1
            prosentspiller1.append((self.spiller1.hent_poeng() / self.spilt))
            prosentspiller2.append((self.spiller2.hent_poeng() / self.spilt))
        print(self.spiller1.motta_navn() + " sine poeng: " +
              str(self.spiller1.hent_poeng()))
        print(self.spiller1.motta_navn() + " vant dermed " +
              str((self.spiller1.hent_poeng() /
                   self.antall_spill) *
                  100).format(":0.2f") +
              " % av spillene.")
        print(self.spiller2.motta_navn() + " sine poeng: " +
              str(self.spiller2.hent_poeng()))
        print(self.spiller2.motta_navn() + " vant dermed " +
              str((self.spiller2.hent_poeng() /
                   self.antall_spill) *
                  100).format(":0.2f") +
              " % av spillene.")
        print(self.spiller1.motta_navn() + " har spilt " +
              str(self.spiller1.har_spilt()))
        print(self.spiller2.motta_navn() + " har spilt " +
              str(self.spiller2.har_spilt()))

        plt.ylabel("Seiersprosent")
        plt.xlabel("Antall spill")
        plt.axis([0, self.antall_spill, 0, 1])
        plt.plot(prosentspiller1)  # vinnprosent spiller1
        plt.plot(prosentspiller2)  # vinnprosent spiller2
        plt.show()


def main():
    """metode for å kjøre spill med tekstgrensesnitt"""
    spiller1 = input("Velg spiller 1: ")
    spiller2 = input("Velg spiller 2: ")
    valg1 = velg_spiller(spiller1)
    valg2 = velg_spiller(spiller2)
    antall = int(input("Hvor mange spill? "))

    spill = MangeSpill(valg1, valg2, antall)
    spill.arranger_turnering()


def velg_spiller(spiller):
    """metode for å velge spilertype"""
    spilleren = ""
    if spiller == "tilfeldig":
        spilleren = Tilfeldig(spiller)
    elif spiller == "sekvensiell":
        spilleren = Sekvensiell(spiller)
    elif spiller == "mestVanlig":
        spilleren = MestVanlig(spiller)
    elif spiller == "historiker":
        spilleren = Historiker(spiller)
    else:
        print("Ugyldig spiller")
    return spilleren


main()
