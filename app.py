import os
import streamlit as st
from openai import OpenAI

# Baca API key dari environment (diisi dari Streamlit Secrets)
api_key = os.getenv("OPENAI_API_KEY")

if api_key:
    client = OpenAI(api_key=api_key)
else:
    client = None

st.set_page_config(page_title="PTP Learning Analytics Studio")

st.title("PTP Learning Analytics Studio")
st.write("""
Selamat datang di PTP Learning Analytics Studio.

Aplikasi ini dikembangkan oleh Pengembang Teknologi Pembelajaran (PTP)
untuk menganalisis data pelatihan berdasarkan teori belajar.
""")

# Info status koneksi ke OpenAI
if client is None:
    st.warning(
        "OPENAI_API_KEY belum tersedia. "
        "Set dulu di Streamlit Secrets (Settings → Secrets) agar fitur AI aktif."
    )
else:
    st.success("Koneksi ke OpenAI siap digunakan ✅")

    st.subheader("Coba tanya sesuatu ke PTP Learning Analytics Studio")
    prompt = st.text_area(
        "Tuliskan pertanyaan atau minta penjelasan (misalnya: "
        "'Jelaskan apa itu self-regulated learning dalam konteks pelatihan PPK')",
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
