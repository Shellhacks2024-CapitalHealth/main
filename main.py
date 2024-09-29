import spending as sp
import pandas as pd
import matplotlib.pyplot as plt

filePath_spending = ""

spendingObj = sp.Spending(filePath_spending)


# Function to track spending vs income over 60 months for the first Account No
def track_spending_vs_income(data_file):
    
    # Read the csv file
    df = pd.read_csv(data_file)

    # Convert 'DATE' column to datetime
    df['DATE'] = pd.to_datetime(df['DATE'])

    # Replace commas in the amounts and convert them to numeric
    df['DEPOSIT AMT'] = pd.to_numeric(df['DEPOSIT AMT'].str.replace(',', ''), errors='coerce')
    df['WITHDRAWAL AMT'] = pd.to_numeric(df['WITHDRAWAL AMT'].str.replace(',', ''), errors='coerce')

    # Extract the first Account No
    first_account_no = df['Account No'].iloc[0]

    # Filter the data to only use transactions for the first account number
    df_filtered = df[df['Account No'] == first_account_no]

    # Extract income (Deposit) and spending (Withdrawal) data for the first account
    income_data = df_filtered[['DATE', 'DEPOSIT AMT']].dropna().copy()
    spending_data = df_filtered[['DATE', 'WITHDRAWAL AMT']].dropna().copy()

    # Group the data by month and year, summing the amounts
    income_data['YearMonth'] = income_data['DATE'].dt.to_period('M')
    spending_data['YearMonth'] = spending_data['DATE'].dt.to_period('M')

    # Sum income and spending for each month
    monthly_income = income_data.groupby('YearMonth')['DEPOSIT AMT'].sum().tail(60)
    monthly_spending = spending_data.groupby('YearMonth')['WITHDRAWAL AMT'].sum().tail(60)

    # Create a DataFrame from the monthly income and spending
    merged_df = pd.DataFrame({
        'Income': monthly_income,
        'Spending': monthly_spending
    }).fillna(0)

    # Calculate net savings for each month
    merged_df['Net Savings'] = merged_df['Income'] - merged_df['Spending']

    # Calculate total income, spending, and net savings
    total_income = merged_df['Income'].sum()
    total_spending = merged_df['Spending'].sum()
    total_net_savings = total_income - total_spending

    # Determine the bank's status
    if total_net_savings > 0 and total_net_savings < 100:
        bank_status = 'Healthy'
    elif total_net_savings > 100:
        bank_status = 'Well Off!'
    else:
        bank_status = 'Unhealthy'

    # Plot income, spending, and net savings for the last 60 months
    plt.figure(figsize=(12, 6))
    plt.plot(merged_df.index.astype(str), merged_df['Income'], label='Income', color='green')
    plt.plot(merged_df.index.astype(str), merged_df['Spending'], label='Spending', color='red')
    plt.plot(merged_df.index.astype(str), merged_df['Net Savings'], label='Net Savings', color='blue')

    # Add text with bank status to the plot
    plt.text(0.05, 0.95, f"Bank Status: {bank_status}",
             transform=plt.gca().transAxes, fontsize=12, verticalalignment='top',
             bbox=dict(facecolor='white', alpha=0.5))

    plt.xlabel('Year-Month')
    plt.ylabel('Amount ($)')
    plt.title(f'Spending vs Income Over the Last 60 Months for Account No: {first_account_no}')
    plt.legend()
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.show()


def compare_income_to_inflation(csv_file, current_income, income_growth_rate):

    # Read the inflation rates from the CSV file
    df_inflation = pd.read_csv(csv_file)

    # Iterate over each year and compare income growth to inflation rate
    for index, row in df_inflation.iterrows():
        year = row['Year']
        inflation_rate = row['Predicted Yearly Inflation Rate (%)']
        
        # Calculate income for that year based on the growth rate
        new_income = current_income * (1 + income_growth_rate / 100) ** (index + 1)

        # Compare income growth to inflation
        if income_growth_rate >= inflation_rate:
            status = "Good Financial Position"
        else:
            status = "Not in a Good Financial Position"

        # Output the result for that year
        print(f"Year: {year}, Inflation Rate: {inflation_rate}%, Income: ${new_income:.2f}, Status: {status}")


# Function to get exchange rates from a public API
def get_exchange_rates(api_url, base_currency, target_currency, api_key):
    url = f"{api_url}?base={base_currency}&symbols={target_currency}&access_key={api_key}"
    response = requests.get(url)
    data = response.json()
    return data['rates'][target_currency]

# Function to predict future exchange rates using Prophet
def predict_exchange_rate(data, periods):
    df = pd.DataFrame(data, columns=['ds', 'y'])  # ds: date, y: exchange rate
    model = Prophet()
    model.fit(df)
    
    # Make future predictions
    future = model.make_future_dataframe(periods=periods)
    forecast = model.predict(future)
    
    # Plot the forecast
    model.plot(forecast)
    plt.show()
    
    return forecast[['ds', 'yhat']]

# Function to advise whether to buy or sell based on predicted rates
def advise_on_exchange(forecast, current_rate, threshold, exchange_type):
    for i, row in forecast.iterrows():
        predicted_rate = row['yhat']
        date = row['ds']
        
        # Calculate the percentage change from the current rate
        percentage_change = ((predicted_rate - current_rate) / current_rate) * 100
        
        # Advice based on whether you're buying or selling
        if exchange_type == 'buy':
            # For buying, lower predicted rates are better
            if percentage_change <= -threshold:
                advice = f"Good time to buy on {date.date()} with predicted rate: {predicted_rate:.2f}"
            else:
                advice = f"Wait to buy, predicted rate on {date.date()} is {predicted_rate:.2f}"
        elif exchange_type == 'sell':
            # For selling, higher predicted rates are better
            if percentage_change >= threshold:
                advice = f"Good time to sell on {date.date()} with predicted rate: {predicted_rate:.2f}"
            else:
                advice = f"Wait to sell, predicted rate on {date.date()} is {predicted_rate:.2f}"
        else:
            raise ValueError("Invalid exchange_type. Please choose 'buy' or 'sell'.")
        
        print(advice)

def main():

    data_file = "dataParse/BANKACCOUNTDATA.csv"

    track_spending_vs_income(data_file)

if __name__ == "__main__":
    main()
    