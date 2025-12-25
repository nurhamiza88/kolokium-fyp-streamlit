import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

# =====================
# CONFIG
# =====================
SHEET_NAME = "BORANG_KOLOKIUM"
WS_AGIHAN = "AGIHAN_JURI_POSTER"
WS_PENILAIAN = "PENILAIAN"

st.set_page_config(page_title="Penilaian Juri Kolokium FYP", layout="wide")
st.title("📋 Sistem Penilaian Juri Kolokium Projek Tahun Akhir")

# =====================
# GOOGLE SHEETS CONNECT
# =====================
def get_gs_client():
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive"
    ]
    creds = ServiceAccountCredentials.from_json_keyfile_dict(
        st.secrets["gcp"]["credentials_json"], scope
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
if "current_poster" not in st.session_state:
    st.session_state.current_poster = None

# =====================
# STEP 1: PILIH NAMA JURI (DARI SHEET)
# =====================
st.subheader("Maklumat Juri")

if st.session_state.nama_juri is None:
    # Ambil senarai NAMA JURI unik dari AGIHAN
    all_rows = ws_agihan.get_all_records()
    nama_juri_list = sorted({r["NAMA JURI"] for r in all_rows})

    nama = st.selectbox("Sila pilih nama juri", [""] + nama_juri_list)

    if st.button("▶️ Mula Penjurian"):
        if nama == "":
            st.warning("Sila pilih nama juri.")
        else:
            st.session_state.nama_juri = nama

            # bina queue poster ikut juri
            posters = [r["KOD POSTER"] for r in all_rows if r["NAMA JURI"] == nama]
            st.session_state.poster_queue = posters.copy()
            st.experimental_rerun()

else:
    st.success(f"Selamat datang, **{st.session_state.nama_juri}**")

# =====================
# STEP 2: PAPAR POSTER SEMASA
# =====================
if st.session_state.nama_juri and st.session_state.poster_queue:

    st.divider()
    st.subheader("Penilaian Poster")

    # ambil poster pertama dalam queue
    st.session_state.current_poster = st.session_state.poster_queue[0]
    kod_poster = st.session_state.current_poster

    st.info(f"Menilai **Kod Poster: {kod_poster}**")

    # Tentukan jenis borang
    if kod_poster.startswith("PRODUK") or kod_poster.startswith("PENDIDIKAN"):
        jenis_borang = "PRODUK / PENDIDIKAN"
    else:
        jenis_borang = "STATISTIK & MATEMATIK GUNAAN"

    st.write(f"Jenis Borang: **{jenis_borang}**")

    # Skala
    skala = {
        "1 – Tidak Setuju": 1,
        "2 – Kurang Setuju": 2,
        "3 – Setuju": 3,
        "4 – Sangat Setuju": 4
    }

    markah = []

    def soalan_radio(teks, key):
        pilihan = st.radio(teks, skala.keys(), horizontal=True, key=key)
        return skala[pilihan]

    # =====================
    # BORANG PRODUK / PENDIDIKAN
    # =====================
    if jenis_borang == "PRODUK / PENDIDIKAN":
        soalan = [
            "Reka bentuk poster jelas, menarik dan penggunaan AI menyokong kefahaman kajian.",
            "Isi kandungan poster dinyatakan dengan tepat dan merangkumi 11 aspek.",
            "Poster menunjukkan elemen inovatif yang bersesuaian dengan jenis kajian.",
            "Produk atau hasil kajian menunjukkan elemen keaslian atau penambahbaikan bermakna.",
            "Produk atau hasil kajian relevan dan berpotensi membantu menyelesaikan masalah.",
            "Produk atau instrumen kajian telah melalui penilaian asas dan disertakan dokumentasi sokongan.",
            "Penyampaian yang sangat yakin dan sangat bertenaga.",
            "Menerangkan kajian secara sistematik dan tepat.",
            "Komunikasi adalah lancar dan tidak termasuk verbiage seperti umm, uhh uhh.",
            "Berupaya menjawab soalan dan berhujah dengan rasional, kritikal dan bernas."
        ]
    else:
        # =====================
        # BORANG STATISTIK & MATEMATIK
        # =====================
        soalan = [
            "Reka bentuk poster jelas, menarik dan penggunaan AI menyokong kefahaman kajian.",
            "Isi kandungan poster dinyatakan dengan tepat dan merangkumi 10 aspek.",
            "Poster menunjukkan elemen inovatif yang bersesuaian dengan jenis kajian.",
            "Pemilihan dan aplikasi kaedah matematik/statistik serta ketepatan analisis data.",
            "Persembahan hasil analisis data dalam bentuk jadual, graf atau rajah adalah tepat.",
            "Penyelidikan memberikan sumbangan bermakna kepada body of knowledge dan disokong draf artikel.",
            "Penyampaian yang sangat yakin dan sangat bertenaga.",
            "Menerangkan kajian secara sistematik dan tepat.",
            "Komunikasi adalah lancar dan tidak termasuk verbiage seperti umm, uhh uhh.",
            "Berupaya menjawab soalan dan berhujah dengan rasional, kritikal dan bernas."
        ]

    for i, s in enumerate(soalan):
        markah.append(soalan_radio(s, f"q{i}"))

    jumlah = sum(markah)
    st.success(f"✅ Jumlah Markah: **{jumlah} / 40**")

    # =====================
    # SUBMIT
    # =====================
    if st.button("📤 SUBMIT PENILAIAN"):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ws_penilaian.append_row([
            timestamp,
            st.session_state.nama_juri,
            kod_poster,
            jenis_borang,
            jumlah
        ])

        # buang poster semasa dari queue
        st.session_state.poster_queue.pop(0)
        st.experimental_rerun()

# =====================
# STEP 3: SIAP SEMUA
# =====================
if st.session_state.nama_juri and not st.session_state.poster_queue:
    st.balloons()
    st.success("🎉 Semua poster yang ditugaskan telah dinilai. Terima kasih!")
