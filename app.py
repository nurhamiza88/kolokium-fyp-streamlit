import streamlit as st
import gspread
import json
from oauth2client.service_account import ServiceAccountCredentials
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
# GOOGLE SHEET: TARIK NAMA JURI
# =====================
def get_juri_list():
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive"
    ]

    creds = ServiceAccountCredentials.from_json_keyfile_dict(
        json.loads(st.secrets["gcp"]["credentials_json"]),
        scope
    )

    client = gspread.authorize(creds)
    sh = client.open("KOLOKIUM_FYP_2026")   # ✅ betul
    ws = sh.worksheet("JURI")               # ✅ sheet JURI

    return ws.col_values(1)[1:]  # buang header

# =====================
# SESSION STATE
# =====================
if "nama_juri" not in st.session_state:
    st.session_state.nama_juri = None

# =====================
# PILIH NAMA JURI (DARI GOOGLE SHEET)
# =====================
st.subheader("Maklumat Juri")

if st.session_state.nama_juri is None:
    senarai_juri = get_juri_list()
    nama = st.selectbox("Pilih Nama Juri", ["-- Pilih --"] + senarai_juri)

    if nama != "-- Pilih --":
        st.session_state.nama_juri = nama
        st.success(f"Nama juri disimpan: {nama}")
else:
    st.info(f"👤 Juri: {st.session_state.nama_juri}")

# =====================
# PILIH KOD POSTER (MASIH STATIK – OK UNTUK FASA 2)
# =====================
st.subheader("Maklumat Poster")

SENARAI_KOD = [
    "PRODUK001", "PRODUK002", "PRODUK003",
    "PENDIDIKAN001", "PENDIDIKAN002",
    "STATISTIKMATEMATIK001", "STATISTIKMATEMATIK002"
]

kod_poster = st.selectbox("Pilih Kod Poster", SENARAI_KOD)

# =====================
# TENTUKAN JENIS BORANG & ITEM (LENGKAP)
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
# SUBMIT (BELUM SIMPAN – OK UNTUK FASA 2)
# =====================
if st.button("📤 Submit Penilaian"):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    st.balloons()
    st.success("Penilaian berjaya direkodkan!")

    st.write("### Ringkasan")
    st.write(f"🕒 Masa: {timestamp}")
    st.write(f"👤 Juri: {st.session_state.nama_juri}")
    st.write(f"🧾 Kod Poster: {kod_poster}")
    st.write(f"📑 Jenis Borang: {jenis_borang}")
    st.write(f"📊 Jumlah Markah: {jumlah}")

    st.info("Sedia untuk nilai poster seterusnya 👌")
