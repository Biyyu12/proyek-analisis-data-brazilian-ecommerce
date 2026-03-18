import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# =========================
# CONFIG
# =========================

st.set_page_config(
    page_title="E-Commerce Dashboard",
    layout="wide"
)

st.title("📊 E-Commerce Business Dashboard")

# =========================
# LOAD DATA
# =========================

@st.cache_data
def load_data():
    df = pd.read_csv("main_df.csv")

    # Gunakan month_year sebagai date
    df['order_date'] = pd.to_datetime(df['month_year'])

    return df

df = load_data()

# =========================
# FILTER (DATE RANGE)
# =========================

st.sidebar.header("🔎 Filter Data")

min_date = df["order_date"].min()
max_date = df["order_date"].max()

start_date, end_date = st.sidebar.date_input(
    "Rentang Waktu",
    min_value=min_date,
    max_value=max_date,
    value=[min_date, max_date]
)

filtered_df = df[
    (df['order_date'] >= pd.to_datetime(start_date)) &
    (df['order_date'] <= pd.to_datetime(end_date))
].copy()

# =========================
# KPI METRICS
# =========================

total_revenue = filtered_df['payment_value'].sum()
total_orders = filtered_df['order_id'].nunique()
total_customers = filtered_df['customer_unique_id'].nunique()
avg_order_value = total_revenue / total_orders if total_orders > 0 else 0

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Revenue", f"${total_revenue:,.0f}")
col2.metric("Total Orders", total_orders)
col3.metric("Total Customers", total_customers)
col4.metric("Avg Order Value", f"${avg_order_value:,.2f}")

st.divider()

# =========================
# REVENUE TREND
# =========================

monthly_revenue = filtered_df.groupby('order_date')['payment_value'].sum().reset_index()

monthly_revenue['month_year'] = monthly_revenue['order_date'].dt.strftime('%m/%Y')

st.subheader("📈 Revenue Trend")

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
# BEST & WORST PRODUCT
# =========================

category_revenue = filtered_df.groupby(
    'product_category_name_english'
)['payment_value'].sum().sort_values(ascending=False)

top_10 = category_revenue.head(10)
bottom_10 = category_revenue.tail(10)

with col_left:
    st.subheader("🏆 Top 10 Product Categories")

    fig2, ax2 = plt.subplots()

    sns.barplot(
        x=top_10.values,
        y=top_10.index,
        ax=ax2
    )

    ax2.set_xlabel("Revenue")
    ax2.set_ylabel("Category")

    st.pyplot(fig2)

with col_right:
    st.subheader("📉 Worst 10 Product Categories")

    fig3, ax3 = plt.subplots()
    bottom_10_reversed = bottom_10.iloc[::-1]

    sns.barplot(
        x=bottom_10_reversed.values,
        y=bottom_10_reversed.index,
        ax=ax3
    )

    ax3.set_xlabel("Revenue")
    ax3.set_ylabel("Category")

    st.pyplot(fig3)

st.divider()

# =========================
# RFM SEGMENTATION
# =========================

st.subheader("👥 Customer Segmentation (RFM)")

segment_count = filtered_df['segment'].value_counts()

fig4, ax4 = plt.subplots()

ax4.pie(
    segment_count.values,
    labels=None,
    autopct='%1.1f%%',
    startangle=90
)

ax4.legend(
    segment_count.index,
    loc="center left",
    bbox_to_anchor=(1, 0.5)
)

ax4.set_title("Customer Segment Distribution")

st.pyplot(fig4)