"""
'config' bevat alle parameters die nodig zijn voor een of meer 'archie' modules.
"""

import sqlite3
from dataclasses import dataclass
from pathlib import Path

import yaml

CONFIG_ARCHIE = Path(__file__).resolve().parent.parent / "config" / "archie.yaml"


@dataclass
class Database:
    pad: Path
    conn: sqlite3.Connection | None = None

    def connect(self):
        if self.conn is None:
            self.conn = sqlite3.connect(self.pad)
            self.conn.row_factory = sqlite3.Row
        return self.conn


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


TOEGESTAAN = yml["toestaan"]
INBOXEN = yml["inboxen"]

CSVBESTAND_STAP1 = Path(yml["csvbestand_stap1"])
CSVBESTAND_STAP2 = Path(yml["csvbestand_stap2"])
DOELMAP = Path(yml["doelmap"])
DOELMAP.mkdir(parents=True, exist_ok=True)
ARCHIEFMAPPEN = Path(yml["archiefmappen"])


# speciaal object om aan te geven dat de gebruiker de max fotos popup heeft geannuleerd
# CANCEL = object()

# ---------------ARCHIVEER ------------------------
KENMERKEN = yml["kenmerken"]
# --------------- parameters XXX ------------------------
# --------------------------------------------------------
