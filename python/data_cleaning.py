import pandas as pd

df = pd.read_csv("../data/OLA_DataSet.csv")

df.drop(columns=["Unnamed: 20"], inplace=True)

df["Driver_Rating"] = pd.to_numeric(df["Driver_Rating"], errors="coerce")
df["Customer_Rating"] = pd.to_numeric(df["Customer_Rating"], errors="coerce")

df.to_csv("../data/OLA_Cleaned_Data.csv", index=False)
print("Cleaned data saved")
