# =====================
# FORCE INSTALL (Streamlit Cloud workaround)
# =====================
import sys
import subprocess
subprocess.check_call([sys.executable, "-m", "pip", "install", "gspread", "oauth2client"])

# =====================
# IMPORTS
# =====================
import streamlit as st
import gspread
import json
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

# =====================
# CONFIG
# =====================
SHEET_NAME = "NAMA_SHEET_BUDDY"   # ⚠️ TUKAR ikut nama Google Sheet sebenar
WS_AGIHAN = "AGIHAN_JURI_POSTER"
WS_PENILAIAN = "PENILAIAN"

st.set_page_config(
    page_title="Sistem Penilaian Juri Kolokium PSM",
    layout="wide"
)

st.title("📋 Sistem Penilaian Juri Kolokium Projek Tahun Akhir")

# =====================
# GOOGLE SHEET CONNECTION
# =====================
def get_gs_client():
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive"
    ]

    # Secrets disimpan sebagai STRING → perlu json.loads
    creds_dict = json.loads(st.secrets["gcp"]["credentials_json"])

    creds = ServiceAccountCredentials.from_json_keyfile_dict(
        creds_dict, scope
    )

    return gspread.authorize(creds)

gc = get_gs_client()
sh = gc.open(SHEET_NAME)
ws_agihan = sh.worksheet(WS_AGIHAN)
ws_penilaian = sh.worksheet(WS_PENILAIAN)

# =====================
# SESSION STATE
# =====================
if "nama_juri" not in st.session_state:
    st.session_state.nama_juri = None

if "poster_queue" not in st.session_state:
    st.session_state.poster_queue = []

# =====================
# STEP 1 — PILIH NAMA JURI
# =====================
st.subheader("Maklumat Juri")

if st.session_state.nama_juri is None:
    data_agihan = ws_agihan.get_all_records()

    senarai_juri = sorted({row["NAMA JURI"] for row in data_agihan})

    nama = st.selectbox("Sila pilih nama juri", [""] + senarai_juri)

    if st.button("▶️ Mula Penjurian"):
        if nama == "":
            st.warning("Sila pilih nama juri.")
        else:
            st.session_state.nama_juri = nama
            st.session_state.poster_queue = [
                row["KOD POSTER"]
                for row in data_agihan
                if row["NAMA JURI"] == nama
            ]
            st.experimental_rerun()

else:
    st.success(f"Selamat datang, **{st.session_state.nama_juri}**")

# =====================
# STEP 2 — PENILAIAN POSTER
# =====================
if st.session_state.nama_juri and st.session_state.poster_queue:

    kod_poster = st.session_state.poster_queue[0]

    st.divider()
    st.subheader(f"Penilaian Kod Poster: {kod_poster}")

  # =====================
# TENTUKAN JENIS BORANG & ITEM
# =====================
if kod_poster.startswith("PRODUK") or kod_poster.startswith("PENDIDIKAN"):
    jenis_borang = "PRODUK / PENDIDIKAN"
    soalan = [
        "Reka bentuk poster jelas, menarik dan penggunaan AI menyokong kefahaman kajian (contoh: visualisasi data, infografik atau sokongan analisis).",
        "Isi kandungan poster dinyatakan dengan tepat dan merangkumi 11 aspek iaitu tajuk, abstrak, pernyataan masalah, objektif/soalan kajian, reka bentuk kajian, populasi/sampel/teknik pensampelan, instrumen, analisis data, dapatan kajian, kesimpulan dan implikasi.",
        "Poster menunjukkan elemen inovatif yang bersesuaian dengan jenis kajian yang dijalankan.",
        "Produk atau hasil kajian menunjukkan elemen keaslian atau penambahbaikan bermakna terhadap amalan sedia ada.",
        "Produk atau hasil kajian relevan dan berpotensi membantu menyelesaikan masalah yang dikenal pasti.",
        "Produk atau instrumen kajian telah melalui penilaian asas (contoh: kesahan kandungan atau kebolehgunaan awal) dan disertakan dokumentasi sokongan (contoh: draf artikel atau laporan).",
        "Penyampaian adalah sangat yakin dan bertenaga.",
        "Kajian diterangkan secara sistematik dan tepat.",
        "Komunikasi adalah lancar dan tidak mengandungi verbiage seperti umm atau uhh.",
        "Pembentang berupaya menjawab soalan dan berhujah dengan rasional, kritikal dan bernas."
    ]
else:
    jenis_borang = "STATISTIK & MATEMATIK GUNAAN"
    soalan = [
        "Reka bentuk poster jelas, menarik dan penggunaan AI menyokong kefahaman kajian (contoh: visualisasi data atau sokongan analisis).",
        "Isi kandungan poster dinyatakan dengan tepat dan merangkumi 10 aspek iaitu tajuk, abstrak, pernyataan masalah, objektif/soalan kajian, penjelasan teknik atau kaedah matematik/statistik, analisis data, dapatan kajian, kesimpulan, implikasi dan rujukan.",
        "Poster menunjukkan elemen inovatif yang bersesuaian dengan jenis kajian yang dijalankan.",
        "Pemilihan dan aplikasi kaedah matematik atau statistik serta ketepatan analisis data adalah bersesuaian untuk menjawab objektif kajian.",
        "Persembahan hasil analisis data dalam bentuk jadual, graf atau rajah adalah tepat dan bersesuaian dengan objektif kajian.",
        "Penyelidikan memberikan sumbangan yang bermakna kepada body of knowledge dalam bidang berkaitan serta disokong dengan penyediaan draf artikel.",
        "Penyampaian adalah sangat yakin dan bertenaga.",
        "Kajian diterangkan secara sistematik dan tepat.",
        "Komunikasi adalah lancar dan tidak mengandungi verbiage seperti umm atau uhh.",
        "Pembentang berupaya menjawab soalan dan berhujah dengan rasional, kritikal dan bernas."
    ]

    st.info(f"Jenis Borang: **{jenis_borang}**")

    skala = {
        "1 – Tidak Setuju": 1,
        "2 – Kurang Setuju": 2,
        "3 – Setuju": 3,
        "4 – Sangat Setuju": 4
    }

    markah = []

    for i, teks in enumerate(soalan):
        pilihan = st.radio(
            teks,
            skala.keys(),
            horizontal=True,
            key=f"q{i}"
        )
        markah.append(skala[pilihan])

    jumlah = sum(markah)
    st.success(f"✅ Jumlah Markah: **{jumlah} / 40**")

    # =====================
    # SUBMIT
    # =====================
    if st.button("📤 SUBMIT PENILAIAN"):
        ws_penilaian.append_row([
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            st.session_state.nama_juri,
            kod_poster,
            jenis_borang,
            jumlah
        ])

        st.session_state.poster_queue.pop(0)
        st.experimental_rerun()

# =====================
# STEP 3 — SELESAI
# =====================
if st.session_state.nama_juri and not st.session_state.poster_queue:
    st.balloons()
    st.success("🎉 Semua poster telah berjaya dinilai. Terima kasih!")
