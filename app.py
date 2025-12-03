import os
import streamlit as st
import pandas as pd
from openai import OpenAI

# ====== KONFIGURASI DASAR ======
st.set_page_config(page_title="PTP Learning Analytics Studio", layout="wide")

# Baca API key OpenAI dari environment (diisi dari Streamlit Secrets)
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key) if api_key else None

# Simpan dataset di session_state (bisa banyak pelatihan)
if "datasets" not in st.session_state:
    # Struktur:
    # {"Nama Pelatihan": {"profile": df, "progress": df, "quiz": df,
    #                     "eval_teacher": df, "eval_org": df}}
    st.session_state.datasets = {}

# ====== FUNGSI BANTU ======
def load_table(uploaded_file):
    """Membaca CSV atau Excel menjadi DataFrame pandas."""
    if uploaded_file is None:
        return None
    name = uploaded_file.name.lower()
    if name.endswith(".csv"):
        # Banyak file KLC pakai pemisah ; → coba dulu ; lalu fallback ,
        try:
            return pd.read_csv(uploaded_file, sep=";")
        except Exception:
            uploaded_file.seek(0)
            return pd.read_csv(uploaded_file)
    elif name.endswith(".xlsx") or name.endswith(".xls"):
        # Pakai openpyxl untuk file Excel
        try:
            return pd.read_excel(uploaded_file, engine="openpyxl")
        except Exception:
            uploaded_file.seek(0)
            return pd.read_excel(uploaded_file)
    else:
        # fallback: coba baca sebagai Excel tanpa lihat ekstensi
        try:
            return pd.read_excel(uploaded_file, engine="openpyxl")
        except Exception:
            uploaded_file.seek(0)
            return pd.read_csv(uploaded_file)

# ====== SIDEBAR MENU ======
st.sidebar.title("PTP Learning Analytics Studio")
page = st.sidebar.radio(
    "Menu",
    ["Beranda", "Upload Data Pelatihan", "Overview Pelatihan"],
)

# Pilihan dataset aktif (untuk halaman selain Upload)
dataset_name = None
if st.session_state.datasets and page != "Upload Data Pelatihan":
    dataset_name = st.sidebar.selectbox(
        "Pilih dataset pelatihan",
        list(st.session_state.datasets.keys()),
    )
    current_data = st.session_state.datasets.get(dataset_name, {})
else:
    current_data = {}

# ====== HALAMAN: BERANDA ======
if page == "Beranda":
    st.title("PTP Learning Analytics Studio")

    st.write("""
    Selamat datang di **PTP Learning Analytics Studio**.

    Aplikasi ini dikembangkan oleh **Pengembang Teknologi Pembelajaran (PTP)**
    untuk menganalisis data pelatihan berdasarkan teori belajar, dengan contoh awal
    pelatihan PPK dan dapat digunakan ulang untuk pelatihan lain.
    """)

    if client is None:
        st.warning(
            "OPENAI_API_KEY belum tersedia. "
            "Set dulu di Streamlit Secrets (Settings → Secrets) agar fitur AI aktif."
        )
    else:
        st.success("Koneksi ke OpenAI siap digunakan ✅")

        st.subheader("Coba tanya sesuatu ke PTP Learning Analytics Studio")
        prompt = st.text_area(
            "Tuliskan pertanyaan atau minta penjelasan "
            "(misalnya: 'Jelaskan apa itu self-regulated learning dalam konteks pelatihan PPK')",
            height=120,
        )

        if st.button("Kirim ke OpenAI") and prompt.strip():
            with st.spinner("Meminta jawaban dari OpenAI..."):
                try:
                    response = client.responses.create(
                        model="gpt-4.1-mini",
                        input=prompt,
                    )
                    answer = response.output[0].content[0].text
                    st.markdown("### Jawaban OpenAI")
                    st.write(answer)
                except Exception as e:
                    st.error(f"Terjadi kesalahan saat memanggil OpenAI: {e}")

# ====== HALAMAN: UPLOAD DATA ======
elif page == "Upload Data Pelatihan":
    st.title("Upload Data Pelatihan")

    st.write("Isi nama pelatihan dan upload berkas datanya (PPK sebagai contoh pilot).")

    nama_pelatihan = st.text_input(
        "Nama pelatihan",
        value="PPK PJJ Kelas A",
        placeholder="Contoh: PPK PJJ Kelas A",
    )

    col1, col2 = st.columns(2)

    with col1:
        profile_file = st.file_uploader(
            "Profil Peserta (CSV/Excel)",
            type=["csv", "xlsx"],
            key="profile",
        )
        progress_file = st.file_uploader(
            "Log Progres KLC/LMS",
            type=["csv", "xlsx"],
            key="progress",
        )
        quiz_file = st.file_uploader(
            "Nilai Kuis/Ujian",
            type=["csv", "xlsx"],
            key="quiz",
        )

    with col2:
        eval_teacher_file = st.file_uploader(
            "Rekap Evaluasi Pengajar (Evajar)",
            type=["csv", "xlsx"],
            key="evajar",
        )
        eval_org_file = st.file_uploader(
            "Rekap Evaluasi Penyelenggara (Evagara)",
            type=["csv", "xlsx"],
            key="evagara",
        )

    if st.button("Simpan dataset pelatihan"):
        if not nama_pelatihan.strip():
            st.error("Nama pelatihan tidak boleh kosong.")
        else:
            st.session_state.datasets[nama_pelatihan.strip()] = {
                "profile": load_table(profile_file),
                "progress": load_table(progress_file),
                "quiz": load_table(quiz_file),
                "eval_teacher": load_table(eval_teacher_file),
                "eval_org": load_table(eval_org_file),
            }
            st.success(f"Dataset '{nama_pelatihan}' tersimpan di sesi aplikasi.")

    if st.session_state.datasets:
        st.markdown("### Dataset yang sudah tersimpan di sesi:")
        st.write(list(st.session_state.datasets.keys()))

# ====== HALAMAN: OVERVIEW ======
elif page == "Overview Pelatihan":
    st.title("Overview Pelatihan")

    if not current_data:
        st.info("Belum ada dataset yang dipilih. Silakan upload data di menu 'Upload Data Pelatihan'.")
    else:
        st.markdown(f"### Ringkasan untuk pelatihan: **{dataset_name}**")

        profile = current_data.get("profile")
        progress = current_data.get("progress")
        quiz = current_data.get("quiz")

        colA, colB, colC = st.columns(3)

        # Contoh metrik sederhana
        if profile is not None:
            colA.metric("Jumlah Peserta", len(profile))
        else:
            colA.metric("Jumlah Peserta", "–")

        if progress is not None:
            colB.metric("Baris log progres", len(progress))
        else:
            colB.metric("Baris log progres", "–")

        if quiz is not None:
            colC.metric("Baris data kuis/ujian", len(quiz))
        else:
            colC.metric("Baris data kuis/ujian", "–")

        st.markdown("#### Cuplikan Data")
        tab1, tab2, tab3 = st.tabs(["Profil Peserta", "Progres KLC/LMS", "Nilai Kuis/Ujian"])

        with tab1:
            if profile is not None:
                st.dataframe(profile.head())
            else:
                st.write("Belum ada data profil peserta.")

        with tab2:
            if progress is not None:
                st.dataframe(progress.head())
            else:
                st.write("Belum ada data progres.")

        with tab3:
            if quiz is not None:
                st.dataframe(quiz.head())
            else:
                st.write("Belum ada data kuis/ujian.")
