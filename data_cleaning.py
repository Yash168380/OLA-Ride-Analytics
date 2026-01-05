import pandas as pd

# Load dataset
df = pd.read_csv("data/OLA_DataSet.csv")

# 1️⃣ Drop unwanted column
if "Unnamed: 20" in df.columns:
    df.drop(columns=["Unnamed: 20"], inplace=True)

# 2️⃣ Convert Date column to datetime
df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

# 3️⃣ Fill missing numeric values with median
num_cols = ["V_TAT", "C_TAT", "Driver_Ratings", "Customer_Rating"]
for col in num_cols:
    df[col] = df[col].fillna(df[col].median())

# 4️⃣ Fill missing categorical values
cat_cols = [
    "Payment_Method",
    "Canceled_Rides_by_Customer",
    "Canceled_Rides_by_Driver",
    "Incomplete_Rides",
    "Incomplete_Rides_Reason"
]
for col in cat_cols:
    df[col] = df[col].fillna("Not Available")

# 5️⃣ Save cleaned data
df.to_csv("data/OLA_Cleaned_Data.csv", index=False)

print("✅ Data Cleaning Completed & File Saved")
