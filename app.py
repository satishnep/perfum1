import streamlit as st
import pandas as pd
import plotly.express as px
import logging

# Page config
st.set_page_config(page_title="Fragrance Marketplace Dashboard", layout="wide")

st.title(" Fragrance Marketplace Dashboard")

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv("cleaned_data.csv")
    df['lastUpdated'] = pd.to_datetime(df['lastUpdated'], errors='coerce')
    df['price'] = pd.to_numeric(df['price'], errors='coerce')
    df['sold'] = pd.to_numeric(df['sold'], errors='coerce')
    df['available'] = pd.to_numeric(df['available'], errors='coerce')
    return df

df = load_data()

# Sidebar filters
st.sidebar.header("Filters")

brand_options = df['brand'].dropna().unique()
type_options = df['type'].dropna().unique()
country_options = df['country'].dropna().unique()

selected_brand = st.sidebar.multiselect("Select Brand", options=sorted(brand_options), default=brand_options)
selected_type = st.sidebar.multiselect("Select Type", options=sorted(type_options), default=type_options)
selected_country = st.sidebar.multiselect("Select Country", options=sorted(country_options), default=country_options)

# Apply filters
df_filtered = df[
    df['brand'].isin(selected_brand) &
    df['type'].isin(selected_type) &
    df['country'].isin(selected_country)
]

# KPI Cards
total_items = df_filtered.shape[0]
total_sold = df_filtered['sold'].sum()
avg_price = df_filtered['price'].mean()

col1, col2, col3 = st.columns(3)
col1.metric("📦 Total Listings", total_items)
col2.metric("🛒 Units Sold", int(total_sold))
col3.metric("💲Average Price", f"${avg_price:.2f}")

st.markdown("---")

# Top Selling Brands
top_brands = df_filtered.groupby('brand')['sold'].sum().sort_values(ascending=False).head(10).reset_index()
fig1 = px.bar(top_brands, x='brand', y='sold', title="🔥 Top Selling Brands", color='sold', text='sold')
st.plotly_chart(fig1, use_container_width=True)

# Price distribution by type
fig2 = px.box(df_filtered, x='type', y='price', title="📊 Price Distribution by Type", points="all")
st.plotly_chart(fig2, use_container_width=True)

# Listings by Country
map_df = df_filtered.groupby('country')['sold'].sum().reset_index()
fig3 = px.choropleth(map_df, locations='country', locationmode='country names', color='sold',
                     title="🌍 Units Sold by Country", color_continuous_scale="plasma")
st.plotly_chart(fig3, use_container_width=True)

logging.getLogger('streamlit.runtime.scriptrunner.script_run_context').setLevel(logging.ERROR)


# Data Preview
with st.expander("🔍 View Raw Data"):
    st.dataframe(df_filtered)
