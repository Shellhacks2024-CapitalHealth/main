import requests
import pandas as pd
from prophet import Prophet
import matplotlib.pyplot as plt

class ExchangeRatePredictor:
    def __init__(self, api_url, base_currency, target_currency, api_key):
        self.api_url = api_url
        self.base_currency = base_currency
        self.target_currency = target_currency
        self.api_key = api_key
        self.current_rate = None
        self.historical_data = None
        self.model = None
        self.forecast = None

    def get_current_exchange_rate(self):
        # Fetch exchange rate from API
        url = f"{self.api_url}?base={self.base_currency}&symbols={self.target_currency}&access_key={self.api_key}"
        response = requests.get(url)
        data = response.json()

        if 'error' in data:
            raise Exception(f"API Error: {data['error']}")

        self.current_rate = data['rates'][self.target_currency]
        return self.current_rate

    def get_historical_data(self, start_date, end_date):
    
        #Fetches historical exchange rate data between start_date and end_date.
        url = f"{self.api_url}/timeseries?start_date={start_date}&end_date={end_date}&base={self.base_currency}&symbols={self.target_currency}&access_key={self.api_key}"
        response = requests.get(url)
        data = response.json()

        if 'error' in data:
            raise Exception(f"API Error: {data['error']}")

        # Convert data to DataFrame
        rates = data['rates']
        df = pd.DataFrame([
            {'ds': date, 'y': rate[self.target_currency]}
            for date, rate in rates.items()
        ])
        df['ds'] = pd.to_datetime(df['ds'])
        df.sort_values('ds', inplace=True)
        self.historical_data = df
        return df

    def predict_exchange_rate(self, periods):
        
        #Uses Prophet to predict future exchange rates.
        if self.historical_data is None:
            raise ValueError("Historical data not loaded. Call get_historical_data() first.")

        self.model = Prophet()
        self.model.fit(self.historical_data)

        # Make future predictions
        future = self.model.make_future_dataframe(periods=periods)
        self.forecast = self.model.predict(future)

        # Plot the forecast
        self.model.plot(self.forecast)
        plt.title(f"Exchange Rate Forecast: {self.base_currency} to {self.target_currency}")
        plt.xlabel("Date")
        plt.ylabel("Exchange Rate")
        plt.show()

        return self.forecast[['ds', 'yhat']]

    def advise_on_exchange(self, threshold, exchange_type):
        
        #Advises whether to buy or sell based on predicted rates.
        if self.current_rate is None:
            self.get_current_exchange_rate()
        if self.forecast is None:
            raise ValueError("Forecast not generated. Call predict_exchange_rate() first.")

        advice_list = []

        for _, row in self.forecast.iterrows():
            predicted_rate = row['yhat']
            date = row['ds']

            # Calculate the percentage change from the current rate
            percentage_change = ((predicted_rate - self.current_rate) / self.current_rate) * 100

            # Advice based on whether you're buying or selling
            if exchange_type == 'buy':
                # For buying, lower predicted rates are better
                if percentage_change <= -threshold:
                    advice = f"Good time to buy on {date.date()} with predicted rate: {predicted_rate:.4f}"
                else:
                    advice = f"Wait to buy, predicted rate on {date.date()} is {predicted_rate:.4f}"
            elif exchange_type == 'sell':
                # For selling, higher predicted rates are better
                if percentage_change >= threshold:
                    advice = f"Good time to sell on {date.date()} with predicted rate: {predicted_rate:.4f}"
                else:
                    advice = f"Wait to sell, predicted rate on {date.date()} is {predicted_rate:.4f}"
            else:
                raise ValueError("Invalid exchange_type. Please choose 'buy' or 'sell'.")

            advice_list.append(advice)

        # Print all advice
        for advice in advice_list:
            print(advice)

        return advice_list
