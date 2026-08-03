"""
'context' bevat de achtergond, de context, voor alle 'archie' modules.
"""

from queue import Queue
import threading
from types import ModuleType
from typing import Optional
import tkinter as tk

# eigen uncties
from progs.configs import config_archie as cfg


class Context:
    def __init__(self):
        self.config: ModuleType
        self.db: cfg.Database
        self.progress_queue: Queue = Queue()
        self.stop_event: threading.Event = threading.Event()
        self.gui_root: Optional[tk.Tk] = None
        self.view_initialized: bool = False
        self.status_actief = False
