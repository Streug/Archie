"""
Dit programma importeert PDF iles uit het op directories gebaseerde documenten archief
dat op de NAS staat naar het 'voorportaal' van het Archie cmagazijn.
Het loopt daarvoor door al deze directories en plaatst de bestandsnaam, het pad van het
document plus de achtereenvolgende subdirectories in een CSV element. Tot slot wordt het
bestand gekopieerd naar het voorportaal.
Het Het CSV bestand bestaat, per regel, uit:
voorstuk:
- bestands kenmerken,
- email kenmerken,
archief kenmerken
(zieDataClass def)
"""

# Imports
import logging
import shutil

# eigen functies
from src import config as cfg
from src import functies as gfie
from src.models import data as mdl
from src.services.lezen import functies as fie


def run():
    logger = logging.getLogger(__name__)
    logger.info("Gestart")

    # initialiseren
    csvpad = cfg.VOORPORTAAL_MAP / cfg.CSVBESTANDSNAAM1
    uniek = 0
    is_uniek = gfie.is_uniek()
    is_al_gelezen_bestand = fie.al_gelezen_bestand()

    # zoek alle bestanden
    bestanden = [p for p in cfg.ARCHIEFMAPPEN.rglob("*") if p.is_file()]
    tot_bestanden = len(bestanden)

    with open(csvpad, "a+", newline="", encoding="utf-8") as csv_bestand:
        for bestand_nr, bestandspad in enumerate(bestanden, start=1):
            csv_record = mdl.CsvRecord()
            # Al gelezen bestand? (zonder het getal)
            org_bestandsnaam = bestandspad.name.replace(",", "*")
            if is_al_gelezen_bestand(
                org_bestandsnaam,
                csv_bestand,
            ):
                continue  # Ja, skip
            unieke_bestandsnaam = (
                f"{bestandspad.stem}{uniek:04d}{bestandspad.suffix}"
            ).replace(",", "*")
            # Nee, is het een document?
            if bestandspad.suffix.lower() in cfg.DOCUMENTEN:
                # is het document ook uniek?
                if is_uniek(bestandspad):
                    csv_record.bestandsnaam = unieke_bestandsnaam
                    uniek += 1
                    csv_record.bestandsmappen = f"{bestandspad.parent}"
                    mappen = bestandspad.parts[1:-1]
                    csv_record.map1 = str(mappen[0] if len(mappen) > 0 else "")
                    csv_record.map2 = str(mappen[1] if len(mappen) > 1 else "")
                    csv_record.map3 = str(mappen[2] if len(mappen) > 2 else "")
                    csv_record.map4 = str(mappen[3] if len(mappen) > 3 else "")
                    csv_record.map5 = str(mappen[4] if len(mappen) > 4 else "")
                    # Kopieer het bestand naar de doelmap
                    shutil.copy2(
                        bestandspad,
                        cfg.VOORPORTAAL_MAP / csv_record.bestandsnaam.replace("*", ","),
                    )
                else:
                    logger.info("Document: %s is niet uniek", bestandspad)
                    csv_record.bestandsnaam = unieke_bestandsnaam
                    csv_record.bestandsmappen = ""
                    csv_record.bestand_overslaan = True
                    csv_record.map1 = ""
                    csv_record.map2 = ""
                    csv_record.map3 = ""
                    csv_record.map4 = ""
                    csv_record.map5 = ""
                    fie.bewaar_kenmerk(csv_record, csv_bestand)
            else:
                logger.info("Bestand: %s niet opgenomen", bestandspad)
                csv_record.bestandsnaam = unieke_bestandsnaam
                csv_record.bestandsmappen = ""
                csv_record.bestand_overslaan = True
                csv_record.map1 = ""
                csv_record.map2 = ""
                csv_record.map3 = ""
                csv_record.map4 = ""
                csv_record.map5 = ""
                fie.bewaar_kenmerk(csv_record, csv_bestand)
            fie.bewaar_kenmerk(csv_record, csv_bestand)

            # Tot slot, de voortgang
            print(f"Voortgang: {bestand_nr}/{tot_bestanden}", end="\r")
            print()  # nieuwe regel na afloop
        logger.info("Geeindigd")
