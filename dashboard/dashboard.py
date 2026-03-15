
import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title='E-Commerce Dashboard', layout='wide')

def create_daily_orders_df(df):
  daily_orders_df = df.resample(rule='D', on='order_purchase_timestamp').agg({
      "order_id": "nunique",
      "payment_value": "sum"})
  return daily_orders_df

# Load
all_df = pd.read_csv(f'C:\\Users\\Pongo\\OneDrive\\Desktop\\datadiri\\submission\\analisis data\\all_data.csv')
all_df['order_purchase_timestamp'] = pd.to_datetime(all_df['order_purchase_timestamp'])

with st.sidebar:
    st.image("https://github.com/dicodingacademy/assets/raw/main/logo.png")
    # Filter rentang waktu
    start_date, end_date = st.date_input(
        label='Rentang Waktu',
        value=[all_df["order_purchase_timestamp"].min(), all_df["order_purchase_timestamp"].max()]
    )

main_df = all_df[(all_df["order_purchase_timestamp"] >= str(start_date)) & 
                (all_df["order_purchase_timestamp"] <= str(end_date))]

main_df['order_purchase_timestamp'] = pd.to_datetime(main_df['order_purchase_timestamp'])

now = main_df['order_purchase_timestamp'].max() + pd.Timedelta(days=1)

rfm_df = main_df.groupby(by="customer_id", as_index=False).agg({
    "order_purchase_timestamp": lambda x: (now - x.max()).days, # Recency
    "order_id": "count", # Frequency
    "price": "sum" # Monetary
})

rfm_df.columns = ["customer_id", "recency", "frequency", "monetary"]

# --- MAIN PAGE ---
st.header('E-Commerce Dashboard :sparkles:')

# Menampilkan Visualisasi (Contoh: Bar Chart Kategori Produk)
st.subheader("Produk dengan Pendapatan Tertinggi")
fig, ax = plt.subplots(figsize=(16, 8))
sns.barplot(x="price", y="product_category_name", data=main_df.head(10), ax=ax)
st.pyplot(fig)

# Menampilkan Metric
col1, col2 = st.columns(2)
with col1:
    total_orders = main_df.order_id.nunique()
    st.metric("Total Pemesanan", value=total_orders)
with col2:
    total_revenue = main_df.price.sum()
    st.metric("Total Pendapatan", value=f"IDR {total_revenue:,.2f}")

st.header('E-Commerce Performance Dashboard :bar_chart:')

st.subheader("Performa Kategori Produk")
fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(24, 10))

# Berdasarkan Pendapatan
sns.barplot(x="price", y="product_category_name", data=main_df.groupby("product_category_name").price.sum().sort_values(ascending=False).reset_index().head(5), ax=ax[0], palette="viridis")
ax[0].set_title("Berdasarkan Pendapatan (Revenue)", fontsize=20)

# Berdasarkan Volume Penjualan
sns.barplot(x="order_id", y="product_category_name", data=main_df.groupby("product_category_name").order_id.nunique().sort_values(ascending=False).reset_index().head(5), ax=ax[1], palette="magma")
ax[1].set_title("Berdasarkan Volume Penjualan", fontsize=20)

st.pyplot(fig)

st.subheader("Distribusi Penjualan Berdasarkan Wilayah")
state_df = main_df.groupby("customer_state").order_id.nunique().sort_values(ascending=False).reset_index()

fig, ax = plt.subplots(figsize=(12, 6))
sns.barplot(x="order_id", y="customer_state", data=state_df.head(10), palette="Blues_r")
ax.set_xlabel("Jumlah Pesanan")
ax.set_ylabel("Negara Bagian (State)")
st.pyplot(fig)

with st.expander("Lihat Detail Analisis Wilayah"):
    st.write(f"Wilayah dengan transaksi tertinggi adalah **{state_df.iloc[0]['customer_state']}**.")
    st.write("Hal ini menunjukkan konsentrasi pasar masih berpusat di wilayah tertentu. Perlu ekspansi logistik di wilayah dengan transaksi rendah.")

st.subheader("Best Customer Based on RFM Parameters")
col1, col2, col3 = st.columns(3)

with col1:
    avg_recency = round(rfm_df.recency.mean(), 1)
    st.metric("Avg. Recency (Days)", value=avg_recency)

with col2:
    avg_frequency = round(rfm_df.frequency.mean(), 2)
    st.metric("Avg. Frequency", value=avg_frequency)

with col3:
    avg_monetary = rfm_df.monetary.mean()
    st.metric("Avg. Monetary", value=f"R$ {avg_monetary:,.2f}")


