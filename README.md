# Proyek Analisis Data: Brazilian E-Commerce Public Dataset

## Deskripsi Proyek
Proyek ini dibuat untuk melakukan analisis mendalam terhadap **Brazilian E-Commerce Public Dataset** (oleh Olist). Tujuan dari proyek ini adalah untuk menerapkan proses analisis data yang komprehensif mulai dari *Data Wrangling* (Pengumpulan, Penilaian, dan Pembersihan Data), *Exploratory Data Analysis* (EDA), hingga *Data Visualization* guna menjawab pertanyaan-pertanyaan bisnis yang relevan. Selain itu, proyek ini juga dilengkapi dengan *dashboard* interaktif.

## Struktur Direktori
- `/dashboard`: Berisi kode sumber untuk *dashboard* interaktif yang dibangun menggunakan Streamlit.
- `/data`: Berisi kumpulan dataset dalam format `.csv` yang digunakan selama proses analisis.
- `Proyek_Analisis_Data.ipynb`: File Jupyter Notebook yang memuat seluruh tahapan analisis data secara berurutan.
- `requirements.txt`: Daftar *library* atau *package* Python yang dibutuhkan untuk menjalankan proyek ini.
- `url.txt`: Tautan menuju *dashboard* yang sudah di-*deploy* ke *cloud* (Streamlit Community Cloud).

## Setup Environment

Untuk menjalankan proyek ini di komputer lokal, ikuti langkah-langkah di bawah ini:

### Menggunakan Anaconda
```bash
conda create --name main-ds python=3.9
conda activate main-ds
pip install -r requirements.txt
```

### Menggunakan Virtual Environment (venv)
```bash
mkdir proyek-analisis-data
cd proyek-analisis-data
python -m venv venv

# Untuk pengguna Windows:
venv\Scripts\activate
# Untuk pengguna Mac/Linux:
source venv/bin/activate

pip install -r requirements.txt
```

### Menjalankan Dashboard
Setelah environment aktif dan semua library terinstal
```bash
cd dashboard
streamlit run dashboard.py
```
