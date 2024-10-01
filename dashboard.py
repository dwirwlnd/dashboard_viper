import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
sns.set(style='dark')

# Helper function untuk menyiapkan dataframe

#Daily Order
def create_daily_orders_df(df):
    daily_orders_df = df.resample(rule='D', on='order_purchase_timestamp').agg({
        "order_id": "nunique",
        "price": "sum"
    })
    daily_orders_df = daily_orders_df.reset_index()
    daily_orders_df.rename(columns={
        "order_id": "order_count",
        "price": "revenue"
    }, inplace=True)
    
    return daily_orders_df

#Selling Product
def create_favorito(df):
    most_least_favorito = df.groupby("product_category_name_english").order_id.nunique().sort_values(ascending=False).reset_index()
    return most_least_favorito

#Rating
def create_rating(df):
    ratings= df.groupby(by="review_score").order_id.nunique().reset_index()
    ratings.rename(columns={
        "order_id": "order_count"
    }, inplace=True)
    
    return ratings

#Grouping City
def create_bycity(df):
    most_least_city = df.groupby("customer_city").customer_id.nunique().sort_values(ascending=False).reset_index()
    return most_least_city

#Grouping State
def create_bystate(df):
    most_least_state = df.groupby("customer_state").customer_id.nunique().sort_values(ascending=False).reset_index()
    return most_least_state

#Load Data
all_df = pd.read_csv("all_data.csv")

datetime_columns = ["order_purchase_timestamp"]
all_df.sort_values(by="order_purchase_timestamp", inplace=True)
all_df.reset_index(inplace=True)
 
for column in datetime_columns:
    all_df[column] = pd.to_datetime(all_df[column])

#Komponen Filter Sidebar

min_date = all_df["order_purchase_timestamp"].min()
max_date = all_df["order_purchase_timestamp"].max()
 
with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("logo.png")
    
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label="Select Time Range",min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

#Main
main_df = all_df[(all_df["order_purchase_timestamp"] >= str(start_date)) & 
                (all_df["order_purchase_timestamp"] <= str(end_date))]

daily_orders_df = create_daily_orders_df(main_df)
most_least_favorito = create_favorito(main_df)
ratings = create_rating(main_df)
most_least_city = create_bycity(main_df)
most_least_state = create_bystate(main_df)

#Visualisasi Data

st.header('Viper E-Commerce Dashboard :snake:')

#Daily Order
st.subheader('Daily Orders')
 
col1, col2 = st.columns(2)
 
with col1:
    total_orders = daily_orders_df.order_count.sum()
    st.metric("Total Orders", value=total_orders)
 
with col2:
    total_revenue = format_currency(daily_orders_df.revenue.sum(), "AUD", locale='es_CO') 
    st.metric("Total Revenue", value=total_revenue)
 
fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(
    daily_orders_df["order_purchase_timestamp"],
    daily_orders_df["order_count"],
    marker='o', 
    linewidth=2,
    color="#7d1010"
)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)
 
st.pyplot(fig)

# Selling Product
st.subheader("Best and Worst Selling Product")

fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(35, 15))
 
colors = ["#7d1010", "#e0b4b4", "#e0b4b4", "#e0b4b4", "#e0b4b4"]
 
sns.barplot(x="order_id", y="product_category_name_english", data=most_least_favorito.head(5), palette=colors, ax=ax[0])
ax[0].set_ylabel(None)
ax[0].set_xlabel("Number of Sales", fontsize=30)
ax[0].set_title("Best Selling Product", loc="center", fontsize=50)
ax[0].tick_params(axis ='x', labelsize=30)
ax[0].tick_params(axis ='y', labelsize=35)
 
sns.barplot(x="order_id", y="product_category_name_english", data=most_least_favorito.sort_values(by="order_id", ascending=True).head(5), palette=colors, ax=ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel("Number of Sales", fontsize=30)
ax[1].invert_xaxis()
ax[1].yaxis.set_label_position("right")
ax[1].yaxis.tick_right()
ax[1].set_title("Worst Selling Product", loc="center", fontsize=50)
ax[1].tick_params(axis ='x', labelsize=30)
ax[1].tick_params(axis ='y', labelsize=35)

st.pyplot(fig)

#Rating
st.subheader("Rating from Customer")

fig, ax = plt.subplots(figsize=(20, 10))
colors = ["#e0b4b4", "#e0b4b4", "#e0b4b4", "#e0b4b4", "#7d1010"]
sns.barplot(
    x="review_score", 
    y="order_count",
    data=ratings.sort_values(by="order_count", ascending=False),
    palette=colors,
    ax=ax
)
ax.set_ylabel("Order", fontsize=30)
ax.set_xlabel("Rating", fontsize=30)
ax.tick_params(axis='y', labelsize=35)
ax.tick_params(axis='x', labelsize=30)
st.pyplot(fig)


#Demopgraphic
st.subheader("Customer Demographics")
fig, ax = plt.subplots(figsize=(35, 15))
colors = ["#7d1010", "#e0b4b4", "#e0b4b4", "#e0b4b4", "#e0b4b4", "#e0b4b4", "#e0b4b4", "#e0b4b4", "#e0b4b4", "#e0b4b4"]

sns.barplot(x="customer_id", y="customer_city", data=most_least_city.head(10), palette=colors)
ax.set_title("Number of Customer by City", loc="center", fontsize=30)
ax.set_ylabel(None)
ax.set_xlabel(None)
ax.tick_params(axis ='y', labelsize=35)
ax.tick_params(axis ='x', labelsize=30)
st.pyplot(fig)

with st.expander("See Explanation"):
    st.write(
        """So, these are the top 10 city that frequently buy products from this store during this period.
        """
    )

fig, ax = plt.subplots(figsize=(35, 15))
colors_ = ["#7d1010", "#e0b4b4", "#e0b4b4", "#e0b4b4", "#e0b4b4", "#e0b4b4", "#e0b4b4", "#e0b4b4", "#e0b4b4", "#e0b4b4"]
sns.barplot(x="customer_id", y="customer_state", data=most_least_state.head(10), palette=colors)
ax.set_title("Number of Customer by State", loc="center", fontsize=30)
ax.set_ylabel(None)
ax.set_xlabel(None)
ax.tick_params(axis ='y', labelsize=35)
ax.tick_params(axis ='x', labelsize=30)
st.pyplot(fig)

with st.expander("See Explanation"):
    st.write(
        """So, these are the top 10 countries that frequently buy products from this store during this period.
        """
    )

st.caption('Copyright (c) dwirwlnd 2024')
