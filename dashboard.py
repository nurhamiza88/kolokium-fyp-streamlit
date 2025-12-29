import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(
    page_title="Dashboard Keputusan Kolokium FYP",
    layout="wide"
)

st.title("📊 Dashboard Keputusan Kolokium Projek Tahun Akhir")
# =====================
# GOOGLE SHEET (RUMUSAN AKHIR)
# =====================
SHEET_ID = "14YrOAWbC0M4Cd2Vg02TEJ_xObOZaMuHEcDwpWM_cvfg"
GID_RUMUSAN = "PASTE_GID_DI_SINI"

CSV_URL = (
    f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/"
    f"export?format=csv&gid={GID_RUMUSAN}"
)

@st.cache_data
def load_rumusan():
    return pd.read_csv(CSV_URL)

