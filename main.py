import pandas as pd
import matplotlib.pyplot as plt
from bank_health import BankAccountAnalyzer as ba
from inflation_analyzer import IncomeInflationAnalyzer as ia
from exchange_predictor import ExchangeRatePredictor as ep
from genAI import GANBankAccountGenerator as gA
from matplotlib.ticker import FuncFormatter
import numpy as np

def main():

    #DEFINE IncomeInflationAnalyzer
    current_income = 50000
    income_growth_rate = 3
    analyzeria = ia("main/dataParse/predicted_yearly_inflation_rates.csv", current_income, income_growth_rate)
    analyzeria.compare_income_to_inflation()

    gan = gA("main/account_transactions.csv")
    gan.train_gan(epochs=100)
    generated_samples = gan.generate_samples(num_samples=10)
   
    row_sums = np.sum(generated_samples, axis=1)
    sums_list = row_sums.tolist()
    
    # Create a DataFrame with appropriate column names
    columns = ['Net Savings']
    df = pd.DataFrame(sums_list, columns=columns)
    
    # Create a multiplication factor that gradually increases from 1000 to 10000 over 20 rows
    multiplication_factors = np.linspace(100000, 100000, num=df.shape[0])

    # Multiply each row by the corresponding factor
    sums_list = sums_list * multiplication_factors[:, np.newaxis]

    # Generate date index for the DataFrame
    dates = pd.date_range(start='2020-01-01', periods=df.shape[0], freq='M')
    df.index = dates

    # Bank status and account number for annotation
    bank_status = 'Active'
    first_account_no = '12345678'

    #DEFINE BankAccountAnalyzer object
    analyzerba = ba("main/account_transactions.csv")
    analyzerba.analyze()

    def thousands_formatter(x, pos):
        return f'{int(x)}000'

    # Plotting
    plt.figure(figsize=(12, 6))
    plt.plot(df.index.astype(str), df['Net Savings'], label='Net Savings', color='blue')
    plt.xlabel('Year-Month')
    plt.ylabel('Amount ($)')
    plt.gca().yaxis.set_major_formatter(FuncFormatter(thousands_formatter))
    plt.title(f'Average Savings Over the Last {df.shape[0]} Months')
    plt.legend()
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()





    # API Details
    API_URL = 'https://api.freecurrencyapi.com/v1/latest?apikey=fca_live_eAA9CEzxMLy2FTcVwuCTXFZqThCY3o23qiYPNqJ5&currencies=EUR%2CUSD%2CCAD'
    HISTORICAL_API_URL = 'https://api.exchangeratesapi.io/v1/2013-12-24'
    BASE_CURRENCY = 'USD'
    TARGET_CURRENCY = 'CAD'
    API_KEY = '3ea93938bd2a266999351bddd2e43524'

    # Initialize Predictor
    predictor = ep(
        api_url=API_URL,
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

