import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# Set page title
st.set_page_config(page_title="Hotel Booking Analysis")

# Load data from CSV
df = pd.read_csv("hotel_booking.csv")

# Display the first few rows of the DataFrame
st.write("First few rows of the dataset:")
st.dataframe(df.head())

# Describe the data
st.write("Data description:")
st.dataframe(df.describe())

# Fill missing values in the 'children' column with 0
df['children'].fillna(0, inplace=True)

# Fill missing values in the 'country' column with "Unknown"
df['country'].fillna('Unknown', inplace=True)

# Drop irrelevant columns
df.drop(['company', 'agent'], axis=1, inplace=True)

# Drop rows where 'adults' and 'children' are both 0
df = df.loc[(df['adults'] + df['children']) > 0]

# Create a new column 'total_guests' by summing 'adults', 'children', and 'babies'
df['total_guests'] = df['adults'] + df['children'] + df['babies']

# Drop the 'babies' column
df.drop('babies', axis=1, inplace=True)

# Convert categorical columns to category type
cat_columns = ['arrival_date_month', 'country', 'meal', 'market_segment', 'distribution_channel',
               'reserved_room_type', 'assigned_room_type', 'deposit_type', 'customer_type', 'reservation_status']
df[cat_columns] = df[cat_columns].astype('category')

# Convert 'reservation_status_date' to datetime
df['reservation_status_date'] = pd.to_datetime(df['reservation_status_date'])

# Drop additional irrelevant columns
df.drop(["name", "email", "phone-number", "credit_card"], axis=1, inplace=True)

# Remove negative values from "adr" column
df = df[df["adr"] > 0]

# Create a histogram of lead time to see the distribution of booking lead times
fig1 = px.histogram(df, x="lead_time", nbins=50, title="Distribution of Booking Lead Time")
st.plotly_chart(fig1)

# Histogram: ADR distribution, faceted by arrival month
fig2 = px.histogram(df, x='adr', color='arrival_date_month', nbins=50, facet_col='arrival_date_month',
                    facet_col_wrap=4, title='ADR Distribution by Arrival Month', labels={'adr': 'Average Daily Rate (ADR)'})
st.plotly_chart(fig2)

# Histogram: Lead Time distribution, faceted by hotel type
fig3 = px.histogram(df, x='lead_time', color='hotel', nbins=50, facet_col='hotel',
                    title='Lead Time Distribution by Hotel Type', labels={'lead_time': 'Lead Time'})
st.plotly_chart(fig3)

# Scatter plot: Lead Time vs. ADR
fig4 = px.scatter(df, x='lead_time', y='adr', title='Lead Time vs. ADR', labels={'lead_time': 'Lead Time', 'adr': 'ADR'})
st.plotly_chart(fig4)

# Scatter plot: Total Guests vs. Stays in Week Nights
fig5 = px.scatter(df, x='total_guests', y='stays_in_week_nights',
                  title='Total Guests vs. Stays in Week Nights',
                  labels={'total_guests': 'Total Guests', 'stays_in_week_nights': 'Stays in Week Nights'})
st.plotly_chart(fig5)