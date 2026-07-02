import streamlit as st
import pandas as pd
from datetime import datetime

# Wir speichern die Daten in einer 'Session State' Liste
# Solange die App im Browser geöffnet bleibt, bleiben die Daten erhalten
if 'wetten' not in st.session_state:
    st.session_state.wetten = pd.DataFrame(columns=["Datum", "Einsatz", "Quote", "Status", "Bilanz"])

st.title("💸 Meine Wetten-Übersicht")

with st.form("wette_form", clear_on_submit=True):
    einsatz = st.number_input("Einsatz (€)", min_value=0.0, step=0.1)
    quote = st.number_input("Quote", min_value=1.0, step=0.01)
    status = st.selectbox("Status", ["Gewonnen", "Verloren"])
    submit = st.form_submit_button("Wette speichern")

if submit:
    gewinn_verlust = (einsatz * quote) - einsatz if status == "Gewonnen" else -einsatz
    neue_wette = pd.DataFrame({
        "Datum": [datetime.now().strftime("%d.%m.%Y %H:%M")],
        "Einsatz": [einsatz],
        "Quote": [quote],
        "Status": [status],
        "Bilanz": [round(gewinn_verlust, 2)]
    })
    st.session_state.wetten = pd.concat([st.session_state.wetten, neue_wette], ignore_index=True)
    st.success("Wette hinzugefügt!")

st.subheader("Deine Historie")
st.dataframe(st.session_state.wetten)

# Anzeige der Bilanz
if not st.session_state.wetten.empty:
    st.write(f"Gesamtbilanz: {st.session_state.wetten['Bilanz'].sum()} €")
