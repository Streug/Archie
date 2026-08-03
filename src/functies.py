"""
Deze code bevat de functie definities van het adocn programma.
"""

# Imports
import hashlib

# eigen functies


def is_uniek():
    """Bepaal of het bestand uniek is, met ander woorden staat het beeld (foto / video)
    al in de database."""
    hashcache: set[str] = set()

    def eerste(flepth):
        nonlocal functie, hashcache

        if hashcache == {}:
            hashcache = set()
        functie = vervolg  # vanaf nu alleen vervolg
        return vervolg(flepth)

    def vervolg(flepth):
        nonlocal hashcache
        hsh = bereken_hash(flepth)
        if hsh not in hashcache:
            hashcache.add(hsh)
            return True
        return False

    functie = eerste

    def wentel(flepth):
        return functie(flepth)

    return wentel


def bereken_hash(flpth):
    """Functie om de bestnds hash volgens SHA-256 te bereken"""
    sha256 = hashlib.sha256()
    with flpth.open("rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            sha256.update(chunk)
    return sha256.hexdigest()
