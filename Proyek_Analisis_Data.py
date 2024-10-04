#!/usr/bin/env python
# coding: utf-8

# # Proyek Analisis Data: [E-Commerce-publick-dataset.zip]
# - **Nama:** [Vito Aji Pradipta]
# - **Email:** [m004b4ky4439@bangkit.academy]
# - **ID Dicoding:** [vito_aji_pradipta_77]

# ## Menentukan Pertanyaan Bisnis

# - Question 1 : How does a shipment have different delivery times and what categories have fast and slow delivery times ?
# - Question 2 : which city has the largest e-commerce revenue and is it directly proportional based on customer review ratings ?

# ## Import Semua Packages/Library yang Digunakan

# In[3]:


#mengimpor semua library
import pandas as pd #untuk data handling
import numpy as np # untuk operasi numerik
import matplotlib.pyplot as plt # untuk visualsasi
import seaborn as sns # untuk statistika visual
import streamlit as st

# ## Data Wrangling

# ### Gathering Data

# In[6]:


#masukkan dataset
orders = pd.read_csv('https://drive.google.com/uc?id=1t6R6b97Oe3TG61-v8FIcSqo08RQxaiZN?hl=id')
products = pd.read_csv('https://drive.google.com/uc?id=1t6R6b97Oe3TG61-v8FIcSqo08RQxaiZN?hl=id')
customers = pd.read_csv('https://drive.google.com/uc?id=1t6R6b97Oe3TG61-v8FIcSqo08RQxaiZN?hl=id')
reviews = pd.read_csv('https://drive.google.com/uc?id=1t6R6b97Oe3TG61-v8FIcSqo08RQxaiZN?hl=id')
payments = pd.read_csv('https://drive.google.com/uc?id=1t6R6b97Oe3TG61-v8FIcSqo08RQxaiZN?hl=id')


# **Insight:**
# - orders dataset will help calculate delivery times and statuses for different products
# - customer and reviews dataset will help to correlate customer satisfaction with revenue

# ### Assessing Data

# In[7]:




# **Insight:**
# - Orders dataset contains importan timestamps such as order creation and delivery times
# - missing values are visible in certain columns, especially in order status, indicating canceled or incomplete orders

# ### Cleaning Data

# In[38]:


#ubah date columns ke datetime
orders['order_purchase_timestamp']= pd.to_datetime(orders['order_purchase_timestamp'])
orders['order_delivered_customer_date']= pd.to_datetime(orders['order_delivered_customer_date'])

#hitung delivery time in days
orders['delivery_time'] = (orders['order_delivered_customer_date']-orders['order_purchase_timestamp']).dt.days

#hapus rows with missing delivery
orders_clean =orders.dropna(subset=['order_delivered_customer_date'])


# **Insight:**
# - some orders maay not have shipping information due to delays
# - the new delivery_time column allows us to analyze delivery times based on factors such as product category or customer location

# ## Exploratory Data Analysis (EDA)

# ### Explore ...

# In[24]:


# masukan order_items dataset
order_items= pd.read_csv('C:/Users/ASUS/Music/E-Commerce Public Dataset/Dashboard/main_data.csv/order_items_dataset.csv')

#satukan orders dengan order_items
order_items_merged=pd.merge(orders_clean,order_items, on='order_id', how='inner')
order_products= pd.merge(order_items_merged, products, on='product_id', how='inner')

#kelompokkan berdasarkan product category dan hitung average delivery time
category_delivery_time = order_products.groupby('product_category_name')['delivery_time'].mean().sort_values()


# **Insight:**
# - categories with the longest delivery times may indicate supply chain issues or logistics challenges
# - shorter delivery times for certain categories indicate an efficient process

# ## Visualization & Explanatory Analysis
st.title("🛒SIMPLE DASBOARD E-COMMERCE")

# ### Pertanyaan 1:

# In[25]:


#visualisasi delivery time by category
st.header("Average Delivery Time by Product Category")
plt.figure(figsize=(10,17))
sns.barplot(x=category_delivery_time.values, y=category_delivery_time.index)
plt.title('Average Delivery Time by Product Category')
plt.xlabel('Average Delivery Time (days)')
plt.ylabel('Product Category')
st.pyplot(plt)

# ### Pertanyaan 2:

# In[26]:


# satukan orders, payments, customers, dan reviews datasets
order_payments = pd.merge(orders_clean, payments, on='order_id', how='inner')
order_customers = pd.merge(order_payments, customers, on='customer_id', how='inner')
order_reviews = pd.merge(order_customers, reviews, on='order_id', how='inner')

# Gabungkan berdasarkan customer state dan hitung total revenue dan average review score
state_revenue_review = order_reviews.groupby('customer_state').agg(
    total_revenue=('payment_value', 'sum'),
    avg_review_score=('review_score', 'mean')
).sort_values('total_revenue', ascending=False)

# Visualize revenue berdasarkan city
st.header("Total Revenue by State")
plt.figure(figsize=(10,6))
sns.barplot(x=state_revenue_review['total_revenue'], y=state_revenue_review.index)
plt.title('Total Revenue by State')
plt.xlabel('Total Revenue')
plt.ylabel('State')
st.pyplot(plt)

# plot untuk melihat korelasi antara revenue dan review scores
st.header("Revenue vs average review score by State")
plt.figure(figsize=(10,6))
sns.scatterplot(x=state_revenue_review['total_revenue'], y=state_revenue_review['avg_review_score'])
plt.title('Revenue vs. Average Review Score by State')
plt.xlabel('Total Revenue')
plt.ylabel('Average Review Score')
st.pyplot(plt)


# **Insight:**
# - For Question 1 =
#   1. categories such as Furniture and Housewares have the longest delivery times, possibly due to their size or logistical complexity.
#   2. categories such as Books and Fashion Accessories have shorter delivery times, possibly due to easier handling and availability.
# 
# - For Question 2 =
#   1. States like São Paulo and Rio de Janeiro contribute significantly to overall revenue.
#   2. There seems to be a weak or negative correlation between total revenue and average review score, which suggests that higher sales do not necessarily equate to higher customer satisfaction.

# ## Conclusion

# - Conclution for question 1 =
#   the analysus shows significant differences in delivery times acroos product categories, which can be noticed by looking at the table that larger items such as furniture experience longer delays, while smaller easy to ship items tend arrive faster
# - Conclution for question 2 =
#   states/city like Sao Paulo are major contributors to e-commerce revenue and customer satisfaction does not have strong correlation, indicating that service quality in revenuee areas must be improved in order to incease customer ratings
