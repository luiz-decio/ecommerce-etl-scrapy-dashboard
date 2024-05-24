import streamlit as st
import pandas as pd
import sqlite3
import altair as alt
import os

# Get the current directory of the script
current_dir = os.path.dirname(os.path.abspath(__file__))
# Construct the absolute path to the database file
db_path = os.path.join(current_dir, '..', '..', 'data', 'quotes.db')

# Check if the database file exists
if not os.path.exists(db_path):
    st.error(f"Database file not found at {db_path}")
else:
    # Connect to the database
    conn = sqlite3.connect(db_path)

    # Load the table "ecommerce_items" to a dataframe
    df = pd.read_sql_query("select * from ecommerce_items", conn)

    # Dashboard page config
    st.set_page_config(
        page_title='E-commerce Price Analysis',
        page_icon='📈',
        layout='wide',
        initial_sidebar_state='collapsed'
    )

    with st.sidebar:
        brands_list = list(df['brand'].unique())
        selected_brand = st.selectbox('Select a brand', brands_list, index=len(brands_list)-1)
        df_selected_brand = df[df.brand == selected_brand]

    # Define the page title and description of the dashboard
    st.title("E-commerce Price Analysis - Men's running shoes")
    st.text('''
            This dashboard is based on the products information of men's running shoes available on one of the largest Brazilian e-commerce websites.

            The goal is to understand the most relevant brands and how the price of the products relates to the clients reviews and then answer weather good products necessarialy has the highest prices.  
            ''')

    # Defining the columns structure for the main KPIs
    st.subheader('Main KPIs')
    col1, col2, col3, col4 = st.columns(4)

    # KPI 1: Items total count
    total_itens = df.shape[0]
    col1.metric(label='Total Items Quantity', value=total_itens)

    # KPI 2: Unique brands count
    unique_brands = df['brand'].nunique()
    col2.metric(label="Brands", value=unique_brands)

    # KPI 3: Average new price (after discount)
    avg_new_price = df['new_price'].mean()
    col3.metric(label='Average Price After Discount (BRL)', value=f'R$ {avg_new_price:.2f}')

    # KPI 4: Average price before discount
    avg_old_price = df['old_price'].mean()
    col4.metric(label='Average Price Before Discount (BRL)', value=f'R$ {avg_old_price:.2f}')

    # Defining the subtitle and the columns structure for the  charts
    st.subheader('Top 20 brands with most products')
    col1, col2 = st.columns([3, 2], gap='medium')

    # Top 20 brands that appear the most
    top_20_brands = df.groupby('brand').aggregate(
        {
            'brand':'count',
            'reviews_amount':'sum',
            'new_price':['mean','max', 'min']
         }
         ).reset_index()
    
    # Flatten the multi-level column index
    top_20_brands.columns = ['_'.join(col).strip() for col in top_20_brands.columns.values]
    # Rename 'brand_count' to 'count'
    top_20_brands.rename(columns={'brand_': 'Brand',
                                  'brand_count': 'Product Qty',
                                  'reviews_amount_sum': "Total Product Reviews",
                                  'new_price_mean':'Average Price',
                                  'new_price_max':'Highest Price',
                                  'new_price_min':'Lowest Price'
                                  }, inplace=True)

    # Sorting by the amount of products and filtering the top 20
    top_20_brands.sort_values(by='Product Qty', ascending=False, inplace=True)
    top_20_brands = top_20_brands.head(20)

    # Create a bar chart with Altair
    top_20_brands_bar_chart = alt.Chart(top_20_brands).mark_bar(color='#FD5B4F').encode(
        x=alt.X('Brand:N', sort='-y'),
        y='Product Qty:Q'
    )

    # Display bar chart in the first column
    with col1:
        st.altair_chart(top_20_brands_bar_chart, use_container_width=True)

    # Display dataframe in the second column
    with col2:
        st.dataframe(top_20_brands, hide_index=True)

    # Average price versus average reviews rating per brand
    st.subheader('Average reviews rating versus average price per brand')
    #avg_price_ratings_brand = df.groupby('brand').aggregate({'new_price':'mean', 'reviews_rating_number':'mean'})
    avg_price_ratings_brand = df.groupby('brand').aggregate(
        new_price = ('new_price','mean'),
        reviews_rating_number = ('reviews_rating_number', lambda x: x[x != 0].mean())
    )
    # Rename the columns
    avg_price_ratings_brand.rename(columns={'brand':'Brand',
                                            'new_price':'Average Product Price',
                                            'reviews_rating_number':'Average Review Rating'},
                                            inplace=True)
    
    # Creating the scatter chart
    st.scatter_chart(avg_price_ratings_brand, 
                    size='Average Review Rating', 
                    color=['#FD5B4F','#FD5B4F']
                    )