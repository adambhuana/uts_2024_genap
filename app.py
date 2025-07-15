# Tambahkan import
import pandas as pd
import plotly.express as px
import streamlit as st
import seaborn as sns
import matplotlib as plt
import matplotlib.pyplot as plt
import csv
from collections import Counter
from lib_sentimen import sentistrength, config

# Set page config harus paling atas sebelum Streamlit command lain
st.set_page_config(page_title='Analisis Sentimen Komentar',
                   layout='wide',
                   initial_sidebar_state='expanded')
def login():
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    if not st.session_state.logged_in:
        st.title("🔐 Login Dosen Prodi Sains Data Semester Genap 2024")
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
                # Tambahan footer
        st.markdown("""
        <div style='text-align: center; color: grey; font-size: 14px; margin-top: 20px;'>
            Developed by <b>Adam Puspabhuana, M.Kom</b> (Data Scientist) &nbsp; | &nbsp; © 2025<br>
            <a href='https://www.linkedin.com/in/adam-puspabhuana-75a94a10/' target='_blank' style='text-decoration: none; color: #0e76a8;'>
                🔗 LinkedIn
            </a>
        </div>
        """, unsafe_allow_html=True)

        st.stop()
login()

if st.sidebar.button("🔓 Logout"):
    st.session_state.logged_in = False
    st.rerun()
# Inisialisasi Sentistrength
senti = sentistrength(config)
# File CSV
DATA_PATH_DBS = "komentar_dbs_reguler.csv"
DATA_PATH_CP = "komentar_cp_reguler.csv"
DATA_PATH_CP_PRO = "komentar_cp_pros.csv"
DATA_PATH_WCD = "komentar_wcd_reguler.csv"
DATA_PATH_WCD_PRO = "komentar_wcd_pros.csv"
DATA_PATH_OOP = "komentar_oop_reguler.csv"
DATA_PATH_DS = "komentar_ds_reguler.csv"
DATA_PATH_STA = "komentar_sta_reguler.csv"
DATA_PATH_DW = "komentar_dw_reguler.csv"

df_profil=pd.read_csv("profil_lulusan.csv")
df_dosen = pd.read_csv("soal_dosen.csv")
df_dosen_uas = pd.read_csv("soal_dosen_uas.csv")
df_abs_dosen = pd.read_csv("abs_dos_reguler.csv")
df_abs_dosen_pro = pd.read_csv("abs_dos_pro.csv")
df_reguler = pd.read_csv("uts_reguler_sains_data.csv",dtype={'NIM': str, 'Tahun': str})
df_tugas_reguler = pd.read_csv("tugas_reg_sains_data.csv",dtype={'NIM': str, 'Tahun': str})
df_kuis_reguler = pd.read_csv("kuis_reg_sains_data.csv",dtype={'NIM': str, 'Tahun': str})
df_akhir_ds_reg = pd.read_csv("akhir_ds_reg_sains_data.csv",dtype={'NIM': str, 'Tahun': str})
df_pro = pd.read_csv("uts_pro_sains_data.csv",dtype={'NIM': str, 'Tahun': str})
df_abs_com_pro_reg = pd.read_csv("absensi_com_pro_reguler_sains_data.csv")
df_abs_com_pro_pros = pd.read_csv("absensi_com_pro_pros_sains_data.csv")
df_abs_ds_reg = pd.read_csv("absensi_ds_reguler_sains_data.csv")
df_abs_ds_pros = pd.read_csv("absensi_ds_pros_sains_data.csv")
df_abs_wcd_reg = pd.read_csv("absensi_wcd_reguler_sains_data.csv")
df_abs_wcd_pros = pd.read_csv("absensi_wcd_pros_sains_data.csv")
df_abs_oop_reg = pd.read_csv("absensi_oop_reguler_sains_data.csv")
df_abs_oop_pros = pd.read_csv("absensi_oop_pros_sains_data.csv")
df_abs_dbs_reg = pd.read_csv("absensi_dbs_reguler_sains_data.csv")
df_abs_dbs_pros = pd.read_csv("absensi_dbs_pros_sains_data.csv")
df_abs_sta_reg = pd.read_csv("absensi_sta_reguler_sains_data.csv")
df_abs_sta_pros = pd.read_csv("absensi_sta_pros_sains_data.csv")
df_abs_dw_reg = pd.read_csv("absensi_dw_reguler_sains_data.csv")
df_abs_dw_pros = pd.read_csv("absensi_dw_pros_sains_data.csv")
#df_senti_dbs_reg = pd.read_csv("komentar_dbs_reguler.csv",dtype={'NIM': str})
df_mhs_reg = pd.read_csv("total_mhs_reguler_sains_data.csv", dtype={'NIM': str, 'Tahun': str})
df_mhs_pro = pd.read_csv("total_mhs_pro_sains_data.csv", dtype={'NIM': str, 'Tahun': str})

import pandas as pd
import plotly.express as px
import streamlit as st
import streamlit.components.v1 as components

def display_html_file(html_path: str = None, uploaded_file=None, height=1000):
    """
    Menampilkan file HTML di Streamlit.
    
    Parameter:
    - html_path: path ke file HTML lokal (opsional)
    - uploaded_file: file uploader dari Streamlit (opsional)
    - height: tinggi tampilan iframe HTML (default: 1000px)
    """
    if uploaded_file is not None:
        # Jika pengguna mengupload file
        html_content = uploaded_file.read().decode("utf-8")
        components.html(html_content, height=height, scrolling=True)

    elif html_path:
        try:
            with open(html_path, 'r', encoding='utf-8') as f:
                html_content = f.read()
            components.html(html_content, height=height, scrolling=True)
        except FileNotFoundError:
            st.error(f"❌ File tidak ditemukan: {html_path}")
    else:
        st.warning("⚠️ Tidak ada file HTML yang diberikan.")

def tampilan_profil_lulusan(df_profil):
    st.title("🎓 Profil Lulusan Prodi Sains Data")
    st.markdown("Berikut adalah daftar profil lulusan yang disesuaikan dengan level KKNI:")
    st.dataframe(df_profil, use_container_width=True)

    st.markdown("---")
    st.write("📌 **Sumber Acuan:**")
    sumber_unik = df_profil['Sumber'].unique()
    for sumber in sumber_unik:
        st.info(f"- {sumber}")

def analisa_statistik_akhir_ds_reg(df_akhir_ds_reg):
     # Bersihkan dan siapkan kolom Lulus
    df_akhir_ds_reg["Lulus"] = df_akhir_ds_reg["Lulus"].fillna("❌")  # Replace NaN dengan tanda silang
    df_akhir_ds_reg["Lulus"] = df_akhir_ds_reg["Lulus"].replace("✔", "✅")  # Pastikan ✔ jadi simbol yang konsisten

    # Tampilkan judul
    st.title("📊 Statistik Nilai Mahasiswa - Sains Data")

    st.header("📋 Data Awal")
    # Format HTML untuk warna silang merah
    def highlight_lulus(val):
        if val == "❌":
            return f'<span style="color:red; font-weight:bold;">{val}</span>'
        elif val == "✅":
            return f'<span style="color:green; font-weight:bold;">{val}</span>'
        return val

    # Buat salinan untuk styling
    df_styled = df_akhir_ds_reg.copy()
    df_styled["Lulus"] = df_styled["Lulus"].apply(highlight_lulus)

    # Tampilkan tabel dengan HTML
    st.markdown(df_styled.to_html(escape=False, index=False), unsafe_allow_html=True)

    # Statistik deskriptif
    st.header("📈 Statistik Deskriptif")
    st.write(df_akhir_ds_reg.describe())

    # Distribusi nilai akhir
    st.subheader("📊 Distribusi Nilai Akhir")
    fig, ax = plt.subplots()
    sns.histplot(df_akhir_ds_reg["Nilai"], kde=True, bins=10, ax=ax, color='skyblue')
    ax.set_xlabel("Nilai Akhir")
    ax.set_ylabel("Jumlah Mahasiswa")
    st.pyplot(fig)

    # Distribusi Grade
    st.subheader("🎓 Distribusi Grade")
    grade_counts = df_akhir_ds_reg["Grade"].value_counts().sort_index()
    st.bar_chart(grade_counts)

    # Statistik kelulusan
    st.subheader("✅ Statistik Kelulusan")
    lulus_counts = df_akhir_ds_reg["Lulus"].value_counts()
    st.write(lulus_counts)

    # Pie Chart
    fig2, ax2 = plt.subplots()
    ax2.pie(lulus_counts, labels=lulus_counts.index, autopct='%1.1f%%', startangle=90, colors=['#4CAF50', '#FF5252'])
    ax2.axis('equal')
    st.pyplot(fig2)

    # Rata-rata per komponen
    st.header("📌 Rata-Rata Nilai per Komponen")
    components = ["QUIZ (20 %)", "UTS (20 %)", "UAS (40 %)", "TUGAS 1 (10 %)", "TUGAS 2 (10 %)"]
    avg_scores = df_akhir_ds_reg[components].mean()
    st.bar_chart(avg_scores)

    # Mahasiswa terbaik dan terendah
    st.header("🏅 Mahasiswa Terbaik & Terendah")
    st.subheader("🎖️ Nilai Tertinggi")
    st.dataframe(df_akhir_ds_reg[df_akhir_ds_reg["Nilai"] == df_akhir_ds_reg["Nilai"].max()][["Nama Mahasiswa", "Nilai", "Grade"]])

    st.subheader("🪫 Nilai Terendah")
    st.dataframe(df_akhir_ds_reg[df_akhir_ds_reg["Nilai"] == df_akhir_ds_reg["Nilai"].min()][["Nama Mahasiswa", "Nilai", "Grade"]])

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

def analisa_statistik_kehadiran_com_pro_pros(df_abs_com_pro_pros):
    st.subheader("📊 Analisa Kehadiran: Communication Protocols")

    # Pastikan kolom numerik
    df_abs_com_pro_pros ["Presentase"] = pd.to_numeric(df_abs_com_pro_pros ["Presentase"], errors="coerce")
    df_abs_com_pro_pros ["Hadir"] = pd.to_numeric(df_abs_com_pro_pros ["Hadir"], errors="coerce")
    df_abs_com_pro_pros ["Pertemuan"] = pd.to_numeric(df_abs_com_pro_pros ["Pertemuan"], errors="coerce")

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
    df_abs_com_pro_pros ["Kategori Kehadiran"] = df_abs_com_pro_pros ["Presentase"].apply(kategori)

    # Statistik dasar
    rata2 = df_abs_com_pro_pros ["Presentase"].mean()
    jumlah_100 = (df_abs_com_pro_pros ["Presentase"] == 100).sum()
    distribusi = df_abs_com_pro_pros ["Kategori Kehadiran"].value_counts().reset_index()
    distribusi.columns = ["Kategori", "Jumlah"]

    # Metrik ringkas
    col1, col2 = st.columns(2)
    col1.metric("📌 Rata-rata Kehadiran", f"{rata2:.2f}%")
    col2.metric("✅ Jumlah Hadir 100%", f"{jumlah_100} Mahasiswa")

    # Tabel utama
    st.write("### 📋 Tabel Kehadiran Mahasiswa")
    st.dataframe(df_abs_com_pro_pros [["Nama_Mahasiswa", "Pertemuan", "Hadir", "Presentase", "Kategori Kehadiran"]],
                 use_container_width=True)

    # Grafik batang jumlah hadir
    st.write("### 📈 Grafik Jumlah Kehadiran per Mahasiswa")
    fig_hadir = px.bar(
        df_abs_com_pro_pros ,
        x="Nama_Mahasiswa",
        y="Hadir",
        text="Hadir",
        title="Jumlah Kehadiran per Mahasiswa",
        color="Kategori Kehadiran",
        labels={"Hadir": "Jumlah Hadir"},
    )
    fig_hadir.update_layout(xaxis_tickangle=-45)
    fig_hadir.update_traces(textposition="outside")
    st.plotly_chart(fig_hadir, use_container_width=True, key="grafik_kehadiran_cp_pro")

    # Distribusi Kategori Kehadiran
    st.write("### 📊 Distribusi Kategori Kehadiran")
    col_a, col_b = st.columns(2)
    with col_a:
        fig_bar = px.bar(distribusi, x="Kategori", y="Jumlah", text="Jumlah", color="Kategori")
        fig_bar.update_traces(textposition="outside")
        st.plotly_chart(fig_bar, use_container_width=True, key="bar_kehadiran_cp_pro")
    with col_b:
        fig_pie = px.pie(distribusi, names="Kategori", values="Jumlah")
        st.plotly_chart(fig_pie, use_container_width=True, key="piekehadiran_cp_pro")

    # Mahasiswa dengan presentase = 0
    st.write("### 🚨 Mahasiswa dengan Kehadiran 0%")
    nol_df = df_abs_com_pro_pros [df_abs_com_pro_pros ["Presentase"] == 0]
    if nol_df.empty:
        st.success("Tidak ada mahasiswa dengan kehadiran 0%")
    else:
        st.error(f"Ada {len(nol_df)} mahasiswa dengan kehadiran 0%:")
        st.dataframe(nol_df[["Nama_Mahasiswa", "Pertemuan", "Hadir", "Presentase"]])

    # Mahasiswa hadir ≥ 7
    st.write("### 📗 Mahasiswa dengan Jumlah Hadir ≥ 7")
    hadir_7plus_df = df_abs_com_pro_pros [df_abs_com_pro_pros ["Hadir"] >= 7]
    if hadir_7plus_df.empty:
        st.warning("Tidak ada mahasiswa yang hadir ≥ 7 kali")
    else:
        st.dataframe(hadir_7plus_df[["Nama_Mahasiswa", "Hadir", "Presentase", "Kategori Kehadiran"]],
                     use_container_width=True)


def analisa_statistik_kehadiran_oop_reg(df_abs_oop_reg):
    st.subheader("📊 Analisa Kehadiran: OOP")

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


def analisa_statistik_kehadiran_oop_pros(df_abs_oop_pros):
    st.subheader("📊 Analisa Kehadiran: OOP")

    # Pastikan kolom numerik
    df_abs_oop_pros ["Presentase"] = pd.to_numeric(df_abs_oop_pros ["Presentase"], errors="coerce")
    df_abs_oop_pros ["Hadir"] = pd.to_numeric(df_abs_oop_pros ["Hadir"], errors="coerce")
    df_abs_oop_pros ["Pertemuan"] = pd.to_numeric(df_abs_oop_pros ["Pertemuan"], errors="coerce")

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
    df_abs_oop_pros ["Kategori Kehadiran"] = df_abs_oop_pros ["Presentase"].apply(kategori)

    # Statistik dasar
    rata2 = df_abs_oop_pros ["Presentase"].mean()
    jumlah_100 = (df_abs_oop_pros ["Presentase"] == 100).sum()
    distribusi = df_abs_oop_pros ["Kategori Kehadiran"].value_counts().reset_index()
    distribusi.columns = ["Kategori", "Jumlah"]

    # Metrik ringkas
    col1, col2 = st.columns(2)
    col1.metric("📌 Rata-rata Kehadiran", f"{rata2:.2f}%")
    col2.metric("✅ Jumlah Hadir 100%", f"{jumlah_100} Mahasiswa")

    # Tabel utama
    st.write("### 📋 Tabel Kehadiran Mahasiswa")
    st.dataframe(df_abs_oop_pros [["Nama_Mahasiswa", "Pertemuan", "Hadir", "Presentase", "Kategori Kehadiran"]],
                 use_container_width=True)

    # Grafik batang jumlah hadir
    st.write("### 📈 Grafik Jumlah Kehadiran per Mahasiswa")
    fig_hadir = px.bar(
        df_abs_oop_pros ,
        x="Nama_Mahasiswa",
        y="Hadir",
        text="Hadir",
        title="Jumlah Kehadiran per Mahasiswa",
        color="Kategori Kehadiran",
        labels={"Hadir": "Jumlah Hadir"},
    )
    fig_hadir.update_layout(xaxis_tickangle=-45)
    fig_hadir.update_traces(textposition="outside")
    st.plotly_chart(fig_hadir, use_container_width=True, key="grafik_kehadiran_oop_pros")

    # Distribusi Kategori Kehadiran
    st.write("### 📊 Distribusi Kategori Kehadiran")
    col_a, col_b = st.columns(2)
    with col_a:
        fig_bar = px.bar(distribusi, x="Kategori", y="Jumlah", text="Jumlah", color="Kategori")
        fig_bar.update_traces(textposition="outside")
        st.plotly_chart(fig_bar, use_container_width=True, key="bar_kehadiran_oop_pros")
    with col_b:
        fig_pie = px.pie(distribusi, names="Kategori", values="Jumlah")
        st.plotly_chart(fig_pie, use_container_width=True, key="pie_kehadiran_oop_pros")

    # Mahasiswa dengan presentase = 0
    st.write("### 🚨 Mahasiswa dengan Kehadiran 0%")
    nol_df = df_abs_oop_pros [df_abs_oop_pros ["Presentase"] == 0]
    if nol_df.empty:
        st.success("Tidak ada mahasiswa dengan kehadiran 0%")
    else:
        st.error(f"Ada {len(nol_df)} mahasiswa dengan kehadiran 0%:")
        st.dataframe(nol_df[["Nama_Mahasiswa", "Pertemuan", "Hadir", "Presentase"]])

    # Mahasiswa hadir ≥ 7
    st.write("### 📗 Mahasiswa dengan Jumlah Hadir ≥ 7")
    hadir_7plus_df = df_abs_oop_pros [df_abs_oop_pros ["Hadir"] >= 7]
    if hadir_7plus_df.empty:
        st.warning("Tidak ada mahasiswa yang hadir ≥ 7 kali")
    else:
        st.dataframe(hadir_7plus_df[["Nama_Mahasiswa", "Hadir", "Presentase", "Kategori Kehadiran"]],
                     use_container_width=True)



def analisa_statistik_kehadiran_wcd_reg(df_abs_wcd_reg):
    st.subheader("📊 Analisa Kehadiran: WCD")

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

def analisa_statistik_kehadiran_wcd_pros(df_abs_wcd_pros):
    st.subheader("📊 Analisa Kehadiran: WCD")

    # Pastikan kolom numerik
    df_abs_wcd_pros ["Presentase"] = pd.to_numeric(df_abs_wcd_pros ["Presentase"], errors="coerce")
    df_abs_wcd_pros ["Hadir"] = pd.to_numeric(df_abs_wcd_pros ["Hadir"], errors="coerce")
    df_abs_wcd_pros ["Pertemuan"] = pd.to_numeric(df_abs_wcd_pros ["Pertemuan"], errors="coerce")

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
    df_abs_wcd_pros["Kategori Kehadiran"] = df_abs_wcd_pros["Presentase"].apply(kategori)

    # Statistik dasar
    rata2 = df_abs_wcd_pros["Presentase"].mean()
    jumlah_100 = (df_abs_wcd_pros["Presentase"] == 100).sum()
    distribusi = df_abs_wcd_pros["Kategori Kehadiran"].value_counts().reset_index()
    distribusi.columns = ["Kategori", "Jumlah"]

    # Metrik ringkas
    col1, col2 = st.columns(2)
    col1.metric("📌 Rata-rata Kehadiran", f"{rata2:.2f}%")
    col2.metric("✅ Jumlah Hadir 100%", f"{jumlah_100} Mahasiswa")

    # Tabel utama
    st.write("### 📋 Tabel Kehadiran Mahasiswa")
    st.dataframe(df_abs_wcd_pros [["Nama_Mahasiswa", "Pertemuan", "Hadir", "Presentase", "Kategori Kehadiran"]],
                 use_container_width=True)

    # Grafik batang jumlah hadir
    st.write("### 📈 Grafik Jumlah Kehadiran per Mahasiswa")
    fig_hadir = px.bar(
        df_abs_wcd_pros ,
        x="Nama_Mahasiswa",
        y="Hadir",
        text="Hadir",
        title="Jumlah Kehadiran per Mahasiswa",
        color="Kategori Kehadiran",
        labels={"Hadir": "Jumlah Hadir"},
    )
    fig_hadir.update_layout(xaxis_tickangle=-45)
    fig_hadir.update_traces(textposition="outside")
    st.plotly_chart(fig_hadir, use_container_width=True,key="grafik_kehadiran_wcd_pro")

    # Distribusi Kategori Kehadiran
    st.write("### 📊 Distribusi Kategori Kehadiran")
    col_a, col_b = st.columns(2)
    with col_a:
        fig_bar = px.bar(distribusi, x="Kategori", y="Jumlah", text="Jumlah", color="Kategori")
        fig_bar.update_traces(textposition="outside")
        st.plotly_chart(fig_bar, use_container_width=True, key="bar_kehadiran_wcd_pro")
    with col_b:
        fig_pie = px.pie(distribusi, names="Kategori", values="Jumlah")
        st.plotly_chart(fig_pie, use_container_width=True, key="pie_kehadiran_wcd_pro")

    # Mahasiswa dengan presentase = 0
    st.write("### 🚨 Mahasiswa dengan Kehadiran 0%")
    nol_df = df_abs_wcd_pros [df_abs_wcd_pros ["Presentase"] == 0]
    if nol_df.empty:
        st.success("Tidak ada mahasiswa dengan kehadiran 0%")
    else:
        st.error(f"Ada {len(nol_df)} mahasiswa dengan kehadiran 0%:")
        st.dataframe(nol_df[["Nama_Mahasiswa", "Pertemuan", "Hadir", "Presentase"]])

    # Mahasiswa hadir ≥ 7
    st.write("### 📗 Mahasiswa dengan Jumlah Hadir ≥ 7")
    hadir_7plus_df = df_abs_wcd_pros [df_abs_wcd_pros ["Hadir"] >= 7]
    if hadir_7plus_df.empty:
        st.warning("Tidak ada mahasiswa yang hadir ≥ 7 kali")
    else:
        st.dataframe(hadir_7plus_df[["Nama_Mahasiswa", "Hadir", "Presentase", "Kategori Kehadiran"]],
                     use_container_width=True)


def analisa_statistik_kehadiran_dbs_reg(df_abs_dbs_reg):
    st.subheader("📊 Analisa Kehadiran: Database Systems")

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
        df_abs_dbs_reg ,
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

def analisa_statistik_kehadiran_dbs_pros(df_abs_dbs_pros):
    st.subheader("📊 Analisa Kehadiran: Database Systems")

    # Pastikan kolom numerik
    df_abs_dbs_pros ["Presentase"] = pd.to_numeric(df_abs_dbs_pros ["Presentase"], errors="coerce")
    df_abs_dbs_pros ["Hadir"] = pd.to_numeric(df_abs_dbs_pros ["Hadir"], errors="coerce")
    df_abs_dbs_pros ["Pertemuan"] = pd.to_numeric(df_abs_dbs_pros ["Pertemuan"], errors="coerce")

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
    df_abs_dbs_pros ["Kategori Kehadiran"] = df_abs_dbs_pros ["Presentase"].apply(kategori)

    # Statistik dasar
    rata2 = df_abs_dbs_pros ["Presentase"].mean()
    jumlah_100 = (df_abs_dbs_pros ["Presentase"] == 100).sum()
    distribusi = df_abs_dbs_pros ["Kategori Kehadiran"].value_counts().reset_index()
    distribusi.columns = ["Kategori", "Jumlah"]

    # Metrik ringkas
    col1, col2 = st.columns(2)
    col1.metric("📌 Rata-rata Kehadiran", f"{rata2:.2f}%")
    col2.metric("✅ Jumlah Hadir 100%", f"{jumlah_100} Mahasiswa")

    # Tabel utama
    st.write("### 📋 Tabel Kehadiran Mahasiswa")
    st.dataframe(df_abs_dbs_pros [["Nama_Mahasiswa", "Pertemuan", "Hadir", "Presentase", "Kategori Kehadiran"]],
                 use_container_width=True)

    # Grafik batang jumlah hadir
    st.write("### 📈 Grafik Jumlah Kehadiran per Mahasiswa")
    fig_hadir = px.bar(
        df_abs_dbs_pros ,
        x="Nama_Mahasiswa",
        y="Hadir",
        text="Hadir",
        title="Jumlah Kehadiran per Mahasiswa",
        color="Kategori Kehadiran",
        labels={"Hadir": "Jumlah Hadir"},
    )
    fig_hadir.update_layout(xaxis_tickangle=-45)
    fig_hadir.update_traces(textposition="outside")
    st.plotly_chart(fig_hadir, use_container_width=True,key="grafik_kehadiran_dbs_pros")

    # Distribusi Kategori Kehadiran
    st.write("### 📊 Distribusi Kategori Kehadiran")
    col_a, col_b = st.columns(2)
    with col_a:
        fig_bar = px.bar(distribusi, x="Kategori", y="Jumlah", text="Jumlah", color="Kategori")
        fig_bar.update_traces(textposition="outside")
        st.plotly_chart(fig_bar, use_container_width=True, key="bar_kehadiran_dbs_pros")
    with col_b:
        fig_pie = px.pie(distribusi, names="Kategori", values="Jumlah")
        st.plotly_chart(fig_pie, use_container_width=True, key="pie_kehadiran_dbs_pros")

    # Mahasiswa dengan presentase = 0
    st.write("### 🚨 Mahasiswa dengan Kehadiran 0%")
    nol_df = df_abs_dbs_pros [df_abs_dbs_pros ["Presentase"] == 0]
    if nol_df.empty:
        st.success("Tidak ada mahasiswa dengan kehadiran 0%")
    else:
        st.error(f"Ada {len(nol_df)} mahasiswa dengan kehadiran 0%:")
        st.dataframe(nol_df[["Nama_Mahasiswa", "Pertemuan", "Hadir", "Presentase"]])

    # Mahasiswa hadir ≥ 7
    st.write("### 📗 Mahasiswa dengan Jumlah Hadir ≥ 7")
    hadir_7plus_df = df_abs_dbs_pros [df_abs_dbs_pros ["Hadir"] >= 7]
    if hadir_7plus_df.empty:
        st.warning("Tidak ada mahasiswa yang hadir ≥ 7 kali")
    else:
        st.dataframe(hadir_7plus_df[["Nama_Mahasiswa", "Hadir", "Presentase", "Kategori Kehadiran"]],
                     use_container_width=True)


def analisa_statistik_kehadiran_ds_reg(df_abs_ds_reg):
    st.subheader("📊 Analisa Kehadiran: Data Structures")

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

def analisa_statistik_kehadiran_ds_pros(df_abs_ds_pros):
    st.subheader("📊 Analisa Kehadiran: Data Structures")

    # Pastikan kolom numerik
    df_abs_ds_pros["Presentase"] = pd.to_numeric(df_abs_ds_pros["Presentase"], errors="coerce")
    df_abs_ds_pros["Hadir"] = pd.to_numeric(df_abs_ds_pros["Hadir"], errors="coerce")
    df_abs_ds_pros["Pertemuan"] = pd.to_numeric(df_abs_ds_pros["Pertemuan"], errors="coerce")

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
    df_abs_ds_pros["Kategori Kehadiran"] = df_abs_ds_pros["Presentase"].apply(kategori)

    # Statistik dasar
    rata2 = df_abs_ds_pros["Presentase"].mean()
    jumlah_100 = (df_abs_ds_pros["Presentase"] == 100).sum()
    distribusi = df_abs_ds_pros["Kategori Kehadiran"].value_counts().reset_index()
    distribusi.columns = ["Kategori", "Jumlah"]

    # Metrik ringkas
    col1, col2 = st.columns(2)
    col1.metric("📌 Rata-rata Kehadiran", f"{rata2:.2f}%")
    col2.metric("✅ Jumlah Hadir 100%", f"{jumlah_100} Mahasiswa")

    # Tabel utama
    st.write("### 📋 Tabel Kehadiran Mahasiswa")
    st.dataframe(df_abs_ds_pros[["Nama_Mahasiswa", "Pertemuan", "Hadir", "Presentase", "Kategori Kehadiran"]],
                 use_container_width=True)

    # Grafik batang jumlah hadir
    st.write("### 📈 Grafik Jumlah Kehadiran per Mahasiswa")
    fig_hadir = px.bar(
        df_abs_ds_pros,
        x="Nama_Mahasiswa",
        y="Hadir",
        text="Hadir",
        title="Jumlah Kehadiran per Mahasiswa",
        color="Kategori Kehadiran",
        labels={"Hadir": "Jumlah Hadir"},
    )
    fig_hadir.update_layout(xaxis_tickangle=-45)
    fig_hadir.update_traces(textposition="outside")
    st.plotly_chart(fig_hadir, use_container_width=True, key="grafik_kehadiran_ds_pros")

    # Distribusi Kategori Kehadiran
    st.write("### 📊 Distribusi Kategori Kehadiran")
    col_a, col_b = st.columns(2)
    with col_a:
        fig_bar = px.bar(distribusi, x="Kategori", y="Jumlah", text="Jumlah", color="Kategori")
        fig_bar.update_traces(textposition="outside")
        st.plotly_chart(fig_bar, use_container_width=True, key="bar_kehadiran_ds_pros")
    with col_b:
        fig_pie = px.pie(distribusi, names="Kategori", values="Jumlah")
        st.plotly_chart(fig_pie, use_container_width=True, key="pie_kehadiran_ds_pros")

    # Mahasiswa dengan presentase = 0
    st.write("### 🚨 Mahasiswa dengan Kehadiran 0%")
    nol_df = df_abs_ds_pros[df_abs_ds_pros["Presentase"] == 0]
    if nol_df.empty:
        st.success("Tidak ada mahasiswa dengan kehadiran 0%")
    else:
        st.error(f"Ada {len(nol_df)} mahasiswa dengan kehadiran 0%:")
        st.dataframe(nol_df[["Nama_Mahasiswa", "Pertemuan", "Hadir", "Presentase"]])

    # Mahasiswa hadir ≥ 7
    st.write("### 📗 Mahasiswa dengan Jumlah Hadir ≥ 7")
    hadir_7plus_df = df_abs_ds_pros[df_abs_ds_pros["Hadir"] >= 7]
    if hadir_7plus_df.empty:
        st.warning("Tidak ada mahasiswa yang hadir ≥ 7 kali")
    else:
        st.dataframe(hadir_7plus_df[["Nama_Mahasiswa", "Hadir", "Presentase", "Kategori Kehadiran"]],
                     use_container_width=True)

def analisa_statistik_kehadiran_sta_reg(df_abs_sta_reg):
    st.subheader("📊 Analisa Kehadiran: Statistical Thinking")

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

def analisa_statistik_kehadiran_sta_pros(df_abs_sta_pros):
    st.subheader("📊 Analisa Kehadiran: Statistical Thinking")

    # Pastikan kolom numerik
    df_abs_sta_pros["Presentase"] = pd.to_numeric(df_abs_sta_pros["Presentase"], errors="coerce")
    df_abs_sta_pros["Hadir"] = pd.to_numeric(df_abs_sta_pros["Hadir"], errors="coerce")
    df_abs_sta_pros["Pertemuan"] = pd.to_numeric(df_abs_sta_pros["Pertemuan"], errors="coerce")

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
    df_abs_sta_pros["Kategori Kehadiran"] = df_abs_sta_pros["Presentase"].apply(kategori)

    # Statistik dasar
    rata2 = df_abs_sta_pros["Presentase"].mean()
    jumlah_100 = (df_abs_sta_pros["Presentase"] == 100).sum()
    distribusi = df_abs_sta_pros["Kategori Kehadiran"].value_counts().reset_index()
    distribusi.columns = ["Kategori", "Jumlah"]

    # Metrik ringkas
    col1, col2 = st.columns(2)
    col1.metric("📌 Rata-rata Kehadiran", f"{rata2:.2f}%")
    col2.metric("✅ Jumlah Hadir 100%", f"{jumlah_100} Mahasiswa")

    # Tabel utama
    st.write("### 📋 Tabel Kehadiran Mahasiswa")
    st.dataframe(df_abs_sta_pros[["Nama_Mahasiswa", "Pertemuan", "Hadir", "Presentase", "Kategori Kehadiran"]],
                 use_container_width=True)

    # Grafik batang jumlah hadir
    st.write("### 📈 Grafik Jumlah Kehadiran per Mahasiswa")
    fig_hadir = px.bar(
        df_abs_sta_pros,
        x="Nama_Mahasiswa",
        y="Hadir",
        text="Hadir",
        title="Jumlah Kehadiran per Mahasiswa",
        color="Kategori Kehadiran",
        labels={"Hadir": "Jumlah Hadir"},
    )
    fig_hadir.update_layout(xaxis_tickangle=-45)
    fig_hadir.update_traces(textposition="outside")
    st.plotly_chart(fig_hadir, use_container_width=True, key="grafik_kehadiran_sta_pros")

    # Distribusi Kategori Kehadiran
    st.write("### 📊 Distribusi Kategori Kehadiran")
    col_a, col_b = st.columns(2)
    with col_a:
        fig_bar = px.bar(distribusi, x="Kategori", y="Jumlah", text="Jumlah", color="Kategori")
        fig_bar.update_traces(textposition="outside")
        st.plotly_chart(fig_bar, use_container_width=True, key="bar_kehadiran_sta_pros")
    with col_b:
        fig_pie = px.pie(distribusi, names="Kategori", values="Jumlah")
        st.plotly_chart(fig_pie, use_container_width=True, key="pie_kehadiran_sta_pros")

    # Mahasiswa dengan presentase = 0
    st.write("### 🚨 Mahasiswa dengan Kehadiran 0%")
    nol_df = df_abs_sta_pros[df_abs_sta_pros["Presentase"] == 0]
    if nol_df.empty:
        st.success("Tidak ada mahasiswa dengan kehadiran 0%")
    else:
        st.error(f"Ada {len(nol_df)} mahasiswa dengan kehadiran 0%:")
        st.dataframe(nol_df[["Nama_Mahasiswa", "Pertemuan", "Hadir", "Presentase"]])

    # Mahasiswa hadir ≥ 7
    st.write("### 📗 Mahasiswa dengan Jumlah Hadir ≥ 7")
    hadir_7plus_df = df_abs_sta_pros[df_abs_sta_pros["Hadir"] >= 7]
    if hadir_7plus_df.empty:
        st.warning("Tidak ada mahasiswa yang hadir ≥ 7 kali")
    else:
        st.dataframe(hadir_7plus_df[["Nama_Mahasiswa", "Hadir", "Presentase", "Kategori Kehadiran"]],
                     use_container_width=True)


def analisa_statistik_kehadiran_dw_reg(df_abs_dw_reg):
    st.subheader("📊 Analisa Kehadiran: Data Wrangling")

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

def analisa_statistik_kehadiran_dw_pros(df_abs_dw_pros):
    st.subheader("📊 Analisa Kehadiran: Data Wrangling")

    # Pastikan kolom numerik
    df_abs_dw_pros["Presentase"] = pd.to_numeric(df_abs_dw_pros["Presentase"], errors="coerce")
    df_abs_dw_pros["Hadir"] = pd.to_numeric(df_abs_dw_pros["Hadir"], errors="coerce")
    df_abs_dw_pros["Pertemuan"] = pd.to_numeric(df_abs_dw_pros["Pertemuan"], errors="coerce")

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
    df_abs_dw_pros["Kategori Kehadiran"] = df_abs_dw_pros["Presentase"].apply(kategori)

    # Statistik dasar
    rata2 = df_abs_dw_pros["Presentase"].mean()
    jumlah_100 = (df_abs_dw_pros["Presentase"] == 100).sum()
    distribusi = df_abs_dw_pros["Kategori Kehadiran"].value_counts().reset_index()
    distribusi.columns = ["Kategori", "Jumlah"]

    # Metrik ringkas
    col1, col2 = st.columns(2)
    col1.metric("📌 Rata-rata Kehadiran", f"{rata2:.2f}%")
    col2.metric("✅ Jumlah Hadir 100%", f"{jumlah_100} Mahasiswa")

    # Tabel utama
    st.write("### 📋 Tabel Kehadiran Mahasiswa")
    st.dataframe(df_abs_dw_pros[["Nama_Mahasiswa", "Pertemuan", "Hadir", "Presentase", "Kategori Kehadiran"]],
                 use_container_width=True)

    # Grafik batang jumlah hadir
    st.write("### 📈 Grafik Jumlah Kehadiran per Mahasiswa")
    fig_hadir = px.bar(
        df_abs_dw_pros,
        x="Nama_Mahasiswa",
        y="Hadir",
        text="Hadir",
        title="Jumlah Kehadiran per Mahasiswa",
        color="Kategori Kehadiran",
        labels={"Hadir": "Jumlah Hadir"},
    )
    fig_hadir.update_layout(xaxis_tickangle=-45)
    fig_hadir.update_traces(textposition="outside")
    st.plotly_chart(fig_hadir, use_container_width=True, key="grafik_kehadiran_dw_pros")

    # Distribusi Kategori Kehadiran
    st.write("### 📊 Distribusi Kategori Kehadiran")
    col_a, col_b = st.columns(2)
    with col_a:
        fig_bar = px.bar(distribusi, x="Kategori", y="Jumlah", text="Jumlah", color="Kategori")
        fig_bar.update_traces(textposition="outside")
        st.plotly_chart(fig_bar, use_container_width=True, key="bar_kehadiran_dw_pros")
    with col_b:
        fig_pie = px.pie(distribusi, names="Kategori", values="Jumlah")
        st.plotly_chart(fig_pie, use_container_width=True, key="pie_kehadiran_dw_pros")

    # Mahasiswa dengan presentase = 0
    st.write("### 🚨 Mahasiswa dengan Kehadiran 0%")
    nol_df = df_abs_dw_pros[df_abs_dw_pros["Presentase"] == 0]
    if nol_df.empty:
        st.success("Tidak ada mahasiswa dengan kehadiran 0%")
    else:
        st.error(f"Ada {len(nol_df)} mahasiswa dengan kehadiran 0%:")
        st.dataframe(nol_df[["Nama_Mahasiswa", "Pertemuan", "Hadir", "Presentase"]])

    # Mahasiswa hadir ≥ 7
    st.write("### 📗 Mahasiswa dengan Jumlah Hadir ≥ 7")
    hadir_7plus_df = df_abs_dw_pros[df_abs_dw_pros["Hadir"] >= 7]
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

def statistik_soal_dosen_uas(df_dosen_uas):
    st.header("📘 Statistik Dataset Soal Dosen")

    st.subheader("📌 Jumlah Level Soal per Dosen")
    df_dosen_uas["Level Soal"] = df_dosen_uas["Level Soal"].astype(str).str.split(",")
    df_exploded = df_dosen_uas.explode("Level Soal")
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


def statistik_dataset_nilai_reg(df_reguler):
    st.header(f"📖 Statistik UTS Kelas Reguler")

    # Ubah ke format long
    df_long = df_reguler.melt(id_vars=["NIM", "Nama_Mahasiswa"], 
                                var_name='Mata Kuliah', 
                                value_name='Nilai')

    # Tabel lengkap siswa
    #st.subheader("📋 Tabel Seluruh Mahasiswa")
    #st.dataframe(df_long, use_container_width=True)

    # List Mata Kuliah untuk Dropdown
    daftar_mk = df_long["Mata Kuliah"].unique().tolist()

    # Dropdown pilihan Mata Kuliah (unique key!)
    pilihan = st.selectbox("Pilih Mata Kuliah (Reguler)", daftar_mk, key='pilihan_mapel_reguler')

    # Filter berdasarkan Mata Kuliah yang dipilih
    df_filtered = df_long[df_long["Mata Kuliah"] == pilihan]

    st.subheader(f"📋 Data Mahasiswa Mata Kuliah {pilihan} (Reguler)")
    st.dataframe(df_filtered, use_container_width=True)

    st.subheader(f"📊 Statistik Deskriptif Mata Kuliah {pilihan} (Reguler)")
    statistik = df_filtered["Nilai"].describe().reset_index()
    statistik.columns = ["Statistik", "Nilai"]
    st.dataframe(statistik, use_container_width=True)

     # Penjelasan manusiawi
    mean = statistik.loc[1,"Nilai"]
    std = statistik.loc[2,"Nilai"]

    st.write("🟣 Penjelasan hubungan Mean dan Standar Deviasi:")
    if mean >= 75 and std < 10:
        st.success("✅ Mean TINGGI dan Standar Deviasi RENDAH — distribusi siswa seragam dan memenuhi standar.")
    elif mean >= 60 and std < 20:
        st.info("ℹ Mean CUKUP dan Standar Deviasi SEDANG — terdapat variasi, sebagian siswa unggul, sebagian membutuhkan perbaikan.")
    else:
        st.error("❌ Mean RENDAH dan Standar Deviasi TINGGI — distribusi siswa tidak merata dan perlu diberi perhatian lebih.")    

    st.write("""
    **Ringkasnya:**  
    - Mean (rata-rata) lebih cocok jika distribusinya normal dan merata.  
    - Standar deviasi yang besar menandakan perbedaan yang cukup luas antara siswa satu dan siswa lain.  
    - Standar deviasi yang kecil berarti siswa lebih seragam dan proses belajar lebih merata.
    """)

    # Boxplot per mata kuliah yang dipilih
    st.subheader(f"📉 Boxplot Distribusi Nilai {pilihan} (Reguler)")

    fig_box = px.box(
        df_filtered,
        y='Nilai',
        color='Mata Kuliah',
        title=f'Boxplot Distribusi Nilai Mata Kuliah {pilihan}'
    )
    st.plotly_chart(fig_box, use_container_width=True)

    # Heatmap Korelasi
    #st.subheader("📈 Korelasi Antar Mata Kuliah (Reguler)", )
    #df_pivot = df_long.pivot(index=["NIM", "Nama_Mahasiswa"], 
    #                         columns='Mata Kuliah', 
    #                         values='Nilai')
    #fig_corr = px.imshow(
    #    df_pivot.corr(), 
    #    text_auto=True, 
    #    color_continuous_scale='RdBu_r',
    #    title='Heatmap Korelasi Mata Kuliah (Reguler)'
    #)
    #st.plotly_chart(fig_corr, use_container_width=True)

def statistik_dataset_tugas_reg(df_tugas_reguler):
    st.header(f"📖 Statistik Nilai Tugas Kelas Reguler")

    # Ubah ke format long
    df_long = df_tugas_reguler.melt(id_vars=["NIM", "Nama_Mahasiswa"], 
                                var_name='Mata Kuliah', 
                                value_name='Nilai')

    # Tabel lengkap siswa
    #st.subheader("📋 Tabel Seluruh Mahasiswa")
    #st.dataframe(df_long, use_container_width=True)

    # List Mata Kuliah untuk Dropdown
    daftar_mk = df_long["Mata Kuliah"].unique().tolist()

    # Dropdown pilihan Mata Kuliah (unique key!)
    pilihan = st.selectbox("Pilih Mata Kuliah (Reguler)", daftar_mk, key='pilihan_mapel_reguler_tugas')

    # Filter berdasarkan Mata Kuliah yang dipilih
    df_filtered = df_long[df_long["Mata Kuliah"] == pilihan]

    st.subheader(f"📋 Data Mahasiswa Mata Kuliah {pilihan} (Reguler)")
    st.dataframe(df_filtered, use_container_width=True)

    st.subheader(f"📊 Statistik Deskriptif Mata Kuliah {pilihan} (Reguler)")
    statistik = df_filtered["Nilai"].describe().reset_index()
    statistik.columns = ["Statistik", "Nilai"]
    st.dataframe(statistik, use_container_width=True)

     # Penjelasan manusiawi
    mean = statistik.loc[1,"Nilai"]
    std = statistik.loc[2,"Nilai"]

    st.write("🟣 Penjelasan hubungan Mean dan Standar Deviasi:")
    if mean >= 75 and std < 10:
        st.success("✅ Mean TINGGI dan Standar Deviasi RENDAH — distribusi siswa seragam dan memenuhi standar.")
    elif mean >= 60 and std < 20:
        st.info("ℹ Mean CUKUP dan Standar Deviasi SEDANG — terdapat variasi, sebagian siswa unggul, sebagian membutuhkan perbaikan.")
    else:
        st.error("❌ Mean RENDAH dan Standar Deviasi TINGGI — distribusi siswa tidak merata dan perlu diberi perhatian lebih.")    

    st.write("""
    **Ringkasnya:**  
    - Mean (rata-rata) lebih cocok jika distribusinya normal dan merata.  
    - Standar deviasi yang besar menandakan perbedaan yang cukup luas antara siswa satu dan siswa lain.  
    - Standar deviasi yang kecil berarti siswa lebih seragam dan proses belajar lebih merata.
    """)

    # Boxplot per mata kuliah yang dipilih
    st.subheader(f"📉 Boxplot Distribusi Nilai {pilihan} (Reguler)")

    fig_box = px.box(
        df_filtered,
        y='Nilai',
        color='Mata Kuliah',
        title=f'Boxplot Distribusi Nilai Mata Kuliah {pilihan}'
    )
    st.plotly_chart(fig_box, use_container_width=True)

    # Heatmap Korelasi
    #st.subheader("📈 Korelasi Antar Mata Kuliah (Reguler)", )
    #df_pivot = df_long.pivot(index=["NIM", "Nama_Mahasiswa"], 
    #                         columns='Mata Kuliah', 
    #                         values='Nilai')
    #fig_corr = px.imshow(
    #    df_pivot.corr(), 
    #    text_auto=True, 
    #    color_continuous_scale='RdBu_r',
    #    title='Heatmap Korelasi Mata Kuliah (Reguler)'
    #)
    #st.plotly_chart(fig_corr, use_container_width=True)

def statistik_dataset_kuis_reg(df_kuis_reguler):
    st.header(f"📖 Statistik Nilai Kuis Kelas Reguler")

    # Ubah ke format long
    df_long = df_kuis_reguler.melt(id_vars=["NIM", "Nama_Mahasiswa"], 
                                var_name='Mata Kuliah', 
                                value_name='Nilai')

    # Tabel lengkap siswa
    #st.subheader("📋 Tabel Seluruh Mahasiswa")
    #st.dataframe(df_long, use_container_width=True)

    # List Mata Kuliah untuk Dropdown
    daftar_mk = df_long["Mata Kuliah"].unique().tolist()

    # Dropdown pilihan Mata Kuliah (unique key!)
    pilihan = st.selectbox("Pilih Mata Kuliah (Reguler)", daftar_mk, key='pilihan_mapel_reguler_kuis')

    # Filter berdasarkan Mata Kuliah yang dipilih
    df_filtered = df_long[df_long["Mata Kuliah"] == pilihan]

    st.subheader(f"📋 Data Mahasiswa Mata Kuliah {pilihan} (Reguler)")
    st.dataframe(df_filtered, use_container_width=True)

    st.subheader(f"📊 Statistik Deskriptif Mata Kuliah {pilihan} (Reguler)")
    statistik = df_filtered["Nilai"].describe().reset_index()
    statistik.columns = ["Statistik", "Nilai"]
    st.dataframe(statistik, use_container_width=True)

     # Penjelasan manusiawi
    mean = statistik.loc[1,"Nilai"]
    std = statistik.loc[2,"Nilai"]

    st.write("🟣 Penjelasan hubungan Mean dan Standar Deviasi:")
    if mean >= 75 and std < 10:
        st.success("✅ Mean TINGGI dan Standar Deviasi RENDAH — distribusi siswa seragam dan memenuhi standar.")
    elif mean >= 60 and std < 20:
        st.info("ℹ Mean CUKUP dan Standar Deviasi SEDANG — terdapat variasi, sebagian siswa unggul, sebagian membutuhkan perbaikan.")
    else:
        st.error("❌ Mean RENDAH dan Standar Deviasi TINGGI — distribusi siswa tidak merata dan perlu diberi perhatian lebih.")    

    st.write("""
    **Ringkasnya:**  
    - Mean (rata-rata) lebih cocok jika distribusinya normal dan merata.  
    - Standar deviasi yang besar menandakan perbedaan yang cukup luas antara siswa satu dan siswa lain.  
    - Standar deviasi yang kecil berarti siswa lebih seragam dan proses belajar lebih merata.
    """)

    # Boxplot per mata kuliah yang dipilih
    st.subheader(f"📉 Boxplot Distribusi Nilai {pilihan} (Reguler)")

    fig_box = px.box(
        df_filtered,
        y='Nilai',
        color='Mata Kuliah',
        title=f'Boxplot Distribusi Nilai Mata Kuliah {pilihan}'
    )
    st.plotly_chart(fig_box, use_container_width=True)

    # Heatmap Korelasi
    #st.subheader("📈 Korelasi Antar Mata Kuliah (Reguler)", )
    #df_pivot = df_long.pivot(index=["NIM", "Nama_Mahasiswa"], 
    #                         columns='Mata Kuliah', 
    #                         values='Nilai')
    #fig_corr = px.imshow(
    #    df_pivot.corr(), 
    #    text_auto=True, 
    #    color_continuous_scale='RdBu_r',
    #    title='Heatmap Korelasi Mata Kuliah (Reguler)'
    #)
    #st.plotly_chart(fig_corr, use_container_width=True)

def statistik_dataset_nilai_pro(df_pro):
    st.header(f"📖 Statistik UTS Kelas Reguler")

    # Ubah ke format long
    df_long = df_pro.melt(id_vars=["NIM", "Nama_Mahasiswa"], 
                                var_name='Mata Kuliah', 
                                value_name='Nilai')

    # Tabel lengkap siswa
    #st.subheader("📋 Tabel Seluruh Mahasiswa")
    #st.dataframe(df_long, use_container_width=True)

    # List Mata Kuliah untuk Dropdown
    daftar_mk = df_long["Mata Kuliah"].unique().tolist()

    # Dropdown pilihan Mata Kuliah (unique key!)
    pilihan = st.selectbox("Pilih Mata Kuliah (Reguler)", daftar_mk, key='pilihan_mapel_pro')

    # Filter berdasarkan Mata Kuliah yang dipilih
    df_filtered = df_long[df_long["Mata Kuliah"] == pilihan]

    st.subheader(f"📋 Data Mahasiswa Mata Kuliah {pilihan} (Reguler)")
    st.dataframe(df_filtered, use_container_width=True)

    st.subheader(f"📊 Statistik Deskriptif Mata Kuliah {pilihan} (Reguler)")
    statistik = df_filtered["Nilai"].describe().reset_index()
    statistik.columns = ["Statistik", "Nilai"]
    st.dataframe(statistik, use_container_width=True)
    # Penjelasan manusiawi
    mean = statistik.loc[1,"Nilai"]
    std = statistik.loc[2,"Nilai"]

    st.write("🟣 Penjelasan hubungan Mean dan Standar Deviasi:")
    if mean >= 75 and std < 10:
        st.success("✅ Mean TINGGI dan Standar Deviasi RENDAH — distribusi siswa seragam dan memenuhi standar.")
    elif mean >= 60 and std < 20:
        st.info("ℹ Mean CUKUP dan Standar Deviasi SEDANG — terdapat variasi, sebagian siswa unggul, sebagian membutuhkan perbaikan.")
    else:
        st.error("❌ Mean RENDAH dan Standar Deviasi TINGGI — distribusi siswa tidak merata dan perlu diberi perhatian lebih.")    

    st.write("""
    **Ringkasnya:**  
    - Mean (rata-rata) lebih cocok jika distribusinya normal dan merata.  
    - Standar deviasi yang besar menandakan perbedaan yang cukup luas antara siswa satu dan siswa lain.  
    - Standar deviasi yang kecil berarti siswa lebih seragam dan proses belajar lebih merata.
    """)
    # Boxplot per mata kuliah yang dipilih
    st.subheader(f"📉 Boxplot Distribusi Nilai {pilihan} (Reguler)")

    fig_box = px.box(
        df_filtered,
        y='Nilai',
        color='Mata Kuliah',
        title=f'Boxplot Distribusi Nilai Mata Kuliah {pilihan}'
    )
    st.plotly_chart(fig_box, use_container_width=True)

    # Heatmap Korelasi
    #st.subheader("📈 Korelasi Antar Mata Kuliah (Reguler)", )
    #df_pivot = df_long.pivot(index=["NIM", "Nama_Mahasiswa"], 
    #                         columns='Mata Kuliah', 
    #                         values='Nilai')
    #fig_corr = px.imshow(
    #    df_pivot.corr(), 
    #    text_auto=True, 
    #    color_continuous_scale='RdBu_r',
    #    title='Heatmap Korelasi Mata Kuliah (Reguler)'
    #)
    #st.plotly_chart(fig_corr, use_container_width=True)

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

def statistik_nilai_lebihsama_60(df_reguler, df_pro):
    st.header("❌ Statistik Mahasiswa dengan Nilai >= 60")

    # Gabungkan kedua dataset untuk keperluan pelaporan
    df_reguler["Kelas"] = "Reguler"
    df_pro["Kelas"] = "Pro dan Aksel"
    df_all = pd.concat([df_reguler, df_pro], ignore_index=True)

    # Ubah ke format long (melt)
    df_long = df_all.melt(id_vars=["NIM", "Nama_Mahasiswa", "Kelas"],
                          var_name="Mata Kuliah",
                          value_name="Nilai")

    # Filter nilai di bawah 60
    df_lebihsama_60 = df_long[df_long["Nilai"] >= 60]

    # Hitung jumlah mahasiswa per mata kuliah per kelas
    summary = df_lebihsama_60.groupby(["Kelas", "Mata Kuliah"]).agg(
        Jumlah_Mahasiswa=("Nama_Mahasiswa", "count"),
        Daftar_Mahasiswa=("Nama_Mahasiswa", lambda x: ", ".join(x))
    ).reset_index()

    st.subheader("📊 Grafik Jumlah Mahasiswa dengan Nilai >= 60")
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

    st.subheader("📋 Tabel Detail Mahasiswa dengan Nilai >= 60")
    st.dataframe(summary, use_container_width=True)

def statistik_nilai_samadengan_0(df_reguler, df_pro):
    st.header("❌ Statistik Mahasiswa dengan Nilai = 0")

    # Gabungkan kedua dataset untuk keperluan pelaporan
    df_reguler["Kelas"] = "Reguler"
    df_pro["Kelas"] = "Pro dan Aksel"
    df_all = pd.concat([df_reguler, df_pro], ignore_index=True)

    # Ubah ke format long (melt)
    df_long = df_all.melt(id_vars=["NIM", "Nama_Mahasiswa", "Kelas"],
                          var_name="Mata Kuliah",
                          value_name="Nilai")

    # Filter nilai di bawah 60
    df_sd_0 = df_long[df_long["Nilai"] == 0]

    # Hitung jumlah mahasiswa per mata kuliah per kelas
    summary = df_sd_0.groupby(["Kelas", "Mata Kuliah"]).agg(
        Jumlah_Mahasiswa=("Nama_Mahasiswa", "count"),
        Daftar_Mahasiswa=("Nama_Mahasiswa", lambda x: ", ".join(x))
    ).reset_index()

    st.subheader("📊 Grafik Jumlah Mahasiswa dengan Nilai = 0")
    fig = px.bar(
        summary,
        x="Mata Kuliah",
        y="Jumlah_Mahasiswa",
        color="Kelas",
        barmode="group",
        text="Jumlah_Mahasiswa",
        title="Jumlah Mahasiswa dengan Nilai = 0 per Mata Kuliah per Kelas",
        labels={"Jumlah_Mahasiswa": "Jumlah Mahasiswa"}
    )
    fig.update_traces(textposition="outside")
    fig.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("📋 Tabel Detail Mahasiswa dengan Nilai = 0")
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
    # Tabel dan Visualisasi per Kelas dan Tahun Angkatan
    st.subheader("📊 Distribusi Mahasiswa per Kelas dan Tahun Angkatan")

    # Menghitung jumlah siswa per Kelas dan Tahun
    df_count = df_mhs_pro.groupby(['Tahun', 'Kelas']).size().reset_index(name='Jumlah')
    st.dataframe(df_count, use_container_width=True)

    # Plot Bar per Kelas dan Tahun
    fig_count = px.bar(
        df_count,
        x='Tahun',
        y='Jumlah',
        color='Kelas',
        barmode='group',
        text='Jumlah',
        title='Jumlah Mahasiswa per Kelas dan Tahun'
    )
    fig_count.update_traces(textposition='outside')
    st.plotly_chart(fig_count, use_container_width=True)

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

def tampilkan_sentimen_dbs_pertemuan(DATA_PATH_DBS, pertemuan=1, senti=None):
    """
    Analisis Sentimen Komentar per Pertemuan
    """
    st.header(f"📝 Analisis Sentimen Komentar Pertemuan {pertemuan}")

    # Membaca CSV
    df = pd.read_csv(DATA_PATH_DBS, dtype=str)

    # Mengambil kolom sesuai pertemuan
    col_name = f"Pertemuan_{pertemuan}"  # pertemuan 1 -> Pertemuan_1
    
    if col_name not in df.columns:
        st.error(f"Kolom {col_name} tidak ditemukan.")
        return
    
    komentar = df[col_name].dropna().astype(str).tolist()

    # Analisis Sentimen
    hasil = [senti.main(text) for text in komentar]
    df[f"Sentimen_Pertemuan_{pertemuan}"] = hasil

    # Tampilkan hasil
    st.subheader("📄 Tabel Hasil Sentimen")
    st.dataframe(
        pd.DataFrame({"Komentar": komentar, "Sentimen": hasil}),
        use_container_width=True
    )

    # Hitung distribusi
    counter = Counter(hasil)
    labels = ["Positif", "Negatif", "Netral"]
    values = [counter.get(l, 0) for l in labels]

    # Pie Chart
    st.subheader("📊 Pie Chart Distribusi Sentimen")
    fig1, ax1 = plt.subplots(figsize=(6, 6))
    explode = [0.05, 0.05, 0.05]
    colors = ["#2ecc71", "#e74c3c", "#f1c40f"]

    ax1.pie(values,
            labels=labels,
            autopct='%1.1f%%',
            startangle=140,
            explode=explode,
            colors=colors,
            textprops={'fontsize': 12})
    ax1.axis('equal')

    st.pyplot(fig1)


    # Bar Chart
    st.subheader("📊 Bar Chart Distribusi Sentimen")
    bar_df = pd.DataFrame({"Sentimen": labels, "Jumlah": values}).set_index("Sentimen")
    st.bar_chart(bar_df)

def tampilkan_sentimen_cp_pertemuan(DATA_PATH_CP, pertemuan=1, senti=None):
    """
    Analisis Sentimen Komentar per Pertemuan
    """
    st.header(f"📝 Analisis Sentimen Komentar Pertemuan {pertemuan}")

    # Membaca CSV
    df = pd.read_csv(DATA_PATH_CP, dtype=str)

    # Mengambil kolom sesuai pertemuan
    col_name = f"Pertemuan_{pertemuan}"  # pertemuan 1 -> Pertemuan_1
    
    if col_name not in df.columns:
        st.error(f"Kolom {col_name} tidak ditemukan.")
        return
    
    komentar = df[col_name].dropna().astype(str).tolist()

    # Analisis Sentimen
    hasil = [senti.main(text) for text in komentar]
    df[f"Sentimen_Pertemuan_{pertemuan}"] = hasil

    # Tampilkan hasil
    st.subheader("📄 Tabel Hasil Sentimen")
    st.dataframe(
        pd.DataFrame({"Komentar": komentar, "Sentimen": hasil}),
        use_container_width=True
    )

    # Hitung distribusi
    counter = Counter(hasil)
    labels = ["Positif", "Negatif", "Netral"]
    values = [counter.get(l, 0) for l in labels]

    # Pie Chart
    st.subheader("📊 Pie Chart Distribusi Sentimen")
    fig1, ax1 = plt.subplots(figsize=(6, 6))
    explode = [0.05, 0.05, 0.05]
    colors = ["#2ecc71", "#e74c3c", "#f1c40f"]

    ax1.pie(values,
            labels=labels,
            autopct='%1.1f%%',
            startangle=140,
            explode=explode,
            colors=colors,
            textprops={'fontsize': 12})
    ax1.axis('equal')

    st.pyplot(fig1)


    # Bar Chart
    st.subheader("📊 Bar Chart Distribusi Sentimen")
    bar_df = pd.DataFrame({"Sentimen": labels, "Jumlah": values}).set_index("Sentimen")
    st.bar_chart(bar_df)

def tampilkan_sentimen_cp_pro_pertemuan(DATA_PATH_CP_PRO, pertemuan=1, senti=None):
    """
    Analisis Sentimen Komentar per Pertemuan
    """
    st.header(f"📝 Analisis Sentimen Komentar Pertemuan {pertemuan}")

    # Membaca CSV
    df = pd.read_csv(DATA_PATH_CP_PRO, dtype=str)

    # Mengambil kolom sesuai pertemuan
    col_name = f"Pertemuan_{pertemuan}"  # pertemuan 1 -> Pertemuan_1
    
    if col_name not in df.columns:
        st.error(f"Kolom {col_name} tidak ditemukan.")
        return
    
    komentar = df[col_name].dropna().astype(str).tolist()

    # Analisis Sentimen
    hasil = [senti.main(text) for text in komentar]
    df[f"Sentimen_Pertemuan_{pertemuan}"] = hasil

    # Tampilkan hasil
    st.subheader("📄 Tabel Hasil Sentimen")
    st.dataframe(
        pd.DataFrame({"Komentar": komentar, "Sentimen": hasil}),
        use_container_width=True
    )

    # Hitung distribusi
    counter = Counter(hasil)
    labels = ["Positif", "Negatif", "Netral"]
    values = [counter.get(l, 0) for l in labels]

    # Pie Chart
    st.subheader("📊 Pie Chart Distribusi Sentimen")
    fig1, ax1 = plt.subplots(figsize=(6, 6))
    explode = [0.05, 0.05, 0.05]
    colors = ["#2ecc71", "#e74c3c", "#f1c40f"]

    ax1.pie(values,
            labels=labels,
            autopct='%1.1f%%',
            startangle=140,
            explode=explode,
            colors=colors,
            textprops={'fontsize': 12})
    ax1.axis('equal')

    st.pyplot(fig1)


    # Bar Chart
    st.subheader("📊 Bar Chart Distribusi Sentimen")
    bar_df = pd.DataFrame({"Sentimen": labels, "Jumlah": values}).set_index("Sentimen")
    st.bar_chart(bar_df)

def tampilkan_sentimen_wcd_pro_pertemuan(DATA_PATH_WCD_PRO, pertemuan=1, senti=None):
    """
    Analisis Sentimen Komentar per Pertemuan
    """
    st.header(f"📝 Analisis Sentimen Komentar Pertemuan {pertemuan}")

    # Membaca CSV
    df = pd.read_csv(DATA_PATH_WCD_PRO, dtype=str)

    # Mengambil kolom sesuai pertemuan
    col_name = f"Pertemuan_{pertemuan}"  # pertemuan 1 -> Pertemuan_1
    
    if col_name not in df.columns:
        st.error(f"Kolom {col_name} tidak ditemukan.")
        return
    
    komentar = df[col_name].dropna().astype(str).tolist()

    # Analisis Sentimen
    hasil = [senti.main(text) for text in komentar]
    df[f"Sentimen_Pertemuan_{pertemuan}"] = hasil

    # Tampilkan hasil
    st.subheader("📄 Tabel Hasil Sentimen")
    st.dataframe(
        pd.DataFrame({"Komentar": komentar, "Sentimen": hasil}),
        use_container_width=True
    )

    # Hitung distribusi
    counter = Counter(hasil)
    labels = ["Positif", "Negatif", "Netral"]
    values = [counter.get(l, 0) for l in labels]

    # Pie Chart
    st.subheader("📊 Pie Chart Distribusi Sentimen")
    fig1, ax1 = plt.subplots(figsize=(6, 6))
    explode = [0.05, 0.05, 0.05]
    colors = ["#2ecc71", "#e74c3c", "#f1c40f"]

    ax1.pie(values,
            labels=labels,
            autopct='%1.1f%%',
            startangle=140,
            explode=explode,
            colors=colors,
            textprops={'fontsize': 12})
    ax1.axis('equal')

    st.pyplot(fig1)


    # Bar Chart
    st.subheader("📊 Bar Chart Distribusi Sentimen")
    bar_df = pd.DataFrame({"Sentimen": labels, "Jumlah": values}).set_index("Sentimen")
    st.bar_chart(bar_df)


def tampilkan_sentimen_wcd_pertemuan(DATA_PATH_WCD, pertemuan=1, senti=None):
    """
    Analisis Sentimen Komentar per Pertemuan
    """
    st.header(f"📝 Analisis Sentimen Komentar Pertemuan {pertemuan}")

    # Membaca CSV
    df = pd.read_csv(DATA_PATH_WCD, dtype=str)

    # Mengambil kolom sesuai pertemuan
    col_name = f"Pertemuan_{pertemuan}"  # pertemuan 1 -> Pertemuan_1
    
    if col_name not in df.columns:
        st.error(f"Kolom {col_name} tidak ditemukan.")
        return
    
    komentar = df[col_name].dropna().astype(str).tolist()

    # Analisis Sentimen
    hasil = [senti.main(text) for text in komentar]
    df[f"Sentimen_Pertemuan_{pertemuan}"] = hasil

    # Tampilkan hasil
    st.subheader("📄 Tabel Hasil Sentimen")
    st.dataframe(
        pd.DataFrame({"Komentar": komentar, "Sentimen": hasil}),
        use_container_width=True
    )

    # Hitung distribusi
    counter = Counter(hasil)
    labels = ["Positif", "Negatif", "Netral"]
    values = [counter.get(l, 0) for l in labels]

    # Pie Chart
    st.subheader("📊 Pie Chart Distribusi Sentimen")
    fig1, ax1 = plt.subplots(figsize=(6, 6))
    explode = [0.05, 0.05, 0.05]
    colors = ["#2ecc71", "#e74c3c", "#f1c40f"]

    ax1.pie(values,
            labels=labels,
            autopct='%1.1f%%',
            startangle=140,
            explode=explode,
            colors=colors,
            textprops={'fontsize': 12})
    ax1.axis('equal')

    st.pyplot(fig1)


    # Bar Chart
    st.subheader("📊 Bar Chart Distribusi Sentimen")
    bar_df = pd.DataFrame({"Sentimen": labels, "Jumlah": values}).set_index("Sentimen")
    st.bar_chart(bar_df)

def tampilkan_sentimen_oop_pertemuan(DATA_PATH_OOP, pertemuan=1, senti=None):
    """
    Analisis Sentimen Komentar per Pertemuan
    """
    st.header(f"📝 Analisis Sentimen Komentar Pertemuan {pertemuan}")

    # Membaca CSV
    df = pd.read_csv(DATA_PATH_OOP, dtype=str)

    # Mengambil kolom sesuai pertemuan
    col_name = f"Pertemuan_{pertemuan}"  # pertemuan 1 -> Pertemuan_1
    
    if col_name not in df.columns:
        st.error(f"Kolom {col_name} tidak ditemukan.")
        return
    
    komentar = df[col_name].dropna().astype(str).tolist()

    # Analisis Sentimen
    hasil = [senti.main(text) for text in komentar]
    df[f"Sentimen_Pertemuan_{pertemuan}"] = hasil

    # Tampilkan hasil
    st.subheader("📄 Tabel Hasil Sentimen")
    st.dataframe(
        pd.DataFrame({"Komentar": komentar, "Sentimen": hasil}),
        use_container_width=True
    )

    # Hitung distribusi
    counter = Counter(hasil)
    labels = ["Positif", "Negatif", "Netral"]
    values = [counter.get(l, 0) for l in labels]

    # Pie Chart
    st.subheader("📊 Pie Chart Distribusi Sentimen")
    fig1, ax1 = plt.subplots(figsize=(6, 6))
    explode = [0.05, 0.05, 0.05]
    colors = ["#2ecc71", "#e74c3c", "#f1c40f"]

    ax1.pie(values,
            labels=labels,
            autopct='%1.1f%%',
            startangle=140,
            explode=explode,
            colors=colors,
            textprops={'fontsize': 12})
    ax1.axis('equal')

    st.pyplot(fig1)


    # Bar Chart
    st.subheader("📊 Bar Chart Distribusi Sentimen")
    bar_df = pd.DataFrame({"Sentimen": labels, "Jumlah": values}).set_index("Sentimen")
    st.bar_chart(bar_df)

def tampilkan_sentimen_ds_pertemuan(DATA_PATH_DS, pertemuan=1, senti=None):
    """
    Analisis Sentimen Komentar per Pertemuan
    """
    st.header(f"📝 Analisis Sentimen Komentar Pertemuan {pertemuan}")

    # Membaca CSV
    df = pd.read_csv(DATA_PATH_DS, dtype=str)

    # Mengambil kolom sesuai pertemuan
    col_name = f"Pertemuan_{pertemuan}"  # pertemuan 1 -> Pertemuan_1
    
    if col_name not in df.columns:
        st.error(f"Kolom {col_name} tidak ditemukan.")
        return
    
    komentar = df[col_name].dropna().astype(str).tolist()

    # Analisis Sentimen
    hasil = [senti.main(text) for text in komentar]
    df[f"Sentimen_Pertemuan_{pertemuan}"] = hasil

    # Tampilkan hasil
    st.subheader("📄 Tabel Hasil Sentimen")
    st.dataframe(
        pd.DataFrame({"Komentar": komentar, "Sentimen": hasil}),
        use_container_width=True
    )

    # Hitung distribusi
    counter = Counter(hasil)
    labels = ["Positif", "Negatif", "Netral"]
    values = [counter.get(l, 0) for l in labels]

    # Pie Chart
    st.subheader("📊 Pie Chart Distribusi Sentimen")
    fig1, ax1 = plt.subplots(figsize=(6, 6))
    explode = [0.05, 0.05, 0.05]
    colors = ["#2ecc71", "#e74c3c", "#f1c40f"]

    ax1.pie(values,
            labels=labels,
            autopct='%1.1f%%',
            startangle=140,
            explode=explode,
            colors=colors,
            textprops={'fontsize': 12})
    ax1.axis('equal')

    st.pyplot(fig1)


    # Bar Chart
    st.subheader("📊 Bar Chart Distribusi Sentimen")
    bar_df = pd.DataFrame({"Sentimen": labels, "Jumlah": values}).set_index("Sentimen")
    st.bar_chart(bar_df)

def tampilkan_sentimen_sta_pertemuan(DATA_PATH_STA, pertemuan=1, senti=None):
    """
    Analisis Sentimen Komentar per Pertemuan
    """
    st.header(f"📝 Analisis Sentimen Komentar Pertemuan {pertemuan}")

    # Membaca CSV
    df = pd.read_csv(DATA_PATH_STA, dtype=str)

    # Mengambil kolom sesuai pertemuan
    col_name = f"Pertemuan_{pertemuan}"  # pertemuan 1 -> Pertemuan_1
    
    if col_name not in df.columns:
        st.error(f"Kolom {col_name} tidak ditemukan.")
        return
    
    komentar = df[col_name].dropna().astype(str).tolist()

    # Analisis Sentimen
    hasil = [senti.main(text) for text in komentar]
    df[f"Sentimen_Pertemuan_{pertemuan}"] = hasil

    # Tampilkan hasil
    st.subheader("📄 Tabel Hasil Sentimen")
    st.dataframe(
        pd.DataFrame({"Komentar": komentar, "Sentimen": hasil}),
        use_container_width=True
    )

    # Hitung distribusi
    counter = Counter(hasil)
    labels = ["Positif", "Negatif", "Netral"]
    values = [counter.get(l, 0) for l in labels]

    # Pie Chart
    st.subheader("📊 Pie Chart Distribusi Sentimen")
    fig1, ax1 = plt.subplots(figsize=(6, 6))
    explode = [0.05, 0.05, 0.05]
    colors = ["#2ecc71", "#e74c3c", "#f1c40f"]

    ax1.pie(values,
            labels=labels,
            autopct='%1.1f%%',
            startangle=140,
            explode=explode,
            colors=colors,
            textprops={'fontsize': 12})
    ax1.axis('equal')

    st.pyplot(fig1)


    # Bar Chart
    st.subheader("📊 Bar Chart Distribusi Sentimen")
    bar_df = pd.DataFrame({"Sentimen": labels, "Jumlah": values}).set_index("Sentimen")
    st.bar_chart(bar_df)

def tampilkan_sentimen_dw_pertemuan(DATA_PATH_DW, pertemuan=1, senti=None):
    """
    Analisis Sentimen Komentar per Pertemuan
    """
    st.header(f"📝 Analisis Sentimen Komentar Pertemuan {pertemuan}")

    # Membaca CSV
    df = pd.read_csv(DATA_PATH_DW, dtype=str)

    # Mengambil kolom sesuai pertemuan
    col_name = f"Pertemuan_{pertemuan}"  # pertemuan 1 -> Pertemuan_1
    
    if col_name not in df.columns:
        st.error(f"Kolom {col_name} tidak ditemukan.")
        return
    
    komentar = df[col_name].dropna().astype(str).tolist()

    # Analisis Sentimen
    hasil = [senti.main(text) for text in komentar]
    df[f"Sentimen_Pertemuan_{pertemuan}"] = hasil

    # Tampilkan hasil
    st.subheader("📄 Tabel Hasil Sentimen")
    st.dataframe(
        pd.DataFrame({"Komentar": komentar, "Sentimen": hasil}),
        use_container_width=True
    )

    # Hitung distribusi
    counter = Counter(hasil)
    labels = ["Positif", "Negatif", "Netral"]
    values = [counter.get(l, 0) for l in labels]

    # Pie Chart
    st.subheader("📊 Pie Chart Distribusi Sentimen")
    fig1, ax1 = plt.subplots(figsize=(6, 6))
    explode = [0.05, 0.05, 0.05]
    colors = ["#2ecc71", "#e74c3c", "#f1c40f"]

    ax1.pie(values,
            labels=labels,
            autopct='%1.1f%%',
            startangle=140,
            explode=explode,
            colors=colors,
            textprops={'fontsize': 12})
    ax1.axis('equal')

    st.pyplot(fig1)


    # Bar Chart
    st.subheader("📊 Bar Chart Distribusi Sentimen")
    bar_df = pd.DataFrame({"Sentimen": labels, "Jumlah": values}).set_index("Sentimen")
    st.bar_chart(bar_df)



def tampilkan_mahasiswa_dbs_dengan_komentar(dataframe, pertemuan=1, nama_dataset='Dataset Reguler'):
    st.header(f"📝 Daftar Mahasiswa yang Memberikan Komentar - {nama_dataset}")

    col_name = f"Pertemuan_{pertemuan}"

    if col_name not in dataframe.columns:
        st.error(f"Kolom {col_name} tidak ditemukan.")
        return

    df_filtered = dataframe[dataframe[col_name] != '-']

    if df_filtered.empty:
        st.info(f"ℹ Tidak ada siswa yang memberikan komentar di {col_name}.")
    else:
        st.success(f"Ada {len(df_filtered)} siswa yang memberikan komentar di {col_name}.")
        st.dataframe(
            df_filtered[["NIM", "Nama_Mahasiswa", col_name]],
            use_container_width=True
        )

def tampilkan_mahasiswa_cp_dengan_komentar(dataframe, pertemuan=1, nama_dataset='Dataset Reguler'):
    st.header(f"📝 Daftar Mahasiswa yang Memberikan Komentar - {nama_dataset}")

    col_name = f"Pertemuan_{pertemuan}"

    if col_name not in dataframe.columns:
        st.error(f"Kolom {col_name} tidak ditemukan.")
        return

    df_filtered = dataframe[dataframe[col_name] != '-']

    if df_filtered.empty:
        st.info(f"ℹ Tidak ada siswa yang memberikan komentar di {col_name}.")
    else:
        st.success(f"Ada {len(df_filtered)} siswa yang memberikan komentar di {col_name}.")
        st.dataframe(
            df_filtered[["NIM", "Nama_Mahasiswa", col_name]],
            use_container_width=True
        )

def tampilkan_mahasiswa_cp_pro_dengan_komentar(dataframe, pertemuan=1, nama_dataset='Dataset Pro dan Akses'):
    st.header(f"📝 Daftar Mahasiswa yang Memberikan Komentar - {nama_dataset}")

    col_name = f"Pertemuan_{pertemuan}"

    if col_name not in dataframe.columns:
        st.error(f"Kolom {col_name} tidak ditemukan.")
        return

    df_filtered = dataframe[dataframe[col_name] != '-']

    if df_filtered.empty:
        st.info(f"ℹ Tidak ada siswa yang memberikan komentar di {col_name}.")
    else:
        st.success(f"Ada {len(df_filtered)} siswa yang memberikan komentar di {col_name}.")
        st.dataframe(
            df_filtered[["NIM", "Nama_Mahasiswa", col_name]],
            use_container_width=True
        )


def tampilkan_mahasiswa_wcd_dengan_komentar(dataframe, pertemuan=1, nama_dataset='Dataset Reguler'):
    st.header(f"📝 Daftar Mahasiswa yang Memberikan Komentar - {nama_dataset}")

    col_name = f"Pertemuan_{pertemuan}"

    if col_name not in dataframe.columns:
        st.error(f"Kolom {col_name} tidak ditemukan.")
        return

    df_filtered = dataframe[dataframe[col_name] != '-']

    if df_filtered.empty:
        st.info(f"ℹ Tidak ada siswa yang memberikan komentar di {col_name}.")
    else:
        st.success(f"Ada {len(df_filtered)} siswa yang memberikan komentar di {col_name}.")
        st.dataframe(
            df_filtered[["NIM", "Nama_Mahasiswa", col_name]],
            use_container_width=True
        )

def tampilkan_mahasiswa_wcd_pro_dengan_komentar(dataframe, pertemuan=1, nama_dataset='Dataset Reguler'):
    st.header(f"📝 Daftar Mahasiswa yang Memberikan Komentar - {nama_dataset}")

    col_name = f"Pertemuan_{pertemuan}"

    if col_name not in dataframe.columns:
        st.error(f"Kolom {col_name} tidak ditemukan.")
        return

    df_filtered = dataframe[dataframe[col_name] != '-']

    if df_filtered.empty:
        st.info(f"ℹ Tidak ada siswa yang memberikan komentar di {col_name}.")
    else:
        st.success(f"Ada {len(df_filtered)} siswa yang memberikan komentar di {col_name}.")
        st.dataframe(
            df_filtered[["NIM", "Nama_Mahasiswa", col_name]],
            use_container_width=True
        )


def tampilkan_mahasiswa_oop_dengan_komentar(dataframe, pertemuan=1, nama_dataset='Dataset Reguler'):
    st.header(f"📝 Daftar Mahasiswa yang Memberikan Komentar - {nama_dataset}")

    col_name = f"Pertemuan_{pertemuan}"

    if col_name not in dataframe.columns:
        st.error(f"Kolom {col_name} tidak ditemukan.")
        return

    df_filtered = dataframe[dataframe[col_name] != '-']

    if df_filtered.empty:
        st.info(f"ℹ Tidak ada siswa yang memberikan komentar di {col_name}.")
    else:
        st.success(f"Ada {len(df_filtered)} siswa yang memberikan komentar di {col_name}.")
        st.dataframe(
            df_filtered[["NIM", "Nama_Mahasiswa", col_name]],
            use_container_width=True
        )

def tampilkan_mahasiswa_ds_dengan_komentar(dataframe, pertemuan=1, nama_dataset='Dataset Reguler'):
    st.header(f"📝 Daftar Mahasiswa yang Memberikan Komentar - {nama_dataset}")

    col_name = f"Pertemuan_{pertemuan}"

    if col_name not in dataframe.columns:
        st.error(f"Kolom {col_name} tidak ditemukan.")
        return

    df_filtered = dataframe[dataframe[col_name] != '-']

    if df_filtered.empty:
        st.info(f"ℹ Tidak ada siswa yang memberikan komentar di {col_name}.")
    else:
        st.success(f"Ada {len(df_filtered)} siswa yang memberikan komentar di {col_name}.")
        st.dataframe(
            df_filtered[["NIM", "Nama_Mahasiswa", col_name]],
            use_container_width=True
        )

def tampilkan_mahasiswa_sta_dengan_komentar(dataframe, pertemuan=1, nama_dataset='Dataset Reguler'):
    st.header(f"📝 Daftar Mahasiswa yang Memberikan Komentar - {nama_dataset}")

    col_name = f"Pertemuan_{pertemuan}"

    if col_name not in dataframe.columns:
        st.error(f"Kolom {col_name} tidak ditemukan.")
        return

    df_filtered = dataframe[dataframe[col_name] != '-']

    if df_filtered.empty:
        st.info(f"ℹ Tidak ada siswa yang memberikan komentar di {col_name}.")
    else:
        st.success(f"Ada {len(df_filtered)} siswa yang memberikan komentar di {col_name}.")
        st.dataframe(
            df_filtered[["NIM", "Nama_Mahasiswa", col_name]],
            use_container_width=True
        )

def tampilkan_mahasiswa_dw_dengan_komentar(dataframe, pertemuan=1, nama_dataset='Dataset Reguler'):
    st.header(f"📝 Daftar Mahasiswa yang Memberikan Komentar - {nama_dataset}")

    col_name = f"Pertemuan_{pertemuan}"

    if col_name not in dataframe.columns:
        st.error(f"Kolom {col_name} tidak ditemukan.")
        return

    df_filtered = dataframe[dataframe[col_name] != '-']

    if df_filtered.empty:
        st.info(f"ℹ Tidak ada siswa yang memberikan komentar di {col_name}.")
    else:
        st.success(f"Ada {len(df_filtered)} siswa yang memberikan komentar di {col_name}.")
        st.dataframe(
            df_filtered[["NIM", "Nama_Mahasiswa", col_name]],
            use_container_width=True
        )




def sentimen_dbs_reguler(DATA_PATH_DBS):
    st.title("📘 Analisis Sentimen Komentar Database ")
    #st.markdown("Analisis otomatis sentimen pada komentar dari dataset **komentar_dbs_reguler.csv**.")

    # Analisis Sentimen per Pertemuan
    if st.sidebar.checkbox("[REGULER] Analisis Sentimen Database Sytems per Pertemuan",key='dbs_sentimen'):

        df = pd.read_csv(DATA_PATH_DBS, dtype=str)

        if len(df.columns) < 5:
            st.error("❌ File CSV harus punya setidaknya 5 kolom (NIM, Nama, Pertemuan_1, Pertemuan_2, Pertemuan_3).")
        else:
            pilihan = st.selectbox("Pilih Pertemuan untuk Analisis Sentimen", [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13], key='pilihan_pertemuan_dbs')
            tampilkan_sentimen_dbs_pertemuan(DATA_PATH_DBS, pertemuan=pilihan, senti=senti)
            tampilkan_mahasiswa_dbs_dengan_komentar(df, pertemuan=pilihan, nama_dataset='Dataset Reguler')

def tampilkan_kehadiran_dosen(df_abs_dosen ):
    if df_abs_dosen .empty:
        st.error("Data kehadiran dosen kosong.")
        return

    # Tabel Kehadiran Dosen
    st.subheader("📋 Tabel Kehadiran Dosen")
    st.dataframe(df_abs_dosen, use_container_width=True)

    # Statistik Kehadiran per Dosen
    st.subheader("📊 Statistik Kehadiran per Dosen")
    # Menghitung total kehadiran per dosen
    df_count = df_abs_dosen .groupby("Mata_kuliah")["Hadir"].sum().reset_index()
    df_count.columns = ["Mata_kuliah", "Jumlah Kehadiran"]
    st.dataframe(df_count, use_container_width=True)

    st.write("""
    🟣 Penjelasan:
    - Tabel di atas menampilkan daftar dosen beserta kehadirannya.
    - Statistik memberikan informasi mengenai total kehadiran masing-masing dosen.
    """)

    # Visualisasi
    st.subheader("📉 Visualisasi Kehadiran per Dosen")
    fig = px.bar(
        df_count,
        x='Mata_kuliah',
        y='Jumlah Kehadiran',
        text='Jumlah Kehadiran',
        color='Jumlah Kehadiran',
        color_continuous_scale='Blues'
    )
    fig.update_traces(textposition='outside')
    st.plotly_chart(fig, use_container_width=True)

def tampilkan_kehadiran_dosen_pro(df_abs_dosen_pro):
 
    if df_abs_dosen_pro.empty:
        st.error("Data kehadiran dosen (Pro) kosong.")
        return

    # Tabel Kehadiran Dosen
    st.subheader("📋 Tabel Kehadiran Dosen (Pro)",)
    st.dataframe(df_abs_dosen_pro, use_container_width=True)

    # Statistik Kehadiran per Mata Kuliah
    st.subheader("📊 Statistik Kehadiran per Mata Kuliah (Pro)",)
    df_count = df_abs_dosen_pro.groupby("Mata_kuliah")["Hadir"].sum().reset_index()
    df_count.columns = ["Mata_kuliah", "Jumlah Kehadiran"]
    st.dataframe(df_count, use_container_width=True)

    # Visualisasi per Mata Kuliah
    st.subheader("📉 Visualisasi Kehadiran per Mata Kuliah (Pro)",)
    fig = px.bar(
        df_count,
        x='Mata_kuliah',
        y='Jumlah Kehadiran',
        text='Jumlah Kehadiran',
        color='Jumlah Kehadiran',
        color_continuous_scale='Blues'
    )
    fig.update_traces(textposition='outside')
    st.plotly_chart(fig, use_container_width=True)


    # Visualisasi per Mata Kuliah dan Kelas
    st.subheader("📉 Visualisasi Kehadiran per Mata Kuliah dan Kelas (Pro)",)
    df_count_kelas = df_abs_dosen_pro.groupby(['Mata_kuliah', 'Kelas'])["Hadir"].sum().reset_index()
    df_count_kelas.columns = ['Mata_kuliah', 'Kelas', 'Jumlah_Kehadiran']

    fig_kelas = px.bar(
        df_count_kelas,
        x='Mata_kuliah',
        y='Jumlah_Kehadiran',
        color='Kelas',
        barmode='group',
        text='Jumlah_Kehadiran',
        title='Jumlah Kehadiran per Mata Kuliah dan Kelas'
    )
    fig_kelas.update_traces(textposition='outside')
    st.plotly_chart(fig_kelas, use_container_width=True)


def sentimen_cp_reguler(DATA_PATH_CP):
    st.title("📘 Analisis Sentimen Komentar Communication Protocols ")
    #st.markdown("Analisis otomatis sentimen pada komentar dari dataset **komentar_dbs_reguler.csv**.")

    # Analisis Sentimen per Pertemuan
    if st.sidebar.checkbox("[REGULER] Analisis Sentimen Communication Protocols per Pertemuan",key='cp_sentimen'):

        df = pd.read_csv(DATA_PATH_CP, dtype=str)

        if len(df.columns) < 5:
            st.error("❌ File CSV harus punya setidaknya 5 kolom (NIM, Nama, Pertemuan_1, Pertemuan_2, Pertemuan_3).")
        else:
            pilihan = st.selectbox("Pilih Pertemuan untuk Analisis Sentimen", [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16], key='pilihan_pertemuan_cp')
            tampilkan_sentimen_cp_pertemuan(DATA_PATH_CP, pertemuan=pilihan, senti=senti)
            tampilkan_mahasiswa_cp_dengan_komentar(df, pertemuan=pilihan, nama_dataset='Dataset Reguler')

def sentimen_cp_pros(DATA_PATH_CP_PRO):
    st.title("📘 Analisis Sentimen Komentar Communication Protocols ")
    #st.markdown("Analisis otomatis sentimen pada komentar dari dataset **komentar_dbs_reguler.csv**.")

    # Analisis Sentimen per Pertemuan
    if st.sidebar.checkbox("[PRO AKSEL] Analisis Sentimen Communication Protocols per Pertemuan",key='cp_sentimen'):

        df = pd.read_csv(DATA_PATH_CP_PRO, dtype=str)

        if len(df.columns) < 5:
            st.error("❌ File CSV harus punya setidaknya 5 kolom (NIM, Nama, Pertemuan_1, Pertemuan_2, Pertemuan_3).")
        else:
            pilihan = st.selectbox("Pilih Pertemuan untuk Analisis Sentimen", [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16], key='pilihan_pertemuan_cp')
            tampilkan_sentimen_cp_pro_pertemuan(DATA_PATH_CP_PRO, pertemuan=pilihan, senti=senti)
            tampilkan_mahasiswa_cp_pro_dengan_komentar(df, pertemuan=pilihan, nama_dataset='Dataset Reguler')

def sentimen_wcd_reguler(DATA_PATH_WCD):
    st.title("📘 Analisis Sentimen Komentar Web Client Development ")
    #st.markdown("Analisis otomatis sentimen pada komentar dari dataset **komentar_dbs_reguler.csv**.")

    # Analisis Sentimen per Pertemuan
    if st.sidebar.checkbox("[REGULER] Analisis Sentimen Web Client per Pertemuan",key='wcd_sentimen'):

        df = pd.read_csv(DATA_PATH_WCD, dtype=str)

        if len(df.columns) < 5:
            st.error("❌ File CSV harus punya setidaknya 5 kolom (NIM, Nama, Pertemuan_1, Pertemuan_2, Pertemuan_3).")
        else:
            pilihan = st.selectbox("Pilih Pertemuan untuk Analisis Sentimen", [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16], key='pilihan_pertemuan_wcd')
            tampilkan_sentimen_wcd_pertemuan(DATA_PATH_WCD, pertemuan=pilihan, senti=senti)
            tampilkan_mahasiswa_wcd_dengan_komentar(df, pertemuan=pilihan, nama_dataset='Dataset Reguler')

def sentimen_wcd_pros(DATA_PATH_WCD_PRO):
    st.title("📘 Analisis Sentimen Komentar Web Client Development ")
    #st.markdown("Analisis otomatis sentimen pada komentar dari dataset **komentar_dbs_reguler.csv**.")

    # Analisis Sentimen per Pertemuan
    if st.sidebar.checkbox("[PRO AKSEL] Analisis Sentimen Web Client per Pertemuan",key='wcd_sentimen'):

        df = pd.read_csv(DATA_PATH_WCD_PRO, dtype=str)

        if len(df.columns) < 5:
            st.error("❌ File CSV harus punya setidaknya 5 kolom (NIM, Nama, Pertemuan_1, Pertemuan_2, Pertemuan_3).")
        else:
            pilihan = st.selectbox("Pilih Pertemuan untuk Analisis Sentimen", [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16], key='pilihan_pertemuan_wcd')
            tampilkan_sentimen_wcd_pro_pertemuan(DATA_PATH_WCD_PRO, pertemuan=pilihan, senti=senti)
            tampilkan_mahasiswa_wcd_pro_dengan_komentar(df, pertemuan=pilihan, nama_dataset='Dataset Reguler')


def sentimen_oop_reguler(DATA_PATH_OOP):
    st.title("📘 Analisis Sentimen Komentar Object Oriented Programming")
    #st.markdown("Analisis otomatis sentimen pada komentar dari dataset **komentar_dbs_reguler.csv**.")

    # Analisis Sentimen per Pertemuan
    if st.sidebar.checkbox("[REGULER] Analisis Sentimen OOP per Pertemuan",key='oop_sentimen'):

        df = pd.read_csv(DATA_PATH_OOP, dtype=str)

        if len(df.columns) < 5:
            st.error("❌ File CSV harus punya setidaknya 5 kolom (NIM, Nama, Pertemuan_1, Pertemuan_2, Pertemuan_3).")
        else:
            pilihan = st.selectbox("Pilih Pertemuan untuk Analisis Sentimen", [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16], key='pilihan_pertemuan_oop')
            tampilkan_sentimen_oop_pertemuan(DATA_PATH_OOP, pertemuan=pilihan, senti=senti)
            tampilkan_mahasiswa_oop_dengan_komentar(df, pertemuan=pilihan, nama_dataset='Dataset Reguler')

def sentimen_ds_reguler(DATA_PATH_DS):
    st.title("📘 Analisis Sentimen Komentar Data Structures")
    #st.markdown("Analisis otomatis sentimen pada komentar dari dataset **komentar_dbs_reguler.csv**.")

    # Analisis Sentimen per Pertemuan
    if st.sidebar.checkbox("[REGULER] Analisis Sentimen Data Structures per Pertemuan",key='ds_sentimen'):

        df = pd.read_csv(DATA_PATH_DS, dtype=str)

        if len(df.columns) < 5:
            st.error("❌ File CSV harus punya setidaknya 5 kolom (NIM, Nama, Pertemuan_1, Pertemuan_2, Pertemuan_3).")
        else:
            pilihan = st.selectbox("Pilih Pertemuan untuk Analisis Sentimen", [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16], key='pilihan_pertemuan_ds')
            tampilkan_sentimen_ds_pertemuan(DATA_PATH_DS, pertemuan=pilihan, senti=senti)
            tampilkan_mahasiswa_ds_dengan_komentar(df, pertemuan=pilihan, nama_dataset='Dataset Reguler')

def sentimen_sta_reguler(DATA_PATH_STA):
    st.title("📘 Analisis Sentimen Komentar Statistical Thinking")
    #st.markdown("Analisis otomatis sentimen pada komentar dari dataset **komentar_dbs_reguler.csv**.")

    # Analisis Sentimen per Pertemuan
    if st.sidebar.checkbox("[REGULER] Analisis Sentimen Statistical Thinking per Pertemuan",key='sta_sentimen'):

        df = pd.read_csv(DATA_PATH_STA, dtype=str)

        if len(df.columns) < 5:
            st.error("❌ File CSV harus punya setidaknya 5 kolom (NIM, Nama, Pertemuan_1, Pertemuan_2, Pertemuan_3).")
        else:
            pilihan = st.selectbox("Pilih Pertemuan untuk Analisis Sentimen", [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16], key='pilihan_pertemuan_sta')
            tampilkan_sentimen_sta_pertemuan(DATA_PATH_STA, pertemuan=pilihan, senti=senti)
            tampilkan_mahasiswa_sta_dengan_komentar(df, pertemuan=pilihan, nama_dataset='Dataset Reguler')

def sentimen_dw_reguler(DATA_PATH_DW):
    st.title("📘 Analisis Sentimen Komentar Data Wrangling")
    #st.markdown("Analisis otomatis sentimen pada komentar dari dataset **komentar_dbs_reguler.csv**.")

    # Analisis Sentimen per Pertemuan
    if st.sidebar.checkbox("[REGULER] Analisis Sentimen Data Wrangling per Pertemuan",key='dw_sentimen'):

        df = pd.read_csv(DATA_PATH_DW, dtype=str)

        if len(df.columns) < 5:
            st.error("❌ File CSV harus punya setidaknya 5 kolom (NIM, Nama, Pertemuan_1, Pertemuan_2, Pertemuan_3).")
        else:
            pilihan = st.selectbox("Pilih Pertemuan untuk Analisis Sentimen", [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16], key='pilihan_pertemuan_dw')
            tampilkan_sentimen_dw_pertemuan(DATA_PATH_DW, pertemuan=pilihan, senti=senti)
            tampilkan_mahasiswa_dw_dengan_komentar(df, pertemuan=pilihan, nama_dataset='Dataset Reguler')



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
menu = st.sidebar.selectbox("📂 Pilih Menu", ["Profil Lulusan","Pemetaan Profesi Tiap Semester","Jumlah Mahasiswa","Kehadiran Mahasiswa", "Kehadiran Dosen","Nilai Tugas","Nilai Kuis","Nilai UTS Mahasiswa", "Nilai UAS Mahasiswa","Nilai Akhir Mahasiswa","Sentimen FeedBack Mahasiswa"])


if menu=="Profil Lulusan":
    st.title("📅 Profil Lulusan")
    tampilan_profil_lulusan(df_profil)
elif menu == "Pemetaan Profesi Tiap Semester":
    st.title("📄 Preview HTML Curriculum Dashboard")
    display_html_file(html_path="curriculum_visualization_ds_only.html")
    # Sub-menu kelas
    #sub_kelas = st.radio("Pilih Semester", ["Semester 1", "Semester 2","Semester 3","Semester 4","Semester 5","Semester 6","Semester 7","Semester 8"])

    #if sub_kelas == "Semester 1":
    #    st.subheader("📘 Mahasiswa - Kelas Reguler")
    #    st.info("📌 Visualisasi Total Mahasiswa untuk kelas Reguler.")
    #    dashboard_curriculum(df_curriculum)
    #elif sub_kelas == "Kelas Pro dan Aksel":
    #    st.subheader("📗 Kehadiran - Kelas Pro dan Aksel")
    #    st.info("📌 Visualisasi Total Mahasiswa untuk kelas Pro dan Aksel belum tersedia. Data atau fitur bisa ditambahkan di sini.")
    #    tampilkan_statistik_mahasiswa(df_mhs_pro)

# ====== Jumlah Seluruh Mahasiswa ======
elif menu == "Jumlah Mahasiswa":
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

# ====== KEHADIRAN Mahasiswa ======
elif menu == "Kehadiran Mahasiswa":
    st.title("📅 Kehadiran Mahasiswa")

    # Sub-menu kelas
    sub_kelas = st.radio("Pilih Kelas", ["Kelas Reguler", "Kelas Pro dan Aksel"])
    # Tambahkan informasi update terakhir
    st.markdown(
        "<div style='color: grey; font-size: 14px; margin-top: -10px;'>"
        "Update Terakhir: <b>Selasa, 15 Juli 2025, Pukul 11:08 AM</b>"
        "</div>",
        unsafe_allow_html=True
    )

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
        #st.info("📌 Visualisasi kehadiran untuk kelas Pro dan Aksel belum tersedia. Data atau fitur bisa ditambahkan di sini.")
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
            analisa_statistik_kehadiran_com_pro_pros(df_abs_com_pro_pros)

        with tab2:
            analisa_statistik_kehadiran_wcd_pros(df_abs_wcd_pros)

        with tab3:
            analisa_statistik_kehadiran_oop_pros(df_abs_oop_pros)

        with tab4:
            analisa_statistik_kehadiran_ds_pros(df_abs_ds_pros)

        with tab5:
            analisa_statistik_kehadiran_dbs_pros(df_abs_dbs_pros)
        
        with tab6:
            analisa_statistik_kehadiran_sta_pros(df_abs_sta_pros)

        with tab7:
            analisa_statistik_kehadiran_dw_pros(df_abs_dw_pros)

# ====== KEHADIRAN Dosen ======
elif menu == "Kehadiran Dosen":
    st.title("📅 Kehadiran Dosen")

    # Sub-menu kelas
    sub_kelas = st.radio("Pilih Kelas", ["Kelas Reguler", "Kelas Pro dan Aksel"])
    st.markdown(
        "<div style='color: grey; font-size: 14px; margin-top: -10px;'>"
        "Update Terakhir: <b>Senin, 07 Juli 2025, Pukul 03:13 PM</b>"
        "</div>",
        unsafe_allow_html=True
    )
    if sub_kelas == "Kelas Reguler":
        st.subheader("📘 Dosen - Kelas Reguler")
        st.info("📌 Visualisasi Total Kehadiran Dosen untuk kelas Reguler.")
        tampilkan_kehadiran_dosen(df_abs_dosen )
    elif sub_kelas == "Kelas Pro dan Aksel":
        st.subheader("📗 Kehadiran - Kelas Pro dan Aksel")
        st.info("📌 Visualisasi Total Kehadiran Dosen untuk kelas Pro dan Aksel")
        tampilkan_kehadiran_dosen_pro(df_abs_dosen_pro)

elif menu == "Nilai Tugas":
    st.title("📅 Nilai Tugas")
    # Sub-menu kelas
    sub_kelas = st.radio("Pilih Kelas", ["Kelas Reguler", "Kelas Pro dan Aksel"])
    st.markdown(
        "<div style='color: grey; font-size: 14px; margin-top: -10px;'>"
        "Update Terakhir: <b>Kamis, 10 Juli 2025, Pukul 10:35 AM</b>"
        "</div>",
        unsafe_allow_html=True
    )
    if sub_kelas == "Kelas Reguler":
        st.subheader("📘 Nilai Tugas - Kelas Reguler")
        st.info("📌 Visualisasi Nilai Tugas kelas Reguler.")
        statistik_dataset_tugas_reg(df_tugas_reguler)
    elif sub_kelas == "Kelas Pro dan Aksel":
        st.subheader("📗 Kehadiran - Kelas Pro dan Aksel")
        st.info("📌 Visualisasi Total Kehadiran Dosen untuk kelas Pro dan Aksel")
        tampilkan_kehadiran_dosen_pro(df_abs_dosen_pro)

elif menu == "Nilai Kuis":
    st.title("📅 Nilai Kuis")
    # Sub-menu kelas
    sub_kelas = st.radio("Pilih Kelas", ["Kelas Reguler", "Kelas Pro dan Aksel"])
    st.markdown(
        "<div style='color: grey; font-size: 14px; margin-top: -10px;'>"
        "Update Terakhir: <b>Kamis, 10 Juli 2025, Pukul 10:35 AM</b>"
        "</div>",
        unsafe_allow_html=True
    )
    if sub_kelas == "Kelas Reguler":
        st.subheader("📘 Nilai Kuis - Kelas Reguler")
        st.info("📌 Visualisasi Nilai Kuis kelas Reguler.")
        statistik_dataset_kuis_reg(df_kuis_reguler)
    elif sub_kelas == "Kelas Pro dan Aksel":
        st.subheader("📗 Kehadiran - Kelas Pro dan Aksel")
        st.info("📌 Visualisasi Total Kehadiran Dosen untuk kelas Pro dan Aksel")
        tampilkan_kehadiran_dosen_pro(df_abs_dosen_pro)


# ====== NILAI UTS ======
elif menu == "Nilai UTS Mahasiswa":
    tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
        "Soal Dosen", 
        "Nilai Reguler", 
        "Nilai Pro/Aksel", 
        "Mahasiswa < 60",
        "Mahasiswa = 0",
        "Mahasiswa > 60",
        "Statistik per Mahasiswa"
    ])

    with tab1:
        statistik_soal_dosen(df_dosen)

    with tab2:
        statistik_dataset_nilai_reg(df_reguler)

    with tab3:
        statistik_dataset_nilai_pro(df_pro)
        
    with tab4:
        statistik_nilai_kurang_60(df_reguler, df_pro)

    with tab5:
        statistik_nilai_samadengan_0(df_reguler, df_pro)

    with tab6:
        statistik_nilai_lebihsama_60(df_reguler, df_pro)

    with tab7:
        statistik_per_mahasiswa_by_kelas(df_reguler, df_pro)
elif menu == "Nilai UAS Mahasiswa":
    tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
        "Soal Dosen", 
        "Nilai Reguler", 
        "Nilai Pro/Aksel", 
        "Mahasiswa < 60",
        "Mahasiswa = 0",
        "Mahasiswa > 60",
        "Statistik per Mahasiswa"
    ])

    with tab1:
        statistik_soal_dosen_uas(df_dosen_uas)

    with tab2:
        statistik_dataset_nilai_reg(df_reguler)

    with tab3:
        statistik_dataset_nilai_pro(df_pro)
        
    with tab4:
        statistik_nilai_kurang_60(df_reguler, df_pro)

    with tab5:
        statistik_nilai_samadengan_0(df_reguler, df_pro)

    with tab6:
        statistik_nilai_lebihsama_60(df_reguler, df_pro)

    with tab7:
        statistik_per_mahasiswa_by_kelas(df_reguler, df_pro)

elif menu == "Nilai Akhir Mahasiswa":
    st.title("📅 Nilai Akhir Mahasiswa")

    # Sub-menu kelas
    sub_kelas = st.radio("Pilih Kelas", ["Kelas Reguler", "Kelas Pro dan Aksel"])
    # Tambahkan informasi update terakhir
    st.markdown(
        "<div style='color: grey; font-size: 14px; margin-top: -10px;'>"
        "Update Terakhir: <b>Kamis, 10 Juli 2025, Pukul 01:39 PM</b>"
        "</div>",
        unsafe_allow_html=True
    )

    if sub_kelas == "Kelas Reguler":
        st.subheader("📘 Nilai Akhir - Kelas Reguler")

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
            analisa_statistik_akhir_ds_reg(df_akhir_ds_reg)

        with tab5:
            analisa_statistik_kehadiran_dbs_reg(df_abs_dbs_reg)
        
        with tab6:
            analisa_statistik_kehadiran_sta_reg(df_abs_sta_reg)

        with tab7:
            analisa_statistik_kehadiran_dw_reg(df_abs_dw_reg)
                
        

    elif sub_kelas == "Kelas Pro dan Aksel":
        st.subheader("📗 Nilai Akhir - Kelas Pro dan Aksel")
        #st.info("📌 Visualisasi kehadiran untuk kelas Pro dan Aksel belum tersedia. Data atau fitur bisa ditambahkan di sini.")
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
            analisa_statistik_kehadiran_com_pro_pros(df_abs_com_pro_pros)

        with tab2:
            analisa_statistik_kehadiran_wcd_pros(df_abs_wcd_pros)

        with tab3:
            analisa_statistik_kehadiran_oop_pros(df_abs_oop_pros)

        with tab4:
            analisa_statistik_kehadiran_ds_pros(df_abs_ds_pros)

        with tab5:
            analisa_statistik_kehadiran_dbs_pros(df_abs_dbs_pros)
        
        with tab6:
            analisa_statistik_kehadiran_sta_pros(df_abs_sta_pros)

        with tab7:
            analisa_statistik_kehadiran_dw_pros(df_abs_dw_pros)


elif menu == "Sentimen FeedBack Mahasiswa":
    st.title("📅 Sentimen FeedBack Mahasiswa")

    # Sub-menu kelas
    sub_kelas = st.radio("Pilih Kelas", ["Kelas Reguler", "Kelas Pro dan Aksel"])

    if sub_kelas == "Kelas Reguler":
        st.subheader("📘 FeedBack - Kelas Reguler")

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
            sentimen_cp_reguler(DATA_PATH_CP)

        with tab2:
            sentimen_wcd_reguler(DATA_PATH_WCD)

        with tab3:
            sentimen_oop_reguler(DATA_PATH_OOP)

        with tab4:
            sentimen_ds_reguler(DATA_PATH_DS)

        with tab5:
            sentimen_dbs_reguler(DATA_PATH_DBS)
        
        with tab6:
            sentimen_sta_reguler(DATA_PATH_STA)

        with tab7:
            sentimen_dw_reguler(DATA_PATH_DW)              

    elif sub_kelas == "Kelas Pro dan Aksel":
        st.subheader("📗 FeedBack - Kelas Pro dan Aksel")
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
            sentimen_cp_pros(DATA_PATH_CP_PRO)

        with tab2:
            #print("test")
            sentimen_wcd_pros(DATA_PATH_WCD_PRO)

        with tab3:
            print("test")
            #sentimen_oop_reguler(DATA_PATH_OOP)

        with tab4:
            print("test")
            #sentimen_ds_reguler(DATA_PATH_DS)

        with tab5:
            print("test")
            #sentimen_dbs_reguler(DATA_PATH_DBS)
        
        with tab6:
            print("test")
            #sentimen_sta_reguler(DATA_PATH_STA)

        with tab7:
            print("test")
            #sentimen_dw_reguler(DATA_PATH_DW)              


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


if st.session_state.get("logged_in", False):
    st.markdown("""
    <style>
    #floating-button {
        position: fixed;
        bottom: 20px;
        right: 20px;
        background-color: #4CAF50;
        color: white;
        border: none;
        padding: 14px 20px;
        border-radius: 50px;
        font-size: 16px;
        box-shadow: 0px 0px 10px rgba(0,0,0,0.2);
        cursor: pointer;
        z-index: 9999;
    }
    </style>
    <a href="https://adambhuana.app.n8n.cloud/webhook/8d1e8904-f75e-493d-b7d1-071d26158c23/chat" target="_blank">
        <div id="floating-button">💬 Chatbot</div>
    </a>
    """, unsafe_allow_html=True)
