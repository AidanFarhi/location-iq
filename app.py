from dash import Dash, html, dcc, callback, Output, Input
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd

df = pd.read_csv(
    './data/RDC_Inventory_Core_Metrics_Zip_History.csv',
    usecols=[
        'postal_code', 
        'month_date_yyyymm', 
        'median_listing_price',
        'median_days_on_market',
        'active_listing_count',
        'price_reduced_count'
    ],
    dtype={'postal_code': 'str', 'month_date_yyyymm': 'str'}
)

app = Dash(external_stylesheets=[dbc.themes.COSMO])

app.layout = [
    html.P(
        id='header',
        children='Location IQ'
    ),
    html.Div(
        id='dropdown-container',
        children=[
            html.Label('Date:'),
            dcc.Dropdown(
                className='dropdown',
                id='date-selection',
                options=sorted(df.month_date_yyyymm.unique()),
                value='202401'
            ),
            html.Label('Zip Code:'),
            dcc.Dropdown(
                className='dropdown',
                id='postal-code-selection',
                options=df.postal_code.unique(),
                value='19977'
            ),
        ]
    ),
    html.Div(
        id='graph-container',
        children=[
            dcc.Graph(className='graph', id='graph-median-price'),
            dcc.Graph(className='graph', id='graph-median-days-on-market'),
            dcc.Graph(className='graph', id='graph-active-listing-count'),
            dcc.Graph(className='graph', id='graph-price-reduced-count')
        ]
    )
]

@callback(
    Output('graph-median-price', 'figure'),
    Output('graph-median-days-on-market', 'figure'),
    Output('graph-active-listing-count', 'figure'),
    Output('graph-price-reduced-count', 'figure'),
    Input('postal-code-selection', 'value'),
    Input('date-selection', 'value')
)
def update_figure(postal_code, date):
    data = df[(df.postal_code==postal_code) & (df.month_date_yyyymm >= date)].sort_values('month_date_yyyymm')
    median_price = px.line(
        data, 
        x='month_date_yyyymm', 
        y='median_listing_price',
        title='Median Listing Price',
    ).update_layout(title={'x': 0.5, 'xanchor': 'center'})
    median_days_on_market = px.line(
        data, 
        x='month_date_yyyymm', 
        y='median_days_on_market',
        title='Median Days On Market',
    ).update_layout(title={'x': 0.5, 'xanchor': 'center'})
    active_listing_count = px.line(
        data, 
        x='month_date_yyyymm', 
        y='active_listing_count',
        title='Active Listing Count',
    ).update_layout(title={'x': 0.5, 'xanchor': 'center'})
    price_reduced_count = px.line(
        data, 
        x='month_date_yyyymm', 
        y='price_reduced_count',
        title='Price Reduced Count',
    ).update_layout(title={'x': 0.5, 'xanchor': 'center'})
    return median_price, median_days_on_market, active_listing_count, price_reduced_count

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port='8000')
