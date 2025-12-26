# =====================
# IMPORT
# =====================
import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

# =====================
# PAGE CONFIG
# =====================
st.set_page_config(
    page_title="Penilaian Juri Kolokium FYP",
    layout="wide"
)

st.title("📋 Sistem Penilaian Juri Kolokium Projek Tahun Akhir")

# =====================
# GOOGLE SHEET: GET JURI LIST
# =====================
def get_juri_list():
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive"
    ]

    creds = ServiceAccountCredentials.from_json_keyfile_dict(
        st.secrets["gcp"]["credentials_json"],
        scope
    )

    client = gspread.authorize(creds)

    # 🔁 PASTIKAN NAMA & TAB BETUL
    sh = client.open("KOLOKIUM_FYP_2026")
    ws = sh.worksheet("JURI")

    return ws.col_values(1)[1:]  # buang header

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
    try:
        senarai_juri = get_juri_list()
        nama = st.selectbox("Pilih Nama Juri", ["-- Pilih --"] + senarai_juri)

        if nama != "-- Pilih --":
            st.session_state.nama_juri = nama
            st.success(f"Nama juri disimpan: {nama}")
    except Exception as e:
        st.error("❌ Gagal tarik senarai juri dari Google Sheet")
        st.stop()
else:
    st.info(f"👤 Juri: {st.session_state.nama_juri}")

# =====================
# SENARAI KOD POSTER (STATIK – SELAMAT)
# =====================
SENARAI_KOD = [
    "PRODUK001", "PRODUK002", "PRODUK003",
    "PENDIDIKAN001", "PENDIDIKAN002",
    "STATISTIKMATEMATIK001", "STATISTIKMATEMATIK002"
]

# =====================
# PILIH KOD POSTER
# =====================
st.subheader("Maklumat Poster")
kod_poster = st.selectbox("Pilih Kod Poster", SENARAI_KOD)

# =====================
# TENTUKAN BORANG & ITEM
# =====================
if kod_poster.startswith("PRODUK") or kod_poster.startswith("PENDIDIKAN"):
    jenis_borang = "PRODUK / PENDIDIKAN"
    soalan = [
        "Reka bentuk poster jelas, menarik dan penggunaan AI menyokong kefahaman kajian.",
        "Isi kandungan poster lengkap merangkumi 11 aspek utama kajian.",
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
        "Isi kandungan poster lengkap merangkumi 10 aspek utama kajian.",
        "Poster menunjukkan elemen inovatif bersesuaian dengan kajian.",
        "Kaedah matematik/statistik dipilih dan diaplikasi dengan tepat.",
        "Persembahan analisis data adalah tepat dan bersesuaian.",
        "Kajian menyumbang kepada body of knowledge dan disertakan draf artikel.",
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
    masa = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    st.balloons()
    st.success("Penilaian berjaya direkodkan!")

    st.write("### Ringkasan Penilaian")
    st.write(f"🕒 Masa: {masa}")
    st.write(f"👤 Juri: {st.session_state.nama_juri}")
    st.write(f"🧾 Kod Poster: {kod_poster}")
    st.write(f"📑 Jenis Borang: {jenis_borang}")
    st.write(f"📊 Jumlah Markah: {jumlah}")

    st.info("Sedia untuk menilai poster seterusnya 👍")
