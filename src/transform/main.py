import pandas as pd
import sqlite3
from datetime import datetime
import os

# Define the JSON file path
df = pd.read_json('../data/products_data.jsonl', lines=True)

# Set pandas to show all the columns
#pd.options.display.max_columns = None

# Add columns with data source and insert date
df['data_source'] = "https://lista.mercadolivre.com.br/tenis-corrida-masculino"
df['insert_date'] = datetime.now()

# Change the data type of the price columns to float
df['old_price_whole'] = df['old_price_whole'].fillna(0).astype(float)
df['old_price_cents'] = df['old_price_cents'].fillna(0).astype(float)
df['new_price_whole'] = df['new_price_whole'].fillna(0).astype(float)
df['new_price_cents'] = df['new_price_cents'].fillna(0).astype(float)
df['reviews_rating_number'] = df['reviews_rating_number'].fillna(0).astype(float)

# Removing the parentheses from the "reviews amount" column and changing it to the integer data type
df['reviews_amount'] = df['reviews_amount'].str.replace('[\(\)]', '', regex=True)
df['reviews_amount'] = df['reviews_amount'].fillna(0).astype(int)

# Transforming the cents columns and adding to the whole value columns
df['old_price'] = df['old_price_whole'] + df['old_price_cents'] / 100
df['new_price'] = df['new_price_whole'] + df['new_price_cents'] / 100

# Droping the cents columns
df.drop(columns=['old_price_whole', 'old_price_cents', 'new_price_whole', 'new_price_cents'], inplace=True)

# Connect to a SQLite Database (or create a new one)
conn = sqlite3.connect('../data/quotes.db')

# Save the transformed dataframe in the Database
df.to_sql('ecommerce_items', conn, if_exists='replace', index=False)

# Close the Database connection
conn.close()

print(df.head())