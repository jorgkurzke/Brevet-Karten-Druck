#!/usr/bin/env python3
"""
PDF-Verschränker
================

Fügt zwei PDF-Dateien seitenweise ineinander:
Seite 1 von PDF 1, Seite 1 von PDF 2, Seite 2 von PDF 1, Seite 2 von PDF 2, usw.

Haben die beiden PDFs unterschiedlich viele Seiten, werden die restlichen
Seiten der längeren Datei am Ende angehängt.

Voraussetzungen (einmalig installieren):
    pip install pypdf

Start:
    python pdf_interleave_merger.py
"""

import tkinter as tk
from tkinter import filedialog, messagebox
import os

try:
    from pypdf import PdfReader, PdfWriter
except ImportError:
    raise SystemExit(
        "Das Modul 'pypdf' wird benötigt.\n"
        "Bitte installieren mit:  pip install pypdf"
    )


def merge_interleaved(pdf_path_1: str, pdf_path_2: str, output_path: str) -> int:
    """
    Fügt pdf_path_1 und pdf_path_2 seitenweise abwechselnd zusammen
    (erst Seite aus Datei 1, dann die zugehörige Seite aus Datei 2)
    und speichert das Ergebnis unter output_path.

    Sind die Dateien unterschiedlich lang, werden die überzähligen
    Seiten der längeren Datei am Ende angehängt.

    Gibt die Gesamtzahl der Seiten der neuen Datei zurück.
    """
    reader_1 = PdfReader(pdf_path_1)
    reader_2 = PdfReader(pdf_path_2)

    pages_1 = reader_1.pages
    pages_2 = reader_2.pages

    writer = PdfWriter()

    max_len = max(len(pages_1), len(pages_2))
    for i in range(max_len):
        if i < len(pages_1):
            writer.add_page(pages_1[i])
        if i < len(pages_2):
            writer.add_page(pages_2[i])

    with open(output_path, "wb") as f:
        writer.write(f)

    return len(writer.pages)


class PdfMergerApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("PDF-Verschränker")
        self.root.resizable(False, False)

        self.path_1 = tk.StringVar()
        self.path_2 = tk.StringVar()

        padding = {"padx": 10, "pady": 6}

        tk.Label(
            root,
            text="Fügt nach jeder Seite von PDF 1 die passende Seite von PDF 2 ein.",
            wraplength=420,
            justify="left",
        ).grid(row=0, column=0, columnspan=3, sticky="w", **padding)

        # PDF 1
        tk.Label(root, text="PDF-Datei 1:").grid(row=1, column=0, sticky="e", **padding)
        tk.Entry(root, textvariable=self.path_1, width=45, state="readonly").grid(
            row=1, column=1, **padding
        )
        tk.Button(root, text="Durchsuchen…", command=self.choose_file_1).grid(
            row=1, column=2, **padding
        )

        # PDF 2
        tk.Label(root, text="PDF-Datei 2:").grid(row=2, column=0, sticky="e", **padding)
        tk.Entry(root, textvariable=self.path_2, width=45, state="readonly").grid(
            row=2, column=1, **padding
        )
        tk.Button(root, text="Durchsuchen…", command=self.choose_file_2).grid(
            row=2, column=2, **padding
        )

        # Aktion
        tk.Button(
            root,
            text="Zusammenfügen und speichern…",
            command=self.run_merge,
            bg="#2e7d32",
            fg="white",
        ).grid(row=3, column=0, columnspan=3, pady=(14, 12))

    def choose_file_1(self):
        path = filedialog.askopenfilename(
            title="PDF-Datei 1 auswählen", filetypes=[("PDF-Dateien", "*.pdf")]
        )
        if path:
            self.path_1.set(path)

    def choose_file_2(self):
        path = filedialog.askopenfilename(
            title="PDF-Datei 2 auswählen", filetypes=[("PDF-Dateien", "*.pdf")]
        )
        if path:
            self.path_2.set(path)

    def run_merge(self):
        p1 = self.path_1.get()
        p2 = self.path_2.get()

        if not p1 or not p2:
            messagebox.showwarning(
                "Fehlende Auswahl", "Bitte zuerst beide PDF-Dateien auswählen."
            )
            return

        if not os.path.isfile(p1) or not os.path.isfile(p2):
            messagebox.showerror("Fehler", "Eine der ausgewählten Dateien wurde nicht gefunden.")
            return

        output_path = filedialog.asksaveasfilename(
            title="Neue PDF-Datei speichern unter…",
            defaultextension=".pdf",
            filetypes=[("PDF-Dateien", "*.pdf")],
            initialfile="zusammengefuehrt.pdf",
        )
        if not output_path:
            return  # Abbruch durch Nutzer

        try:
            total_pages = merge_interleaved(p1, p2, output_path)
        except Exception as exc:  # noqa: BLE001 - dem Nutzer die genaue Ursache zeigen
            messagebox.showerror("Fehler beim Zusammenfügen", str(exc))
            return

        messagebox.showinfo(
            "Fertig",
            f"Die neue PDF-Datei mit {total_pages} Seiten wurde gespeichert unter:\n{output_path}",
        )


def main():
    root = tk.Tk()
    PdfMergerApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
