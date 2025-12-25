import streamlit as st

st.set_page_config(page_title="Penilaian Juri Kolokium FYP", layout="wide")
st.title("📋 Sistem Penilaian Juri Kolokium Projek Tahun Akhir")

# =====================
# MAKLUMAT JURI
# =====================
st.subheader("Maklumat Juri")
nama_juri = st.text_input("Nama Juri").upper()

kod_poster = st.selectbox(
    "Kod Poster",
    [
        "PRODUK001",
        "PENDIDIKAN002",
        "STATISTIKMATEMATIK003"
    ]
)

# =====================
# TENTUKAN JENIS BORANG
# =====================
if kod_poster.startswith("PRODUK") or kod_poster.startswith("PENDIDIKAN"):
    jenis_borang = "PRODUK / PENDIDIKAN"
else:
    jenis_borang = "STATISTIK & MATEMATIK GUNAAN"

st.info(f"Jenis Borang: **{jenis_borang}**")

# =====================
# SKALA
# =====================
skala = {
    "1 – Tidak Setuju": 1,
    "2 – Kurang Setuju": 2,
    "3 – Setuju": 3,
    "4 – Sangat Setuju": 4
}

markah = []

def soalan_radio(teks):
    pilihan = st.radio(teks, skala.keys(), horizontal=True)
    return skala[pilihan]

# =====================
# BORANG PRODUK / PENDIDIKAN
# =====================
if jenis_borang == "PRODUK / PENDIDIKAN":
    st.subheader("Borang Penjurian – Produk / Pendidikan")

    soalan = [
        "Reka bentuk poster jelas, menarik dan penggunaan AI menyokong kefahaman kajian.",
        "Isi kandungan poster dinyatakan dengan tepat dan merangkumi 11 aspek.",
        "Poster menunjukkan elemen inovatif yang bersesuaian dengan jenis kajian.",
        "Produk atau hasil kajian menunjukkan elemen keaslian atau penambahbaikan bermakna terhadap amalan sedia ada.",
        "Produk atau hasil kajian relevan dan berpotensi membantu menyelesaikan masalah yang dikenal pasti.",
        "Produk atau instrumen kajian telah melalui penilaian asas dan disertakan dokumentasi sokongan.",
        "Penyampaian yang sangat yakin dan sangat bertenaga.",
        "Menerangkan kajian secara sistematik dan tepat.",
        "Komunikasi adalah lancar dan tidak termasuk verbiage seperti umm, uhh uhh.",
        "Berupaya menjawab soalan dan berhujah dengan rasional, kritikal dan bernas."
    ]

    for s in soalan:
        markah.append(soalan_radio(s))

# =====================
# BORANG STATISTIK & MATEMATIK
# =====================
else:
    st.subheader("Borang Penjurian – Statistik & Matematik Gunaan")

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

    for s in soalan:
        markah.append(soalan_radio(s))

# =====================
# JUMLAH & SUBMIT
# =====================
jumlah = sum(markah)
st.success(f"✅ Jumlah Markah: **{jumlah} / 40**")

if st.button("📤 SUBMIT PENILAIAN"):
    st.success("Penilaian berjaya direkod (simulasi).")
