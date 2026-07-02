import streamlit as st
import pandas as pd
import os
from datetime import datetime, timedelta

# Dateiname für die dauerhafte Speicherung
DATA_FILE = "wetten_daten.csv"

# Daten laden oder leeren DataFrame erstellen
if os.path.exists(DATA_FILE):
    df_data = pd.read_csv(DATA_FILE)
    df_data['Datum'] = pd.to_datetime(df_data['Datum'])
else:
    df_data = pd.DataFrame(columns=["Datum", "Einsatz", "Quote", "Status", "Bilanz"])

st.title("💸 Meine Wetten-Übersicht")

# --- EINGABE ---
with st.expander("Neue Wette hinzufügen"):
    with st.form("wette_form", clear_on_submit=True):
        einsatz = st.number_input("Einsatz (€)", min_value=0.0, step=0.1)
        quote = st.number_input("Quote", min_value=1.0, step=0.01)
        status = st.selectbox("Status", ["Gewonnen", "Verloren"])
        submit = st.form_submit_button("Wette speichern")

if submit:
    gewinn_verlust = (einsatz * quote) - einsatz if status == "Gewonnen" else -einsatz
    neue_wette = pd.DataFrame({
        "Datum": [datetime.now()],
        "Einsatz": [einsatz],
        "Quote": [quote],
        "Status": [status],
        "Bilanz": [round(gewinn_verlust, 2)]
    })
    
    # Daten zusammenführen und speichern
    df_data = pd.concat([df_data, neue_wette], ignore_index=True)
    df_data.to_csv(DATA_FILE, index=False)
    st.success("Wette dauerhaft gespeichert!")

# --- FILTER ---
st.sidebar.header("Filter & Ansichten")
ansicht = st.sidebar.selectbox("Zeitraum wählen", ["Gesamt", "Heute", "Letzte 7 Tage", "Aktueller Monat"])

df_filtered = df_data.copy()
if not df_filtered.empty:
    heute = datetime.now()
    if ansicht == "Heute":
        df_filtered = df_filtered[df_filtered['Datum'].dt.date == heute.date()]
    elif ansicht == "Letzte 7 Tage":
        df_filtered = df_filtered[df_filtered['Datum'] >= heute - timedelta(days=7)]
    elif ansicht == "Aktueller Monat":
        df_filtered = df_filtered[(df_filtered['Datum'].dt.month == heute.month) & (df_filtered['Datum'].dt.year == heute.year)]

    st.subheader(f"Ansicht: {ansicht}")
    st.dataframe(df_filtered)
    st.metric("Gesamtbilanz", f"{df_filtered['Bilanz'].sum():.2f} €")
else:
    st.write("Noch keine Daten vorhanden.")
