# ptp-learning-analytics-studio
Dashboard analitik pelatihan berbasis learning theory

# PTP Learning Analytics Studio

**PTP Learning Analytics Studio** adalah aplikasi dashboard analitik pelatihan yang dikembangkan oleh **Pengembang Teknologi Pembelajaran (PTP)** di Pusdiklat Anggaran dan Perbendaharaan.

Proyek ini menghubungkan:

- **Teori belajar (learning theory)**  
- **Data pelatihan** (profil peserta, progres LMS/KLC, nilai kuis/ujian, evaluasi pengajar & penyelenggara, dsb.)  
- Menjadi **insight dan rekomendasi desain pembelajaran** yang bisa digunakan berulang kali untuk berbagai pelatihan.

Pilot awal menggunakan data pelatihan **PPK (Pejabat Pembuat Komitmen)**, tetapi struktur sistem dirancang agar **bisa digunakan untuk pelatihan lain** cukup dengan meng-upload data baru.

---

## 🎯 Tujuan Proyek

1. Menyediakan **dashboard analitik pelatihan** yang:
   - Mudah digunakan oleh pengelola pelatihan dan widyaiswara.
   - Dapat di-*reuse* untuk berbagai jenis pelatihan.

2. Mengimplementasikan pendekatan **“from learning theory to learning technology”**:
   - Pertanyaan analitik berangkat dari **teori belajar**.
   - Hasil analitik diterjemahkan menjadi **rekomendasi redesign pembelajaran**.

3. Memanfaatkan:
   - **Streamlit** sebagai antarmuka aplikasi.
   - **GitHub** untuk versioning & kolaborasi.
   - **OpenAI** untuk:
     - Menjelaskan hasil analisis dalam bahasa natural.
     - Meringkas komentar/saran peserta.
     - Mengusulkan ide redesign pembelajaran.

---

## 🧠 Lensa Teori Belajar & Pertanyaan Analitik

PTP Learning Analytics Studio menggunakan beberapa lensa teori belajar. Tiap lensa dihubungkan dengan **pertanyaan analitik** dan **data yang dibutuhkan**.

### 1. Behaviourism (Perilaku & Penguatan)

Fokus: hubungan **stimulus – respon – reinforcement** (contoh: latihan soal + feedback + pengulangan).

**Contoh pertanyaan analitik:**

- Apakah peserta yang **lebih sering mengulang kuis** (lebih banyak attempt) memiliki **skor akhir lebih tinggi**?
- Apakah pola attempt peserta mengindikasikan **latihan yang bermakna**, atau sekadar **trial-and-error untuk mengejar nilai minimal**?
- Bagaimana distribusi skor kuis per attempt (attempt 1 vs attempt terakhir)?

**Data yang dibutuhkan:**

- Log nilai kuis/ujian dengan:
  - ID peserta (misal: NIP, `participant_id`)
  - Jenis kuis/ujian
  - Nomor attempt (1, 2, 3, dst.)
  - Skor per attempt

---

### 2. Cognitivism (Pemrosesan Informasi & Time-on-Task)

Fokus: bagaimana peserta **memproses informasi**, mengelola memori, dan membangun **struktur pengetahuan**.

**Contoh pertanyaan analitik:**

- Berapa **total durasi belajar** (time-on-task) tiap peserta di KLC/LMS?
- Modul mana yang:
  - Sangat cepat diselesaikan (mungkin terlalu mudah atau hanya diklik tanpa diperhatikan).
  - Sangat lama diselesaikan (mungkin materinya sulit atau navigasinya membingungkan).
- Adakah hubungan antara **total waktu belajar** dan **nilai kuis/ujian**?

**Data yang dibutuhkan:**

- Log progres belajar yang memuat:
  - ID peserta
  - Nama/kode modul
  - Tanggal/waktu mulai
  - Tanggal/waktu selesai (opsional)
  - Durasi belajar (bisa dalam format jam:menit:detik)
- Data nilai kuis/ujian:
  - ID peserta
  - Skor

---

### 3. Self-Regulated Learning (SRL)

Fokus: kemampuan peserta untuk **mengatur belajar sendiri** (menetapkan tujuan, mengelola waktu, memonitor progres, dan refleksi).

**Contoh pertanyaan analitik:**

- Kapan peserta mulai mengerjakan modul?  
  Apakah mereka:
  - “Early starters” (mulai awal, progres stabil),
  - “Steady workers” (bertahap),
  - atau “Last-minute learners” (menumpuk di akhir)?
- Seberapa banyak aktivitas belajar yang terjadi di **hari-hari terakhir** sebelum ujian?
- Apakah pola belajar (steady vs last-minute) berhubungan dengan:
  - Peluang kelulusan,
  - Nilai kuis/ujian,
  - Evaluasi diri (jika ada)?

**Data yang dibutuhkan:**

- Log progres belajar dengan:
  - ID peserta
  - Tanggal/waktu penyelesaian modul
- Informasi jadwal pelatihan:
  - Tanggal mulai
  - Tanggal akhir
  - Tanggal ujian (jika ada)
- Data nilai kuis/ujian dan/atau status kelulusan.

---

### 4. Social Constructivism (Belajar sebagai Proses Sosial)

Fokus: pengetahuan dikonstruksi bersama melalui **interaksi sosial**, diskusi, dan kolaborasi.

**Contoh pertanyaan analitik:**

- Seberapa aktif peserta di:
  - Forum diskusi,
  - Chat/komentar,
  - Kegiatan kelompok (kalau ada datanya)?
- Apakah peserta yang lebih aktif berdiskusi:
  - Lebih tinggi nilai tugas/ujian,
  - Lebih puas terhadap pelatihan,
  - atau memberi masukan yang berbeda?

**Data yang dibutuhkan:**

- Log interaksi sosial di LMS:
  - ID peserta
  - Jumlah posting, reply, likes, views, dsb.
- Data hasil belajar (nilai, kelulusan).
- Data evaluasi (kepuasan, persepsi manfaat).

---

## 📊 Jenis Data Pelatihan yang Didukung

Secara umum, PTP Learning Analytics Studio dirancang untuk menangani beberapa jenis data berikut:

1. **Profil Peserta**
   - ID peserta (NIP / `participant_id`)
   - Nama
   - Unit kerja / instansi
   - Jabatan
   - Informasi lain (opsional)

2. **Progres Belajar (KLC / LMS)**
   - ID peserta
   - Nama/kode modul
   - Status (belum mulai / sedang / selesai)
   - Durasi belajar (dalam menit atau jam:menit:detik)
   - Tanggal/waktu akses dan penyelesaian (jika tersedia)

3. **Nilai Kuis / Ujian**
   - ID peserta
   - Jenis kuis/ujian
   - Nomor attempt
   - Skor per attempt
   - Skor rata-rata / skor akhir (bisa dihitung di aplikasi)

4. **Evaluasi Pengajar (Evajar)**
   - Nama pengajar
   - Mata pelajaran
   - Skor harapan & kenyataan per aspek
   - Saran / masukan naratif

5. **Evaluasi Penyelenggara (Evagara)**
   - Aspek layanan (administrasi, sarana prasarana, dukungan teknis, dsb.)
   - Skor harapan & kenyataan
   - Saran / masukan naratif

6. **(Opsional) Aktivitas Forum / Diskusi**
   - ID peserta
   - Jumlah posting
   - Jumlah reply
   - Jumlah views / likes
   - Waktu posting

---

## 🏗️ Arsitektur Aplikasi (Singkat)

- **Frontend & logika aplikasi:**  
  - [Streamlit](https://streamlit.io/) (Python)
- **Pengolahan data:**  
  - `pandas`, `numpy`, `scipy`
- **Analitik & narasi berbasis AI:**  
  - API [OpenAI](https://platform.openai.com/) untuk:
    - Penjelasan hasil korelasi/ANOVA
    - Ringkasan komentar/saran
    - Rekomendasi redesign pembelajaran
- **Version control & kolaborasi:**
  - Git + GitHub

---

## 🚀 Fitur Utama PTP Learning Analytics Studio

1. **Upload & Kelola Dataset Pelatihan**
   - Upload data profil, progres, kuis, dan evaluasi dalam format CSV/Excel.
   - Mendukung banyak pelatihan sekaligus (misalnya PPK, pelatihan lain sebagai pilot berikutnya).

2. **Overview Pelatihan**
   - Jumlah peserta.
   - Completion rate modul.
   - Ringkasan time-on-task.
   - (Opsional) ringkasan kelulusan (NA, NK, retake, dsb. jika datanya tersedia).

3. **Learning Theory Lens**
   - Tab khusus untuk setiap lensa teori:
     - Behaviourism
     - Cognitivism
     - Self-Regulated Learning (SRL)
     - Social Constructivism (jika data interaksi tersedia)
   - Menampilkan visualisasi data (grafik) dan **narasi otomatis** berbasis OpenAI.

4. **Evaluasi Pengajar & Penyelenggara**
   - Ringkasan skor harapan vs kenyataan.
   - Ringkasan tema utama dari “Saran / Masukan” peserta (dengan bantuan OpenAI).

5. **Participant 360 & Early Warning**
   - Tampilan profil belajar per peserta:
     - Progres modul.
     - Time-on-task.
     - Skor kuis/ujian.
   - Indikator risiko (misalnya progres rendah menjelang akhir pelatihan).
   - Contoh pesan coaching personal yang dihasilkan dengan OpenAI.

6. **Hypothesis Builder (From Theory to Analysis)**
   - Memilih:
     - Outcome (mis. nilai, kelulusan, kepuasan).
     - Predictor (time-on-task, jumlah attempt, pola belajar, dsb.).
     - Lensa teori.
   - Menjalankan analisis sederhana (korelasi, ANOVA).
   - Menghasilkan penjelasan hasil dan implikasi desain pembelajaran.

---

## 📦 Instalasi & Menjalankan Aplikasi (Ringkas)

> Catatan: bagian ini contoh. Silakan sesuaikan dengan kebutuhan lingkungan Ibu.

1. **Clone repository**

   ```bash
   git clone https://github.com/USERNAME/ptp-learning-analytics-studio.git
   cd ptp-learning-analytics-studio
