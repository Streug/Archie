"""
Dit programma importeert PDF iles uit het op directories gebaseerde documenten archief dat op de NAS staat
naar het 'voorportaal' van het Archie cmagazijn.
Het loopt daarvoor door al deze directories en plaatst de bestandsnaam, het pad van het document
plus de achtereenvolgende subdirectories in een CSV element. Tot slot wordt het bestand gekopieerd naar het
voorportaal.
Het Het CSV bestand bestaat, per regel, uit:
voorstuk:
- bestandsnaam,
- bestandspad,
email kenmerk 1, email kenmerk 2, email kenmerk 3, email kenmerk 4, email kenmerk 5
archief kenmerk 1 - archief kenmerk 10,
"""

# Imports
import logging
from pathlib import Path

# eigen functies
from src import config as cfg
from src import functies as fie
from src.models import data as mdl


def run():
    logging.FileHandler(
        cfg.LOGBESTAND, encoding="utf-8"
    )  # voorkomt dat er een logger foutmelding
    logger = logging.getLogger(__name__)

    logger.info("Start importeren")
    csvpad = Path(cfg.DOELMAP) / cfg.CSVBESTAND_STAP1
    record = mdl.CsvRecord()
    uniek = 0
    uniek_bestand = fie.is_uniek()
    with open(csvpad, "a", newline="", encoding="utf-8") as resultaat:
        for origineel in cfg.ARCHIEFMAPPEN.rglob("*"):
            if origineel.is_file():
                # is het bestand uniek?
                # code
                if not uniek_bestand(origineel):
                    logger.info("Niet uniek: %s", origineel)
                    continue
                record.bestandsnaam = f"{origineel.stem}-{uniek}" f"{origineel.suffix}"
                uniek += 1
                record.bestandspad = origineel.parent
                mappen = origineel.parts[1:-1]
                record.map1 = str(mappen[0] if len(mappen) > 0 else "")
                record.map2 = str(mappen[1] if len(mappen) > 1 else "")
                record.map3 = str(mappen[2] if len(mappen) > 2 else "")
                record.map4 = str(mappen[3] if len(mappen) > 3 else "")
                record.map5 = str(mappen[4] if len(mappen) > 4 else "")
                resultaat.write(record.as_csv() + "\n")
                if origineel.suffix.lower() not in cfg.TOEGESTAAN:
                    logger.info("Bijlage: %s is niet toegestaan", origineel)
    logger.info("Einde importeren")
