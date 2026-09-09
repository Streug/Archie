"""
'Archie' is een programma om documenten te kunnen archiveren en terug te vinden.
Het bestaat uirt een register, een database, en een magazijn, eenbestands directorie.
"""

import sqlite3
from dataclasses import astuple, dataclass
from pathlib import Path


@dataclass
class CsvRecord:
    bestandsnaam: str = ""
    bestandsmappen: str = ""
    bestand_overslaan: bool = False  # bestandsregel niet verwerken
    email_id: str = ""
    onderwerp: str = ""
    afzender: str = ""
    ontvangstdatum: str = ""
    emailadres: str = ""
    map1: str = ""
    map2: str = ""
    map3: str = ""
    map4: str = ""
    map5: str = ""

    def as_csv(self) -> str:
        return ",".join(map(str, astuple(self)))


@dataclass
class Database:
    pad: Path
    conn: sqlite3.Connection | None = None

    def connect(self):
        if self.conn is None:
            self.conn = sqlite3.connect(self.pad)
            self.conn.row_factory = sqlite3.Row
        return self.conn
