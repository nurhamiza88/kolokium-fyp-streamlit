import streamlit as st
from datetime import datetime
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
# GOOGLE FORM CONFIG
# =====================
FORM_URL = "https://docs.google.com/forms/d/e/1K6tBmnv7JBX_TCTIhCg3UxTKuGLbxbd5UYf4N4lFLmM/formResponse"

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
# DATA STATIK
# =====================
SENARAI_JURI = [
    "Dr. Nur Hamiza binti Adenan",
    "Dr. A",
    "Dr. B",
    "Dr. C"
]

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
# JENIS BORANG & SOALAN
# =====================
if kod_poster.startswith("PRODUK") or kod_poster.startswith("PENDIDIKAN"):
    jenis_borang = "PRODUK / PENDIDIKAN"
else:
    jenis_borang = "STATISTIK & MATEMATIK GUNAAN"

soalan = [f"Item {i}" for i in range(1, 11)]

# =====================
# BORANG PENILAIAN
# =====================
st.divider()
st.subheader(f"Instrumen Penilaian ({jenis_borang})")
st.caption("Skala: 1 = Tidak Setuju | 4 = Sangat Setuju")

markah = []

for i in range(10):
    skor = st.radio(
        f"{i+1}. {soalan[i]}",
        [1, 2, 3, 4],
        horizontal=True,
        key=f"item_{i+1}"
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
        FORM_MAPPING["item_1"]: markah[0],
        FORM_MAPPING["item_2"]: markah[1],
        FORM_MAPPING["item_3"]: markah[2],
        FORM_MAPPING["item_4"]: markah[3],
        FORM_MAPPING["item_5"]: markah[4],
        FORM_MAPPING["item_6"]: markah[5],
        FORM_MAPPING["item_7"]: markah[6],
        FORM_MAPPING["item_8"]: markah[7],
        FORM_MAPPING["item_9"]: markah[8],
        FORM_MAPPING["item_10"]: markah[9],
    }

    response = requests.post(FORM_URL, data=payload)

    if response.status_code == 200:
        st.balloons()
        st.success("✅ Penilaian berjaya dihantar ke Google Sheet!")
    else:
        st.error("❌ Gagal hantar data ke Google Form.")
