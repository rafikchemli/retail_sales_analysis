import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
import plotly.subplots as sp
import streamlit as st
import calendar  # Add this import statement
import pandas as pd
import openpyxl  # Add this import at the beginning of your code

# Read the data from the xlsx file using openpyxl
df = pd.read_excel("retail_data.xlsx", engine='openpyxl')
# Set wide mode
st.set_page_config(layout="wide")


unique_skus = df['L1-Product ID'].unique()
store_names = df['Store Name'].unique()

def sales_by_location(df_sku, fig):
    location_sales = df_sku.groupby('Store Name')['Sales: $'].sum().reset_index()
    location_sales = location_sales.sort_values(by='Sales: $', ascending=False)
    fig.add_trace(go.Bar(x=location_sales['Store Name'], y=location_sales['Sales: $'], name='Sales by Location'))
    fig.update_xaxes(tickangle=45)  # Add this line to update the angle of x-axis tick labels
    fig.update_layout(yaxis_title="Sales ($)")

def seasonal_sales(df_sku, fig):
    df_sku['Week End Date'] = pd.to_datetime(df_sku['Week End Date'])
    df_sku['Month'] = df_sku['Week End Date'].dt.month
    df_sku['Month Name'] = df_sku['Month'].apply(lambda x: calendar.month_abbr[x])  # Convert month number to month name
    seasonality = df_sku.groupby('Month Name')['Sales: $'].sum().reset_index()

    # Add a column for month numbers and sort the DataFrame by month number
    month_number_mapping = {month_abbr: i for i, month_abbr in enumerate(calendar.month_abbr)}
    seasonality['Month Number'] = seasonality['Month Name'].map(month_number_mapping)
    seasonality = seasonality.sort_values(by='Month Number')

    # Add the trace with the sorted month names and sales data
    fig.add_trace(go.Scatter(x=seasonality['Month Name'], y=seasonality['Sales: $'], mode='lines+markers', name='Seasonal Sales'))
    fig.update_layout(yaxis_title="Sales ($)")

def weekly_sales_by_sku(df_sku, fig):
    weekly_sales = df_sku.groupby('Week End Date')['Sales: $'].sum().reset_index()
    fig.add_trace(go.Scatter(x=weekly_sales['Week End Date'], y=weekly_sales['Sales: $'], mode='lines+markers', name='Weekly Sales by SKU'))
    fig.update_layout(yaxis_title="Sales ($)")

def monthly_sales_by_sku(df_sku, fig):
    monthly_sales = df_sku.groupby(pd.Grouper(key='Week End Date', freq='M'))['Sales: $'].sum().reset_index()
    fig.add_trace(go.Scatter(x=monthly_sales['Week End Date'], y=monthly_sales['Sales: $'], mode='lines+markers', name='Monthly Sales by SKU'))
    fig.update_layout(yaxis_title="Sales ($)")

def sales_vs_units_sold(df_sku, fig):
    sales_qty = df_sku.groupby('Store Name')[['Sales: $', 'Sales: Qty']].sum().reset_index()
    scatter = go.Scatter(x=sales_qty['Sales: Qty'], y=sales_qty['Sales: $'], mode='markers', name='Sales vs. Units Sold', text=sales_qty['Store Name'])
    fig.add_trace(scatter)
    fig.update_traces(textposition='top center', textfont_size=10)
    fig.update_layout(title_text="Sales vs. Units Sold")
    fig.update_layout(yaxis_title="Sales ($)")

def all_sku_seasonal_sales(df, fig):
    df['Week End Date'] = pd.to_datetime(df['Week End Date'])
    df['Month'] = df['Week End Date'].dt.month
    df['Month Name'] = df['Month'].apply(lambda x: calendar.month_abbr[x])

    unique_skus = df['L1-Product ID'].unique()

    # Create a dictionary for month number mapping
    month_number_mapping = {month_abbr: i for i, month_abbr in enumerate(calendar.month_abbr)}

    # Calculate total sales for each month
    total_monthly_sales = df.groupby('Month Name')['Sales: $'].sum().reset_index()
    total_monthly_sales['Month Number'] = total_monthly_sales['Month Name'].map(month_number_mapping)
    total_monthly_sales = total_monthly_sales.sort_values(by='Month Number')

    # Add a bar chart trace for total sales
    fig.add_trace(go.Bar(x=total_monthly_sales['Month Name'], y=total_monthly_sales['Sales: $'], name='Total Sales', opacity=0.5))

    for sku in unique_skus:
        df_sku = df[df['L1-Product ID'] == sku]
        seasonality = df_sku.groupby('Month Name')['Sales: $'].sum().reset_index()

        # Add a column for month numbers and sort the DataFrame by month number
        seasonality['Month Number'] = seasonality['Month Name'].map(month_number_mapping)
        seasonality = seasonality.sort_values(by='Month Number')

        # Add the trace with the sorted month names and sales data
        fig.add_trace(go.Scatter(x=seasonality['Month Name'], y=seasonality['Sales: $'], mode='lines+markers', name=f'SKU {sku}'))
    
    fig.update_layout(yaxis_title="Sales ($)")

def all_sku_weekly_sales(df, fig):
    unique_skus = df['L1-Product ID'].unique()

    # Calculate total sales for each week
    total_weekly_sales = df.groupby('Week End Date')['Sales: $'].sum().reset_index()

    # Add a bar chart trace for total sales
    fig.add_trace(go.Bar(x=total_weekly_sales['Week End Date'], y=total_weekly_sales['Sales: $'], name='Total Sales', opacity=0.5))

    for sku in unique_skus:
        df_sku = df[df['L1-Product ID'] == sku]
        weekly_sales = df_sku.groupby('Week End Date')['Sales: $'].sum().reset_index()
        fig.add_trace(go.Scatter(x=weekly_sales['Week End Date'], y=weekly_sales['Sales: $'], mode='lines+markers', name=f'SKU {sku}'))
    fig.update_layout(yaxis_title="Sales ($)")

def all_sku_monthly_sales(df, fig):
    unique_skus = df['L1-Product ID'].unique()

    # Calculate total sales for each month
    total_monthly_sales = df.groupby(pd.Grouper(key='Week End Date', freq='M'))['Sales: $'].sum().reset_index()

    # Add a bar chart trace for total sales
    fig.add_trace(go.Bar(x=total_monthly_sales['Week End Date'], y=total_monthly_sales['Sales: $'], name='Total Sales', opacity=0.5))

    for sku in unique_skus:
        df_sku = df[df['L1-Product ID'] == sku]
        monthly_sales = df_sku.groupby(pd.Grouper(key='Week End Date', freq='M'))['Sales: $'].sum().reset_index()
        fig.add_trace(go.Scatter(x=monthly_sales['Week End Date'], y=monthly_sales['Sales: $'], mode='lines+markers', name=f'SKU {sku}'))
    fig.update_layout(yaxis_title="Sales ($)")

import streamlit as st

# def display_top_stores(df, num_stores=10):
#     # Calculate total sales for each store across all products
#     store_total_sales = df.groupby('Store Name')['Sales: $'].sum().reset_index()

#     # Sort the DataFrame by total sales in descending order
#     store_total_sales = store_total_sales.sort_values(by='Sales: $', ascending=False)

#     # Display the top stores
#     top_stores = store_total_sales.head(num_stores)
#     st.subheader(f"Top {num_stores} Stores by Total Sales Across All Products")
#     st.dataframe(top_stores)

def display_top_stores(df, sku=None, num_stores=10):
    if sku:
        df = df[df['L1-Product ID'] == sku]

    store_sales = df.groupby('Store Name')['Sales: $'].sum().reset_index()
    store_units_sold = df.groupby('Store Name')['Sales: Qty'].sum().reset_index()
    store_summary = store_sales.merge(store_units_sold, on='Store Name')
    store_summary = store_summary.nlargest(num_stores, 'Sales: $')

    # Reset the index and add 1
    store_summary = store_summary.reset_index(drop=True)
    store_summary.index = store_summary.index + 1
    return store_summary

def display_worst_stores(df, sku=None, num_stores=10):
    if sku:
        df = df[df['L1-Product ID'] == sku]

    store_sales = df.groupby('Store Name')['Sales: $'].sum().reset_index()
    store_units_sold = df.groupby('Store Name')['Sales: Qty'].sum().reset_index()
    store_summary = store_sales.merge(store_units_sold, on='Store Name')
    store_summary = store_summary.nsmallest(num_stores, 'Sales: $')

    # Reset the index and add 1
    store_summary = store_summary.reset_index(drop=True)
    store_summary.index = store_summary.index + 1

    return store_summary


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


    # display_top_stores(df, num_stores=10)  # Change 10 to your desired number of top stores

Top_worst_tab = st.expander("Store Performance")
with Top_worst_tab:
    # In your Streamlit app
    st.title("Top and Worst Stores by Total Sales")

    # Create columns to place filters side by side
    filter_col1, filter_col2 = st.columns(2)

    # Add the SKU filter in the first column
    selected_sku = filter_col1.selectbox("Filter by SKU:", ["All"] + list(unique_skus), index=0)

    if selected_sku == "All":
        selected_sku = None

    # Add the number of stores input in the second column
    num_stores = filter_col2.number_input("Number of stores to display:", min_value=1, value=10, step=1)

    # Create columns to display the top and worst stores side by side
    col1, col2 = st.columns(2)

    col1.subheader(f"Top {num_stores} Stores")
    top_stores = display_top_stores(df, sku=selected_sku, num_stores=num_stores)
    col1.dataframe(top_stores)

    col2.subheader(f"Worst {num_stores} Stores")
    worst_stores = display_worst_stores(df, sku=selected_sku, num_stores=num_stores)
    col2.dataframe(worst_stores)


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
    fig2.update_layout(title_text="Seasonal Trends")

    weekly_sales_by_sku(df_sku, fig1)
    fig1.update_layout(title_text="Weekly Sales")

    monthly_sales_by_sku(df_sku, fig4)
    fig4.update_layout(title_text="Monthly Sales")

    st.plotly_chart(fig3)
    st.plotly_chart(fig2)
    st.plotly_chart(fig1)
    st.plotly_chart(fig4)




#


