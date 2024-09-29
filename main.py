import spending as sp
import pandas as pd
import matplotlib.pyplot as plt
from bank_health import BankAccountAnalyzer as ba
from inflation_analyzer import IncomeInflationAnalyzer as ia
from exchange_predictor import ExchangeRatePredictor as ep

filePath_spending = ""

spendingObj = sp.Spending(filePath_spending)



def main():

    data_file = "dataParse/BANKACCOUNTDATA.csv"
    analyzerba = ba(data_file)
    analyzerba.analyze()

    inf_file = "dataParse/predicted_yearly_inflation_rates.csv"
    current_income = 50000
    income_growth_rate = 3

    analyzeria = ia(inf_file, current_income, income_growth_rate)
    analyzeria.compare_income_to_inflation()

    # API Details
    API_URL = ''
    HISTORICAL_API_URL = ''
    BASE_CURRENCY = 'USD'
    TARGET_CURRENCY = 'EUR'
    API_KEY = ''

    # Initialize Predictor
    predictor = ep(
        api_url=HISTORICAL_API_URL,
        base_currency=BASE_CURRENCY,
        target_currency=TARGET_CURRENCY,
        api_key=API_KEY
    )

    #Current Exchange Rate
    current_rate = predictor.get_current_exchange_rate()
    print(f"Current Exchange Rate ({BASE_CURRENCY} to {TARGET_CURRENCY}): {current_rate}")

    # Fetch data
    start_date = '2022-01-01'
    end_date = '2024-01-01'

    predictor.get_historical_data(start_date=start_date, end_date=end_date)

    # Predict Exchange Rate
    periods = 30 # 30 days
    forecast = predictor.predict_exchange_rate(periods=periods)

    # Advice Exchange
    threshold = 1.0 # 1% Threshold
    exchange_type = 'buy' #or 'sell

    predictor.advise_on_exchange(threshold=threshold, exchange_type=exchange_type)

if __name__ == "__main__":
    
    main()
