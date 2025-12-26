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
# GOOGLE SHEET (CSV)
# =====================

# Senarai juri
CSV_JURI_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSlsLSz46lRS0ncB4idH-6Xn_pGWb5jXXKsZdwKygizIHDrkjbjvzB3vzD9qxV06_2FTMLGxunuZUpy/pub?gid=1188865026&single=true&output=csv"

# Agihan juri → kod poster
CSV_AGIHAN_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSlsLSz46lRS0ncB4idH-6Xn_pGWb5jXXKsZdwKygizIHDrkjbjvzB3vzD9qxV06_2FTMLGxunuZUpy/pub?gid=381457985&single=true&output=csv"

def get_juri():
    df = pd.read_csv(CSV_JURI_URL)
    df.columns = df.columns.str.strip()
    return df["Nama Juri"].dropna().unique().tolist()

def get_kod_poster_juri(nama_juri):
    df = pd.read_csv(CSV_AGIHAN_URL)
    df.columns = df.columns.str.strip()  # 🔒 FIX UTAMA
    kod = df.loc[
        df["Nama Juri"] == nama_juri,
        "Kod Poster"
    ].dropna().unique().tolist()
    return kod

# =====================
# GOOGLE FORM
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
        "entry.200002443",
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
    senarai_juri = get_juri()
except Exception:
    st.error("❌ Gagal tarik senarai juri.")
    st.stop()

if st.session_state.nama_juri is None:
    nama = st.selectbox("Pilih Nama Juri", ["-- Pilih --"] + senarai_juri)
    if nama != "-- Pilih --":
        st.session_state.nama_juri = nama
        st.success(f"Nama juri disimpan: {nama}")
else:
    st.info(f"👤 Juri: {st.session_state.nama_juri}")

# =====================
# MAKLUMAT POSTER (IKUT AGIHAN)
# =====================
st.subheader("Maklumat Poster")

try:
    kod_dibenarkan = get_kod_poster_juri(st.session_state.nama_juri)
except Exception:
    st.error("❌ Gagal tarik agihan juri.")
    st.stop()

if not kod_dibenarkan:
    st.warning("⚠️ Tiada poster diagihkan kepada juri ini.")
    st.stop()

kod_poster = st.selectbox("Pilih Kod Poster", kod_dibenarkan)

# =====================
# RUBRIK
# =====================
if kod_poster.startswith("PRODUK") or kod_poster.startswith("PENDIDIKAN"):
    jenis_borang = "PRODUK / PENDIDIKAN"
    soalan = [
        "Reka bentuk poster jelas dan menarik.",
        "Isi kandungan poster lengkap merangkumi aspek utama.",
        "Poster menunjukkan elemen inovatif.",
        "Produk atau hasil kajian menunjukkan keaslian.",
        "Produk atau hasil kajian relevan.",
        "Instrumen/kajian melalui penilaian asas.",
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

for i, teks in enumerate(soalan, start=1):
    skor = st.radio(
        f"{i}. {teks}",
        [1, 2, 3, 4],
        horizontal=True,
        key=f"item_{i}"
    )
    markah.append(skor)

jumlah = sum(markah)
st.success(f"✅ Jumlah Markah: {jumlah} / 40")

# =====================
# SUBMIT
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

    if r.status_code == 200:
        st.balloons()
        st.success("🎉 Penilaian berjaya dihantar ke Google Sheet!")
    else:
        st.error(f"❌ Gagal hantar data (Status: {r.status_code})")
