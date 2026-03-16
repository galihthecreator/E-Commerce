
import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
st.set_page_config(page_title='E-Commerce Dashboard', layout='wide')

def create_daily_orders_df(df):
  daily_orders_df = df.resample(rule='D', on='order_purchase_timestamp').agg({
      "order_id": "nunique",
      "payment_value": "sum"})
  return daily_orders_df

# Load
parent_path = Path(__file__).parent
file_path = parent_path / "all_data.csv"

@st.cache_data
def load_data(path):
    df = pd.read_csv(path)
    df['order_purchase_timestamp'] = pd.to_datetime(df['order_purchase_timestamp'])
    return df

if not file_path.exists():
    st.error(f"File {file_path} tidak ditemukan! Pastikan main_data.csv ada di folder dashboard.")
    st.stop()

all_df = load_data(file_path)

# --- SIDEBAR FILTER ---
with st.sidebar:
    st.image("https://github.com/dicodingacademy/assets/raw/main/logo.png")
    st.title("Filter Data")
    
    # Filter Rentang Waktu (Aspek Time-bound SMART)
    start_date, end_date = st.date_input(
        label='Rentang Waktu Analisis',
        min_value=all_df['order_purchase_timestamp'].min(),
        max_value=all_df['order_purchase_timestamp'].max(),
        value=[all_df['order_purchase_timestamp'].min(), all_df['order_purchase_timestamp'].max()]
    )

# Filter dataframe utama
main_df = all_df[(all_df["order_purchase_timestamp"] >= str(start_date)) & 
                (all_df["order_purchase_timestamp"] <= str(end_date))]

# --- HEADER ---
st.header('E-Commerce Performance Dashboard 📊')
st.write(f"Analisis data dari periode **{start_date}** sampai **{end_date}**")

# --- METRICS UTAMA ---
col1, col2, col3 = st.columns(3)
with col1:
    total_orders = main_df.order_id.nunique()
    st.metric("Total Pesanan", value=total_orders)
with col2:
    total_revenue = main_df.price.sum()
    st.metric("Total Pendapatan", value=f"R$ {total_revenue:,.2f}")
with col3:
    avg_review = main_df.review_score.mean() if 'review_score' in main_df.columns else 0
    st.metric("Rata-rata Rating", value=f"{avg_review:.2f}")

# --- PERTANYAAN 1: REVENUE BY CATEGORY ---
st.subheader("1. Kategori Produk dengan Pendapatan Tertinggi")
category_rev_df = main_df.groupby("product_category_name_english").price.sum().sort_values(ascending=False).reset_index().head(10)

fig, ax = plt.subplots(figsize=(12, 6))
sns.barplot(x="price", y="product_category_name_english", data=category_rev_df, palette="viridis", ax=ax)
ax.set_title("Top 10 Kategori Produk (Revenue)", fontsize=15)
st.pyplot(fig)

with st.expander("Insight Pertanyaan 1"):
    best_cat = category_rev_df.iloc[0]['product_category_name_english']
    st.write(f"Kategori **{best_cat}** Insight: Kategori Health & Beauty dan Watches & Gifts menghasilkan pendapatan tertinggi, namun Bed Bath Table memiliki volume penjualan (jumlah transaksi) terbanyak. Hal ini menunjukkan kategori kecantikan memiliki nilai per transaksi yang lebih tinggi (High Value).")
    st.write(f" Rekomendasi Langkah: Marketing Focus: Alokasikan anggaran iklan (Ads) lebih besar pada kategori Health & Beauty untuk memaksimalkan ROI (Return on Investment).Bundling Strategy: Buat paket bundling antara produk Bed Bath Table (yang populer) dengan aksesoris dari kategori Health & Beauty untuk meningkatkan nilai rata-rata keranjang belanja (Average Order Value).")

# --- PERTANYAAN 2: SAO PAULO ANALYSIS ---
st.subheader("2. Produk Terlaris di Wilayah Sao Paulo (SP)")
sp_df = main_df[main_df['customer_state'] == 'SP']
sp_cat_df = sp_df.groupby("product_category_name_english").order_id.nunique().sort_values(ascending=False).reset_index().head(5)

fig, ax = plt.subplots(figsize=(12, 6))
sns.barplot(x="order_id", y="product_category_name_english", data=sp_cat_df, palette="magma", ax=ax)
ax.set_title("Top 5 Kategori Paling Sering Dibeli di Sao Paulo", fontsize=15)
st.pyplot(fig)

with st.expander("Insight Pertanyaan 2"):
    st.write("Insight: Sao Paulo adalah pasar terbesar dengan kebutuhan dominan pada produk rumah tangga (Bed Bath Table dan Furniture Decor). Pengiriman ke wilayah ini paling padat namun memiliki potensi keterlambatan jika stok tidak siap.")
    st.write("Rekomendasi Langkah: Inventory Placement: Pastikan stok kategori rumah tangga selalu tersedia di gudang/pusat distribusi yang paling dekat dengan wilayah Sao Paulo untuk menjamin pengiriman Same Day atau Next Day.Localized Promo: Berikan promo ongkos kirim flat atau gratis untuk wilayah SP pada kategori furnitur besar guna menghilangkan hambatan biaya kirim bagi pelanggan.")
# --- PERTANYAAN 3: REGIONAL CONTRIBUTION ---
st.subheader("3. Kontribusi Pendapatan Wilayah (>50%)")
state_rev_df = main_df.groupby("customer_state").price.sum().sort_values(ascending=False).reset_index()
state_rev_df['percentage'] = (state_rev_df['price'] / state_rev_df['price'].sum()) * 100
state_rev_df['cumulative'] = state_rev_df['percentage'].cumsum()

# Filter yang kumulatifnya sampai 50% lebih sedikit
top_states = state_rev_df[state_rev_df['cumulative'] <= 60] # Mengambil hingga ~60% agar terlihat visualnya

fig, ax = plt.subplots(figsize=(10, 5))
sns.barplot(x="customer_state", y="percentage", data=top_states, palette="Blues_r", ax=ax)
ax.set_title("Negara Bagian Penyumbang Pendapatan Terbesar", fontsize=15)
st.pyplot(fig)

with st.expander("Insight Pertanyaan 3"):
    st.write("Insight: Sekitar 50% pendapatan berasal dari beberapa negara bagian utama seperti Sao Paulo (SP), Rio de Janeiro (RJ), dan Minas Gerais (MG). Ini menunjukkan ketergantungan yang tinggi pada pasar-pasar besar tersebut.")
    st.write("Rekomendasi Langkah: Market Diversification: Kembangkan strategi pemasaran untuk memperluas jangkauan ke negara bagian lain yang potensial untuk mengurangi risiko ketergantungan pada pasar besar.Regional Campaigns: Buat kampanye pemasaran yang disesuaikan dengan karakteristik dan preferensi konsumen di negara bagian utama untuk mempertahankan dan meningkatkan pangsa pasar di wilayah tersebut.")

# --- ANALISIS RFM ---
st.subheader("Best Customer Based on RFM Parameters")
# Logika sederhana RFM
now = main_df['order_purchase_timestamp'].max() + pd.Timedelta(days=1)
rfm_df = main_df.groupby(by="customer_id", as_index=False).agg({
    "order_purchase_timestamp": lambda x: (now - x.max()).days,
    "order_id": "count",
    "price": "sum"
})
rfm_df.columns = ["customer_id", "recency", "frequency", "monetary"]

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Avg Recency (Days)", value=round(rfm_df.recency.mean(), 1))
with col2:
    st.metric("Avg Frequency", value=round(rfm_df.frequency.mean(), 2))
with col3:
    st.metric("Avg Monetary", value=f"R$ {rfm_df.monetary.mean():,.2f}")

with st.expander("Insight RFM Analysis"):
    st.write("Insight: Pelanggan dengan nilai RFM tinggi (recency rendah, frequency tinggi, monetary tinggi) adalah pelanggan terbaik yang memberikan kontribusi signifikan terhadap pendapatan. Mereka cenderung lebih loyal dan memiliki nilai seumur hidup pelanggan (Customer Lifetime Value) yang tinggi.")
    st.write("Rekomendasi Langkah: Loyalty Programs: Buat program loyalitas untuk memberikan penghargaan kepada pelanggan terbaik ini, seperti diskon eksklusif atau akses awal ke produk baru. Personalized Marketing: Gunakan data RFM untuk mengirimkan penawaran yang dipersonalisasi kepada pelanggan terbaik, meningkatkan kemungkinan pembelian ulang.")

st.caption("Copyright (c) galihagustansukidayo gambarimasu 2026")