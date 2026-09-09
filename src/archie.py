"""
'Archie' is een programma om documenten te kunnen archiveren en terug te vinden.
Het bestaat uirt een register, een database, en een magazijn, eenbestands directorie.
"""

import logging

# eigen functies
from src import config as cfg
from src.context import Context
from src.services.lezen import lezen_mails, lezen_mappen, wegschrijven_kenmerken
from src.setup_logging import setup_logging


def build_context():
    ctx = Context()
    # --- config ---
    ctx.config = cfg
    # --- database ---
    # ctx.db = cfg.Database(pad=cfg.database.pad)
    # --- services ---
    return ctx


def archie():

    # context = build_context()

    # root = tk.Tk()
    # root.title(cfg.titel_archie_scherm)
    # root.geometry(cfg.grootte_archie_scherm)

    # context.gui_root = root

    # context = build_context()

    logger = setup_logging(
        cfg.LEVEL,
        cfg.LOGBESTAND,
        cfg.FORMAT,
        cfg.MAX_BYTES,
        cfg.BACKUPS,
    )

    logger.info("Gestart")

    logger = logging.getLogger(__name__)

    # lezen_mails.run()
    # lezen_mappen.run()
    wegschrijven_kenmerken.run()

    logger.info("Geeindigd")


archie()
