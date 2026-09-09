"""
'config' bevat alle parameters die nodig zijn voor een of meer 'archie' modules.
"""

from pathlib import Path

import yaml

CONFIG_ARCHIE = Path(__file__).resolve().parent.parent / "config" / "archie.yaml"


# Get the parameter data for all foto modules
with open(CONFIG_ARCHIE, "r") as yml:
    yml = yaml.safe_load(yml)

    # --------------- parameters FOTO ------------------------
    # --------------------------------------------------------
    #
    # logging
    LEVEL = yml["logging"]["level"]
    LOGBESTAND = yml["logging"]["logbestand"]
    FORMAT = yml["logging"]["format"]
    MAX_BYTES = yml["logging"]["max_bytes"]
    BACKUPS = yml["logging"]["backups"]


csv_container = yml["csv_container"]
bestand_kenmerken = csv_container[0]
email_kenmerken = csv_container[1]
archief_kenmerken = csv_container[2]


# Database pad
# database = Database(pad=Path(yml["database_file"]))


DOCUMENTEN = yml["documenten"]  # Lijst toegestande documenten
INBOXEN = yml["inboxen"]  # Lijst folders die gelezen worden

CSVBESTANDSNAAM1 = Path(yml["csvbestandsnaam1"])
CSVBESTANDSNAAM2 = Path(yml["csvbestandsnaam2"])
VOORPORTAAL_MAP = Path(yml["voorportaal_pad"])
MAGZIJN_MAP = Path(yml["magazijn_pad"])
ARCHIEFMAPPEN = Path(yml["archiefmappen"])


# speciaal object om aan te geven dat de gebruiker de max fotos popup heeft geannuleerd
# CANCEL = object()

# ---------------ARCHIVEER ------------------------
KENMERKEN = yml["kenmerken"]
# --------------- parameters XXX ------------------------
# --------------------------------------------------------
