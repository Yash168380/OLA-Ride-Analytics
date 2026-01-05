import pandas as pd

# Load cleaned data
df = pd.read_csv("../data/OLA_Cleaned_Data.csv")

# Basic KPIs
print("Total Rides:", len(df))
print("Total Revenue:", df["Booking_Value"].sum())
print("Average Ride Distance:", df["Ride_Distance"].mean())

# Booking Status distribution
print("\nBooking Status Count:")
print(df["Booking_Status"].value_counts())

# Vehicle type distribution
print("\nVehicle Type Count:")
print(df["Vehicle_Type"].value_counts())

# Average rating
print("\nAverage Driver Rating:", df["Driver_Ratings"].mean())
print("Average Customer Rating:", df["Customer_Rating"].mean())
