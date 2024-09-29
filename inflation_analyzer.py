import pandas as pd

class IncomeInflationAnalyzer:
    def __init__(self, csv_file, current_income, income_growth_rate):
        # Initialize analyzer with data
        self.csv_file = csv_file
        self.current_income = current_income
        self.income_growth_rate = income_growth_rate
        self.df_inflation = None

    def load_inflation_data(self):
        # Loads inflation data
        self.df_inflation = pd.read_csv(self.csv_file)

    def compare_income_to_inflation(self):
        
       #Financial Status Predictor
        if self.df_inflation is None:
            self.load_inflation_data()

        # Iterate over each year and compare income growth to inflation rate
        for index, row in self.df_inflation.iterrows():
            year = row['Year']
            inflation_rate = row['Predicted Yearly Inflation Rate (%)']
            
            # Calculate income for that year based on the growth rate
            new_income = self.current_income * (1 + self.income_growth_rate / 100) ** (index + 1)

            # Compare income growth to inflation
            if self.income_growth_rate >= inflation_rate:
                status = "Good Financial Position"
            else:
                status = "Not in a Good Financial Position"

            # Output the result for that year
            print(f"Year: {year}, Inflation Rate: {inflation_rate}%, Income: ${new_income:.2f}, Status: {status}")
