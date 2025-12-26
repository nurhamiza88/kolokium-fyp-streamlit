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
# KONFIG GOOGLE (SELAMAT)
# =====================

# 1️⃣ CSV JURI (Publish to web → CSV)
JURI_CSV_URL = (
https://docs.google.com/spreadsheets/d/e/2PACX-1vSlsLSz46lRS0ncB4idH-6Xn_pGWb5jXXKsZdwKygizIHDrkjbjvzB3vzD9qxV06_2FTMLGxunuZUpy/pub?gid=1188865026&single=true&output=csv
)

# 2️⃣ Google Form (formResponse)
FORM_URL = (
    "https://docs.google.com/forms/d/e/"
    "1K6tBmnv7JBX_TCTIhCg3UxTKuGLbxbd5UYf4N4lFLmM"
    "/formResponse"
)

# 3️⃣ FORM MAPPING (WAJIB IKUT FORM)
FORM_MAPPING = {
    "nama_juri": "entry.1101626450",
    "kod_poster": "entry.1011436319",
    "jenis_borang": "entry.2043825743",
    "jumlah_markah": "entry.2012388652",
    "item_1": "entry.994184812",
    "item_2": "entry.1025336879",
    "item_3": "entry.1540256323",
    "item_4": "entry.90543189",
    "item_5": "entry.1040594050",
    "item_6": "entry.1209343348",
    "item_7": "entry.1535785034",
    "item_8": "entry.895520193",
    "item_9": "entry.964162367",
    "item_10": "entry.200002443",
}

# =====================
# AMBIL SENARAI JURI (CSV)
# =====================
@st.cache_data
def load_juri():
    df = pd.read_csv(JURI_CSV_URL)
    return df.iloc[:, 0].dropna().tolist()

SENARAI_JURI = load_juri()

# =====================
# SENARAI KOD POSTER
# =====================
SENARAI_KOD = [
    "PRODUK001", "PRODUK002", "PRODUK003",
    "PENDIDIKAN001", "PENDIDIKAN002",
    "STATISTIKMATEMATIK001", "STATISTIKMATEMATIK002"
]

# =====================
# SESSION STATE
# =====================
if "nama_juri" not in st.session_state:
    st.session_state.nama_juri = None

# =====================
# MAKLUMAT JURI
# =====================
st.subheader("Maklumat Juri")

if st.session_state.nama_juri is None:
    nama = st.selectbox("Pilih Nama Juri", ["-- Pilih --"] + SENARAI_JURI)
    if nama != "-- Pilih --":
        st.session_state.nama_juri = nama
        st.success(f"Nama juri disimpan: {nama}")
else:
    st.info(f"👤 Juri: {st.session_state.nama_juri}")

# =====================
# MAKLUMAT POSTER
# =====================
st.subheader("Maklumat Poster")
kod_poster = st.selectbox("Pilih Kod Poster", SENARAI_KOD)

# =====================
# RUBRIK AUTOMATIK
# =====================
if kod_poster.startswith("PRODUK") or kod_poster.startswith("PENDIDIKAN"):
    jenis_borang = "PRODUK / PENDIDIKAN"
    soalan = [
        "Reka bentuk poster jelas dan menarik.",
        "Isi kandungan poster lengkap (11 aspek).",
        "Elemen inovatif bersesuaian.",
        "Keaslian atau penambahbaikan bermakna.",
        "Relevan dan membantu selesaikan masalah.",
        "Instrumen dinilai & dokumentasi sokongan.",
        "Penyampaian yakin dan bertenaga.",
        "Huraian kajian sistematik dan tepat.",
        "Komunikasi lancar tanpa verbiage.",
        "Jawapan rasional, kritikal dan bernas."
    ]
else:
    jenis_borang = "STATISTIK & MATEMATIK GUNAAN"
    soalan = [
        "Reka bentuk poster jelas dan kemas.",
        "Isi kandungan poster lengkap (10 aspek).",
        "Elemen inovatif bersesuaian.",
        "Kaedah matematik/statistik tepat.",
        "Analisis data tepat dan relevan.",
        "Sumbangan kepada body of knowledge.",
        "Penyampaian yakin dan bertenaga.",
        "Huraian kajian sistematik.",
        "Komunikasi lancar tanpa verbiage.",
        "Jawapan rasional dan kritikal."
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
        FORM_MAPPING["jumlah_markah"]: jumlah,
    }

    for i in range(10):
        payload[FORM_MAPPING[f"item_{i+1}"]] = markah[i]

    r = requests.post(FORM_URL, data=payload)

    if r.status_code == 200:
        st.balloons()
        st.success("✅ Penilaian berjaya dihantar ke Google Sheet!")
        st.info("Sedia menilai poster seterusnya 👌")
    else:
        st.error("❌ Gagal hantar data. Sila cuba semula.")
