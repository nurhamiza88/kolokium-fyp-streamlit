import streamlit as st

st.set_page_config(
    page_title="Penilaian Juri Kolokium FYP",
    layout="wide"
)

st.title("📋 Sistem Penilaian Juri Kolokium Projek Tahun Akhir")

# =====================
# MAKLUMAT JURI
# =====================
st.subheader("Maklumat Juri")

nama_juri = st.text_input("Nama Juri").upper()
kod_poster = st.text_input(
    "Kod Poster (contoh: PRODUK001 / PENDIDIKAN001 / STATISTIKMATEMATIK001)"
)

# =====================
# TENTUKAN JENIS BORANG
# =====================
jenis_borang = None

if kod_poster.startswith("PRODUK") or kod_poster.startswith("PENDIDIKAN"):
    jenis_borang = "PRODUK / PENDIDIKAN"
elif kod_poster.startswith("STATISTIKMATEMATIK"):
    jenis_borang = "STATISTIK & MATEMATIK GUNAAN"

if kod_poster:
    if jenis_borang:
        st.info(f"Jenis Borang: **{jenis_borang}**")
    else:
        st.warning("Kod poster tidak dikenali. Sila semak format kod.")

# =====================
# RUBRIK PRODUK / PENDIDIKAN
# =====================
if jenis_borang == "PRODUK / PENDIDIKAN":
    st.subheader("Rubrik Penilaian – Produk / Pendidikan")

    k1 = st.slider("Reka bentuk poster & penggunaan AI", 1, 4)
    k2 = st.slider("Kandungan poster merangkumi 11 aspek", 1, 4)
    k3 = st.slider("Elemen inovatif kajian", 1, 4)
    k4 = st.slider("Keaslian / penambahbaikan bermakna", 1, 4)
    k5 = st.slider("Relevan menyelesaikan masalah", 1, 4)
    k6 = st.slider("Instrumen melalui penilaian asas", 1, 4)
    k7 = st.slider("Penyampaian yakin & bertenaga", 1, 4)
    k8 = st.slider("Penerangan kajian sistematik", 1, 4)
    k9 = st.slider("Komunikasi lancar", 1, 4)
    k10 = st.slider("Keupayaan menjawab soalan", 1, 4)

    jumlah = k1 + k2 + k3 + k4 + k5 + k6 + k7 + k8 + k9 + k10

    st.success(f"✅ Jumlah Markah: **{jumlah} / 40**")

# =====================
# RUBRIK STATISTIK & MATEMATIK
# =====================
elif jenis_borang == "STATISTIK & MATEMATIK GUNAAN":
    st.subheader("Rubrik Penilaian – Statistik & Matematik Gunaan")

    s1 = st.slider("Reka bentuk poster & penggunaan AI", 1, 4)
    s2 = st.slider("Kandungan poster (10 aspek)", 1, 4)
    s3 = st.slider("Pemilihan & aplikasi kaedah statistik/matematik", 1, 4)
    s4 = st.slider("Ketepatan analisis data", 1, 4)
    s5 = st.slider("Persembahan data (jadual/graf/rajah)", 1, 4)
    s6 = st.slider("Sumbangan kepada body of knowledge", 1, 4)
    s7 = st.slider("Penyampaian yakin & bertenaga", 1, 4)
    s8 = st.slider("Penerangan kajian sistematik", 1, 4)
    s9 = st.slider("Komunikasi lancar", 1, 4)
    s10 = st.slider("Keupayaan menjawab soalan", 1, 4)

    jumlah = s1 + s2 + s3 + s4 + s5 + s6 + s7 + s8 + s9 + s10

    st.success(f"✅ Jumlah Markah: **{jumlah} / 40**")

