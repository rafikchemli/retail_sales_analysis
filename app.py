import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
import plotly.subplots as sp
import streamlit as st

# Read the data from the xlsx file
# Upload your data file using the Streamlit file uploader
uploaded_file = st.file_uploader("Upload your sales data file", type=["xlsx", "xls"])

def sales_by_location(df_sku, fig):
    location_sales = df_sku.groupby('Store Name')['Sales: $'].sum().reset_index()
    location_sales = location_sales.sort_values(by='Sales: $', ascending=False)
    fig.add_trace(go.Bar(x=location_sales['Store Name'], y=location_sales['Sales: $'], name='Sales by Location'))

def seasonal_sales(df_sku, fig):
    df_sku['Week End Date'] = pd.to_datetime(df_sku['Week End Date'])
    df_sku['Month'] = df_sku['Week End Date'].dt.month
    seasonality = df_sku.groupby('Month')['Sales: $'].sum().reset_index()
    fig.add_trace(go.Scatter(x=seasonality['Month'], y=seasonality['Sales: $'], mode='lines+markers', name='Seasonal Sales'))

def weekly_sales_by_sku(df_sku, fig):
    weekly_sales = df_sku.groupby('Week End Date')['Sales: $'].sum().reset_index()
    fig.add_trace(go.Scatter(x=weekly_sales['Week End Date'], y=weekly_sales['Sales: $'], mode='lines+markers', name='Weekly Sales by SKU'))

def monthly_sales_by_sku(df_sku, fig):
    monthly_sales = df_sku.groupby(pd.Grouper(key='Week End Date', freq='M'))['Sales: $'].sum().reset_index()
    fig.add_trace(go.Scatter(x=monthly_sales['Week End Date'], y=monthly_sales['Sales: $'], mode='lines+markers', name='Monthly Sales by SKU'))

if uploaded_file:
    df = pd.read_excel(uploaded_file)
else:
    st.warning("Please upload a valid sales data file.")
    st.stop()


# Extract unique SKUs and store names
unique_skus = df['L1-Product ID'].unique()
store_names = df['Store Name'].unique()

st.title("Sales Analysis Dashboard")

selected_sku = st.selectbox("Select SKU:", unique_skus)

# Filter the data by selected SKU
df_sku = df[df['L1-Product ID'] == selected_sku]

# Get the product name
product_name = df_sku.iloc[0]['Product Name']

st.subheader(f"Sales Analysis for {product_name} (SKU {selected_sku})")

fig1 = sp.make_subplots(rows=1, cols=1)
fig2 = sp.make_subplots(rows=1, cols=1)
fig3 = sp.make_subplots(rows=1, cols=1)
fig4 = sp.make_subplots(rows=1, cols=1)

sales_by_location(df_sku, fig3)
fig3.update_layout(title_text="Sales by Location")

seasonal_sales(df_sku, fig2)
fig2.update_layout(title_text="Seasonal Sales")

weekly_sales_by_sku(df_sku, fig1)
fig1.update_layout(title_text="Weekly Sales by SKU")

monthly_sales_by_sku(df_sku, fig4)
fig4.update_layout(title_text="Monthly Sales by SKU")

st.plotly_chart(fig1)
st.plotly_chart(fig2)
st.plotly_chart(fig3)
st.plotly_chart(fig4)

