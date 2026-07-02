import streamlit as st
import pandas as pd
import os
from datetime import datetime

# Dateiname für die Speicherung
DATA_FILE = "wetten.csv"

# Überschrift
st.title("💸 Meine Wetten-Übersicht")

# Formular für die Eingabe
with st.form("wette_form"):
    einsatz = st.number_input("Einsatz (€)", min_value=0.0, step=0.1)
    quote = st.number_input("Quote", min_value=1.0, step=0.01)
    status = st.selectbox("Status", ["Gewonnen", "Verloren"])
    submit = st.form_submit_button("Wette speichern")

if submit:
    # Daten zusammenstellen
    datum = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    gewinn_verlust = (einsatz * quote) - einsatz if status == "Gewonnen" else -einsatz
    
    neue_wette = pd.DataFrame({
        "Datum": [datum],
        "Einsatz": [einsatz],
        "Quote": [quote],
        "Status": [status],
        "Bilanz": [round(gewinn_verlust, 2)]
    })
    
    # In CSV speichern
    if os.path.exists(DATA_FILE):
        neue_wette.to_csv(DATA_FILE, mode='a', header=False, index=False)
    else:
        neue_wette.to_csv(DATA_FILE, index=False)
    
    st.success("Wette erfolgreich gespeichert!")

# Daten anzeigen
if os.path.exists(DATA_FILE):
    df = pd.read_csv(DATA_FILE)
    st.subheader("Deine Historie")
    st.dataframe(df)
else:
    st.write("Noch keine Wetten erfasst.")
