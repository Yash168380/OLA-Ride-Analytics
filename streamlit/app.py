import streamlit as st
import pandas as pd
import os

# -----------------------------
# Page Config
# -----------------------------
st.set_page_config(
    page_title="OLA Ride Analytics Dashboard",
    layout="wide"
)

# -----------------------------
# Load Data (SAFE PATH)
# -----------------------------
@st.cache_data
def load_data():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(base_dir, "..", "data", "OLA_Cleaned_Data.csv")
    return pd.read_csv(data_path)

try:
    df = load_data()
except Exception as e:
    st.error("❌ CSV file load nahi ho rahi")
    st.code(str(e))
    st.stop()

# -----------------------------
# Date Column FIX (IMPORTANT)
# -----------------------------
df["Date"] = pd.to_datetime(df["Date"])

# -----------------------------
# Sidebar Filters
# -----------------------------
st.sidebar.header("🔍 Filters")

vehicle_type = st.sidebar.selectbox(
    "Select Vehicle Type",
    ["All"] + sorted(df["Vehicle_Type"].dropna().unique())
)

booking_status = st.sidebar.selectbox(
    "Select Booking Status",
    ["All"] + sorted(df["Booking_Status"].dropna().unique())
)

city = st.sidebar.selectbox(
    "Select Pickup Location",
    ["All"] + sorted(df["Pickup_Location"].dropna().unique())
)

# -----------------------------
# Date Filter (ULTRA SAFE)
# -----------------------------
date_input = st.sidebar.date_input(
    "Select Date / Date Range",
    value=(df["Date"].min().date(), df["Date"].max().date())
)

# 🔒 HARD SAFE CONVERSION
if isinstance(date_input, (list, tuple)):
    if len(date_input) == 2:
        start_date = pd.to_datetime(date_input[0])
        end_date = pd.to_datetime(date_input[1])
    else:
        start_date = end_date = pd.to_datetime(date_input[0])
else:
    start_date = end_date = pd.to_datetime(date_input)

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
    (filtered_df["Date"] >= start_date) &
    (filtered_df["Date"] <= end_date)
]

# -----------------------------
# Dashboard Title
# -----------------------------
st.title("🚖 OLA Ride Analytics Dashboard")

# -----------------------------
# KPIs
# -----------------------------
c1, c2, c3, c4, c5 = st.columns(5)

c1.metric("Total Rides", f"{len(filtered_df):,}")
c2.metric("Total Revenue", f"₹ {filtered_df['Booking_Value'].sum():,.0f}")
c3.metric("Avg Distance (km)", f"{filtered_df['Ride_Distance'].mean():.2f}")
c4.metric("Avg Driver Rating", f"{filtered_df['Driver_Ratings'].mean():.2f}")
c5.metric("Avg Customer Rating", f"{filtered_df['Customer_Rating'].mean():.2f}")

# -----------------------------
# Charts
# -----------------------------
st.subheader("📊 Booking Status Distribution")
st.bar_chart(filtered_df["Booking_Status"].value_counts())

st.subheader("🚗 Vehicle Type Distribution")
st.bar_chart(filtered_df["Vehicle_Type"].value_counts())

st.subheader("📈 Revenue Trend Over Time")
st.line_chart(filtered_df.groupby("Date")["Booking_Value"].sum())

st.subheader("⭐ Driver Ratings Distribution")
st.bar_chart(filtered_df["Driver_Ratings"].value_counts().sort_index())

st.subheader("⭐ Customer Ratings Distribution")
st.bar_chart(filtered_df["Customer_Rating"].value_counts().sort_index())

# -----------------------------
# Footer
# -----------------------------
st.markdown("---")
st.markdown(
    "📌 **Project:** OLA Ride Analytics | **Tools:** Python, Pandas, Streamlit, Power BI"
)
