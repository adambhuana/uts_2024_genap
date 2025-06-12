# Tambahkan import
import pandas as pd
import plotly.express as px
import streamlit as st
import seaborn as sns
import matplotlib as plt
import csv
def login():
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    if not st.session_state.logged_in:
        st.title("🔐 Login Dosen Prodi Sains Data")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            with open("login_users.txt", "r") as f:
                users = list(csv.reader(f))
                user_dict = {u[0]: u[1] for u in users}

            if username in user_dict and password == user_dict[username]:
                st.session_state.logged_in = True
                st.success("✅ Login berhasil!")
                st.rerun()
            else:
                st.error("❌ Username atau password salah.")

        st.stop()
login()

if st.sidebar.button("🔓 Logout"):
    st.session_state.logged_in = False
    st.rerun()

df_dosen = pd.read_csv("soal_dosen.csv")
df_reguler = pd.read_csv("uts_reguler_sains_data.csv")
df_pro = pd.read_csv("uts_pro_sains_data.csv")
df_abs_com_pro_reg = pd.read_csv("absensi_com_pro_reguler_sains_data.csv")
df_abs_ds_reg = pd.read_csv("absensi_ds_reguler_sains_data.csv")
df_abs_wcd_reg = pd.read_csv("absensi_wcd_reguler_sains_data.csv")
df_abs_oop_reg = pd.read_csv("absensi_oop_reguler_sains_data.csv")
df_abs_dbs_reg = pd.read_csv("absensi_dbs_reguler_sains_data.csv")
df_abs_sta_reg = pd.read_csv("absensi_sta_reguler_sains_data.csv")
df_abs_dw_reg = pd.read_csv("absensi_dw_reguler_sains_data.csv")
df_mhs_reg = pd.read_csv("total_mhs_reguler_sains_data.csv", dtype={'NIM': str, 'Tahun': str})
df_mhs_pro = pd.read_csv("total_mhs_pro_sains_data.csv", dtype={'NIM': str, 'Tahun': str})


import pandas as pd
import plotly.express as px
import streamlit as st

def analisa_statistik_kehadiran_com_pro_reg(df_abs_com_pro_reg ):
    st.subheader("📊 Analisa Kehadiran: Communication Protocols")

    # Pastikan kolom numerik
    df_abs_com_pro_reg ["Presentase"] = pd.to_numeric(df_abs_com_pro_reg ["Presentase"], errors="coerce")
    df_abs_com_pro_reg ["Hadir"] = pd.to_numeric(df_abs_com_pro_reg ["Hadir"], errors="coerce")
    df_abs_com_pro_reg ["Pertemuan"] = pd.to_numeric(df_abs_com_pro_reg ["Pertemuan"], errors="coerce")

    # Tambahkan kategori kehadiran
    def kategori(p):
        if p == 100:
            return "Sangat Baik"
        elif p >= 75:
            return "Baik"
        elif p >= 60:
            return "Cukup"
        else:
            return "Kurang"
    df_abs_com_pro_reg ["Kategori Kehadiran"] = df_abs_com_pro_reg ["Presentase"].apply(kategori)

    # Statistik dasar
    rata2 = df_abs_com_pro_reg ["Presentase"].mean()
    jumlah_100 = (df_abs_com_pro_reg ["Presentase"] == 100).sum()
    distribusi = df_abs_com_pro_reg ["Kategori Kehadiran"].value_counts().reset_index()
    distribusi.columns = ["Kategori", "Jumlah"]

    # Metrik ringkas
    col1, col2 = st.columns(2)
    col1.metric("📌 Rata-rata Kehadiran", f"{rata2:.2f}%")
    col2.metric("✅ Jumlah Hadir 100%", f"{jumlah_100} Mahasiswa")

    # Tabel utama
    st.write("### 📋 Tabel Kehadiran Mahasiswa")
    st.dataframe(df_abs_com_pro_reg [["Nama_Mahasiswa", "Pertemuan", "Hadir", "Presentase", "Kategori Kehadiran"]],
                 use_container_width=True)

    # Grafik batang jumlah hadir
    st.write("### 📈 Grafik Jumlah Kehadiran per Mahasiswa")
    fig_hadir = px.bar(
        df_abs_com_pro_reg ,
        x="Nama_Mahasiswa",
        y="Hadir",
        text="Hadir",
        title="Jumlah Kehadiran per Mahasiswa",
        color="Kategori Kehadiran",
        labels={"Hadir": "Jumlah Hadir"},
    )
    fig_hadir.update_layout(xaxis_tickangle=-45)
    fig_hadir.update_traces(textposition="outside")
    st.plotly_chart(fig_hadir, use_container_width=True, key="grafik_kehadiran_cp")

    # Distribusi Kategori Kehadiran
    st.write("### 📊 Distribusi Kategori Kehadiran")
    col_a, col_b = st.columns(2)
    with col_a:
        fig_bar = px.bar(distribusi, x="Kategori", y="Jumlah", text="Jumlah", color="Kategori")
        fig_bar.update_traces(textposition="outside")
        st.plotly_chart(fig_bar, use_container_width=True, key="bar_kehadiran_cp")
    with col_b:
        fig_pie = px.pie(distribusi, names="Kategori", values="Jumlah")
        st.plotly_chart(fig_pie, use_container_width=True, key="piekehadiran_cp")

    # Mahasiswa dengan presentase = 0
    st.write("### 🚨 Mahasiswa dengan Kehadiran 0%")
    nol_df = df_abs_com_pro_reg [df_abs_com_pro_reg ["Presentase"] == 0]
    if nol_df.empty:
        st.success("Tidak ada mahasiswa dengan kehadiran 0%")
    else:
        st.error(f"Ada {len(nol_df)} mahasiswa dengan kehadiran 0%:")
        st.dataframe(nol_df[["Nama_Mahasiswa", "Pertemuan", "Hadir", "Presentase"]])

    # Mahasiswa hadir ≥ 7
    st.write("### 📗 Mahasiswa dengan Jumlah Hadir ≥ 7")
    hadir_7plus_df = df_abs_com_pro_reg [df_abs_com_pro_reg ["Hadir"] >= 7]
    if hadir_7plus_df.empty:
        st.warning("Tidak ada mahasiswa yang hadir ≥ 7 kali")
    else:
        st.dataframe(hadir_7plus_df[["Nama_Mahasiswa", "Hadir", "Presentase", "Kategori Kehadiran"]],
                     use_container_width=True)

def analisa_statistik_kehadiran_oop_reg(df_abs_oop_reg):
    st.subheader("📊 Analisa Kehadiran: Communication Protocols")

    # Pastikan kolom numerik
    df_abs_oop_reg ["Presentase"] = pd.to_numeric(df_abs_oop_reg ["Presentase"], errors="coerce")
    df_abs_oop_reg ["Hadir"] = pd.to_numeric(df_abs_oop_reg ["Hadir"], errors="coerce")
    df_abs_oop_reg ["Pertemuan"] = pd.to_numeric(df_abs_oop_reg ["Pertemuan"], errors="coerce")

    # Tambahkan kategori kehadiran
    def kategori(p):
        if p == 100:
            return "Sangat Baik"
        elif p >= 75:
            return "Baik"
        elif p >= 60:
            return "Cukup"
        else:
            return "Kurang"
    df_abs_oop_reg ["Kategori Kehadiran"] = df_abs_oop_reg ["Presentase"].apply(kategori)

    # Statistik dasar
    rata2 = df_abs_oop_reg ["Presentase"].mean()
    jumlah_100 = (df_abs_oop_reg ["Presentase"] == 100).sum()
    distribusi = df_abs_oop_reg ["Kategori Kehadiran"].value_counts().reset_index()
    distribusi.columns = ["Kategori", "Jumlah"]

    # Metrik ringkas
    col1, col2 = st.columns(2)
    col1.metric("📌 Rata-rata Kehadiran", f"{rata2:.2f}%")
    col2.metric("✅ Jumlah Hadir 100%", f"{jumlah_100} Mahasiswa")

    # Tabel utama
    st.write("### 📋 Tabel Kehadiran Mahasiswa")
    st.dataframe(df_abs_oop_reg [["Nama_Mahasiswa", "Pertemuan", "Hadir", "Presentase", "Kategori Kehadiran"]],
                 use_container_width=True)

    # Grafik batang jumlah hadir
    st.write("### 📈 Grafik Jumlah Kehadiran per Mahasiswa")
    fig_hadir = px.bar(
        df_abs_oop_reg ,
        x="Nama_Mahasiswa",
        y="Hadir",
        text="Hadir",
        title="Jumlah Kehadiran per Mahasiswa",
        color="Kategori Kehadiran",
        labels={"Hadir": "Jumlah Hadir"},
    )
    fig_hadir.update_layout(xaxis_tickangle=-45)
    fig_hadir.update_traces(textposition="outside")
    st.plotly_chart(fig_hadir, use_container_width=True, key="grafik_kehadiran_oop")

    # Distribusi Kategori Kehadiran
    st.write("### 📊 Distribusi Kategori Kehadiran")
    col_a, col_b = st.columns(2)
    with col_a:
        fig_bar = px.bar(distribusi, x="Kategori", y="Jumlah", text="Jumlah", color="Kategori")
        fig_bar.update_traces(textposition="outside")
        st.plotly_chart(fig_bar, use_container_width=True, key="bar_kehadiran_oop")
    with col_b:
        fig_pie = px.pie(distribusi, names="Kategori", values="Jumlah")
        st.plotly_chart(fig_pie, use_container_width=True, key="pie_kehadiran_oop")

    # Mahasiswa dengan presentase = 0
    st.write("### 🚨 Mahasiswa dengan Kehadiran 0%")
    nol_df = df_abs_oop_reg [df_abs_oop_reg ["Presentase"] == 0]
    if nol_df.empty:
        st.success("Tidak ada mahasiswa dengan kehadiran 0%")
    else:
        st.error(f"Ada {len(nol_df)} mahasiswa dengan kehadiran 0%:")
        st.dataframe(nol_df[["Nama_Mahasiswa", "Pertemuan", "Hadir", "Presentase"]])

    # Mahasiswa hadir ≥ 7
    st.write("### 📗 Mahasiswa dengan Jumlah Hadir ≥ 7")
    hadir_7plus_df = df_abs_oop_reg [df_abs_oop_reg ["Hadir"] >= 7]
    if hadir_7plus_df.empty:
        st.warning("Tidak ada mahasiswa yang hadir ≥ 7 kali")
    else:
        st.dataframe(hadir_7plus_df[["Nama_Mahasiswa", "Hadir", "Presentase", "Kategori Kehadiran"]],
                     use_container_width=True)



def analisa_statistik_kehadiran_wcd_reg(df_abs_wcd_reg):
    st.subheader("📊 Analisa Kehadiran: Communication Protocols")

    # Pastikan kolom numerik
    df_abs_wcd_reg ["Presentase"] = pd.to_numeric(df_abs_wcd_reg ["Presentase"], errors="coerce")
    df_abs_wcd_reg ["Hadir"] = pd.to_numeric(df_abs_wcd_reg ["Hadir"], errors="coerce")
    df_abs_wcd_reg ["Pertemuan"] = pd.to_numeric(df_abs_wcd_reg ["Pertemuan"], errors="coerce")

    # Tambahkan kategori kehadiran
    def kategori(p):
        if p == 100:
            return "Sangat Baik"
        elif p >= 75:
            return "Baik"
        elif p >= 60:
            return "Cukup"
        else:
            return "Kurang"
    df_abs_wcd_reg ["Kategori Kehadiran"] = df_abs_wcd_reg ["Presentase"].apply(kategori)

    # Statistik dasar
    rata2 = df_abs_wcd_reg ["Presentase"].mean()
    jumlah_100 = (df_abs_wcd_reg ["Presentase"] == 100).sum()
    distribusi = df_abs_wcd_reg ["Kategori Kehadiran"].value_counts().reset_index()
    distribusi.columns = ["Kategori", "Jumlah"]

    # Metrik ringkas
    col1, col2 = st.columns(2)
    col1.metric("📌 Rata-rata Kehadiran", f"{rata2:.2f}%")
    col2.metric("✅ Jumlah Hadir 100%", f"{jumlah_100} Mahasiswa")

    # Tabel utama
    st.write("### 📋 Tabel Kehadiran Mahasiswa")
    st.dataframe(df_abs_wcd_reg [["Nama_Mahasiswa", "Pertemuan", "Hadir", "Presentase", "Kategori Kehadiran"]],
                 use_container_width=True)

    # Grafik batang jumlah hadir
    st.write("### 📈 Grafik Jumlah Kehadiran per Mahasiswa")
    fig_hadir = px.bar(
        df_abs_wcd_reg ,
        x="Nama_Mahasiswa",
        y="Hadir",
        text="Hadir",
        title="Jumlah Kehadiran per Mahasiswa",
        color="Kategori Kehadiran",
        labels={"Hadir": "Jumlah Hadir"},
    )
    fig_hadir.update_layout(xaxis_tickangle=-45)
    fig_hadir.update_traces(textposition="outside")
    st.plotly_chart(fig_hadir, use_container_width=True,key="grafik_kehadiran_wcd")

    # Distribusi Kategori Kehadiran
    st.write("### 📊 Distribusi Kategori Kehadiran")
    col_a, col_b = st.columns(2)
    with col_a:
        fig_bar = px.bar(distribusi, x="Kategori", y="Jumlah", text="Jumlah", color="Kategori")
        fig_bar.update_traces(textposition="outside")
        st.plotly_chart(fig_bar, use_container_width=True, key="bar_kehadiran_wcd")
    with col_b:
        fig_pie = px.pie(distribusi, names="Kategori", values="Jumlah")
        st.plotly_chart(fig_pie, use_container_width=True, key="pie_kehadiran_wcd")

    # Mahasiswa dengan presentase = 0
    st.write("### 🚨 Mahasiswa dengan Kehadiran 0%")
    nol_df = df_abs_wcd_reg [df_abs_wcd_reg ["Presentase"] == 0]
    if nol_df.empty:
        st.success("Tidak ada mahasiswa dengan kehadiran 0%")
    else:
        st.error(f"Ada {len(nol_df)} mahasiswa dengan kehadiran 0%:")
        st.dataframe(nol_df[["Nama_Mahasiswa", "Pertemuan", "Hadir", "Presentase"]])

    # Mahasiswa hadir ≥ 7
    st.write("### 📗 Mahasiswa dengan Jumlah Hadir ≥ 7")
    hadir_7plus_df = df_abs_wcd_reg [df_abs_wcd_reg ["Hadir"] >= 7]
    if hadir_7plus_df.empty:
        st.warning("Tidak ada mahasiswa yang hadir ≥ 7 kali")
    else:
        st.dataframe(hadir_7plus_df[["Nama_Mahasiswa", "Hadir", "Presentase", "Kategori Kehadiran"]],
                     use_container_width=True)

def analisa_statistik_kehadiran_dbs_reg(df_abs_dbs_reg):
    st.subheader("📊 Analisa Kehadiran: Communication Protocols")

    # Pastikan kolom numerik
    df_abs_dbs_reg ["Presentase"] = pd.to_numeric(df_abs_dbs_reg ["Presentase"], errors="coerce")
    df_abs_dbs_reg ["Hadir"] = pd.to_numeric(df_abs_dbs_reg ["Hadir"], errors="coerce")
    df_abs_dbs_reg ["Pertemuan"] = pd.to_numeric(df_abs_dbs_reg ["Pertemuan"], errors="coerce")

    # Tambahkan kategori kehadiran
    def kategori(p):
        if p == 100:
            return "Sangat Baik"
        elif p >= 75:
            return "Baik"
        elif p >= 60:
            return "Cukup"
        else:
            return "Kurang"
    df_abs_dbs_reg ["Kategori Kehadiran"] = df_abs_dbs_reg ["Presentase"].apply(kategori)

    # Statistik dasar
    rata2 = df_abs_dbs_reg ["Presentase"].mean()
    jumlah_100 = (df_abs_dbs_reg ["Presentase"] == 100).sum()
    distribusi = df_abs_dbs_reg ["Kategori Kehadiran"].value_counts().reset_index()
    distribusi.columns = ["Kategori", "Jumlah"]

    # Metrik ringkas
    col1, col2 = st.columns(2)
    col1.metric("📌 Rata-rata Kehadiran", f"{rata2:.2f}%")
    col2.metric("✅ Jumlah Hadir 100%", f"{jumlah_100} Mahasiswa")

    # Tabel utama
    st.write("### 📋 Tabel Kehadiran Mahasiswa")
    st.dataframe(df_abs_dbs_reg [["Nama_Mahasiswa", "Pertemuan", "Hadir", "Presentase", "Kategori Kehadiran"]],
                 use_container_width=True)

    # Grafik batang jumlah hadir
    st.write("### 📈 Grafik Jumlah Kehadiran per Mahasiswa")
    fig_hadir = px.bar(
        df_abs_wcd_reg ,
        x="Nama_Mahasiswa",
        y="Hadir",
        text="Hadir",
        title="Jumlah Kehadiran per Mahasiswa",
        color="Kategori Kehadiran",
        labels={"Hadir": "Jumlah Hadir"},
    )
    fig_hadir.update_layout(xaxis_tickangle=-45)
    fig_hadir.update_traces(textposition="outside")
    st.plotly_chart(fig_hadir, use_container_width=True,key="grafik_kehadiran_dbs")

    # Distribusi Kategori Kehadiran
    st.write("### 📊 Distribusi Kategori Kehadiran")
    col_a, col_b = st.columns(2)
    with col_a:
        fig_bar = px.bar(distribusi, x="Kategori", y="Jumlah", text="Jumlah", color="Kategori")
        fig_bar.update_traces(textposition="outside")
        st.plotly_chart(fig_bar, use_container_width=True, key="bar_kehadiran_dbs")
    with col_b:
        fig_pie = px.pie(distribusi, names="Kategori", values="Jumlah")
        st.plotly_chart(fig_pie, use_container_width=True, key="pie_kehadiran_dbs")

    # Mahasiswa dengan presentase = 0
    st.write("### 🚨 Mahasiswa dengan Kehadiran 0%")
    nol_df = df_abs_dbs_reg [df_abs_dbs_reg ["Presentase"] == 0]
    if nol_df.empty:
        st.success("Tidak ada mahasiswa dengan kehadiran 0%")
    else:
        st.error(f"Ada {len(nol_df)} mahasiswa dengan kehadiran 0%:")
        st.dataframe(nol_df[["Nama_Mahasiswa", "Pertemuan", "Hadir", "Presentase"]])

    # Mahasiswa hadir ≥ 7
    st.write("### 📗 Mahasiswa dengan Jumlah Hadir ≥ 7")
    hadir_7plus_df = df_abs_dbs_reg [df_abs_dbs_reg ["Hadir"] >= 7]
    if hadir_7plus_df.empty:
        st.warning("Tidak ada mahasiswa yang hadir ≥ 7 kali")
    else:
        st.dataframe(hadir_7plus_df[["Nama_Mahasiswa", "Hadir", "Presentase", "Kategori Kehadiran"]],
                     use_container_width=True)


def analisa_statistik_kehadiran_ds_reg(df_abs_ds_reg):
    st.subheader("📊 Analisa Kehadiran: Communication Protocols")

    # Pastikan kolom numerik
    df_abs_ds_reg["Presentase"] = pd.to_numeric(df_abs_ds_reg["Presentase"], errors="coerce")
    df_abs_ds_reg["Hadir"] = pd.to_numeric(df_abs_ds_reg["Hadir"], errors="coerce")
    df_abs_ds_reg["Pertemuan"] = pd.to_numeric(df_abs_ds_reg["Pertemuan"], errors="coerce")

    # Tambahkan kategori kehadiran
    def kategori(p):
        if p == 100:
            return "Sangat Baik"
        elif p >= 75:
            return "Baik"
        elif p >= 60:
            return "Cukup"
        else:
            return "Kurang"
    df_abs_ds_reg["Kategori Kehadiran"] = df_abs_ds_reg["Presentase"].apply(kategori)

    # Statistik dasar
    rata2 = df_abs_ds_reg["Presentase"].mean()
    jumlah_100 = (df_abs_ds_reg["Presentase"] == 100).sum()
    distribusi = df_abs_ds_reg["Kategori Kehadiran"].value_counts().reset_index()
    distribusi.columns = ["Kategori", "Jumlah"]

    # Metrik ringkas
    col1, col2 = st.columns(2)
    col1.metric("📌 Rata-rata Kehadiran", f"{rata2:.2f}%")
    col2.metric("✅ Jumlah Hadir 100%", f"{jumlah_100} Mahasiswa")

    # Tabel utama
    st.write("### 📋 Tabel Kehadiran Mahasiswa")
    st.dataframe(df_abs_ds_reg[["Nama_Mahasiswa", "Pertemuan", "Hadir", "Presentase", "Kategori Kehadiran"]],
                 use_container_width=True)

    # Grafik batang jumlah hadir
    st.write("### 📈 Grafik Jumlah Kehadiran per Mahasiswa")
    fig_hadir = px.bar(
        df_abs_ds_reg,
        x="Nama_Mahasiswa",
        y="Hadir",
        text="Hadir",
        title="Jumlah Kehadiran per Mahasiswa",
        color="Kategori Kehadiran",
        labels={"Hadir": "Jumlah Hadir"},
    )
    fig_hadir.update_layout(xaxis_tickangle=-45)
    fig_hadir.update_traces(textposition="outside")
    st.plotly_chart(fig_hadir, use_container_width=True, key="grafik_kehadiran_ds")

    # Distribusi Kategori Kehadiran
    st.write("### 📊 Distribusi Kategori Kehadiran")
    col_a, col_b = st.columns(2)
    with col_a:
        fig_bar = px.bar(distribusi, x="Kategori", y="Jumlah", text="Jumlah", color="Kategori")
        fig_bar.update_traces(textposition="outside")
        st.plotly_chart(fig_bar, use_container_width=True, key="bar_kehadiran_ds")
    with col_b:
        fig_pie = px.pie(distribusi, names="Kategori", values="Jumlah")
        st.plotly_chart(fig_pie, use_container_width=True, key="pie_kehadiran_ds")

    # Mahasiswa dengan presentase = 0
    st.write("### 🚨 Mahasiswa dengan Kehadiran 0%")
    nol_df = df_abs_ds_reg[df_abs_ds_reg["Presentase"] == 0]
    if nol_df.empty:
        st.success("Tidak ada mahasiswa dengan kehadiran 0%")
    else:
        st.error(f"Ada {len(nol_df)} mahasiswa dengan kehadiran 0%:")
        st.dataframe(nol_df[["Nama_Mahasiswa", "Pertemuan", "Hadir", "Presentase"]])

    # Mahasiswa hadir ≥ 7
    st.write("### 📗 Mahasiswa dengan Jumlah Hadir ≥ 7")
    hadir_7plus_df = df_abs_ds_reg[df_abs_ds_reg["Hadir"] >= 7]
    if hadir_7plus_df.empty:
        st.warning("Tidak ada mahasiswa yang hadir ≥ 7 kali")
    else:
        st.dataframe(hadir_7plus_df[["Nama_Mahasiswa", "Hadir", "Presentase", "Kategori Kehadiran"]],
                     use_container_width=True)

def analisa_statistik_kehadiran_sta_reg(df_abs_sta_reg):
    st.subheader("📊 Analisa Kehadiran: Communication Protocols")

    # Pastikan kolom numerik
    df_abs_sta_reg["Presentase"] = pd.to_numeric(df_abs_sta_reg["Presentase"], errors="coerce")
    df_abs_sta_reg["Hadir"] = pd.to_numeric(df_abs_sta_reg["Hadir"], errors="coerce")
    df_abs_sta_reg["Pertemuan"] = pd.to_numeric(df_abs_sta_reg["Pertemuan"], errors="coerce")

    # Tambahkan kategori kehadiran
    def kategori(p):
        if p == 100:
            return "Sangat Baik"
        elif p >= 75:
            return "Baik"
        elif p >= 60:
            return "Cukup"
        else:
            return "Kurang"
    df_abs_sta_reg["Kategori Kehadiran"] = df_abs_sta_reg["Presentase"].apply(kategori)

    # Statistik dasar
    rata2 = df_abs_sta_reg["Presentase"].mean()
    jumlah_100 = (df_abs_sta_reg["Presentase"] == 100).sum()
    distribusi = df_abs_sta_reg["Kategori Kehadiran"].value_counts().reset_index()
    distribusi.columns = ["Kategori", "Jumlah"]

    # Metrik ringkas
    col1, col2 = st.columns(2)
    col1.metric("📌 Rata-rata Kehadiran", f"{rata2:.2f}%")
    col2.metric("✅ Jumlah Hadir 100%", f"{jumlah_100} Mahasiswa")

    # Tabel utama
    st.write("### 📋 Tabel Kehadiran Mahasiswa")
    st.dataframe(df_abs_sta_reg[["Nama_Mahasiswa", "Pertemuan", "Hadir", "Presentase", "Kategori Kehadiran"]],
                 use_container_width=True)

    # Grafik batang jumlah hadir
    st.write("### 📈 Grafik Jumlah Kehadiran per Mahasiswa")
    fig_hadir = px.bar(
        df_abs_sta_reg,
        x="Nama_Mahasiswa",
        y="Hadir",
        text="Hadir",
        title="Jumlah Kehadiran per Mahasiswa",
        color="Kategori Kehadiran",
        labels={"Hadir": "Jumlah Hadir"},
    )
    fig_hadir.update_layout(xaxis_tickangle=-45)
    fig_hadir.update_traces(textposition="outside")
    st.plotly_chart(fig_hadir, use_container_width=True, key="grafik_kehadiran_sta")

    # Distribusi Kategori Kehadiran
    st.write("### 📊 Distribusi Kategori Kehadiran")
    col_a, col_b = st.columns(2)
    with col_a:
        fig_bar = px.bar(distribusi, x="Kategori", y="Jumlah", text="Jumlah", color="Kategori")
        fig_bar.update_traces(textposition="outside")
        st.plotly_chart(fig_bar, use_container_width=True, key="bar_kehadiran_sta")
    with col_b:
        fig_pie = px.pie(distribusi, names="Kategori", values="Jumlah")
        st.plotly_chart(fig_pie, use_container_width=True, key="pie_kehadiran_sta")

    # Mahasiswa dengan presentase = 0
    st.write("### 🚨 Mahasiswa dengan Kehadiran 0%")
    nol_df = df_abs_sta_reg[df_abs_sta_reg["Presentase"] == 0]
    if nol_df.empty:
        st.success("Tidak ada mahasiswa dengan kehadiran 0%")
    else:
        st.error(f"Ada {len(nol_df)} mahasiswa dengan kehadiran 0%:")
        st.dataframe(nol_df[["Nama_Mahasiswa", "Pertemuan", "Hadir", "Presentase"]])

    # Mahasiswa hadir ≥ 7
    st.write("### 📗 Mahasiswa dengan Jumlah Hadir ≥ 7")
    hadir_7plus_df = df_abs_sta_reg[df_abs_sta_reg["Hadir"] >= 7]
    if hadir_7plus_df.empty:
        st.warning("Tidak ada mahasiswa yang hadir ≥ 7 kali")
    else:
        st.dataframe(hadir_7plus_df[["Nama_Mahasiswa", "Hadir", "Presentase", "Kategori Kehadiran"]],
                     use_container_width=True)

def analisa_statistik_kehadiran_dw_reg(df_abs_dw_reg):
    st.subheader("📊 Analisa Kehadiran: Communication Protocols")

    # Pastikan kolom numerik
    df_abs_dw_reg["Presentase"] = pd.to_numeric(df_abs_dw_reg["Presentase"], errors="coerce")
    df_abs_dw_reg["Hadir"] = pd.to_numeric(df_abs_dw_reg["Hadir"], errors="coerce")
    df_abs_dw_reg["Pertemuan"] = pd.to_numeric(df_abs_dw_reg["Pertemuan"], errors="coerce")

    # Tambahkan kategori kehadiran
    def kategori(p):
        if p == 100:
            return "Sangat Baik"
        elif p >= 75:
            return "Baik"
        elif p >= 60:
            return "Cukup"
        else:
            return "Kurang"
    df_abs_dw_reg["Kategori Kehadiran"] = df_abs_dw_reg["Presentase"].apply(kategori)

    # Statistik dasar
    rata2 = df_abs_dw_reg["Presentase"].mean()
    jumlah_100 = (df_abs_dw_reg["Presentase"] == 100).sum()
    distribusi = df_abs_dw_reg["Kategori Kehadiran"].value_counts().reset_index()
    distribusi.columns = ["Kategori", "Jumlah"]

    # Metrik ringkas
    col1, col2 = st.columns(2)
    col1.metric("📌 Rata-rata Kehadiran", f"{rata2:.2f}%")
    col2.metric("✅ Jumlah Hadir 100%", f"{jumlah_100} Mahasiswa")

    # Tabel utama
    st.write("### 📋 Tabel Kehadiran Mahasiswa")
    st.dataframe(df_abs_dw_reg[["Nama_Mahasiswa", "Pertemuan", "Hadir", "Presentase", "Kategori Kehadiran"]],
                 use_container_width=True)

    # Grafik batang jumlah hadir
    st.write("### 📈 Grafik Jumlah Kehadiran per Mahasiswa")
    fig_hadir = px.bar(
        df_abs_dw_reg,
        x="Nama_Mahasiswa",
        y="Hadir",
        text="Hadir",
        title="Jumlah Kehadiran per Mahasiswa",
        color="Kategori Kehadiran",
        labels={"Hadir": "Jumlah Hadir"},
    )
    fig_hadir.update_layout(xaxis_tickangle=-45)
    fig_hadir.update_traces(textposition="outside")
    st.plotly_chart(fig_hadir, use_container_width=True, key="grafik_kehadiran_dw")

    # Distribusi Kategori Kehadiran
    st.write("### 📊 Distribusi Kategori Kehadiran")
    col_a, col_b = st.columns(2)
    with col_a:
        fig_bar = px.bar(distribusi, x="Kategori", y="Jumlah", text="Jumlah", color="Kategori")
        fig_bar.update_traces(textposition="outside")
        st.plotly_chart(fig_bar, use_container_width=True, key="bar_kehadiran_dw")
    with col_b:
        fig_pie = px.pie(distribusi, names="Kategori", values="Jumlah")
        st.plotly_chart(fig_pie, use_container_width=True, key="pie_kehadiran_dw")

    # Mahasiswa dengan presentase = 0
    st.write("### 🚨 Mahasiswa dengan Kehadiran 0%")
    nol_df = df_abs_dw_reg[df_abs_dw_reg["Presentase"] == 0]
    if nol_df.empty:
        st.success("Tidak ada mahasiswa dengan kehadiran 0%")
    else:
        st.error(f"Ada {len(nol_df)} mahasiswa dengan kehadiran 0%:")
        st.dataframe(nol_df[["Nama_Mahasiswa", "Pertemuan", "Hadir", "Presentase"]])

    # Mahasiswa hadir ≥ 7
    st.write("### 📗 Mahasiswa dengan Jumlah Hadir ≥ 7")
    hadir_7plus_df = df_abs_dw_reg[df_abs_dw_reg["Hadir"] >= 7]
    if hadir_7plus_df.empty:
        st.warning("Tidak ada mahasiswa yang hadir ≥ 7 kali")
    else:
        st.dataframe(hadir_7plus_df[["Nama_Mahasiswa", "Hadir", "Presentase", "Kategori Kehadiran"]],
                     use_container_width=True)

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

def statistik_visualisasi_mahasiswa_reguler(df_mhs_reg):
    st.title("📊 Data Mahasiswa Reguler Sains Data")

    # Menampilkan seluruh data mahasiswa
    st.subheader("📋 Seluruh Data Mahasiswa")
    st.dataframe(df_mhs_reg)

    # Menampilkan total keseluruhan mahasiswa
    total_mahasiswa = len(df_mhs_reg)
    st.subheader("🔢 Total Mahasiswa")
    st.metric(label="Jumlah Mahasiswa", value=total_mahasiswa)

    # Visualisasi jumlah mahasiswa per angkatan
    st.subheader("📈 Jumlah Mahasiswa per Angkatan")
    fig1 = px.histogram(df_mhs_reg, x="Angkatan", color="Angkatan",
                        title="Distribusi Mahasiswa per Angkatan",
                        labels={"Angkatan": "Angkatan", "count": "Jumlah"},
                        category_orders={"Angkatan": sorted(df_mhs_reg['Angkatan'].unique())},
                        color_discrete_sequence=px.colors.sequential.Blues)
    st.plotly_chart(fig1)

    # Visualisasi jumlah mahasiswa per tahun masuk
    st.subheader("📊 Jumlah Mahasiswa per Tahun Masuk")
    fig2 = px.histogram(df_mhs_reg, x="Tahun", color="Tahun",
                        title="Distribusi Mahasiswa per Tahun Masuk",
                        labels={"Tahun": "Tahun Masuk", "count": "Jumlah"},
                        category_orders={"Tahun": sorted(df_mhs_reg['Tahun'].dropna().unique())},
                        color_discrete_sequence=px.colors.sequential.Greens)
    st.plotly_chart(fig2)

def tampilkan_statistik_mahasiswa(df_mhs_pro):
    st.title("📊 Statistik Data Mahasiswa Prodi Sains")

    # Menampilkan seluruh data mahasiswa
    st.subheader("📋 Data Mahasiswa")
    st.dataframe(df_mhs_pro)

    # Menampilkan total mahasiswa
    total = len(df_mhs_pro)
    st.metric("🎓 Total Mahasiswa", total)

    # Statistik deskriptif (jika ada kolom numerik)
    #st.subheader("📈 Statistik Deskriptif")
    #st.write(df_mhs_pro.describe(include='all'))

    # Visualisasi jumlah mahasiswa per angkatan
    if 'Angkatan' in df_mhs_pro.columns:
        st.subheader("📊 Distribusi Mahasiswa per Angkatan")
        fig1 = px.histogram(df_mhs_pro, x="Angkatan", color="Angkatan",
                            title="Jumlah Mahasiswa per Angkatan",
                            labels={"Angkatan": "Angkatan", "count": "Jumlah"},
                            category_orders={"Angkatan": sorted(df_mhs_pro['Angkatan'].dropna().unique())},
                            color_discrete_sequence=px.colors.sequential.Plasma)
        st.plotly_chart(fig1)

    # Visualisasi jumlah mahasiswa per tahun masuk
    if 'Tahun' in df_mhs_pro.columns:
        st.subheader("📊 Distribusi Mahasiswa per Tahun Masuk")
        fig2 = px.histogram(df_mhs_pro, x="Tahun", color="Tahun",
                            title="Jumlah Mahasiswa per Tahun Masuk",
                            labels={"Tahun": "Tahun Masuk", "count": "Jumlah"},
                            category_orders={"Tahun": sorted(df_mhs_pro['Tahun'].dropna().unique())},
                            color_discrete_sequence=px.colors.sequential.Teal)
        st.plotly_chart(fig2)
st.markdown("<h1 style='text-align: center; color: #4A6D8C;'>🎓 Analisa Nilai Program Studi Sains Data</h1>", unsafe_allow_html=True)
st.markdown("---")


# Menampilkan logo Universitas Cakrawala dan judul program studi di sidebar
import base64

# Encode logo menjadi base64 (jalankan hanya sekali)
with open("logo-cakrawala-black.png", "rb") as image_file:
    encoded = base64.b64encode(image_file.read()).decode()


st.sidebar.markdown(
    f"""
    <div style='text-align: center;'>
        <img src="data:image/png;base64,{encoded}" width="120">
        <h4 style='margin-top: 0;'>📘 Data Science Study Program</h4>
    </div>
    """,
    unsafe_allow_html=True
)

# ====== SIDEBAR MENU ======
menu = st.sidebar.selectbox("📂 Pilih Menu", ["Jumlah Mahasiswa","Kehadiran Mahasiswa", "Nilai UTS Mahasiswa", "Sentimen FeedBack Mahasiswa"])

# ====== Jumlah Seluruh Mahasiswa ======
if menu == "Jumlah Mahasiswa":
    st.title("📅 Total Mahasiswa")

    # Sub-menu kelas
    sub_kelas = st.radio("Pilih Kelas", ["Kelas Reguler", "Kelas Pro dan Aksel"])

    if sub_kelas == "Kelas Reguler":
        st.subheader("📘 Mahasiswa - Kelas Reguler")
        st.info("📌 Visualisasi Total Mahasiswa untuk kelas Reguler.")
        statistik_visualisasi_mahasiswa_reguler(df_mhs_reg)
    elif sub_kelas == "Kelas Pro dan Aksel":
        st.subheader("📗 Kehadiran - Kelas Pro dan Aksel")
        st.info("📌 Visualisasi Total Mahasiswa untuk kelas Pro dan Aksel belum tersedia. Data atau fitur bisa ditambahkan di sini.")
        tampilkan_statistik_mahasiswa(df_mhs_pro)

# ====== KEHADIRAN ======
elif menu == "Kehadiran Mahasiswa":
    st.title("📅 Kehadiran Mahasiswa")

    # Sub-menu kelas
    sub_kelas = st.radio("Pilih Kelas", ["Kelas Reguler", "Kelas Pro dan Aksel"])

    if sub_kelas == "Kelas Reguler":
        st.subheader("📘 Kehadiran - Kelas Reguler")

        tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
            "Communication Protocols", 
            "Web Client Development", 
            "Object Oriented Programming",
            "Data Structures", 
            "Database Systems",
            "Statistical Thinking",
            "Data Wrangling"
        ])

        with tab1:
            analisa_statistik_kehadiran_com_pro_reg(df_abs_com_pro_reg)

        with tab2:
            analisa_statistik_kehadiran_wcd_reg(df_abs_wcd_reg)

        with tab3:
            analisa_statistik_kehadiran_oop_reg(df_abs_oop_reg)

        with tab4:
            analisa_statistik_kehadiran_ds_reg(df_abs_ds_reg)

        with tab5:
            analisa_statistik_kehadiran_dbs_reg(df_abs_dbs_reg)
        
        with tab6:
            analisa_statistik_kehadiran_sta_reg(df_abs_sta_reg)

        with tab7:
            analisa_statistik_kehadiran_dw_reg(df_abs_dw_reg)
                
        

    elif sub_kelas == "Kelas Pro dan Aksel":
        st.subheader("📗 Kehadiran - Kelas Pro dan Aksel")
        st.info("📌 Visualisasi kehadiran untuk kelas Pro dan Aksel belum tersedia. Data atau fitur bisa ditambahkan di sini.")

# ====== NILAI UTS ======
elif menu == "Nilai UTS Mahasiswa":
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

elif menu == "Sentimen FeedBack Mahasiswa":
    st.title("📅 Sentimen FeedBack Mahasiswa")

    # Sub-menu kelas
    sub_kelas = st.radio("Pilih Kelas", ["Kelas Reguler", "Kelas Pro dan Aksel"])

    if sub_kelas == "Kelas Reguler":
        st.subheader("📘 Kehadiran - Kelas Reguler")

        tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
            "Communication Protocols", 
            "Web Client Development", 
            "Object Oriented Programming",
            "Data Structures", 
            "Database Systems",
            "Statistical Thinking",
            "Data Wrangling"
        ])

        with tab1:
            analisa_statistik_kehadiran_com_pro_reg(df_abs_com_pro_reg)

        with tab2:
            analisa_statistik_kehadiran_wcd_reg(df_abs_wcd_reg)

        with tab3:
            analisa_statistik_kehadiran_oop_reg(df_abs_oop_reg)

        with tab4:
            analisa_statistik_kehadiran_ds_reg(df_abs_ds_reg)

        with tab5:
            analisa_statistik_kehadiran_dbs_reg(df_abs_dbs_reg)
        
        with tab6:
            analisa_statistik_kehadiran_sta_reg(df_abs_sta_reg)

        with tab7:
            analisa_statistik_kehadiran_dw_reg(df_abs_dw_reg)
                
        

    elif sub_kelas == "Kelas Pro dan Aksel":
        st.subheader("📗 Kehadiran - Kelas Pro dan Aksel")
        st.info("📌 Visualisasi kehadiran untuk kelas Pro dan Aksel belum tersedia. Data atau fitur bisa ditambahkan di sini.")


# ====== FOOTER ======
st.markdown("---", unsafe_allow_html=True)
st.markdown(
    """
    <div style='text-align: center; color: grey; font-size: 14px;'>
        Developed by <b>Adam Puspabhuana, M.Kom</b> (Data Science) &nbsp; | &nbsp; © 2025<br>
        <a href="https://www.linkedin.com/in/adam-puspabhuana-75a94a10/" target="_blank" style='text-decoration: none; color: #0e76a8;'>
            🔗 LinkedIn
        </a>
    </div>
    """,
    unsafe_allow_html=True
)