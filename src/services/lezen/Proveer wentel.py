"""
Deze code bevat de functie definities van het lezen_mail_bijlagen programma.
"""

# Imports
# import csv

# eigen functies

eids: set[str] = set()


def al_gelezen():
    """Kijk of de email al gelezen is."""

    eids: set[str] = set()

    def eerste(csvbst, eid):
        nonlocal functie, eids
        eids = gelezen_mails(csvbst)

        functie = vervolg  # vanaf nu alleen vervolg
        return vervolg(csvbst, eid)  # deel 2 ook meteen uitvoeren

    def vervolg(csvbst, eid):
        nonlocal eids

        if eid not in eids:
            eids.add(eid)
            return False
        return True

    functie = eerste

    def wentel(csvrslt, eid):
        return functie(csvrslt, eid)

    return wentel


def gelezen_mails(cb):
    eids.add(cb)
    print(f"Gelezen mail: {cb}")
    return eids


# GEBRUIK
waarden = [(1, 2), (30, 40), (500, 600), (7000, 8000), (90000, 100000)]
# wentel = model_wentel()
# print("Test van de wentel functie:")

# for a1, a2 in waarden:
#    rslt = wentel(a1, a2)
#    print(rslt)

is_al_gelezen = al_gelezen()
for a1, a2 in waarden:
    rslt = is_al_gelezen(a1, a2)
    print(rslt)
    print(f"eids: {eids}")
