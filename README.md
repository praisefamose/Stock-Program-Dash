# Stock Dashboard Application

This Stock Dashboard Application is a web-based tool that allows users to visualize and forecast stock prices using historical data. It is built using Python, Dash, and Plotly, with data sourced from Yahoo Finance.

## Features

- **Stock Price Visualization**: View historical stock prices for selected companies.
- **Technical Indicators**: Display technical indicators like the 20-Day Exponential Moving Average (EMA).
- **Forecasting**: Predict future stock prices using machine learning models.

## Project Structure

- `main.py`: The main application script that defines the layout, callbacks, and functionality of the Dash app.
- `model.py`: Contains the machine learning model used for stock price prediction.
- `assets/styles.css`: Custom CSS for styling the application.
- `requirements.txt`: List of required Python packages for the project.
- `assets/your-pic.jpeg`: Profile image for the footer (ensure this is placed in the `assets` directory).

## Installation

1. **Clone the repository**:

    ```bash
    git clone https://github.com/your-repo/stock-dashboard.git
    cd stock-dashboard
    ```

2. **Create a virtual environment**:

    ```bash
    pip install pipenv
    pipenv install
    pipenv shell
    ```

3. **Install dependencies**:

    ```bash
    pip install -r requirements.txt
    ```

4. **Run the application**:

    ```bash
    python main.py
    ```

    The app will run on [http://127.0.0.1:5501/](http://127.0.0.1:5501/).

## Usage

- Enter the stock ticker symbol in the input box and click "Submit".
- Choose a date range to view the historical stock prices.
- Use the buttons to visualize stock prices, indicators, or predict future stock prices.

## Customization

- **Profile Image**: Replace the image `assets/your-pic.jpeg` with your profile picture.
- **LinkedIn Profile**: Update the LinkedIn URL in `main.py` to link to your LinkedIn profile.

## Requirements

Ensure that the `assets/styles.css` file and the image `assets/your-pic.jpeg` are present in the appropriate directories.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
