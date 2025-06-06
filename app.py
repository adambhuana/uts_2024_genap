# Tambahkan import
import pandas as pd
import plotly.express as px
import streamlit as st

df_dosen = pd.read_csv("soal_dosen.csv")
df_reguler = pd.read_csv("uts_reguler_sains_data.csv")
df_pro = pd.read_csv("uts_pro_sains_data.csv")

def statistik_soal_dosen(df_dosen):
    st.header("📘 Statistik Dataset Soal Dosen")

    st.subheader("📌 Jumlah Level Soal per Dosen")
    df_dosen["Level Soal"] = df_dosen["Level Soal"].astype(str).str.split(",")
    df_exploded = df_dosen.explode("Level Soal")
    df_exploded["Level Soal"] = df_exploded["Level Soal"].str.strip()

    level_counts = df_exploded["Level Soal"].value_counts().sort_index()
    fig = px.bar(
        x=level_counts.index,
        y=level_counts.values,
        labels={"x": "Level Kognitif", "y": "Jumlah"},
        title="Distribusi Level Kognitif (C1–C6)",
        color=level_counts.values,
        color_continuous_scale="Tealgrn"
    )
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("📊 Heatmap Jumlah Soal per Dosen dan Level")
    pivot = df_exploded.groupby(["Nama Dosen", "Level Soal"]).size().reset_index(name="Jumlah")
    heatmap_data = pivot.pivot(index="Nama Dosen", columns="Level Soal", values="Jumlah").fillna(0)

    st.dataframe(heatmap_data.style.background_gradient(cmap='YlGnBu'), use_container_width=True)

def statistik_dataset_nilai(df_nilai, nama_dataset="Dataset Nilai"):
    st.header(f"📖 Statistik {nama_dataset}")

    df_clean = df_nilai.drop(columns=["NIM", "Nama_Mahasiswa"])
    
    st.subheader("📌 Statistik Deskriptif")
    st.dataframe(df_clean.describe().T, use_container_width=True)

    st.subheader("📊 Korelasi Antar Mata Kuliah")
    fig_corr = px.imshow(df_clean.corr(), 
                         text_auto=True, 
                         color_continuous_scale='RdBu_r',
                         title="Heatmap Korelasi")
    st.plotly_chart(fig_corr, use_container_width=True)

    st.subheader("📉 Boxplot Nilai per Mata Kuliah")
    fig_box = px.box(
        df_clean.melt(var_name="Mata Kuliah", value_name="Nilai"),
        x="Mata Kuliah",
        y="Nilai",
        title="Distribusi Nilai per Mata Kuliah",
        color="Mata Kuliah"
    )
    st.plotly_chart(fig_box, use_container_width=True)
def statistik_nilai_kurang_60(df_reguler, df_pro):
    st.header("❌ Statistik Mahasiswa dengan Nilai < 60")

    # Gabungkan kedua dataset untuk keperluan pelaporan
    df_reguler["Kelas"] = "Reguler"
    df_pro["Kelas"] = "Pro dan Aksel"
    df_all = pd.concat([df_reguler, df_pro], ignore_index=True)

    # Ubah ke format long (melt)
    df_long = df_all.melt(id_vars=["NIM", "Nama_Mahasiswa", "Kelas"],
                          var_name="Mata Kuliah",
                          value_name="Nilai")

    # Filter nilai di bawah 60
    df_kurang_60 = df_long[df_long["Nilai"] < 60]

    # Hitung jumlah mahasiswa per mata kuliah per kelas
    summary = df_kurang_60.groupby(["Kelas", "Mata Kuliah"]).agg(
        Jumlah_Mahasiswa=("Nama_Mahasiswa", "count"),
        Daftar_Mahasiswa=("Nama_Mahasiswa", lambda x: ", ".join(x))
    ).reset_index()

    st.subheader("📊 Grafik Jumlah Mahasiswa dengan Nilai < 60")
    fig = px.bar(
        summary,
        x="Mata Kuliah",
        y="Jumlah_Mahasiswa",
        color="Kelas",
        barmode="group",
        text="Jumlah_Mahasiswa",
        title="Jumlah Mahasiswa dengan Nilai < 60 per Mata Kuliah per Kelas",
        labels={"Jumlah_Mahasiswa": "Jumlah Mahasiswa"}
    )
    fig.update_traces(textposition="outside")
    fig.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("📋 Tabel Detail Mahasiswa dengan Nilai < 60")
    st.dataframe(summary, use_container_width=True)
def statistik_per_mahasiswa_by_kelas(df_reguler, df_pro):
    st.header("🎓 Statistik Nilai Mahasiswa Berdasarkan Kelas")

    # Pilihan kelas
    kelas = st.selectbox("Pilih Kelas", ["Reguler", "Pro dan Aksel"])

    # Pilih dataset sesuai kelas
    df_pilihan = df_reguler if kelas == "Reguler" else df_pro

    # Dropdown nama mahasiswa
    nama_mahasiswa = st.selectbox(
        "Pilih Nama Mahasiswa", 
        sorted(df_pilihan["Nama_Mahasiswa"].unique())
    )

    # Ambil data nilai mahasiswa
    data_mahasiswa = df_pilihan[df_pilihan["Nama_Mahasiswa"] == nama_mahasiswa]

    if data_mahasiswa.empty:
        st.warning("Mahasiswa tidak ditemukan.")
        return

    nilai_df = data_mahasiswa.drop(columns=["NIM", "Nama_Mahasiswa"]).T
    nilai_df.columns = ["Nilai"]
    nilai_df["Mata Kuliah"] = nilai_df.index
    nilai_df.reset_index(drop=True, inplace=True)

    # ✅ Pastikan Nilai bertipe numerik
    nilai_df["Nilai"] = pd.to_numeric(nilai_df["Nilai"], errors="coerce")


    # Statistik
    rata = nilai_df["Nilai"].mean()
    maks = nilai_df["Nilai"].max()
    mini = nilai_df["Nilai"].min()

    st.subheader(f"📋 Tabel Nilai - {nama_mahasiswa}")
    st.dataframe(nilai_df.set_index("Mata Kuliah"))

    col1, col2, col3 = st.columns(3)
    col1.metric("📌 Rata-rata", f"{rata:.2f}")
    col2.metric("⬆️ Maksimum", f"{maks}")
    col3.metric("⬇️ Minimum", f"{mini}")

    # Grafik batang
    fig = px.bar(
        nilai_df,
        x="Mata Kuliah",
        y="Nilai",
        text="Nilai",
        color="Nilai",
        color_continuous_scale="Viridis",
        title=f"Grafik Nilai Mata Kuliah - {nama_mahasiswa}",
        range_y=[0, 100]
    )
    fig.update_traces(textposition="outside")
    fig.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig, use_container_width=True)


tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Soal Dosen", 
    "Nilai Reguler", 
    "Nilai Pro/Aksel", 
    "Mahasiswa < 60",
    "Statistik per Mahasiswa"
])

with tab1:
    statistik_soal_dosen(df_dosen)

with tab2:
    statistik_dataset_nilai(df_reguler, nama_dataset="Kelas Reguler")

with tab3:
    statistik_dataset_nilai(df_pro, nama_dataset="Kelas Pro dan Aksel")

with tab4:
    statistik_nilai_kurang_60(df_reguler, df_pro)
with tab5:
    statistik_per_mahasiswa_by_kelas(df_reguler, df_pro)