import streamlit as st
import pandas as pd
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
# URL CSV GOOGLE SHEET
# =====================
JURI_CSV = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSlsLSz46lRS0ncB4idH-6Xn_pGWb5jXXKsZdwKygizIHDrkjbjvzB3vzD9qxV06_2FTMLGxunuZUpy/pub?gid=1188865026&single=true&output=csv"

# =====================
# LOAD AGIHAN JURI
# =====================
@st.cache_data
def load_agihan():
    return pd.read_csv(AGIHAN_JURI_CSV)

df_agihan = load_agihan()

# =====================
# SESSION STATE
# =====================
if "nama_juri" not in st.session_state:
    st.session_state.nama_juri = None

# =====================
# PILIH JURI
# =====================
st.subheader("Maklumat Juri")

senarai_juri = sorted(df_agihan["Nama Juri"].unique())

if st.session_state.nama_juri is None:
    nama = st.selectbox("Pilih Nama Juri", ["-- Pilih --"] + senarai_juri)
    if nama != "-- Pilih --":
        st.session_state.nama_juri = nama
        st.success(f"Nama juri disimpan: {nama}")
else:
    st.info(f"👤 Juri: {st.session_state.nama_juri}")

# =====================
# PILIH KOD POSTER (IKUT AGIHAN)
# =====================
st.subheader("Maklumat Poster")

df_juri = df_agihan[df_agihan["Nama Juri"] == st.session_state.nama_juri]
senarai_kod = df_juri["Kod Poster"].tolist()

kod_poster = st.selectbox("Pilih Kod Poster", senarai_kod)

# =====================
# TENTUKAN JENIS BORANG
# =====================
if kod_poster.startswith("PRODUK") or kod_poster.startswith("PENDIDIKAN"):
    jenis_borang = "PRODUK / PENDIDIKAN"
    soalan = [
        "Reka bentuk poster jelas dan menarik.",
        "Isi kandungan lengkap merangkumi 11 aspek kajian.",
        "Poster menunjukkan elemen inovatif.",
        "Produk menunjukkan keaslian / penambahbaikan bermakna.",
        "Produk relevan dan membantu menyelesaikan masalah.",
        "Instrumen/produk melalui penilaian asas.",
        "Penyampaian yakin dan bertenaga.",
        "Kajian diterangkan secara sistematik.",
        "Komunikasi lancar.",
        "Pembentang menjawab soalan dengan bernas."
    ]
else:
    jenis_borang = "STATISTIK & MATEMATIK GUNAAN"
    soalan = [
        "Reka bentuk poster jelas.",
        "Isi kandungan lengkap merangkumi 10 aspek kajian.",
        "Poster menunjukkan elemen inovatif.",
        "Kaedah matematik/statistik sesuai dan tepat.",
        "Analisis data dipersembahkan dengan betul.",
        "Kajian menyumbang kepada body of knowledge.",
        "Penyampaian yakin dan bertenaga.",
        "Kajian diterangkan secara sistematik.",
        "Komunikasi lancar.",
        "Pembentang menjawab soalan dengan bernas."
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
# SUBMIT (PAPARAN SAHAJA – SELAMAT)
# =====================
if st.button("📤 Submit Penilaian"):
    masa = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    st.success("Penilaian berjaya direkodkan (paparan sistem).")
    st.write("### Ringkasan")
    st.write(f"🕒 Masa: {masa}")
    st.write(f"👤 Juri: {st.session_state.nama_juri}")
    st.write(f"🧾 Kod Poster: {kod_poster}")
    st.write(f"📑 Jenis Borang: {jenis_borang}")
    st.write(f"📊 Jumlah Markah: {jumlah}")

    st.info("Sedia untuk nilai poster seterusnya 👍")
