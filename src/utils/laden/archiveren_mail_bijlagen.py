"""
Dit programma smaakt het mogelijk om snel kenmerken toe te voegen aan een document,
bij het verwerken van grote hoeveelheden documenten. Documenten staan in het voorportaal van
het Archie archief.  De resultaten worden opgeslagen in een CSV bestand, dat later kan
worden ingelezen in Archie.
"""

# Imports
import csv
import logging
import os
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, ttk

import fitz  # PyMuPDF
from PIL import Image, ImageTk

# eigen functies
from progs.configs import config_archie as cfg


def run():
    logging.FileHandler(
        "archie.log", encoding="utf-8"
    )  # voorkomt dat er een logger foutmelding
    logger = logging.getLogger(__name__)

    logger.info("Start importeren")

    """
    PDF Reviewer Tool
    -----------------
    Bekijk PDF's in het venster en vul kenmerken in per document.
    Resultaten worden opgeslagen in een CSV bestand.

    Installatie:
        pip install pymupdf

    Gebruik:
        python pdf_reviewer.py

    Pas de FEATURES lijst hieronder aan naar jouw kenmerken.
    """

    try:
        HAS_PYMUPDF = True
    except ImportError:
        HAS_PYMUPDF = False

    # ──────────────────────────────────────────────
    # CONFIGURATIE — pas hier je kenmerken aan
    # ──────────────────────────────────────────────

    class PDFReviewer:
        def __init__(self, root):
            self.root = root
            self.root.title("PDF Reviewer")
            self.root.geometry("1200x800")
            self.root.configure(bg="#1e1e2e")

            self.pdf_files = []
            self.current_index = 0
            self.current_doc = None
            self.current_page = 0
            self.zoom = 1.5
            self.all_results = []
            self.photo = None
            self._check_dependencies()
            self._build_ui()
            self._load_existing_csv()

        def _check_dependencies(self):
            if not HAS_PYMUPDF:
                messagebox.showerror(
                    "Ontbrekende bibliotheek",
                    "Installeer PyMuPDF en Pillow:\n\n  pip install pymupdf pillow",
                )
                self.root.destroy()

        # ── UI opbouw ──────────────────────────────

        def _build_ui(self):
            style = ttk.Style()
            style.theme_use("clam")
            style.configure(
                "TLabel",
                background="#1e1e2e",
                foreground="#cdd6f4",
                font=("Georgia", 11),
            )
            style.configure("TButton", font=("Georgia", 10), padding=6)
            style.configure("TEntry", font=("Courier New", 11))
            style.configure("TFrame", background="#1e1e2e")

            # Toolbar
            toolbar = tk.Frame(self.root, bg="#181825", pady=8, padx=12)
            toolbar.pack(side=tk.TOP, fill=tk.X)

            tk.Button(
                toolbar,
                text="📂  Map openen",
                command=self._open_folder,
                bg="#89b4fa",
                fg="#1e1e2e",
                font=("Georgia", 10, "bold"),
                relief=tk.FLAT,
                padx=12,
                pady=4,
            ).pack(side=tk.LEFT, padx=(0, 8))

            tk.Button(
                toolbar,
                text="📄  PDF's kiezen",
                command=self._open_files,
                bg="#a6e3a1",
                fg="#1e1e2e",
                font=("Georgia", 10, "bold"),
                relief=tk.FLAT,
                padx=12,
                pady=4,
            ).pack(side=tk.LEFT, padx=(0, 16))

            self.progress_label = tk.Label(
                toolbar,
                text="Geen bestanden geladen",
                bg="#181825",
                fg="#6c7086",
                font=("Courier New", 10),
            )
            self.progress_label.pack(side=tk.LEFT)

            tk.Button(
                toolbar,
                text="💾  CSV opslaan",
                command=self._save_csv,
                bg="#f38ba8",
                fg="#1e1e2e",
                font=("Georgia", 10, "bold"),
                relief=tk.FLAT,
                padx=12,
                pady=4,
            ).pack(side=tk.RIGHT)

            # Hoofd splitter
            paned = tk.PanedWindow(
                self.root,
                orient=tk.HORIZONTAL,
                bg="#313244",
                sashwidth=6,
                sashrelief=tk.FLAT,
            )
            paned.pack(fill=tk.BOTH, expand=True, padx=0, pady=0)

            # ── Linker paneel: PDF viewer ──
            left = tk.Frame(paned, bg="#181825")
            paned.add(left, minsize=400)

            # PDF navigatie
            nav = tk.Frame(left, bg="#181825", pady=4)
            nav.pack(fill=tk.X, padx=8)

            tk.Button(
                nav,
                text="◀◀ Vorige PDF",
                command=self._prev_pdf,
                bg="#313244",
                fg="#cdd6f4",
                font=("Courier New", 9),
                relief=tk.FLAT,
                padx=8,
            ).pack(side=tk.LEFT)
            tk.Button(
                nav,
                text="▶▶ Volgende PDF",
                command=self._next_pdf,
                bg="#313244",
                fg="#cdd6f4",
                font=("Courier New", 9),
                relief=tk.FLAT,
                padx=8,
            ).pack(side=tk.LEFT, padx=4)

            self.file_label = tk.Label(
                nav, text="—", bg="#181825", fg="#89b4fa", font=("Courier New", 9)
            )
            self.file_label.pack(side=tk.LEFT, padx=8)

            # Pagina navigatie
            page_nav = tk.Frame(left, bg="#181825", pady=2)
            page_nav.pack(fill=tk.X, padx=8)

            tk.Button(
                page_nav,
                text="◀ Pagina",
                command=self._prev_page,
                bg="#45475a",
                fg="#cdd6f4",
                font=("Courier New", 9),
                relief=tk.FLAT,
                padx=6,
            ).pack(side=tk.LEFT)
            tk.Button(
                page_nav,
                text="Pagina ▶",
                command=self._next_page,
                bg="#45475a",
                fg="#cdd6f4",
                font=("Courier New", 9),
                relief=tk.FLAT,
                padx=6,
            ).pack(side=tk.LEFT, padx=4)
            self.page_label = tk.Label(
                page_nav, text="", bg="#181825", fg="#6c7086", font=("Courier New", 9)
            )
            self.page_label.pack(side=tk.LEFT, padx=4)

            tk.Button(
                page_nav,
                text="＋ Zoom",
                command=lambda: self._zoom(1.25),
                bg="#45475a",
                fg="#cdd6f4",
                font=("Courier New", 9),
                relief=tk.FLAT,
                padx=6,
            ).pack(side=tk.RIGHT)
            tk.Button(
                page_nav,
                text="－ Zoom",
                command=lambda: self._zoom(0.8),
                bg="#45475a",
                fg="#cdd6f4",
                font=("Courier New", 9),
                relief=tk.FLAT,
                padx=6,
            ).pack(side=tk.RIGHT, padx=4)

            # Canvas met scrollbars
            canvas_frame = tk.Frame(left, bg="#181825")
            canvas_frame.pack(fill=tk.BOTH, expand=True, padx=4, pady=4)

            self.canvas = tk.Canvas(canvas_frame, bg="#0f0f17", highlightthickness=0)
            v_scroll = tk.Scrollbar(
                canvas_frame, orient=tk.VERTICAL, command=self.canvas.yview
            )
            h_scroll = tk.Scrollbar(
                canvas_frame, orient=tk.HORIZONTAL, command=self.canvas.xview
            )
            self.canvas.configure(
                yscrollcommand=v_scroll.set, xscrollcommand=h_scroll.set
            )

            v_scroll.pack(side=tk.RIGHT, fill=tk.Y)
            h_scroll.pack(side=tk.BOTTOM, fill=tk.X)
            self.canvas.pack(fill=tk.BOTH, expand=True)
            self.canvas.bind("<MouseWheel>", self._on_mousewheel)
            self.canvas.bind("<Button-4>", self._on_mousewheel)
            self.canvas.bind("<Button-5>", self._on_mousewheel)

            # ── Rechter paneel: invoervelden ──
            right = tk.Frame(paned, bg="#1e1e2e")
            paned.add(right, minsize=280)

            tk.Label(
                right,
                text="KENMERKEN",
                bg="#1e1e2e",
                fg="#89dceb",
                font=("Courier New", 11, "bold"),
            ).pack(pady=(20, 4), padx=20, anchor=tk.W)
            ttk.Separator(right).pack(fill=tk.X, padx=20, pady=(0, 12))

            self.entries = {}
            for feat in cfg.KENMERKEN:
                tk.Label(
                    right, text=feat, bg="#1e1e2e", fg="#bac2de", font=("Georgia", 10)
                ).pack(anchor=tk.W, padx=20, pady=(4, 1))

                if feat.lower() in ("opmerking", "notities", "notes", "beschrijving"):
                    frame = tk.Frame(right, bg="#1e1e2e")
                    frame.pack(fill=tk.X, padx=20, pady=(0, 6))
                    text_widget = tk.Text(
                        frame,
                        height=4,
                        font=("Courier New", 10),
                        bg="#313244",
                        fg="#cdd6f4",
                        insertbackground="#cdd6f4",
                        relief=tk.FLAT,
                        padx=6,
                        pady=4,
                    )
                    text_widget.pack(fill=tk.X)
                    self.entries[feat] = text_widget
                else:
                    entry = tk.Entry(
                        right,
                        font=("Courier New", 11),
                        bg="#313244",
                        fg="#cdd6f4",
                        insertbackground="#cdd6f4",
                        relief=tk.FLAT,
                    )
                    entry.pack(fill=tk.X, padx=20, pady=(0, 6))
                    entry.bind("<Return>", lambda e: self._save_and_next())
                    self.entries[feat] = entry

            # Knoppen onder de velden
            btn_frame = tk.Frame(right, bg="#1e1e2e")
            btn_frame.pack(fill=tk.X, padx=20, pady=16)

            tk.Button(
                btn_frame,
                text="✓  Opslaan & Volgende",
                command=self._save_and_next,
                bg="#a6e3a1",
                fg="#1e1e2e",
                font=("Georgia", 11, "bold"),
                relief=tk.FLAT,
                pady=8,
            ).pack(fill=tk.X, pady=(0, 6))

            tk.Button(
                btn_frame,
                text="↩  Overslaan",
                command=self._skip,
                bg="#45475a",
                fg="#cdd6f4",
                font=("Georgia", 10),
                relief=tk.FLAT,
                pady=6,
            ).pack(fill=tk.X)

            # Status onder
            self.status_bar = tk.Label(
                right,
                text="",
                bg="#181825",
                fg="#a6e3a1",
                font=("Courier New", 9),
                pady=4,
            )
            self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

            # Resultaten tabel
            tk.Label(
                right,
                text="OPGESLAGEN",
                bg="#1e1e2e",
                fg="#89dceb",
                font=("Courier New", 10, "bold"),
            ).pack(pady=(12, 2), padx=20, anchor=tk.W)

            tree_frame = tk.Frame(right, bg="#1e1e2e")
            tree_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 4))

            cols = ["bestand"] + cfg.KENMERKEN
            self.tree = ttk.Treeview(
                tree_frame, columns=cols, show="headings", height=6
            )
            style.configure(
                "Treeview",
                background="#313244",
                foreground="#cdd6f4",
                fieldbackground="#313244",
                font=("Courier New", 8),
            )
            style.configure(
                "Treeview.Heading",
                background="#45475a",
                foreground="#89b4fa",
                font=("Courier New", 8, "bold"),
            )

            for col in cols:
                self.tree.heading(col, text=col[:12])
                self.tree.column(col, width=80, anchor=tk.W)

            tree_scroll = tk.Scrollbar(
                tree_frame, orient=tk.VERTICAL, command=self.tree.yview
            )
            self.tree.configure(yscrollcommand=tree_scroll.set)
            tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)
            self.tree.pack(fill=tk.BOTH, expand=True)

            paned.paneconfigure(left, width=720)

        # ── Bestanden laden ────────────────────────

        def _open_folder(self):
            folder = filedialog.askdirectory(title="Kies een map met PDF's")
            if folder:
                files = sorted(Path(folder).glob("*.pdf"))
                self._load_file_list([str(f) for f in files])

        def _open_files(self):
            files = filedialog.askopenfilenames(
                title="Kies PDF bestanden", filetypes=[("PDF bestanden", "*.pdf")]
            )
            if files:
                self._load_file_list(list(files))

        def _load_file_list(self, files):
            self.pdf_files = files
            self.current_index = 0
            self._update_progress()
            if files:
                self._load_current_pdf()

        def _load_existing_csv(self):
            """Laad bestaande resultaten als het CSV-bestand al bestaat."""
            if os.path.exists(cfg.OUTPUT_CSV):
                try:
                    with open(OUTPUT_CSV, newline="", encoding="utf-8") as f:
                        reader = csv.DictReader(f)
                        for row in reader:
                            self.all_results.append(dict(row))
                            self.tree.insert(
                                "",
                                tk.END,
                                values=[
                                    row.get(c, "") for c in ["bestand"] + cfg.KENMERKEN
                                ],
                            )
                    self._set_status(
                        f"✓ {len(self.all_results)} bestaande rijen geladen"
                    )
                except Exception:
                    pass

        # ── PDF weergave ───────────────────────────

        def _load_current_pdf(self):
            if not self.pdf_files:
                return
            path = self.pdf_files[self.current_index]
            self.file_label.config(text=Path(path).name)
            try:
                if self.current_doc:
                    self.current_doc.close()
                self.current_doc = fitz.open(path)
                self.current_page = 0
                self._render_page()
                self._clear_entries()
                self._prefill_if_exists(Path(path).name)
            except Exception as e:
                messagebox.showerror("Fout", f"Kan PDF niet openen:\n{e}")

        def _render_page(self):
            if not self.current_doc:
                return
            page = self.current_doc[self.current_page]
            mat = fitz.Matrix(self.zoom, self.zoom)
            pix = page.get_pixmap(matrix=mat)
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            self.photo = ImageTk.PhotoImage(img)
            self.canvas.delete("all")
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.photo)
            self.canvas.configure(scrollregion=(0, 0, pix.width, pix.height))
            total = len(self.current_doc)
            self.page_label.config(text=f"Pagina {self.current_page + 1} / {total}")

        def _prev_page(self):
            if self.current_doc and self.current_page > 0:
                self.current_page -= 1
                self._render_page()

        def _next_page(self):
            if self.current_doc and self.current_page < len(self.current_doc) - 1:
                self.current_page += 1
                self._render_page()

        def _zoom(self, factor):
            self.zoom = max(0.5, min(4.0, self.zoom * factor))
            self._render_page()

        def _on_mousewheel(self, event):
            if event.num == 4 or event.delta > 0:
                self.canvas.yview_scroll(-1, "units")
            else:
                self.canvas.yview_scroll(1, "units")

        # ── Navigatie ──────────────────────────────

        def _prev_pdf(self):
            if self.current_index > 0:
                self.current_index -= 1
                self._update_progress()
                self._load_current_pdf()

        def _next_pdf(self):
            if self.current_index < len(self.pdf_files) - 1:
                self.current_index += 1
                self._update_progress()
                self._load_current_pdf()

        def _update_progress(self):
            if self.pdf_files:
                self.progress_label.config(
                    text=f"PDF {self.current_index + 1} van {len(self.pdf_files)}"
                )
            else:
                self.progress_label.config(text="Geen bestanden geladen")

        # ── Invoervelden ───────────────────────────

        def _clear_entries(self):
            for widget in self.entries.values():
                if isinstance(widget, tk.Text):
                    widget.delete("1.0", tk.END)
                else:
                    widget.delete(0, tk.END)

        def _prefill_if_exists(self, filename):
            """Vul velden in als dit bestand al eerder is opgeslagen."""
            for row in self.all_results:
                if row.get("bestand") == filename:
                    for feat in cfg.KENMERKEN:
                        val = row.get(feat, "")
                        w = self.entries[feat]
                        if isinstance(w, tk.Text):
                            w.insert("1.0", val)
                        else:
                            w.insert(0, val)
                    break

        def _get_entry_values(self):
            values = {}
            for feat, widget in self.entries.items():
                if isinstance(widget, tk.Text):
                    values[feat] = widget.get("1.0", tk.END).strip()
                else:
                    values[feat] = widget.get().strip()
            return values

        # ── Opslaan ────────────────────────────────

        def _save_and_next(self):
            if not self.pdf_files:
                messagebox.showwarning("Geen bestanden", "Laad eerst PDF-bestanden.")
                return

            filename = Path(self.pdf_files[self.current_index]).name
            values = self._get_entry_values()
            row = {"bestand": filename, **values}

            # Vervang bestaande rij of voeg toe
            existing = [r for r in self.all_results if r["bestand"] == filename]
            if existing:
                self.all_results = [
                    r for r in self.all_results if r["bestand"] != filename
                ]
                # Verwijder uit treeview
                for item in self.tree.get_children():
                    if self.tree.item(item)["values"][0] == filename:
                        self.tree.delete(item)
                        break

            self.all_results.append(row)
            self.tree.insert(
                "", tk.END, values=[row.get(c, "") for c in ["bestand"] + cfg.KENMERKEN]
            )

            self._auto_save()
            self._set_status(f"✓ Opgeslagen: {filename}")

            # Naar volgende
            if self.current_index < len(self.pdf_files) - 1:
                self.current_index += 1
                self._update_progress()
                self._load_current_pdf()
            else:
                messagebox.showinfo(
                    "Klaar! 🎉",
                    f"Alle {len(self.pdf_files)} PDF's verwerkt.\n"
                    f"Resultaten staan in: {OUTPUT_CSV}",
                )

        def _skip(self):
            """Sla dit bestand over zonder op te slaan."""
            if self.current_index < len(self.pdf_files) - 1:
                self.current_index += 1
                self._update_progress()
                self._load_current_pdf()

        def _auto_save(self):
            """Sla automatisch op na elke invoer."""
            self._write_csv()

        def _save_csv(self):
            self._write_csv()
            messagebox.showinfo(
                "Opgeslagen", f"CSV opgeslagen als:\n{os.path.abspath(OUTPUT_CSV)}"
            )

        def _write_csv(self):
            fieldnames = ["bestand"] + cfg.KENMERKEN
            with open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
                writer.writeheader()
                writer.writerows(self.all_results)

        def _set_status(self, msg):
            self.status_bar.config(text=msg)
            self.root.after(4000, lambda: self.status_bar.config(text=""))

    # ── Start ─────────────u─────────────────────────

    if __name__ == "__main__":
        root = tk.Tk()
        app = PDFReviewer(root)
        root.mainloop()

    # Behoort tot wat in de CSV wordt opgeslagen aan kenmerken ook een identificatie van
    # de PDF file?
    #
    # Ja, de bestandsnaam wordt altijd opgeslagen. In het CSV-bestand is de eerste
    # kolom "bestand" met de naam van het PDF-bestand (bijv. factuur_2024_001.pdf).
    # Wil je daarnaast ook het volledige pad bewaren? Dat kan handig zijn als je PDF's
    # uit verschillende mappen verwerkt.
