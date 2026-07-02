import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime

# Authentifizierung
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
creds = Credentials.from_service_account_file("google-credentials.json", scopes=SCOPES)
client = gspread.authorize(creds)

# Sheet öffnen (ID aus URL)
SHEET_ID = "HIER_DEINE_SHEET_ID_EINFÜGEN"
sh = client.open_by_key(SHEET_ID)
worksheet = sh.sheet1

st.title("💸 Meine Wetten-Übersicht")

# --- EINGABE ---
with st.form("wette_form", clear_on_submit=True):
    einsatz = st.number_input("Einsatz (€)", min_value=0.0, step=0.1)
    quote = st.number_input("Quote", min_value=1.0, step=0.01)
    status = st.selectbox("Status", ["Gewonnen", "Verloren"])
    submit = st.form_submit_button("Wette speichern")

if submit:
    gewinn_verlust = (einsatz * quote) - einsatz if status == "Gewonnen" else -einsatz
    row = [datetime.now().strftime("%d.%m.%Y %H:%M"), einsatz, quote, status, round(gewinn_verlust, 2)]
    worksheet.append_row(row) # Der direkte Befehl zum Anhängen einer Zeile
    st.success("Wette gespeichert!")

# --- ANZEIGE ---
data = worksheet.get_all_records()
df = pd.DataFrame(data)
st.dataframe(df)

if not df.empty:
    st.metric("Gesamtbilanz", f"{df['Bilanz'].sum():.2f} €")
