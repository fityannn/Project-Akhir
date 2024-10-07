import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency

sns.set(style='dark')

def create_monthly_orders_df(df):
    monthly_orders_df = df.resample(rule='D', on='shipping_limit_date').agg({
        "order_id": "nunique",
        "price": "sum"
    })
    monthly_orders_df = monthly_orders_df.reset_index()
    monthly_orders_df.rename(columns={
        "order_id": "order_count",
        "price": "revenue"
    }, inplace=True)
    
    return monthly_orders_df

def create_sum_order_items_df(df):
    sum_order_items_df = df.groupby("product_category_name")["order_id"].nunique().sort_values(ascending=False).reset_index()
    sum_order_items_df.rename(columns={"order_id": "number_of_sales"}, inplace=True)  # Rename for clarity
    return sum_order_items_df

# Load your data
all_df = pd.read_csv("https://raw.githubusercontent.com/fityannn/Project-Akhir/refs/heads/main/dashboard/all_data.csv")

# Ensure 'shipping_limit_date' is in datetime format
all_df['shipping_limit_date'] = pd.to_datetime(all_df['shipping_limit_date'])

# Create monthly_orders_df
monthly_orders_df = create_monthly_orders_df(all_df)

st.header('E-Commerce Public :sparkles:')

st.subheader('Daily Orders')

col1, col2 = st.columns(2)

with col1:
    total_orders = monthly_orders_df.order_count.sum()
    st.metric("Total orders", value=total_orders)

with col2:
    total_revenue = format_currency(monthly_orders_df.revenue.sum(), "AUD", locale='es_CO') 
    st.metric("Total Revenue", value=total_revenue)

fig, ax = plt.subplots(figsize=(15, 5))
ax.plot(
    monthly_orders_df["shipping_limit_date"],
    monthly_orders_df["order_count"],
    marker='o', 
    linewidth=2,
    color="#90CAF9"
)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)

st.pyplot(fig)

st.subheader("Best & Worst Performing Product")

# Call this function to create the DataFrame
sum_order_items_df = create_sum_order_items_df(all_df)  

fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(20, 10))

colors = ["#90CAF9", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]

# Best Performing Product
sns.barplot(x="number_of_sales", y="product_category_name", data=sum_order_items_df.head(5), palette=colors, ax=ax[0])
ax[0].set_ylabel(None)
ax[0].set_xlabel("Number of Sales", fontsize=20)
ax[0].set_title("Best Performing Product", loc="center", fontsize=25)
ax[0].tick_params(axis='y', labelsize=15)
ax[0].tick_params(axis='x', labelsize=15)

# Worst Performing Product
sns.barplot(x="number_of_sales", y="product_category_name", data=sum_order_items_df.sort_values(by="number_of_sales", ascending=True).head(5), palette=colors, ax=ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel("Number of Sales", fontsize=20)
ax[1].invert_xaxis()
ax[1].yaxis.set_label_position("right")
ax[1].yaxis.tick_right()
ax[1].set_title("Worst Performing Product", loc="center", fontsize=25)
ax[1].tick_params(axis='y', labelsize=15)
ax[1].tick_params(axis='x', labelsize=15)

st.pyplot(fig)

orders_df = pd.read_csv("https://raw.githubusercontent.com/fityannn/Project-Akhir/refs/heads/main/dashboard/orders.csv")
fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(20, 10))
monthly_orders_df['shipping_limit_date'] = pd.to_datetime(monthly_orders_df['shipping_limit_date'], format='%Y-%m')

# Filter the DataFrame for the desired date range (September 2017 to August 2018)
start_date = '2017-09-01'
end_date = '2018-08-31'
filtered_orders_df = monthly_orders_df[(monthly_orders_df['shipping_limit_date'] >= start_date) & 
                                        (monthly_orders_df['shipping_limit_date'] <= end_date)]

# Set up the Streamlit app
st.title("Pembelian dari 2017 sampai 2018")
st.write("Visualisasi jumlah pesanan dari bulan September 2017 hingga Agustus 2018.")

# Create the plot
plt.figure(figsize=(12, 6))
sns.set_theme(style="whitegrid")

# Plot with fill
plt.plot(filtered_orders_df['shipping_limit_date'], 
         filtered_orders_df['order_count'], 
         marker='o', 
         linewidth=2, 
         color="#72BCD4")

plt.fill_between(filtered_orders_df['shipping_limit_date'], 
                 filtered_orders_df['order_count'], 
                 color="#B2E0EB", alpha=0.3)

# Title and labels
plt.title("Jumlah Pesanan Bulanan", fontsize=24, loc='center')

# Set x-ticks to show only specific months
tick_dates = filtered_orders_df['shipping_limit_date'][::3]  # Show every third month
plt.xticks(filtered_orders_df['shipping_limit_date'],
           filtered_orders_df['shipping_limit_date'].dt.strftime('%B %Y'),
           rotation=45)

plt.xlabel("Bulan", fontsize=16)
plt.ylabel("Jumlah Pesanan", fontsize=16)

# Add gridlines for better readability
plt.grid(axis='y', linestyle='--', alpha=0.7)

# Annotate the highest point if there are any orders
if not filtered_orders_df.empty:
    max_orders = filtered_orders_df['order_count'].max()
    max_month = filtered_orders_df['shipping_limit_date'][filtered_orders_df['order_count'].idxmax()]
    plt.annotate(f'Max: {max_orders}', 
                 xy=(max_month, max_orders), 
                 xytext=(max_month, max_orders + 20),
                 arrowprops=dict(facecolor='black', shrink=0.05),
                 fontsize=12, 
                 color='black', 
                 horizontalalignment='center')

plt.tight_layout()  # Adjust layout for better spacing

# Render the plot in Streamlit
st.pyplot(fig)
