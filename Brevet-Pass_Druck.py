#!/usr/bin/env python3
"""
PDF-Verschränker (Kommandozeilen-Version, kein tkinter nötig)
================================================================

Fügt zwei PDF-Dateien seitenweise ineinander:
Seite 1 von PDF 1, Seite 1 von PDF 2, Seite 2 von PDF 1, Seite 2 von PDF 2, usw.

Haben die beiden PDFs unterschiedlich viele Seiten, werden die restlichen
Seiten der längeren Datei am Ende angehängt.

Voraussetzung (einmalig installieren):
    pip install pypdf

Verwendung:
    python pdf_interleave_merger_cli.py datei1.pdf datei2.pdf ausgabe.pdf

Ohne Angabe von Dateien fragt das Programm interaktiv danach.
"""

import argparse
import os
import sys

try:
    from pypdf import PdfReader, PdfWriter
except ImportError:
    raise SystemExit(
        "Das Modul 'pypdf' wird benötigt.\n"
        "Bitte installieren mit:  pip install pypdf"
    )


def merge_interleaved(pdf_path_1: str, pdf_path_2: str, output_path: str) -> int:
    """
    Fügt pdf_path_1 und pdf_path_2 seitenweise abwechselnd zusammen:
    nach jeder Seite aus Datei 1 wird eine Seite aus Datei 2 eingefügt,
    und speichert das Ergebnis unter output_path.

    Hat Datei 2 weniger Seiten als Datei 1, werden ihre Seiten zyklisch
    wiederholt (z.B. wird bei einer einzelnen Seite in Datei 2 genau diese
    Seite nach jeder Seite von Datei 1 eingefügt). Hat Datei 2 mehr Seiten
    als Datei 1, werden die überzähligen Seiten am Ende angehängt.

    Gibt die Gesamtzahl der Seiten der neuen Datei zurück.
    """
    reader_1 = PdfReader(pdf_path_1)
    reader_2 = PdfReader(pdf_path_2)

    pages_1 = reader_1.pages
    pages_2 = reader_2.pages

    if len(pages_2) == 0:
        raise ValueError("PDF-Datei 2 enthält keine Seiten.")

    writer = PdfWriter()

    for i in range(len(pages_1)):
        writer.add_page(pages_1[i])
        writer.add_page(pages_2[i % len(pages_2)])

    # Falls PDF 2 mehr Seiten hat als PDF 1: Rest am Ende anhängen.
    if len(pages_2) > len(pages_1):
        for i in range(len(pages_1), len(pages_2)):
            writer.add_page(pages_2[i])

    with open(output_path, "wb") as f:
        writer.write(f)

    return len(writer.pages)


def ask_for_path(prompt: str, must_exist: bool = True) -> str:
    while True:
        path = input(prompt).strip().strip('"')
        if must_exist and not os.path.isfile(path):
            print(f"  -> Datei nicht gefunden: {path}")
            continue
        return path


def main():
    parser = argparse.ArgumentParser(
        description="Fügt zwei PDF-Dateien seitenweise abwechselnd zusammen."
    )
    parser.add_argument("pdf1", nargs="?", help="Erste PDF-Datei")
    parser.add_argument("pdf2", nargs="?", help="Zweite PDF-Datei")
    parser.add_argument("output", nargs="?", help="Ziel-Datei für das Ergebnis")
    args = parser.parse_args()

    pdf1 = args.pdf1 or ask_for_path("Pfad zu PDF-Datei 1: ")
    pdf2 = args.pdf2 or ask_for_path("Pfad zu PDF-Datei 2: ")
    output = args.output or ask_for_path(
        "Pfad für die neue PDF-Datei (z.B. ergebnis.pdf): ", must_exist=False
    )

    for path in (pdf1, pdf2):
        if not os.path.isfile(path):
            print(f"Fehler: Datei nicht gefunden: {path}")
            sys.exit(1)

    try:
        total_pages = merge_interleaved(pdf1, pdf2, output)
    except Exception as exc:  # noqa: BLE001 - dem Nutzer die genaue Ursache zeigen
        print(f"Fehler beim Zusammenfügen: {exc}")
        sys.exit(1)

    print(f"Fertig: {output} wurde mit {total_pages} Seiten gespeichert.")


if __name__ == "__main__":
    main()
