import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
import plotly.subplots as sp
import streamlit as st
import calendar  # Add this import statement



# Read the data from the xlsx file
# Upload your data file using the Streamlit file uploader
uploaded_file = st.file_uploader("Upload your sales data file", type=["xlsx", "xls"])
if uploaded_file:
    df = pd.read_excel(uploaded_file)
else:
    st.warning("Please upload a valid sales data file.")
    st.stop()

unique_skus = df['L1-Product ID'].unique()
store_names = df['Store Name'].unique()

def sales_by_location(df_sku, fig):
    location_sales = df_sku.groupby('Store Name')['Sales: $'].sum().reset_index()
    location_sales = location_sales.sort_values(by='Sales: $', ascending=False)
    fig.add_trace(go.Bar(x=location_sales['Store Name'], y=location_sales['Sales: $'], name='Sales by Location'))
    fig.update_xaxes(tickangle=45)  # Add this line to update the angle of x-axis tick labels


def seasonal_sales(df_sku, fig):
    df_sku['Week End Date'] = pd.to_datetime(df_sku['Week End Date'])
    df_sku['Month'] = df_sku['Week End Date'].dt.month
    df_sku['Month Name'] = df_sku['Month'].apply(lambda x: calendar.month_abbr[x])  # Convert month number to month name
    seasonality = df_sku.groupby('Month Name')['Sales: $'].sum().reset_index()
    fig.add_trace(go.Scatter(x=seasonality['Month Name'], y=seasonality['Sales: $'], mode='lines+markers', name='Seasonal Sales'))

def weekly_sales_by_sku(df_sku, fig):
    weekly_sales = df_sku.groupby('Week End Date')['Sales: $'].sum().reset_index()
    fig.add_trace(go.Scatter(x=weekly_sales['Week End Date'], y=weekly_sales['Sales: $'], mode='lines+markers', name='Weekly Sales by SKU'))

def monthly_sales_by_sku(df_sku, fig):
    monthly_sales = df_sku.groupby(pd.Grouper(key='Week End Date', freq='M'))['Sales: $'].sum().reset_index()
    fig.add_trace(go.Scatter(x=monthly_sales['Week End Date'], y=monthly_sales['Sales: $'], mode='lines+markers', name='Monthly Sales by SKU'))

def sales_vs_units_sold(df_sku, fig):
    sales_qty = df_sku.groupby('Store Name')[['Sales: $', 'Sales: Qty']].sum().reset_index()
    scatter = go.Scatter(x=sales_qty['Sales: Qty'], y=sales_qty['Sales: $'], mode='markers', name='Sales vs. Units Sold', text=sales_qty['Store Name'])
    fig.add_trace(scatter)
    fig.update_traces(textposition='top center', textfont_size=10)
    fig.update_layout(title_text="Sales vs. Units Sold")

def all_sku_seasonal_sales(df, fig):
    df['Week End Date'] = pd.to_datetime(df['Week End Date'])
    df['Month'] = df['Week End Date'].dt.month
    df['Month Name'] = df['Month'].apply(lambda x: calendar.month_abbr[x])  # Convert month number to month name
    
    for sku in unique_skus:
        df_sku = df[df['L1-Product ID'] == sku]
        seasonality = df_sku.groupby('Month Name')['Sales: $'].sum().reset_index()
        fig.add_trace(go.Scatter(x=seasonality['Month Name'], y=seasonality['Sales: $'], mode='lines+markers', name=f'Seasonal Sales (SKU {sku})'))


def all_sku_weekly_sales(df, fig):
    for sku in unique_skus:
        df_sku = df[df['L1-Product ID'] == sku]
        weekly_sales = df_sku.groupby('Week End Date')['Sales: $'].sum().reset_index()
        fig.add_trace(go.Scatter(x=weekly_sales['Week End Date'], y=weekly_sales['Sales: $'], mode='lines+markers', name=f'Weekly Sales (SKU {sku})'))

def all_sku_monthly_sales(df, fig):
    for sku in unique_skus:
        df_sku = df[df['L1-Product ID'] == sku]
        monthly_sales = df_sku.groupby(pd.Grouper(key='Week End Date', freq='M'))['Sales: $'].sum().reset_index()
        fig.add_trace(go.Scatter(x=monthly_sales['Week End Date'], y=monthly_sales['Sales: $'], mode='lines+markers', name=f'Monthly Sales (SKU {sku})'))


st.title("Sales Analysis Dashboard")

comparison_tab = st.expander("Comparison of multiple SKUs")
with comparison_tab:
    st.title("Comparison of All SKUs")

    fig6 = sp.make_subplots(rows=1, cols=1)
    fig7 = sp.make_subplots(rows=1, cols=1)
    fig8 = sp.make_subplots(rows=1, cols=1)

    all_sku_seasonal_sales(df, fig6)
    fig6.update_layout(title_text="All SKUs - Seasonal Sales")

    all_sku_weekly_sales(df, fig7)
    fig7.update_layout(title_text="All SKUs - Weekly Sales")

    all_sku_monthly_sales(df, fig8)
    fig8.update_layout(title_text="All SKUs - Monthly Sales")

    st.plotly_chart(fig6)
    st.plotly_chart(fig7)
    st.plotly_chart(fig8)




SelectedSKU_tab = st.expander("Individual SKU insights")
with SelectedSKU_tab:
    
    st.title("Selected SKU Analysis")
    selected_sku = st.selectbox("Select SKU:", unique_skus)

    #Filter the data by selected SKU
    df_sku = df[df['L1-Product ID'] == selected_sku]

    # Get the product name
    product_name = df_sku.iloc[0]['Product Name']

    st.subheader(f"Product Name: {product_name} (SKU {selected_sku})")

    fig1 = sp.make_subplots(rows=1, cols=1)
    fig2 = sp.make_subplots(rows=1, cols=1)
    fig3 = sp.make_subplots(rows=1, cols=1)
    fig4 = sp.make_subplots(rows=1, cols=1)

    sales_by_location(df_sku, fig3)
    fig3.update_layout(title_text="Sales by Location")

    seasonal_sales(df_sku, fig2)
    fig2.update_layout(title_text="Seasonal")

    weekly_sales_by_sku(df_sku, fig1)
    fig1.update_layout(title_text="Weekly Sales")

    monthly_sales_by_sku(df_sku, fig4)
    fig4.update_layout(title_text="Monthly Sales")

    st.plotly_chart(fig3)
    st.plotly_chart(fig1)
    st.plotly_chart(fig2)
    st.plotly_chart(fig4)




#


