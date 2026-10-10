from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

plt.style.use("seaborn-v0_8")

st.title("California Housing Data (1990) by Tianwei Lu")

# Read housing.csv from the same folder as this script.
df = pd.read_csv(Path(__file__).with_name("housing.csv"))

house_value_filter = st.slider(
    "Minimal Median House Value",
    min_value=0,
    max_value=500001,
    value=200000,
)

st.subheader("See more filters in the sidebar:")

location_types = df["ocean_proximity"].unique().tolist()
location_filter = st.sidebar.multiselect(
    "Choose the location type",
    options=location_types,
    default=location_types,
)

income_filter = st.sidebar.radio(
    "Choose income level",
    options=["Low", "Medium", "High"],
)

# Apply the price and location filters, then the selected income range.
df = df[df["median_house_value"] >= house_value_filter]
df = df[df["ocean_proximity"].isin(location_filter)]

# median_income is measured in tens of thousands of US dollars.
if income_filter == "Low":
    df = df[df["median_income"] <= 2.5]
elif income_filter == "Medium":
    df = df[(df["median_income"] > 2.5) & (df["median_income"] < 4.5)]
else:
    df = df[df["median_income"] >= 4.5]

if df.empty:
    st.info("No districts match these filters. Adjust the filters to see data.")

# Show the locations of the filtered districts.
st.map(df[["latitude", "longitude"]])

# Show a 30-bin histogram below the map.
st.subheader("Median House Value Distribution")
fig, ax = plt.subplots(figsize=(10, 5))
ax.hist(df["median_house_value"], bins=30, edgecolor="white")
ax.set_xlabel("Median House Value (US dollars)")
ax.set_ylabel("Number of Districts")
st.pyplot(fig)
plt.close(fig)
