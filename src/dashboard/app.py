import streamlit as st
import pandas as pd
import sqlite3
import altair as alt

# Connect to the database
conn = sqlite3.connect('../data/quotes.db')

# Load the table "ecommerce_items" to a dataframe
df = pd.read_sql_query("select * from ecommerce_items", conn)

# Close the Database connection
conn.close()

# Dashboard page config
st.set_page_config(
    page_title='Ecommerce Price Analysis',
    page_icon='📈',
    layout='wide',
    initial_sidebar_state='collapsed'
)

with st.sidebar:
    brands_list = list(df['brand'].unique())
    selected_brand = st.selectbox('Select a brand', brands_list, index=len(brands_list)-1)
    df_selected_brand = df[df.brand == selected_brand]

# Define the app title and subtitle
st.title("Ecommerce Price Analysis - Men's running shoes")
st.subheader('Main KPIs')

# Defining the columns structure for the main KPIs
col1, col2, col3 = st.columns(3)

# KPI 1: Items total count
total_itens = df.shape[0]
col1.metric(label='Total Items Quantity', value=total_itens)

# KPI 2: Unique brands count
unique_brands = df['brand'].nunique()
col2.metric(label="Brands", value=unique_brands)

# KPI 3: Average new price (after discount)
avg_new_price = df['new_price'].mean()
col3.metric(label='Average Price After Discount (BRL)', value=f'{avg_new_price:.2f}')

# Defining the subtitle and the columns structure for the  charts
st.subheader('Product count by brand')
col1, col2 = st.columns([4, 2], gap='medium')

# Top 20 brands that appear the most
top_20_brands = df['brand'].value_counts().head(20)
col1.bar_chart(
    top_20_brands,
    color='#FD5B4F'
)
col2.write(top_20_brands)

# Average price per brand
st.subheader('Average reviews rating versus average price per brand')
#col1 = st.columns([1,5],gap='medium')

#avg_review_rating = df.groupby('brand')['reviews_rating_number'] \
#                      .mean().sort_values(ascending=False)
#col1.write(avg_review_rating)

#avg_price_per_brand = df.groupby('brand')['new_price'].mean().sort_values(ascending=False)
avg_price_ratings_brand = df.groupby('brand').aggregate({'new_price':'mean', 'reviews_rating_number':'mean'})
st.scatter_chart(avg_price_ratings_brand, 
                 size='reviews_rating_number', 
                 color=['#FD5B4F','#FD5B4F']                 
                 )