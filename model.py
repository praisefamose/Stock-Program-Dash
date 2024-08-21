import numpy as np
import yfinance as yf
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.svm import SVR
from datetime import date, timedelta
import plotly.graph_objs as go

def predict_stock_price(ticker, forecast_days):
    # Load stock data
    stock_data = yf.download(ticker, period='3mo')
    stock_data.reset_index(inplace=True)
    stock_data['Day'] = stock_data.index

    # Prepare data for model training
    day_indices = np.array(stock_data.index).reshape(-1, 1)
    closing_prices = stock_data['Close'].values

    x_train, x_test, y_train, y_test = train_test_split(day_indices, closing_prices, test_size=0.1, shuffle=False)

    # Hyperparameter tuning and model training
    svr_params = {
        'C': [0.001, 0.01, 0.1, 1, 100, 1000],
        'epsilon': [0.0001, 0.001, 0.01, 0.1, 1],
        'gamma': [0.001, 0.01, 0.1, 1]
    }
    grid_search = GridSearchCV(SVR(kernel='rbf'), param_grid=svr_params, cv=5, scoring='neg_mean_absolute_error', n_jobs=-1)
    grid_search.fit(x_train, y_train)
    best_svr = grid_search.best_estimator_

    # Forecast future stock prices
    future_days = np.array([i + x_test[-1][0] for i in range(1, forecast_days)]).reshape(-1, 1)
    predicted_dates = [date.today() + timedelta(days=i) for i in range(forecast_days)]

    # Plot actual vs predicted prices
    forecast_graph = go.Figure()
    forecast_graph.add_trace(go.Scatter(x=x_test.flatten(), y=y_test, mode='markers', name='Actual'))
    forecast_graph.add_trace(go.Scatter(x=x_test.flatten(), y=best_svr.predict(x_test), mode='lines', name='Predicted'))
    forecast_graph.add_trace(go.Scatter(x=predicted_dates, y=best_svr.predict(future_days), mode='lines+markers', name='Forecast'))

    forecast_graph.update_layout(title=f"Predicted Stock Prices for {forecast_days - 1} Days", xaxis_title="Date", yaxis_title="Close Price")
    return forecast_graph
