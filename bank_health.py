import pandas as pd
import matplotlib.pyplot as plt

class BankAccountAnalyzer:

    def __init__(self, data_file):
        self.data_file = data_file
        self.df = None
        self.merged_df = None
        self.first_account_no = None
        self.bank_status = None

    def load_data(self):
        
        # Read the CSV file
        self.df = pd.read_csv(self.data_file)
        
        # Convert 'DATE' column to datetime
        self.df['date of transaction'] = pd.to_datetime(self.df['date of transaction'])
        
        # Replace commas in the amounts and convert them to numeric
        self.df['deposits'] = pd.to_numeric(
            self.df['deposits'].astype(str).str.replace(',', ''), errors='coerce'
        )
        self.df['withdrawals'] = pd.to_numeric(
            self.df['withdrawals'].astype(str).str.replace(',', ''), errors='coerce'
        )

    def process_data(self):
        
        # Extract the first Account No
        self.first_account_no = self.df['account number'].iloc[0]
        
        # Filter the data for the first account number
        df_filtered = self.df[self.df['account number'] == self.first_account_no]
        
        # Extract income and spending data
        income_data = df_filtered[['date of transaction', 'deposits']].dropna().copy()
        spending_data = df_filtered[['date of transaction', 'withdrawals']].dropna().copy()
        
        # Group the data by month and sum the amounts
        income_data['YearMonth'] = income_data['date of transaction'].dt.to_period('M')
        spending_data['YearMonth'] = spending_data['date of transaction'].dt.to_period('M')
        
        # Sum income and spending for each month
        monthly_income = income_data.groupby('YearMonth')['deposits'].sum().tail(60)
        monthly_spending = spending_data.groupby('YearMonth')['withdrawals'].sum().tail(60)
        
        # Create a DataFrame from the monthly income and spending
        self.merged_df = pd.DataFrame({
            'Income': monthly_income,
            'Spending': monthly_spending
        }).fillna(0)
        
        # Calculate net savings for each month
        self.merged_df['Net Savings'] = self.merged_df['Income'] - self.merged_df['Spending']

    def calculate_totals_and_status(self):

        # Calculate totals
        total_income = self.merged_df['Income'].sum()
        total_spending = self.merged_df['Spending'].sum()
        total_net_savings = total_income - total_spending
        
        # Determine the bank's status
        if total_net_savings > 100:
            self.bank_status = 'Well Off!'
        elif total_net_savings > 0:
            self.bank_status = 'Healthy'
        else:
            self.bank_status = 'Unhealthy'

    def plot_data(self):

        # Plots data
        plt.figure(figsize=(12, 6))
        plt.plot(self.merged_df.index.astype(str), self.merged_df['Income'], label='Income', color='green')
        plt.plot(self.merged_df.index.astype(str), self.merged_df['Spending'], label='Spending', color='red')
        plt.plot(self.merged_df.index.astype(str), self.merged_df['Net Savings'], label='Net Savings', color='blue')
        
        # Add text with bank status to the plot
        plt.text(0.05, 0.95, f"Bank Status: {self.bank_status}",
                 transform=plt.gca().transAxes, fontsize=12, verticalalignment='top',
                 bbox=dict(facecolor='white', alpha=0.5))
        
        plt.xlabel('Year-Month')
        plt.ylabel('Amount ($)')
        plt.title(f'Spending vs Income Over the Last 60 Months for Account No: {self.first_account_no}')
        plt.legend()
        plt.grid(True)
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

    def analyze(self):
        # Runs the full analysis pipeline
        self.load_data()
        self.process_data()
        self.calculate_totals_and_status()
        self.plot_data()
