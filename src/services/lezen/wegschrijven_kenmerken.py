"""
Dit programma leest het CSV-bestand en presenteert per bestandsregel het document en
 er aan verbonden kenmerken. Het is zodanig ingericht dat het de werkwijze ”Toevoegen
 Document” volgt. Van een document dat ‘geschreven’ is, is het resultaat een CSV -regel
 die wordt opgeslagen in een tweede  CSV-bestand en staat het document onder een Archie
documentnaam in het Magazijn/Voorportaal.
"""

# Imports
import logging
import tkinter as tk

# eigen functies
from src.services.lezen import gui as ui


def run():
    logger = logging.getLogger(__name__)

    logger.info("Gestart")

    root = tk.Tk()
    ui.PDFReviewer(root)
    root.mainloop()
