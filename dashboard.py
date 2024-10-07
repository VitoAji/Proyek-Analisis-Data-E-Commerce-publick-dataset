# # Proyek Analisis Data: [E-Commerce-publick-dataset.zip]
# - **Nama:** [Vito Aji Pradipta]
# - **Email:** [m004b4ky4439@bangkit.academy]
# - **ID Dicoding:** [vito_aji_pradipta_77]

#mengimpor semua library
import pandas as pd #untuk data handling
import numpy as np # untuk operasi numerik
import matplotlib.pyplot as plt # untuk visualsasi
import seaborn as sns # untuk statistika visual
import streamlit as st


#masukkan dataset
orders = pd.read_csv('C:/Users/ASUS/Music/E-Commerce Public Dataset/Dashboard/main_data.csv/orders_dataset.csv')
products = pd.read_csv('C:/Users/ASUS/Music/E-Commerce Public Dataset/Dashboard/main_data.csv/products_dataset.csv')
customers = pd.read_csv('C:/Users/ASUS/Music/E-Commerce Public Dataset/Dashboard/main_data.csv/customers_dataset.csv')
reviews = pd.read_csv('C:/Users/ASUS/Music/E-Commerce Public Dataset/Dashboard/main_data.csv/order_reviews_dataset.csv')
payments = pd.read_csv('C:/Users/ASUS/Music/E-Commerce Public Dataset/Dashboard/main_data.csv/order_payments_dataset.csv')


#ubah date columns ke datetime
orders['order_purchase_timestamp']= pd.to_datetime(orders['order_purchase_timestamp'])
orders['order_delivered_customer_date']= pd.to_datetime(orders['order_delivered_customer_date'])

#hitung delivery time in days
orders['delivery_time'] = (orders['order_delivered_customer_date']-orders['order_purchase_timestamp']).dt.days

#hapus rows with missing delivery
orders_clean =orders.dropna(subset=['order_delivered_customer_date'])


# masukan order_items dataset
order_items= pd.read_csv('C:/Users/ASUS/Music/E-Commerce Public Dataset/Dashboard/main_data.csv/order_items_dataset.csv')

#satukan orders dengan order_items
order_items_merged=pd.merge(orders_clean,order_items, on='order_id', how='inner')
order_products= pd.merge(order_items_merged, products, on='product_id', how='inner')

#kelompokkan berdasarkan product category dan hitung average delivery time
category_delivery_time = order_products.groupby('product_category_name')['delivery_time'].mean().sort_values()

# Satukan dataset
order_payments = pd.merge(orders_clean, payments, on='order_id', how='inner')
order_customers = pd.merge(order_payments, customers, on='customer_id', how='inner')
order_reviews = pd.merge(order_customers, reviews, on='order_id', how='inner')

# Gabungkan berdasarkan customer state dan hitung total revenue dan average review score
state_revenue_review = order_reviews.groupby('customer_state').agg(
    total_revenue=('payment_value', 'sum'),
    avg_review_score=('review_score', 'mean'),
    customer_count=('customer_id', 'nunique')
).sort_values('total_revenue', ascending=False).reset_index()

# Menampilkan judul aplikasi
st.title("DASHBOARD E-COMMERCE🛒")

# Fitur Filtering
state_options = state_revenue_review['customer_state'].tolist()  # Ambil daftar state yang tersedia

# Gunakan multiselect untuk memungkinkan pengguna memilih beberapa state
selected_states = st.multiselect("SELECT STATE:", state_options, default=state_options)

# Filter data berdasarkan state yang dipilih
filtered_data = state_revenue_review[state_revenue_review['customer_state'].isin(selected_states)]

# Visualisasi menarik: Number of Customers by State
st.header("Number of Customers by State")
plt.figure(figsize=(10, 5))


colors_ = ["#72BCD4"] + ["#D3D3D3"] * (len(filtered_data) - 1)  # Warna berbeda untuk highlight

sns.barplot(
    x="customer_count", 
    y="customer_state",
    data=filtered_data.sort_values(by="customer_count", ascending=False),
    palette=colors_
)


plt.title("Number of Customers by State", loc="center", fontsize=15)
plt.ylabel(None)  
plt.xlabel(None)  
plt.tick_params(axis='y', labelsize=12) 

st.pyplot(plt)

# Visualisasi untuk total revenue
st.header("Total Revenue by State")
plt.figure(figsize=(10, 6))

# Palet warna untuk revenue
colors_revenue = sns.color_palette("Blues_r", len(filtered_data))

sns.barplot(
    x="total_revenue", 
    y="customer_state",
    data=filtered_data.sort_values(by="total_revenue", ascending=False),
    palette=colors_revenue
)

# Tambahkan gaya pada visualisasi revenue
plt.title("Total Revenue by State", loc="center", fontsize=15)
plt.ylabel(None)
plt.xlabel(None)
plt.tick_params(axis='y', labelsize=12)

st.pyplot(plt)

# plot untuk melihat korelasi antara revenue dan review scores
st.header("Revenue vs Average Review Score by State")
plt.figure(figsize=(10, 6))
sns.scatterplot(x=filtered_data['total_revenue'], y=filtered_data['avg_review_score'], s=100, color="#72BCD4")


plt.title('Revenue vs. Average Review Score by State', fontsize=15)
plt.xlabel('Total Revenue', fontsize=12)
plt.ylabel('Average Review Score', fontsize=12)
plt.grid(True)

st.pyplot(plt)