import pandas as pd

class Inflation:

    dataBase = pd.DataFrame

    #CONSTRUCTOR
    def __init__(self, file):
        self.dataBase = pd.read_csv(file)

    #Prints the first 5 rows of the data base
    def printRow5(self):
        self.dataBase.head()

    #print (row, col)
    def findSize(self):
        print(self.dataBase.shape)
