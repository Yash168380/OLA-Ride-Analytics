import pandas as pd

df = pd.read_csv("data/OLA_DataSet.csv")

print(df.head())
print(df.info())
print(df.isnull().sum())
