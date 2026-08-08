"""
'context' bevat de achtergond, de context, voor alle 'Archie' modules.
"""

import threading
import tkinter as tk
from queue import Queue
from types import ModuleType

# eigen uncties
from src import config as cfg


class Context:
    def __init__(self):
        self.config: ModuleType
        self.db: cfg.Database
        self.progress_queue: Queue = Queue()
        self.stop_event: threading.Event = threading.Event()
        self.gui_root: tk.Tk | None = None
        self.view_initialized: bool = False
        self.status_actief = False
