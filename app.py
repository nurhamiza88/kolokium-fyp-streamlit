import streamlit as st
import pandas as pd
import requests

# =====================
# CONFIG
# =====================
st.set_page_config(
    page_title="Penilaian Juri Kolokium FYP",
    layout="wide"
)

st.title("📋 Sistem Penilaian Juri Kolokium Projek Tahun Akhir")

# =====================
# GOOGLE SHEET (CSV)
# =====================

# Senarai Juri
CSV_JURI_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSlsLSz46lRS0ncB4idH-6Xn_pGWb5jXXKsZdwKygizIHDrkjbjvzB3vzD9qxV06_2FTMLGxunuZUpy/pub?gid=1188865026&single=true&output=csv"

# Agihan Juri → Kod Poster
CSV_AGIHAN_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSlsLSz46lRS0ncB4idH-6Xn_pGWb5jXXKsZdwKygizIHDrkjbjvzB3vzD9qxV06_2FTMLGxunuZUpy/pub?gid=381457985&single=true&output=csv"

@st.cache_data
def get_juri_from_sheet():
    df = pd.read_csv(CSV_JURI_URL)
    df.columns = df.columns.str.strip()
    return df["Nama Juri"].dropna().unique().tolist()

@st.cache_data
def get_agihan_juri():
    df = pd.read_csv(CSV_AGIHAN_URL)
    df.columns = df.columns.str.strip()
    df["Nama Juri"] = df["Nama Juri"].str.strip()
    df["Kod Poster"] = df["Kod Poster"].str.strip()
    return df

# =====================
# GOOGLE FORM (SUBMIT)
# =====================
FORM_URL = "https://docs.google.com/forms/d/e/1K6tBmnv7JBX_TCTIhCg3UxTKuGLbxbd5UYf4N4lFLmM/formResponse"

FORM_MAPPING = {
    "nama_juri": "entry.1101626450",
    "kod_poster": "entry.1011436319",
    "jenis_borang": "entry.2043825743",
    "jumlah": "entry.2012388652",
    "item": [
        "entry.994184812",
        "entry.1025336879",
        "entry.1540256323",
        "entry.90543189",
        "entry.1040594050",
        "entry.1209343348",
        "entry.1535785034",
        "entry.895520193",
        "entry.964162367",
        "entry.200002443"
    ]
}

# =====================
# SESSION STATE
# =====================
if "nama_juri" not in st.session_state:
    st.session_state.nama_juri = None

# =====================
# MAKLUMAT JURI
# =====================
st.subheader("Maklumat Juri")

try:
    SENARAI_JURI = get_juri_from_sheet()
except Exception:
    st.error("❌ Gagal tarik senarai juri dari Google Sheet.")
    st.stop()

if st.session_state.nama_juri is None:
    nama = st.selectbox(
        "Pilih Nama Juri",
        ["-- Pilih --"] + SENARAI_JURI
    )
    if nama != "-- Pilih --":
        st.session_state.nama_juri = nama
        st.success(f"Nama juri disimpan: {nama}")
else:
    st.info(f"👤 Juri: {st.session_state.nama_juri}")

# =====================
# MAKLUMAT POSTER (IKUT AGIHAN JURI)
# =====================
st.subheader("Maklumat Poster")

df_agihan = get_agihan_juri()

nama_juri = st.session_state.nama_juri
if nama_juri is None:
    st.stop()

nama_juri = nama_juri.strip()

kod_dibenarkan = (
    df_agihan[
        df_agihan["Nama Juri"].str.lower() == nama_juri.lower()
    ]["Kod Poster"]
    .dropna()
    .unique()
    .tolist()
)

if not kod_dibenarkan:
    st.warning("⚠️ Tiada kod poster diagihkan kepada juri ini.")
    st.stop()

kod_poster = st.selectbox(
    "Pilih Kod Poster (Diagihkan kepada anda)",
    kod_dibenarkan
)

# =====================
# RUBRIK PENILAIAN
# =====================
if kod_poster.startswith("PRODUK") or kod_poster.startswith("PENDIDIKAN"):
    jenis_borang = "PRODUK / PENDIDIKAN"
    soalan = [
        "Reka bentuk poster jelas dan menarik.",
        "Isi kandungan poster lengkap merangkumi aspek utama kajian.",
        "Poster menunjukkan elemen inovatif.",
        "Produk atau hasil kajian menunjukkan keaslian.",
        "Produk atau hasil kajian relevan.",
        "Produk atau instrumen kajian melalui penilaian asas.",
        "Penyampaian yakin dan bertenaga.",
        "Kajian diterangkan secara sistematik.",
        "Komunikasi lancar.",
        "Menjawab soalan dengan kritikal."
    ]
else:
    jenis_borang = "STATISTIK & MATEMATIK GUNAAN"
    soalan = [
        "Reka bentuk poster menyokong kefahaman kajian.",
        "Isi kandungan poster lengkap.",
        "Poster menunjukkan elemen inovatif.",
        "Kaedah matematik/statistik sesuai.",
        "Analisis data tepat.",
        "Kajian menyumbang kepada ilmu.",
        "Penyampaian yakin.",
        "Kajian sistematik.",
        "Komunikasi lancar.",
        "Jawapan kritikal."
    ]

# =====================
# BORANG PENILAIAN
# =====================
st.divider()
st.subheader(f"Instrumen Penilaian ({jenis_borang})")
st.caption("Skala: 1 = Tidak Setuju | 2 = Kurang Setuju | 3 = Setuju | 4 = Sangat Setuju")

markah = []

for i, item in enumerate(soalan, start=1):
    skor = st.radio(
        f"{i}. {item}",
        [1, 2, 3, 4],
        horizontal=True,
        key=f"item_{i}"
    )
    markah.append(skor)

jumlah = sum(markah)
st.success(f"✅ Jumlah Markah: {jumlah} / 40")

# =====================
# SUBMIT KE GOOGLE FORM
# =====================
if st.button("📤 Submit Penilaian"):
    payload = {
        FORM_MAPPING["nama_juri"]: nama_juri,
        FORM_MAPPING["kod_poster"]: kod_poster,
        FORM_MAPPING["jenis_borang"]: jenis_borang,
        FORM_MAPPING["jumlah"]: jumlah,
    }

    for i, skor in enumerate(markah):
        payload[FORM_MAPPING["item"][i]] = skor

    response = req
