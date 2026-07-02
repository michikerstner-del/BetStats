import streamlit as st
import pandas as pd
from datetime import datetime
from googleapiclient.discovery import build
from google.oauth2 import service_account

# WICHTIG: Hier musst du die URL deiner Google Sheet einfügen!
SHEET_URL = "HIER_DEINE_GOOGLE_SHEET_URL_EINTRAGEN"

st.title("💸 Meine Wetten-Übersicht")

with st.form("wette_form"):
    einsatz = st.number_input("Einsatz (€)", min_value=0.0, step=0.1)
    quote = st.number_input("Quote", min_value=1.0, step=0.01)
    status = st.selectbox("Status", ["Gewonnen", "Verloren"])
    submit = st.form_submit_button("Wette speichern")

if submit:
    # Berechnung
    gewinn_verlust = (einsatz * quote) - einsatz if status == "Gewonnen" else -einsatz
    neue_zeile = [str(datetime.now()), einsatz, quote, status, round(gewinn_verlust, 2)]
    
    # Hier werden wir später den Google Sheets Code einfügen
    st.write("Speichern in Google Sheets folgt im nächsten Schritt!")
    st.success("Wette 'simuliert' gespeichert!")
