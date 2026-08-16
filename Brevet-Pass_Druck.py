"""
PDF-Verschränker – Streamlit-Version
=====================================

Fügt zwei hochgeladene PDF-Dateien seitenweise ineinander:
Seite 1 von PDF 1, Seite 1 von PDF 2, Seite 2 von PDF 1, Seite 2 von PDF 2, usw.

Haben die beiden PDFs unterschiedlich viele Seiten, werden die restlichen
Seiten der längeren Datei am Ende angehängt.

Voraussetzungen (in requirements.txt):
    streamlit
    pypdf

Lokal starten:
    streamlit run streamlit_pdf_interleave_app.py

Für Streamlit Cloud: dieses Skript als Haupt-App-Datei verwenden und eine
requirements.txt mit den beiden obigen Zeilen ins Repo legen.
KEIN tkinter verwenden – das funktioniert auf einem Server ohne Bildschirm nicht.
"""

from io import BytesIO

import streamlit as st
from pypdf import PdfReader, PdfWriter


def merge_interleaved(pdf_bytes_1: bytes, pdf_bytes_2: bytes) -> tuple[bytes, int]:
    """
    Fügt zwei PDFs (als Bytes) seitenweise abwechselnd zusammen
    (erst Seite aus Datei 1, dann die zugehörige Seite aus Datei 2).

    Sind die Dateien unterschiedlich lang, werden die überzähligen
    Seiten der längeren Datei am Ende angehängt.

    Gibt (Ergebnis-PDF als Bytes, Gesamtseitenzahl) zurück.
    """
    reader_1 = PdfReader(BytesIO(pdf_bytes_1))
    reader_2 = PdfReader(BytesIO(pdf_bytes_2))

    pages_1 = reader_1.pages
    pages_2 = reader_2.pages

    writer = PdfWriter()

    max_len = max(len(pages_1), len(pages_2))
    for i in range(max_len):
        if i < len(pages_1):
            writer.add_page(pages_1[i])
        if i < len(pages_2):
            writer.add_page(pages_2[i])

    output = BytesIO()
    writer.write(output)
    return output.getvalue(), len(writer.pages)


st.set_page_config(page_title="PDF-Verschränker", page_icon="📄")

st.title("📄 PDF-Verschränker")
st.write(
    "Fügt nach jeder Seite von PDF 1 die passende Seite von PDF 2 ein "
    "(Seite 1, Seite 1, Seite 2, Seite 2, …)."
)

col1, col2 = st.columns(2)
with col1:
    file_1 = st.file_uploader("PDF-Datei 1", type="pdf", key="pdf1")
with col2:
    file_2 = st.file_uploader("PDF-Datei 2", type="pdf", key="pdf2")

if file_1 and file_2:
    if st.button("Zusammenfügen", type="primary"):
        try:
            result_bytes, total_pages = merge_interleaved(
                file_1.getvalue(), file_2.getvalue()
            )
        except Exception as exc:  # noqa: BLE001 - Fehlerursache dem Nutzer zeigen
            st.error(f"Fehler beim Zusammenfügen: {exc}")
        else:
            st.success(f"Fertig – die neue PDF-Datei hat {total_pages} Seiten.")
            st.download_button(
                label="Ergebnis-PDF herunterladen",
                data=result_bytes,
                file_name="zusammengefuehrt.pdf",
                mime="application/pdf",
            )
else:
    st.info("Bitte beide PDF-Dateien oben auswählen.")
