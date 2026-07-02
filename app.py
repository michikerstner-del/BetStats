import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# Initialisierung der Daten
if 'wetten' not in st.session_state:
    st.session_state.wetten = pd.DataFrame(columns=["Datum", "Einsatz", "Quote", "Status", "Bilanz"])

st.title("💸 Meine Wetten-Übersicht")

# --- EINGABE-BEREICH ---
with st.expander("Neue Wette hinzufügen"):
    with st.form("wette_form", clear_on_submit=True):
        einsatz = st.number_input("Einsatz (€)", min_value=0.0, step=0.1)
        quote = st.number_input("Quote", min_value=1.0, step=0.01)
        status = st.selectbox("Status", ["Gewonnen", "Verloren"])
        submit = st.form_submit_button("Wette speichern")

if submit:
    gewinn_verlust = (einsatz * quote) - einsatz if status == "Gewonnen" else -einsatz
    neue_wette = pd.DataFrame({
        "Datum": [datetime.now()], # Wir speichern echte Zeitstempel für die Filter
        "Einsatz": [einsatz],
        "Quote": [quote],
        "Status": [status],
        "Bilanz": [round(gewinn_verlust, 2)]
    })
    st.session_state.wetten = pd.concat([st.session_state.wetten, neue_wette], ignore_index=True)
    st.success("Wette gespeichert!")

# --- FILTER-BEREICH ---
st.sidebar.header("Filter & Ansichten")
ansicht = st.sidebar.selectbox("Zeitraum wählen", ["Gesamt", "Heute", "Letzte 7 Tage", "Aktueller Monat"])

df = st.session_state.wetten.copy()
if not df.empty:
    df['Datum'] = pd.to_datetime(df['Datum'])
    heute = datetime.now()

    if ansicht == "Heute":
        df = df[df['Datum'].dt.date == heute.date()]
    elif ansicht == "Letzte 7 Tage":
        df = df[df['Datum'] >= heute - timedelta(days=7)]
    elif ansicht == "Aktueller Monat":
        df = df[(df['Datum'].dt.month == heute.month) & (df['Datum'].dt.year == heute.year)]

    # --- AUSGABE ---
    st.subheader(f"Ansicht: {ansicht}")
    st.dataframe(df)
    st.metric("Gesamtbilanz", f"{df['Bilanz'].sum():.2f} €")
else:
    st.write("Noch keine Daten vorhanden.")
