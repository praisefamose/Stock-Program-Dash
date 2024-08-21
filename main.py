import dash
from dash import dcc, html
from dash.dependencies import Output, Input, State
from dash.exceptions import PreventUpdate
import datetime as dt
import yfinance as yf
import pandas as pd
import plotly.express as px
from model import predict_stock_price

app = dash.Dash(__name__, external_stylesheets=['assets/styles.css'])
server = app.server

# Define the layout components

# Navigation component
navigation_bar = html.Div(
    [
        html.P("Welcome to the Stock Dashboard!", className="welcome-text"),

        html.Div([
            # Stock ticker input
            dcc.Input(id='ticker-input', type='text', placeholder='Enter stock ticker', className='ticker-input-box'),
            html.Button('Submit', id='submit-ticker', className='submit-button')
        ], className="ticker-input"),

        html.Div([
            # Date range picker
            dcc.DatePickerRange(
                id='date-picker', start_date=dt.datetime(2018, 1, 1).date(), end_date=dt.datetime.now().date(), className='date-picker')
        ]),

        html.Div([
            # Buttons for stock price, indicators, and forecast
            html.Button('Show Stock Prices', id='show-prices-button', className='action-button'),
            html.Button('Show Indicators', id='show-indicators-button', className='action-button'),
            dcc.Input(id='forecast-input', type='number', placeholder='Forecast days', className='forecast-input-box'),
            html.Button('Predict', id='predict-button', className='action-button')
        ], className="action-buttons")
    ],
    className="navigation"
)

# Content component
content_area = html.Div(
    [
        html.Div(
            [
                html.Img(id='company-logo', className='company-logo'),
                html.H1(id='company-name', className='company-name')
            ],
            className="header"
        ),
        html.Div(id="company-description", className="company-description"),
        html.Div(id="price-graph-container", className="graph-container"),
        html.Div(id="indicator-graph-container", className="graph-container"),
        html.Div(id="forecast-graph-container", className="graph-container")
    ],
    className="content"
)

# Footer component
footer = html.Div(
    [
        html.Div(
            [
                html.Img(src='assets/your-pic.jpeg', className='footer-image'),
                html.P("Programmed by Praise Famose", className="footer-text"),
                html.A("LinkedIn", href="https://www.linkedin.com/in/praise-famose-843449274", target="_blank", className="footer-link")
            ],
            className="footer-content"
        )
    ],
    className="footer"
)

# Set the layout
app.layout = html.Div(className='container', children=[navigation_bar, content_area, footer])

# Callbacks

# Callback to update the data based on the submitted stock ticker
@app.callback(
    [
        Output("company-description", "children"),
        Output("company-logo", "src"),
        Output("company-name", "children"),
        Output("show-prices-button", "n_clicks"),
        Output("show-indicators-button", "n_clicks"),
        Output("predict-button", "n_clicks")
    ],
    [Input("submit-ticker", "n_clicks")],
    [State("ticker-input", "value")]
)
def update_company_info(n_clicks, ticker):
    if n_clicks is None or ticker is None:
        raise PreventUpdate

    company = yf.Ticker(ticker)
    company_info = company.info

    if 'logo_url' not in company_info:
        return None, None, None, None, None, None
    else:
        company_name = company_info['longName']
        logo_url = company_info['logo_url']
        description = company_info['longBusinessSummary']
        return description, logo_url, company_name, None, None, None


# Callback for displaying stock price graphs
@app.callback(
    [Output("price-graph-container", "children")],
    [
        Input("show-prices-button", "n_clicks"),
        Input('date-picker', 'start_date'),
        Input('date-picker', 'end_date')
    ],
    [State("ticker-input", "value")]
)
def display_stock_prices(n_clicks, start_date, end_date, ticker):
    if n_clicks is None or ticker is None:
        raise PreventUpdate
    
    stock_data = yf.download(ticker, start=start_date, end=end_date)
    stock_data.reset_index(inplace=True)
    price_graph = px.line(stock_data, x="Date", y=["Close", "Open"], title="Stock Prices Over Time")

    return [dcc.Graph(figure=price_graph)]


# Callback for displaying indicators
@app.callback(
    [Output("indicator-graph-container", "children")],
    [
        Input("show-indicators-button", "n_clicks"),
        Input('date-picker', 'start_date'),
        Input('date-picker', 'end_date')
    ],
    [State("ticker-input", "value")]
)
def display_indicators(n_clicks, start_date, end_date, ticker):
    if n_clicks is None or ticker is None:
        raise PreventUpdate
    
    indicator_data = yf.download(ticker, start=start_date, end=end_date)
    indicator_data.reset_index(inplace=True)
    indicator_graph = create_indicator_graph(indicator_data)

    return [dcc.Graph(figure=indicator_graph)]


def create_indicator_graph(data):
    data['EMA_20'] = data['Close'].ewm(span=20, adjust=False).mean()
    ema_graph = px.scatter(data, x="Date", y="EMA_20", title="20-Day Exponential Moving Average")
    ema_graph.update_traces(mode='lines+markers')
    return ema_graph


# Callback for displaying forecast
@app.callback(
    [Output("forecast-graph-container", "children")],
    [Input("predict-button", "n_clicks")],
    [State("forecast-input", "value"),
     State("ticker-input", "value")]
)
def display_forecast(n_clicks, forecast_days, ticker):
    if n_clicks is None or ticker is None:
        raise PreventUpdate

    forecast_graph = predict_stock_price(ticker, int(forecast_days) + 1)
    return [dcc.Graph(figure=forecast_graph)]


if __name__ == '__main__':
    app.run_server(debug=True, port=5501)
