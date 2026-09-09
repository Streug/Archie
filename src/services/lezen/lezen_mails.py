"""
In lees_mails worden de Oulook e-mail berichten gelezen. Van de e-mails met een bijlage
(attachment) wordt gekeken of het een document is.
De kenmerken: email_id, onderwerp, afzender, ontvangstdatum, emailadres en het kenmerk
bestand_overslaan = False worden opgenomen in een CSV-bestand. De documenten worden,
opgeslagen, mits uniek, in het Magazijn/Voorportal. Het programma is zodanig dat
uitsluitend ongelezen berichten worden verwerkt.
Een gelezen email dat niet aan de criteria voldoet wordt in het CSV-bestand
weggeschreven, met de kenmerken: email-id, bestand_overslaan = True; de rest is leeg
"""

# Imports
import logging
import tempfile
from pathlib import Path

import win32com.client

# eigen functies
from src import config as cfg
from src import functies as fia
from src.models import data as mdl
from src.services.lezen import functies as fie


def run():
    logger = logging.getLogger(__name__)

    # Initialiseren
    csvpad = cfg.VOORPORTAAL_MAP / cfg.CSVBESTANDSNAAM1

    # Initialisaties
    outlook = win32com.client.Dispatch("Outlook.Application")
    namespace = outlook.GetNamespace("MAPI")
    store = namespace.DefaultStore.GetRootFolder()

    tot_folders = len(store.Folders)  # Ivm tonen voortgang

    uniek = 0
    uniek_bestand = fia.is_uniek()
    is_al_gelezen_mail = fie.al_gelezen_mail()

    logger.info("Gestart")

    with open(csvpad, "a+", encoding="utf-8", newline="") as csv_bestand:

        # Ontvangen emails lezen en verwerken
        for folder_nr, folder in enumerate(store.Folders):
            if folder.Name in cfg.INBOXEN:
                logger.info("Map: %s", folder.Name)
                tot_items = len(folder.Items)  # Ivm tonen voortgang
                for item_nr, item in enumerate(folder.Items):
                    csv_record = mdl.CsvRecord()
                    if item.Class != 43:  # Alleen mailItems
                        continue
                    # Lees mail bericht
                    csv_record.email_id = item.EntryID
                    # Ongelezen bericht?
                    if is_al_gelezen_mail(
                        csv_record.email_id,
                        csv_bestand,
                    ):
                        continue  # Ja

                    # Ongelezen bericht!
                    csv_record.onderwerp = item.Subject.replace(
                        ",", ""
                    )  # vervang eventuele komma door spatie
                    csv_record.afzender = item.SenderName.replace(
                        ",", ""
                    )  # vervang eventuele komma doo..
                    csv_record.ontvangstdatum = item.ReceivedTime.strftime(
                        "%Y-%m-%d %H:%M:%S"
                    )
                    sender = item.Sender
                    if sender:
                        exchange = sender.GetExchangeUser()
                        if exchange:
                            csv_record.emailadres = exchange.PrimarySmtpAddress
                        else:
                            csv_record.emailadres = item.SenderEmailAddress
                    # Sla documenten uit bericht bijlagen op.
                    for attachment in item.Attachments:
                        document = Path(attachment.FileName)
                        csv_record.bestandsnaam = (
                            f"{document.stem}-{uniek}.{document.suffix}"
                        )
                        uniek += 1
                        # Een document?
                        if document.suffix.lower() in cfg.DOCUMENTEN:
                            # Is het document uniek
                            # (Tijdelijk bestand van document maken, bijlagen zitten
                            # immers in de email niet in een map.
                            with tempfile.TemporaryDirectory() as tmpdir:
                                pad = Path(tmpdir) / document
                                attachment.SaveAsFile(str(pad))
                                # en dan..
                                if not uniek_bestand(pad):
                                    # Bewaar email_id en vermeld bestandsregel: verwerkt.
                                    csv_record.bestandsnaam = ""
                                    csv_record.bestand_overslaan = True
                                    csv_record.onderwerp = ""
                                    csv_record.afzender = ""
                                    csv_record.ontvangstdatum = ""
                                    csv_record.emailadres = ""
                                    fie.bewaar_kenmerk(csv_record, csv_bestand)
                                    logger.info("Document niet uniek: %s", document)
                                    continue  # het volgend mailbericht attachement
                            fie.bewaar_kenmerk(csv_record, csv_bestand)
                            # Kopieer bestand naar het Archie voorportaal
                            attachment.SaveAsFile(
                                str(cfg.VOORPORTAAL_MAP / csv_record.bestandsnaam)
                            )
                        else:
                            logger.info("Niet opgenomen: %s", document)
                            # Bewaar email_id en vermeld bestandsregel: verwerkt.
                            csv_record.bestandsnaam = ""
                            csv_record.bestand_overslaan = True
                            csv_record.onderwerp = ""
                            csv_record.afzender = ""
                            csv_record.ontvangstdatum = ""
                            csv_record.emailadres = ""
                            fie.bewaar_kenmerk(csv_record, csv_bestand)

                    # Tot slot, de voortgang
                    print(f"\rVoortgang: {item_nr+1}/{tot_items}", end="")
                    print()  # nieuwe regel na afloop

                print(f"\rVoortgang: {folder_nr+1}/{tot_folders}", end="")
                print()  # nieuwe regel na afloop

    logger.info("Geeindigd")
