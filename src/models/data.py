"""
'Archie' is een programma om documenten te kunnen archiveren en terug te vinden.
Het bestaat uirt een register, een database, en een magazijn, eenbestands directorie.
"""

from dataclasses import dataclass, astuple


@dataclass
class CsvRecord:
    bestandsnaam: str = ""
    bestandspad: str = ""
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
