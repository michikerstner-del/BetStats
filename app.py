import streamlit as st
import pandas as pd
from datetime import datetime
from streamlit_gsheets import GSheetsConnection  # <--- DIESE ZEILE HINZUFÜGEN

# Verbindung zu Google Sheets registrieren
conn = st.connection("gsheets", type=GSheetsConnection) # <--- 'type' geändert

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
    neue_wette = pd.DataFrame([{
        "Datum": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Einsatz": einsatz,
        "Quote": quote,
        "Status": status,
        "Bilanz": round(gewinn_verlust, 2)
    }])
    
    # In Google Sheet schreiben
    existing_data = conn.read()
    updated_df = pd.concat([existing_data, neue_wette], ignore_index=True)
    conn.update(data=updated_df)
    st.success("Wette in Google Sheets gespeichert!")

# --- ANZEIGE ---
st.subheader("Historie aus Google Sheets")
df = conn.read()
st.dataframe(df)
if not df.empty:
    st.metric("Gesamtbilanz", f"{df['Bilanz'].sum():.2f} €")
