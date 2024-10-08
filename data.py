import pandas as pd


class dataFrame:
    dataBase = pd.DataFrame

    #CONSTRUCTOR
    def __init__(self, file):
        self.dataBase = pd.read_csv(file)

    #Prints the first 5 rows of the data base
    def printRow5(self):
        print(self.dataBase.head())

    #print (row, col)
    def findSize(self):
        print(self.dataBase.shape)

    #Returns number of columns
    def returnCols(self):
        return self.dataBase.columns
    
    #Get Data
    def getDataFrame(self):
        return self.dataBase