import streamlit as st
import pandas as pd

# -----------------------------
# Page Config
# -----------------------------
st.set_page_config(
    page_title="OLA Ride Analytics Dashboard",
    layout="wide"
)

# -----------------------------
# Load Cleaned Data
# -----------------------------
@st.cache_data
def load_data():
    return pd.read_csv("../data/OLA_Cleaned_Data.csv")

df = load_data()

# -----------------------------
# Sidebar Filters
# -----------------------------
st.sidebar.header("🔍 Filters")

# Vehicle Type Filter
vehicle_type = st.sidebar.selectbox(
    "Select Vehicle Type",
    ["All"] + sorted(df["Vehicle_Type"].unique())
)

# Booking Status Filter
booking_status = st.sidebar.selectbox(
    "Select Booking Status",
    ["All"] + sorted(df["Booking_Status"].unique())
)

# Pickup Location / City Filter
city = st.sidebar.selectbox(
    "Select Pickup Location",
    ["All"] + sorted(df["Pickup_Location"].unique())
)

# Date range filter
df["Date"] = pd.to_datetime(df["Date"])
min_date = df["Date"].min()
max_date = df["Date"].max()

date_range = st.sidebar.date_input(
    "Select Date Range",
    value=[min_date, max_date],
    min_value=min_date,
    max_value=max_date
)

# -----------------------------
# Handle single or range date input
# -----------------------------
if isinstance(date_range, list) or isinstance(date_range, tuple):
    if len(date_range) == 2:
        start_date, end_date = date_range
    else:
        start_date = end_date = date_range[0]
else:
    start_date = end_date = date_range

# -----------------------------
# Apply Filters
# -----------------------------
filtered_df = df.copy()
if vehicle_type != "All":
    filtered_df = filtered_df[filtered_df["Vehicle_Type"] == vehicle_type]
if booking_status != "All":
    filtered_df = filtered_df[filtered_df["Booking_Status"] == booking_status]
if city != "All":
    filtered_df = filtered_df[filtered_df["Pickup_Location"] == city]

filtered_df = filtered_df[
    (filtered_df["Date"] >= pd.to_datetime(start_date)) &
    (filtered_df["Date"] <= pd.to_datetime(end_date))
]

# -----------------------------
# Dashboard Title
# -----------------------------
st.title("🚖 OLA Ride Analytics Dashboard")

# -----------------------------
# KPI Metrics
# -----------------------------
col1, col2, col3, col4, col5 = st.columns(5)

total_rides = filtered_df.shape[0]
total_revenue = filtered_df["Booking_Value"].sum()
avg_distance = filtered_df["Ride_Distance"].mean()
avg_driver_rating = filtered_df["Driver_Ratings"].mean()
avg_customer_rating = filtered_df["Customer_Rating"].mean()

col1.metric("Total Rides", f"{total_rides/1000:.2f} K")
col2.metric("Total Revenue", f"₹ {total_revenue/1e6:.2f} M")
col3.metric("Avg Distance (km)", f"{avg_distance:.2f}")
col4.metric("Avg Driver Rating", f"{avg_driver_rating:.2f}")
col5.metric("Avg Customer Rating", f"{avg_customer_rating:.2f}")

# -----------------------------
# Booking Status Distribution
# -----------------------------
st.subheader("📊 Booking Status Distribution")
st.bar_chart(filtered_df["Booking_Status"].value_counts())

# -----------------------------
# Vehicle Type Distribution
# -----------------------------
st.subheader("🚗 Vehicle Type Distribution")
st.bar_chart(filtered_df["Vehicle_Type"].value_counts())

# -----------------------------
# Revenue Trend Over Time
# -----------------------------
st.subheader("📈 Revenue Trend Over Time")
revenue_trend = filtered_df.groupby("Date")["Booking_Value"].sum()
st.line_chart(revenue_trend)

# -----------------------------
# Driver Ratings Distribution
# -----------------------------
st.subheader("⭐ Driver Ratings Distribution")
st.bar_chart(filtered_df["Driver_Ratings"].value_counts().sort_index())

# -----------------------------
# Customer Ratings Distribution
# -----------------------------
st.subheader("⭐ Customer Ratings Distribution")
st.bar_chart(filtered_df["Customer_Rating"].value_counts().sort_index())

# -----------------------------
# Footer / Info
# -----------------------------
st.markdown("---")
st.markdown(
    "📌 **Project:** OLA Ride Analytics | **Tools:** Python, Pandas, Streamlit, Power BI"
)
