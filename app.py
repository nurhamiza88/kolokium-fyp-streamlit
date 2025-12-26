import requests

FORM_URL = "https://docs.google.com/forms/d/e/1K6tBmnv7JBX_TCTIhCg3UxTKuGLbxbd5UYf4N4lFLmM/formResponse"

FORM_MAPPING = {
    "nama_juri": "entry.1101626450",
    "kod_poster": "entry.1011436319",
    "jenis_borang": "entry.2043825743",
    "jumlah": "entry.2012388652",
    "item": [
        "entry.994184812",   # Item 1
        "entry.1025336879",  # Item 2
        "entry.1540256323",  # Item 3
        "entry.90543189",    # Item 4
        "entry.1040594050",  # Item 5
        "entry.1209343348",  # Item 6
        "entry.1535785034",  # Item 7
        "entry.895520193",   # Item 8
        "entry.964162367",   # Item 9
        "entry.200002443"    # Item 10
    ]
}


import streamlit as st
import pandas as pd
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
# GOOGLE SHEET (CSV) – SENARAI JURI
# =====================
CSV_JURI_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSlsLSz46lRS0ncB4idH-6Xn_pGWb5jXXKsZdwKygizIHDrkjbjvzB3vzD9qxV06_2FTMLGxunuZUpy/pub?gid=1188865026&single=true&output=csv"

def get_juri_from_sheet():
    df = pd.read_csv(CSV_JURI_URL)
    return df["NAMA JURI"].dropna().tolist()

# =====================
# SESSION STATE
# =====================
if "nama_juri" not in st.session_state:
    st.session_state.nama_juri = None

# =====================
# MAKLUMAT JURI (DROPDOWN DARI GOOGLE SHEET)
# =====================
st.subheader("Maklumat Juri")

try:
    SENARAI_JURI = get_juri_from_sheet()
except Exception:
    st.error("❌ Gagal tarik senarai juri dari Google Sheet. Sila semak CSV.")
    st.stop()

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
SENARAI_KOD = [
    "PRODUK001", "PRODUK002", "PRODUK003",
    "PENDIDIKAN001", "PENDIDIKAN002",
    "STATISTIKMATEMATIK001", "STATISTIKMATEMATIK002"
]

st.subheader("Maklumat Poster")
kod_poster = st.selectbox("Pilih Kod Poster", SENARAI_KOD)

# =====================
# TENTUKAN JENIS BORANG & ITEM
# =====================
if kod_poster.startswith("PRODUK") or kod_poster.startswith("PENDIDIKAN"):
    jenis_borang = "PRODUK / PENDIDIKAN"
    soalan = [
        "Reka bentuk poster jelas, menarik dan penggunaan AI menyokong kefahaman kajian.",
        "Isi kandungan poster lengkap merangkumi 11 aspek utama kajian (tajuk, abstrak, pernyataan masalah, objektif/soalan kajian, reka bentuk kajian, populasi/sampel/teknik pensampelan, instrumen, analisis data, dapatan, kesimpulan dan implikasi).",
        "Poster menunjukkan elemen inovatif bersesuaian dengan kajian.",
        "Produk atau hasil kajian menunjukkan keaslian atau penambahbaikan bermakna.",
        "Produk atau hasil kajian relevan dan membantu menyelesaikan masalah.",
        "Produk atau instrumen kajian melalui penilaian asas dan dokumentasi sokongan.",
        "Penyampaian adalah sangat yakin dan bertenaga.",
        "Kajian diterangkan secara sistematik dan tepat.",
        "Komunikasi lancar tanpa verbiage seperti umm atau uhh.",
        "Pembentang berupaya menjawab soalan dengan rasional dan kritikal."
    ]
else:
    jenis_borang = "STATISTIK & MATEMATIK GUNAAN"
    soalan = [
        "Reka bentuk poster jelas, menarik dan penggunaan AI menyokong kefahaman kajian.",
        "Isi kandungan poster lengkap merangkumi 10 aspek utama kajian (tajuk, abstrak, pernyataan masalah, objektif/soalan kajian, penjelasan teknik/kaedah matematik/statistik, analisis data, dapatan kajian, kesimpulan, implikasi dan rujukan).",
        "Poster menunjukkan elemen inovatif bersesuaian dengan kajian.",
        "Kaedah matematik/statistik yang dipilih bersesuaian dan diaplikasi dengan tepat.",
        "Persembahan analisis data tepat dan bersesuaian.",
        "Kajian menyumbang kepada body of knowledge dan draf artikel disediakan.",
        "Penyampaian adalah sangat yakin dan bertenaga.",
        "Kajian diterangkan secara sistematik dan tepat.",
        "Komunikasi lancar tanpa verbiage seperti umm atau uhh.",
        "Pembentang berupaya menjawab soalan dengan rasional dan kritikal."
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
        options=[1, 2, 3, 4],
        horizontal=True,
        key=f"item_{i}"
    )
    markah.append(skor)

jumlah = sum(markah)
st.success(f"✅ Jumlah Markah: {jumlah} / 40")

# =====================
# SUBMIT (BELUM HANTAR KE GOOGLE FORM – SELAMAT)
# =====================
if st.button("📤 Submit Penilaian"):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    st.balloons()
    st.success("Penilaian berjaya direkodkan (paparan sahaja).")

    st.write("### Ringkasan")
    st.write(f"🕒 Masa: {timestamp}")
    st.write(f"👤 Juri: {st.session_state.nama_juri}")
    st.write(f"🧾 Kod Poster: {kod_poster}")
    st.write(f"📑 Jenis Borang: {jenis_borang}")
    st.write(f"📊 Jumlah Markah: {jumlah}")

    st.info("Langkah seterusnya: sambung ke Google Form untuk simpan data.")
