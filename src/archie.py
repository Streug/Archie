"""
'Archie' is een programma om documenten te kunnen archiveren en terug te vinden.
Het bestaat uirt een register, een database, en een magazijn, eenbestands directorie.
"""

import logging

# eigen functies
from progs import adocn
from progs.context.context import Context
from progs.eenmalig import imdocn
from progs.services.setup_logging_archie import setup_logging
from progs.configs import config_archie as cfg


def build_context():
    ctx = Context()
    # --- config ---
    ctx.config = cfg
    # --- database ---
    # ctx.db = cfg.Database(pad=cfg.database.pad)
    # --- services ---
    return ctx


def main():
    logging.getLogger(__name__).info("Gestart")

    context = build_context()

    # root = tk.Tk()
    # root.title(cfg.titel_archie_scherm)
    # root.geometry(cfg.grootte_archie_scherm)

    # context.gui_root = root

    setup_logging(
        cfg.LEVEL,
        cfg.LOGBESTAND,
        cfg.FORMAT,
        cfg.MAX_BYTES,
        cfg.BACKUPS,
    )

    adocn.run()
    imdocn.run()

    # root.mainloop()


if __name__ == "__main__":
    main()
