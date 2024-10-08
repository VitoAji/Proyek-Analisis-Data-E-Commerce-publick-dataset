# Proyek Analisis Data: [E-Commerce-publick-dataset.zip]
# Nama:[Vito Aji Pradipta]
# Email: [m004b4ky4439@bangkit.academy]
# D Dicoding: [vito_aji_pradipta_77]

import pandas as pd #untuk data handling
import numpy as np # untuk operasi numerik
import matplotlib.pyplot as plt # untuk visualsasi
import seaborn as sns # untuk statistika visual
import streamlit as st 

# Masukan datasets
orders = pd.read_csv('orders_dataset.csv')
products = pd.read_csv('products_dataset.csv')
customers = pd.read_csv('customers_dataset.csv')
reviews = pd.read_csv('order_reviews_dataset.csv')
payments = pd.read_csv('order_payments_dataset.csv')
order_items = pd.read_csv('order_items_dataset.csv')

# Ubah date columns ke datetime
orders['order_purchase_timestamp'] = pd.to_datetime(orders['order_purchase_timestamp'])
orders['order_delivered_customer_date'] = pd.to_datetime(orders['order_delivered_customer_date'])

# Hitung delivery time in days
orders['delivery_time'] = (orders['order_delivered_customer_date'] - orders['order_purchase_timestamp']).dt.days

# Hapus rows with missing delivery
orders_clean = orders.dropna(subset=['order_delivered_customer_date'])

# Satukan orders dengan order_items
order_items_merged = pd.merge(orders_clean, order_items, on='order_id', how='inner')
order_products = pd.merge(order_items_merged, products, on='product_id', how='inner')

# Kelompokkan berdasarkan product category dan hitung average delivery time
category_delivery_time = order_products.groupby('product_category_name')['delivery_time'].mean().sort_values()

# Satukan dataset orders, payments, customers, reviews
order_payments = pd.merge(orders_clean, payments, on='order_id', how='inner')
order_customers = pd.merge(order_payments, customers, on='customer_id', how='inner')
order_reviews = pd.merge(order_customers, reviews, on='order_id', how='inner')

# Gabungkan berdasarkan customer state dan hitung total revenue, average review score, dan customer count
state_revenue_review = order_reviews.groupby('customer_state').agg(
    total_revenue=('payment_value', 'sum'),
    avg_review_score=('review_score', 'mean'),
    customer_count=('customer_id', 'nunique')
).sort_values('total_revenue', ascending=False).reset_index()

# Tampilan judul aplikasi
st.title("DASHBOARD E-COMMERCE🛒")

st.header("Revenue & Average Review Score by State")

# Filter untuk State
state_options = state_revenue_review['customer_state'].tolist()

# Pilihan multiselect untuk State
selected_states = st.multiselect("SELECT STATE:", state_options, default=state_options)

# Filter data berdasarkan state yang dipilih
filtered_data = state_revenue_review[state_revenue_review['customer_state'].isin(selected_states)]

# Visualisasi Number of Customers by State
st.header("Number of Customers by State")
plt.figure(figsize=(10, 5))
colors_ = ["#ADD8E6"] + ["#BDBDBD"] * (len(filtered_data) - 1)  # Gunakan warna biru muda
sns.barplot(x="customer_count", y="customer_state", data=filtered_data.sort_values(by="customer_count", ascending=False), palette=colors_)
plt.title("Number of Customers by State", loc="center", fontsize=15)
plt.ylabel(None)
plt.xlabel('Customer Count', fontsize=12)
plt.grid(False)
sns.despine()
st.pyplot(plt)

# Visualisasi Total Revenue by State
st.header("Total Revenue by State")
plt.figure(figsize=(10, 6))
colors_revenue = sns.color_palette("Blues_r", len(filtered_data))  # Gunakan warna biru muda seperti diminta
sns.barplot(x="total_revenue", y="customer_state", data=filtered_data.sort_values(by="total_revenue", ascending=False), palette=colors_revenue)
plt.title("Total Revenue by State", loc="center", fontsize=15)
plt.ylabel(None)
plt.xlabel('Total Revenue', fontsize=12)
plt.grid(False)
sns.despine()
st.pyplot(plt)

# Visualisasi Revenue vs Average Review Score by State
st.header("Revenue vs Average Review Score by State")
plt.figure(figsize=(10, 6))
sns.scatterplot(x=filtered_data['total_revenue'], y=filtered_data['avg_review_score'], s=100, color="#72BCD4")
plt.title('Revenue vs. Average Review Score by State', fontsize=15)
plt.xlabel('Total Revenue', fontsize=12)
plt.ylabel('Average Review Score', fontsize=12)
plt.grid(True, linestyle='--', alpha=0.6)
sns.despine()
st.pyplot(plt)

st.markdown("<p style='text-align: center;'>states like Sao Paulo are major contributors to e-commerce revenue and customer satisfaction does not have strong correlation, indicating that service quality in revenuee areas must be improved in order to incease customer ratings</p>", unsafe_allow_html=True)

#pembatas
st.markdown("<p style='text-align: center;'>---------------------------------------------------------------------------------------</p>", unsafe_allow_html=True)

st.header("Average Product Delivery")

# Filter untuk Product Category
product_categories = category_delivery_time.index.tolist()

# Pilihan multiselect untuk Product Category
selected_categories = st.multiselect("SELECT PRODUCT CATEGORY:", product_categories, default=product_categories)

# Filter data
filtered_category_data = category_delivery_time[category_delivery_time.index.isin(selected_categories)]

# Top 5 Average Delivery Produk Terlama
st.header("Top 5 Products With Longest Delivery")
top_5_slowest = category_delivery_time.nlargest(5)
plt.figure(figsize=(10, 5))
sns.barplot(x=top_5_slowest.values, y=top_5_slowest.index, palette=sns.color_palette("Blues_r", 5))  # Palet biru muda
plt.title('Top 5 Products With Longest Delivery', fontsize=15)
plt.xlabel('Average Delivery Time (days)', fontsize=12)
plt.ylabel('Product Category', fontsize=12)
plt.grid(False)
sns.despine()
st.pyplot(plt)

# Top 5 Average Delivery Produk Tercepat
st.header("Top 5 Products With Fastest Delivery")
top_5_fastest = category_delivery_time.nsmallest(5)
plt.figure(figsize=(10, 5))
sns.barplot(x=top_5_fastest.values, y=top_5_fastest.index, palette=sns.color_palette("Blues_r", 5))  # Palet biru muda
plt.title('Top 5 Products With Fastest Delivery', fontsize=15)
plt.xlabel('Average Delivery Time (days)', fontsize=12)
plt.ylabel('Product Category', fontsize=12)
plt.grid(False)
sns.despine()
st.pyplot(plt)

#statement penjelasan
st.markdown("<p style='text-align: center;'>It can be seen by looking at the table that larger items experience longer delays, while smaller, easy-to-ship items tend to arrive faster.</p>", unsafe_allow_html=True)
