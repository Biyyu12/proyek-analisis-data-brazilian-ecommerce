import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# =========================
# LOAD DATA
# =========================

customers = pd.read_csv("data/olist_customers_dataset.csv")
orders = pd.read_csv("data/olist_orders_dataset.csv")
payments = pd.read_csv("data/olist_order_payments_dataset.csv")
order_items = pd.read_csv("data/olist_order_items_dataset.csv")
products = pd.read_csv("data/olist_products_dataset.csv")
category = pd.read_csv("data/product_category_name_translation.csv")

orders['order_purchase_timestamp'] = pd.to_datetime(
    orders['order_purchase_timestamp']
)

# =========================
# DATA MERGING
# =========================

df = orders.merge(payments, on="order_id")
df = df.merge(order_items, on="order_id")
df = df.merge(products, on="product_id")
df = df.merge(category, on="product_category_name", how="left")

# =========================
# DASHBOARD SETUP
# =========================

st.set_page_config(
    page_title="E-Commerce Dashboard",
    layout="wide"
)

st.title("📊 E-Commerce Business Dashboard")

# =========================
# KPI METRICS
# =========================

total_revenue = df['payment_value'].sum()
total_orders = df['order_id'].nunique()
total_customers = customers['customer_unique_id'].nunique()
avg_order_value = total_revenue / total_orders

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Revenue", f"${total_revenue:,.0f}")
col2.metric("Total Orders", total_orders)
col3.metric("Total Customers", total_customers)
col4.metric("Avg Order Value", f"${avg_order_value:,.2f}")

st.divider()

# =========================
# MONTHLY REVENUE
# =========================

df['month_year'] = df['order_purchase_timestamp'].dt.to_period('M')

monthly_revenue = df.groupby('month_year')['payment_value'].sum().reset_index()

monthly_revenue['month_year'] = monthly_revenue['month_year'].astype(str)

st.subheader("📈 Monthly Revenue Trend")

fig1, ax1 = plt.subplots(figsize=(12,5))

sns.lineplot(
    data=monthly_revenue,
    x='month_year',     
    y='payment_value',
    marker='o',
    ax=ax1
)

ax1.set_xlabel("Month/Year")
ax1.set_ylabel("Revenue")
ax1.grid(axis='y')

plt.xticks(rotation=45)

st.pyplot(fig1)

st.divider()

col_left, col_right = st.columns(2)

# =========================
# TOP PRODUCT CATEGORY
# =========================

category_revenue = df.groupby(
    'product_category_name_english'
)['payment_value'].sum().sort_values(ascending=False).head(10)

with col_left:

    st.subheader("🏆 Top 10 Product Categories")

    fig2, ax2 = plt.subplots()

    sns.barplot(
        x=category_revenue.values,
        y=category_revenue.index,
        ax=ax2
    )

    ax2.set_xlabel("Revenue")
    ax2.set_ylabel("Category")

    st.pyplot(fig2)

# =========================
# RFM ANALYSIS
# =========================

snapshot_date = df['order_purchase_timestamp'].max()

rfm = df.groupby('customer_id').agg({
    'order_purchase_timestamp': lambda x: (snapshot_date - x.max()).days,
    'order_id': 'nunique',
    'payment_value': 'sum'
})

rfm.columns = ['Recency', 'Frequency', 'Monetary']

rfm['R_score'] = pd.qcut(rfm['Recency'], 5, labels=[5,4,3,2,1])
rfm['F_score'] = pd.qcut(rfm['Frequency'].rank(method='first'),5,labels=[1,2,3,4,5])
rfm['M_score'] = pd.qcut(rfm['Monetary'],5,labels=[1,2,3,4,5])

rfm = rfm.astype(int)

def segment_customer(row):

    if row['R_score'] >= 4 and row['F_score'] >= 4:
        return "Champions"

    elif row['F_score'] >= 4:
        return "Loyal Customers"

    elif row['R_score'] >= 4:
        return "Potential Loyalists"

    elif row['R_score'] <= 2:
        return "At Risk"

    else:
        return "Others"

rfm['segment'] = rfm.apply(segment_customer, axis=1)

segment_count = rfm['segment'].value_counts()

with col_right:

    st.subheader("👥 Customer Segmentation (RFM)")

    fig3, ax3 = plt.subplots()

    ax3.pie(
        segment_count.values,
        labels=None,
        autopct='%1.1f%%',
        startangle=90,
    )

    ax3.legend(
        segment_count.index,
        loc="center left",
        bbox_to_anchor=(1,0.5)
    )

    ax3.set_title("Customer Segment Distribution")

    st.pyplot(fig3)

st.divider()

