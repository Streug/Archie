"""
Deze code bevat de functie definities van het laden_mail_bijlagen programma.
"""

# Imports
import logging
import tempfile
from pathlib import Path

# eigen functies
from src import config as cfg
from src import functies as fie


def lees_inbox(lgr, folder, rec, rslt):
    uniek = 0
    uniek_bestand = fie.is_uniek()
    for item in folder.Items:
        if item.Class != 43:  # Alleen MailItem
            continue
        rec.onderwerp = item.Subject.replace(
            ",", ""
        )  # vervang eventuele komma door spatie
        rec.afzender = item.SenderName.replace(",", "")  # vervang eventuele komma doo..
        rec.ontvangstdatum = item.ReceivedTime.strftime("%Y-%m-%d %H:%M:%S")
        sender = item.Sender
        if sender:
            exchange = sender.GetExchangeUser()
            if exchange:
                rec.emailadres = exchange.PrimarySmtpAddress
            else:
                rec.emailadres = item.SenderEmailAddress
        for attachment in item.Attachments:
            origineel = Path(attachment.FileName)
            if origineel.suffix.lower() not in cfg.TOEGESTAAN:
                lgr.info("Niet opgenomen is bijlage:%s", origineel)
                continue
            # is het bestand uniek?
            # eerst een tijdelijk bestand maken
            with tempfile.TemporaryDirectory() as tmpdir:
                bestand = Path(tmpdir) / attachment.FileName
                attachment.SaveAsFile(str(bestand))
                # en dan..
                if not uniek_bestand(bestand):
                    lgr.info("Niet uniek: %s", origineel)
                    continue
            rec.bestandsnaam = f"{origineel.stem}-{uniek}" f"{origineel.suffix}"
            uniek += 1
            rec.bestandspad = f"{origineel.parent}"
            rslt.write(rec.as_csv() + "\n")
            doelbestand = Path(cfg.DOELMAP) / rec.bestandsnaam
            attachment.SaveAsFile(str(doelbestand))


def verwerk_berichten(bern, unk, rslt):
    logger = logging.getLogger(__name__)

    for bericht in bern:
        # mail kenmerken ophalen
        try:
            cfg.email_kenmerken[0] = bericht.Subject
            cfg.email_kenmerken[1] = bericht.SenderName
            cfg.email_kenmerken[2] = bericht.ReceivedTime
            sender = bericht.Sender
            if sender:
                exchange = sender.GetExchangeUser()
                if exchange:
                    cfg.email_kenmerken[3] = exchange.PrimarySmtpAddress
                else:
                    cfg.email_kenmerken[3] = bericht.SenderEmailAddress

            attachments = bericht.Attachments
        except Exception:
            logger.exception("Geen email kenmerken")
            continue

        if bericht.Class != 43:
            logger.info("Onderwerp: %s", bericht.Subject)
            continue

        for i in range(1, attachments.Count + 1):
            attachment = attachments.Item(i)
            origineel = Path(attachment.FileName)
            if origineel.suffix.lower() not in cfg.TOEGESTAAN:
                logger.info("Bijlage: %s is niet toegestaan", origineel)
                continue
            cfg.bestand[0] = f"{origineel.stem}-{unk}" f"{origineel.suffix}"
            unk += 1
            cfg.bestand[1] = f"{origineel.parents}"

            csv_reeks = maak_reeks(cfg.csv_container)
            rslt.write(csv_reeks + "\n")

            doelbestand = Path(cfg.DOELMAP) / cfg.bestand[0]
            attachment.SaveAsFile(str(doelbestand))


def maak_reeks(csv_cntr):
    return ",".join(str(p) for p in csv_cntr)
