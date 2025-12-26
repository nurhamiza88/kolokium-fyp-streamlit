import streamlit as st
import pandas as pd
import requests
from datetime import datetime

# =====================
# CONFIG
# =====================
st.set_page_config(
    page_title="Penilaian Juri Kolokium FYP",
    layout="wide"
)

st.title("📋 Sistem Penilaian Juri Kolokium Projek Tahun Akhir")

# =====================
# GOOGLE SHEET CSV
# =====================
CSV_JURI_URL = (
    "https://docs.google.com/spreadsheets/d/e/"
    "2PACX-1vSlsLSz46lRS0ncB4idH-6Xn_pGWb5jXXKsZdwKygizIHDrkjbjvzB3vzD9qxV06_2FTMLGxunuZUpy"
    "/pub?gid=1188865026&single=true&output=csv"
)

CSV_AGIHAN_URL = (
    "https://docs.google.com/spreadsheets/d/e/"
    "2PACX-1vSlsLSz46lRS0ncB4idH-6Xn_pGWb5jXXKsZdwKygizIHDrkjbjvzB3vzD9qxV06_2FTMLGxunuZUpy"
    "/pub?gid=381457985&single=true&output=csv"
)

# =====================
# GOOGLE FORM
# =====================
FORM_URL = (
    "https://docs.google.com/forms/d/e/"
    "1FAIpQLSdacWjlgA6fyQYvstqN0e792nzIowM6r4ceqOnVt67WgRWTfg"
    "/formResponse"
)

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
# LOAD DATA (CSV)
# =====================
@st.cache_data
def load_juri():
    df = pd.read_csv(CSV_JURI_URL)
    return df["NAMA JURI"].dropna().tolist()

@st.cache_data
def load_agihan():
    return pd.read_csv(CSV_AGIHAN_URL)

# =====================
# SESSION STATE
# =====================
if "nama_juri" not in st.session_state:
    st.session_state.nama_juri = None

# =====================
# PILIH JURI
# =====================
st.subheader("Maklumat Juri")

try:
    SENARAI_JURI = load_juri()
except Exception:
    st.error("❌ Gagal tarik senarai juri.")
    st.stop()

if st.session_state.nama_juri is None:
    nama = st.selectbox("Pilih Nama Juri", ["-- Pilih --"] + SENARAI_JURI)
    if nama != "-- Pilih --":
        st.session_state.nama_juri = nama
        st.success(f"Nama juri disimpan: {nama}")
else:
    st.info(f"👤 Juri: {st.session_state.nama_juri}")

# =====================
# PILIH KOD POSTER (IKUT AGIHAN)
# =====================
st.subheader("Maklumat Poster")

df_agihan = load_agihan()

kod_dibenarkan = df_agihan[
    df_agihan["Nama Juri"] == st.session_state.nama_juri
]["Kod Poster"].dropna().unique().tolist()

if not kod_dibenarkan:
    st.warning("⚠️ Tiada kod poster diagihkan kepada juri ini.")
    st.stop()

kod_poster = st.selectbox("Pilih Kod Poster", kod_dibenarkan)

# =====================
# RUBRIK
# =====================
if kod_poster.startswith("PRODUK") or kod_poster.startswith("PENDIDIKAN"):
    jenis_borang = "PRODUK / PENDIDIKAN"
    soalan = [
        "Reka bentuk poster jelas, menarik dan penggunaan AI menyokong kefahaman kajian (contoh: visualisasi data, infografik, atau sokongan analisis).",
        "Isi kandungan poster dinyatakan dengan tepat dan merangkumi 11 aspek (tajuk,abstrak, pernyataan masalah, objektif /soalan kajian, rekabentuk, populasi/sampel/Teknik pensampelan, instrumen, analisis data, dapatan, kesimpulan, implikasi)",
        "Poster menunjukkan elemen inovatif yang bersesuaian dengan jenis kajian.",
        "Produk atau hasil kajian menunjukkan elemen keaslian atau penambahbaikan bermakna terhadap amalan sedia ada.",
        "Produk atau hasil kajian relevan dan berpotensi membantu menyelesaikan masalah yang dikenal pasti.",
        "Produk atau instrumen kajian telah melalui penilaian asas (contoh: kesahan kandungan, kebolehgunaan awal) dan disertakan dokumentasi sokongan (contoh: draf artikel/laporan).",
        "Penyampaian adalah yakin dan bertenaga.",
        "Kajian diterangkan secara sistematik.",
        "Komunikasi lancar tanpa verbiage.",
        "Berupaya menjawab soalan dan berhujah dengan rasional, kritikal dan bernas."
    ]
else:
    jenis_borang = "STATISTIK & MATEMATIK GUNAAN"
    soalan = [
        "Reka bentuk poster jelas, menarik dan penggunaan AI menyokong kefahaman kajian (contoh: visualisasi data, infografik, atau sokongan analisis).",
        "Isi kandungan poster dinyatakan dengan tepat dan merangkumi 10 aspek (tajuk, abstrak, pernyataan masalah, objektif/soalan kajian, penjelasan teknik/kaedah matematik/statistik, analisis data, dapatan kajian, kesimpulan, implikasi dan rujukan.)",
        "Poster menunjukkan elemen inovatif yang bersesuaian dengan jenis kajian.",
        "Pemilihan dan aplikasi kaedah matematik/statistik serta ketepatan analisis data dalam menjawab objektif kajian.",
        "Persembahan hasil analisis data dalam bentuk jadual, graf atau rajah adalah tepat dan bersesuaian dengan objektif kajian.",
        "Penyelidikan memberikan sumbangan yang bermakna kepada body of knowledge dalam bidang berkaitan, menunjukkan kesinambungan kajian yang jelas, serta disokong dengan penyediaan draf artikel.",
        "Penyampaian adalah yakin dan bertenaga.",
        "Kajian diterangkan secara sistematik.",
        "Komunikasi lancar tanpa verbiage.",
        "Berupaya menjawab soalan dan berhujah dengan rasional, kritikal dan bernas."
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
        FORM_MAPPING["nama_juri"]: st.session_state.nama_juri,
        FORM_MAPPING["kod_poster"]: kod_poster,
        FORM_MAPPING["jenis_borang"]: jenis_borang,
        FORM_MAPPING["jumlah"]: jumlah,
    }

    for i, skor in enumerate(markah):
        payload[FORM_MAPPING["item"][i]] = skor

    r = requests.post(FORM_URL, data=payload)

    if r.status_code in [200, 302]:
        st.balloons()
        st.success("🎉 Penilaian berjaya dihantar ke Google Sheet!")
    else:
        st.error(f"❌ Gagal hantar data (Status: {r.status_code})")
