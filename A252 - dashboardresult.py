# =====================
# KEPUTUSAN MENGIKUT KATEGORI
# =====================
st.divider()
st.subheader("🏆 Keputusan Mengikut Kategori")

for kategori in ["Inovasi", "Bukan Inovasi"]:

    df_kat = df[df["Kategori"] == kategori].copy()

    if df_kat.empty:
        continue

    # Susun mengikut markah tertinggi
    df_kat = df_kat.sort_values(
        "Jumlah Markah",
        ascending=False
    )

    # Tambah ranking
    df_kat.insert(
        0,
        "Ranking",
        range(1, len(df_kat) + 1)
    )

    # Tajuk kategori
    if kategori == "Inovasi":
        st.markdown("## 🏆 Kategori Inovasi")
    else:
        st.markdown("## 📚 Kategori Bukan Inovasi")

    # Papar jadual
    df_table = df_kat[
        [
            "Ranking",
            "Kod Poster",
            "Jumlah Markah",
            "Bilangan Juri"
        ]
    ]

    st.dataframe(
        style_table(df_table),
        use_container_width=True
    )
