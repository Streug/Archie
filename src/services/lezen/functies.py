"""
Deze code bevat de functie definities van de lezen modules.
"""

# Imports
import csv

# eigen functies


def bewaar_kenmerk(csvr, csvb):
    """Bewaar kenemrken."""
    csvb.write(csvr.as_csv() + "\n")


def al_gelezen_mail():
    """Kijk of de email al gelezen is."""

    eids: set[str] = set()

    def eerste(eid, csvbst):
        nonlocal functie, eids
        eids = gelezen_mails(csvbst)

        functie = vervolg  # vanaf nu alleen vervolg
        return vervolg(eid, csvbst)  # deel 2 ook meteen uitvoeren

    def vervolg(eid, csvbst):
        nonlocal eids

        if eid not in eids:
            eids.add(eid)
            return False
        return True

    functie = eerste

    def wentel(eid, csvbst):
        return functie(eid, csvbst)

    return wentel


def al_gelezen_bestand():
    """Kijk of het bestand al gelezen is."""

    bstn: set[str] = set()

    def eerste(pad, csvbst):
        nonlocal functie, bstn
        bstn = gelezen_bestanden(csvbst)
        functie = vervolg  # vanaf nu alleen vervolg
        return vervolg(pad, csvbst)  # deel 2 ook meteen uitvoeren

    def vervolg(pad, csvbst):
        nonlocal bstn

        if pad in bstn:
            return True
        bstn.add(pad)
        return False

    functie = eerste

    def wentel(pd, csvb):
        return functie(pd, csvb)

    return wentel


def gelezen_mails(csvb):
    csvb.seek(0)
    reader = csv.reader(csvb)
    return {rij[3] for rij in reader}


def gelezen_bestanden(csvb) -> set[str]:
    # In csvb is een bestandsnaam met een ',' vervangen door '*'
    # De bestndsnaam is aangevuld om uniciteit met: "-getal"
    # Hier wordt de bestandsnaam plus een eventuele extentie, dus zonder
    # "-'getal" bewaard in een set.

    bestanden = set()
    csvb.seek(0)
    reader = csv.reader(csvb)
    for regel in reader:
        delen = regel[0].rsplit(".", 1)
        bnaam = delen[0][:-4]  # zonder de meeste rechtse 4 getallen
        bext = ("." + delen[1]) if len(delen) == 2 else ""
        bestanden.add(bnaam + bext)
    return bestanden
