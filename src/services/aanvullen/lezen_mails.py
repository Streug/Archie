"""
Dit programma opent Outlook, leest de Inbox en vervolgens de Aechief map. Het
haalt de bijlage(n) uit de ingelezen email. Van de bijlage(n) wordt de bestandsnaam,
pad waar het bestand plus een aantal email kenmerken, in een CSV bestand opgeslagen.
Het bestand zelf wordt opgeslagen in de submap "Voorportaal" van de Archie map:
"magazijn".De naam van het CSV bestand is: emailbijlagen.csv".
Het CSV bestand (emailbijlagen.csv) bestaat, per regel, uit:
-bestandsnaam,
-bestandspad,
-email kenmerken: Onderwerp, Afzender, Ontvangstdatum, Emailadres,email kenmerk5
-document kenmerk1 - .. document kenmerk10,
-archief kenmerk1 - .. archief kenmerk10
"""

# Imports
import logging
import pathlib

import win32com.client

# eigen functies
from src import config as cfg
from src.models import data as mdl
from src.services.aanvullen import functies as fie


def run():

    logging.FileHandler(
        cfg.LOGBESTAND, encoding="utf-8"
    )  # voorkomt dat er een logger foutmelding
    logger = logging.getLogger(__name__)
    logger.info("Started")

    # Initialiseren
    csvpad = pathlib.Path(cfg.DOELMAP) / cfg.CSVBESTAND_STAP1
    record = mdl.CsvRecord()

    # Outlook starten
    outlook = win32com.client.Dispatch("Outlook.Application")
    namespace = outlook.GetNamespace("MAPI")
    store = namespace.DefaultStore.GetRootFolder()

    with csvpad.open("a", encoding="utf-8", newline="") as resultaat:

        # inbox'en ophalen
        for folder in store.Folders:
            if folder.Name in cfg.INBOXEN:
                logger.info("Map: %s", folder.Name)
                fie.lees_inbox(logger, folder, record, resultaat)
