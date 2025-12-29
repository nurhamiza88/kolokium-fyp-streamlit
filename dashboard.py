import streamlit as st
import pandas as pd
from datetime import datetime
from zoneinfo import ZoneInfo

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
    "dalam pengiraan markah."
)

# =====================
# GOOGLE SHEET CSV (PUBLISH TO WEB)
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
except Exception:
    st.error("❌ Gagal memuatkan data dari Google Sheet.")
    st.stop()

# Jangkaan kolum:
# Kod Poster | Jumlah Markah | Bilangan Juri

# =====================
# TAMBAH KATEGORI POSTER
# =====================
def kategori_poster(kod):
    kod = str(kod)
    if kod.startswith("PRODUK"):
        return "Produk"
    elif kod.startswith("PENDIDIKAN"):
        return "Pendidikan"
    else:
        return "Statistik / Matematik"

df["Kategori"] = df["Kod Poster"].apply(kategori_poster)

# =====================
# RINGKASAN KESELURUHAN
# =====================
st.subheader("📌 Ringkasan Keseluruhan")

c1, c2, c3 = st.columns(3)

with c1:
    st.metric("Jumlah Poster Dinilai", df["Kod Poster"].nunique())

with c2:
    st.metric(
        "Purata Jumlah Markah (2 Juri)",
        f"{df['Jumlah Markah'].mean():.2f} / 80"
    )

with c3:
    st.metric(
        "Poster Lengkap 2 Juri",
        int((df["Bilangan Juri"] == 2).sum())
    )

# =====================
# STYLE TABLE
# =====================
def style_table(df_table):
    def highlight(row):
        styles = [""] * len(row)

        # Ranking 1
        if row["Ranking"] == 1:
            styles = ["background-color:#e8f5e9;font-weight:bold"] * len(row)

        # Status bilangan juri
        if row["Bilangan Juri"] < 2:
            styles = ["background-color:#fff3cd"] * len(row)
        elif row["Bilangan Juri"] == 2:
            styles = ["background-color:#e8f5e9"] * len(row)

        return styles

    return (
        df_table.style
        .apply(highlight, axis=1)
        .set_properties(**{"text-align": "center"})
        .set_table_styles([
            {"selector": "th", "props": [("text-align", "center")]}
        ])
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

    df_kat = df_kat.sort_values("Jumlah Markah", ascending=False)
    df_kat.insert(0, "Ranking", range(1, len(df_kat) + 1))

    st.markdown(f"### {kategori}")
    st.caption(
        f"Purata Jumlah Markah Kategori {kategori}: "
        f"{df_kat['Jumlah Markah'].mean():.2f} / 80"
    )

    df_table = df_kat[
        ["Ranking", "Kod Poster", "Jumlah Markah", "Bilangan Juri"]
    ]

    st.dataframe(
        style_table(df_table),
        use_container_width=True
    )

# =====================
# FOOTER (MALAYSIA TIME)
# =====================
st.divider()
st.caption(
    f"Sumber Data: Google Form & Google Sheet (Automatik) | "
    f"Dikemaskini: {datetime.now(ZoneInfo('Asia/Kuala_Lumpur')).strftime('%d %B %Y, %I:%M %p')}"
)
st.caption(
    "© UPSI | Sistem Penilaian Kolokium Projek Tahun Akhir"
)
