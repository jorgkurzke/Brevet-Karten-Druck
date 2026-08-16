import streamlit as st
from pypdf import PdfReader, PdfWriter
import io

st.set_page_config(page_title="Brevet-Pass Druck", layout="centered")

st.title("📄 Brevet-Pass PDF Generator")

st.write("Lade zwei PDF-Dateien hoch:")
st.write("1️⃣ Die Haupt-PDF-Datei (mit den zu druckenden Seiten)")
st.write("2️⃣ Die Einlege-PDF-Datei mit **nur einer Seite**, die zwischen jede Seite der Haupt-PDF eingefügt wird")

uploaded_main = st.file_uploader("Haupt-PDF-Datei hochladen", type="pdf")
uploaded_insert = st.file_uploader("Einlege-PDF-Datei hochladen (nur 1 Seite)", type="pdf")

if uploaded_main and uploaded_insert:
    main_reader = PdfReader(uploaded_main)
    insert_reader = PdfReader(uploaded_insert)

    if len(insert_reader.pages) != 1:
        st.error("Die Einlege-PDF darf nur eine Seite enthalten.")
    else:
        writer = PdfWriter()
        insert_page = insert_reader.pages[0]

        for page in main_reader.pages:
            writer.add_page(page)
            writer.add_page(insert_page)

        output_pdf = io.BytesIO()
        writer.write(output_pdf)
        output_pdf.seek(0)

        st.download_button(
            label="📥 download PDF",
            data=output_pdf,
            file_name="Brevet-Pass_final_gedruckt.pdf",
            mime="application/pdf",
            key="download_button",
        )

        st.write("Streamlit hat die PDF-Datei erfolgreich erstellt.")

        st.button(
            "🔁 Neue PDF erstellen",
            on_click=lambda: st.session_state.clear(),
        )
