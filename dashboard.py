import streamlit as st
import pandas as pd
from datetime import datetime

# =====================
# CONFIG
# =====================
st.set_page_config(
    page_title="Dashboard Keputusan Kolokium FYP",
    layout="wide"
)

st.title("📊 Dashboard Keputusan Kolokium Projek Tahun Akhir")

st.info(
    "📌 Sekiranya penilaian dihantar lebih daripada sekali oleh juri yang sama "
    "bagi poster yang sama, hanya penilaian TERKINI akan diambil kira "
    "dalam pengiraan markah."
)

# =====================
# GOOGLE SHEET CSV (PUBLISH TO WEB)
# =====================
CSV_URL = (
    "https://docs.google.com/spreadsheets/d/e/"
    "2PACX-1vSmxI1CuK3pVwsVlHtyrsJ1yLxyPzZmpa_eX3daieYJPsBt7_POD9-Iu4FZb9x3NQjMxdJAoH52_0sv"
    "/pub?gid=694659483&single=true&output=csv"
)

@st.cache_data
def load_data():
    df = pd.read_csv(CSV_URL)
    df.columns = [c.strip() for c in df.columns]
    return df

# =====================
# LOAD DATA
# =====================
try:
    df = load_data()
except Exception:
    st.error("❌ Gagal memuatkan data dari Google Sheet.")
    st.stop()

# Andaian kolum:
# Kod Poster | Jumlah Markah | Bilangan Juri

# =====================
# TAMBAH KATEGORI POSTER
# =====================
def kategori_poster(kod):
    kod = str(kod)
    if kod.startswith("PRODUK"):
        return "Produk"
    elif kod.startswith("PENDIDIKAN"):
        return "Pendidikan"
    else:
        return "Statistik / Matematik"

df["Kategori"] = df["Kod Poster"].apply(kategori_poster)

# =====================
# RINGKASAN KESELURUHAN
# =====================
st.subheader("📌 Ringkasan Keseluruhan")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Jumlah Poster Dinilai", df["Kod Poster"].nunique())

with col2:
    st.metric(
        "Purata Jumlah Markah (2 Juri)",
        f"{df['Jumlah Markah'].mean():.2f} / 80"
    )

with col3:
    st.metric(
        "Poster Lengk
