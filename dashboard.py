import streamlit as st
import pandas as pd
from datetime import datetime

# =====================
# CONFIG
# =====================
st.set_page_config(
    page_title="Dashboard Keputusan Kolokium FYP",
    layout="wide"
)

st.title("📊 Dashboard Keputusan Kolokium Projek Tahun Akhir")

st.info(
    "📌 Sekiranya penilaian dihantar lebih daripada sekali oleh juri yang sama "
    "bagi poster yang sama, hanya penilaian TERKINI akan diambil kira "
    "dalam pengiraan purata markah."
)

# =====================
# GOOGLE SHEET CSV (Published link)
# =====================
CSV_URL = (
    "https://docs.google.com/spreadsheets/d/e/"
    "2PACX-1vSmxI1CuK3pVwsVlHtyrsJ1yLxyPzZmpa_eX3daieYJPsBt7_POD9-Iu4FZb9x3NQjMxdJAoH52_0sv"
    "/pub?gid=694659483&single=true&output=csv"
)

@st.cache_data
def load_data():
    df = pd.read_csv(CSV_URL)
    df.columns = [c.strip() for c in df.columns]
    return df

# =====================
# LOAD DATA
# =====================
try:
    df = load_data()
except Exception as e:
    st.error("❌ Gagal memuatkan data dari Google Sheet.")
    st.stop()

# Pastikan sheet ada:
# - "Kod Poster"
# - "Purata Markah"

# =====================
# TAMBAH KATEGORI
# =====================
def kategori_poster(kod):
    if str(kod).startswith("PRODUK"):
        return "Produk"
    elif str(kod).startswith("PENDIDIKAN"):
        return "Pendidikan"
    else:
        return "Statistik / Matematik"

df["Kategori"] = df["Kod Poster"].apply(kategori_poster)

# =====================
# RINGKASAN KESELURUHAN
# =====================
st.subheader("📌 Ringkasan Keseluruhan")

col1, col2 = st.columns(2)

with col1:
    st.metric("Jumlah Poster Dinilai", df["Kod Poster"].nunique())

with col2:
    st.metric(
        "Purata Markah Keseluruhan",
        f"{df['Purata Markah'].mean():.2f} / 40"
    )

# =====================
# KEPUTUSAN MENGIKUT KATEGORI
# =====================
st.divider()
st.subheader("📂 Keputusan Mengikut Kategori")

for kategori in ["Produk", "Pendidikan", "Statistik / Matematik"]:
    df_kat = df[df["Kategori"] == kategori].copy()
    if df_kat.empty:
        continue

    df_kat = df_kat.sort_values("Purata Markah", ascending=False)
    df_kat.insert(0, "Ranking", range(1, len(df_kat) + 1))

    st.markdown(f"### {kategori}")
    st.caption(
        f"Purata Kategori {kategori}: "
        f"{df_kat['Purata Markah'].mean():.2f} / 40"
    )

    st.dataframe(
        df_kat[["Ranking", "Kod Poster", "Purata Markah"]],
        use_container_width=True
    )

# =====================
# FOOTER
# =====================
st.divider()
st.caption(
    f"Sumber Data: Google Form & Google Sheet (Automatik) | "
    f"Dikemaskini: {datetime.now().strftime('%d %B %Y, %I:%M %p')}"
)
st.caption(
    "© UPSI | Sistem Penilaian Kolokium Projek Tahun Akhir"
)
