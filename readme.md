📊 E-Commerce Data Analysis Project
📌 Deskripsi
Proyek ini menganalisis E-Commerce Public Dataset dengan tujuan:

Mengidentifikasi performa kategori produk berdasarkan pendapatan.

Menemukan pola pembelian di wilayah tertentu (khususnya Sao Paulo).

Menganalisis perilaku pelanggan menggunakan metode RFM (Recency, Frequency, Monetary).

🎯 Pertanyaan Bisnis (SMART)
Specific & Time-bound: Kategori produk apa yang menghasilkan total pendapatan tertinggi selama periode Januari 2017 – Agustus 2018?

Specific & Measurable: Apa saja 3 kategori produk dengan volume penjualan terbanyak di wilayah Sao Paulo (SP) pada rentang tahun 2017–2018?

Action-oriented: Wilayah mana saja yang memberikan kontribusi pendapatan kumulatif lebih dari 50%, dan bagaimana rekomendasi strategis untuk wilayah tersebut?

📂 Struktur Folder
dashboard/ → berisi dashboard.py (visualisasi) dan main_data.csv (data yang sudah dibersihkan).

data/ → berisi dataset mentah (raw data) dalam format CSV.

notebook.ipynb → berisi proses Data Wrangling, EDA, dan visualisasi data.

requirements.txt → daftar library Python yang dibutuhkan.

url.txt → tautan dashboard yang sudah dideploy di Streamlit Cloud.

⚙️ Cara Menjalankan Dashboard Secara Lokal

1. Persiapkan Virtual Environment
   bash
   python -m venv venv
2. Aktivasi Virtual Environment
   Windows (PowerShell):

bash
.\venv\Scripts\Activate.ps1
Windows (CMD):

bash
venv\Scripts\activate
macOS/Linux:

bash
source venv/bin/activate 3. Instalasi Library
bash
pip install -r requirements.txt 4. Menjalankan Dashboard Streamlit
bash
streamlit run
