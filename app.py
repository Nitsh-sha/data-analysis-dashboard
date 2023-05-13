import pandas as pd
import plotly.express as px
import streamlit as st

# Set page title
st.set_page_config(page_title="Hotel Booking Analysis")

# Display the title
st.title("Hotel Bookings Analysis")

# Introduction
st.write("To perform an exploratory data analysis on the hotel booking data, we will work through the following steps:")

# Step 1: Load the data
st.header("Step 1: Load the Data")
st.write("We start by loading the hotel booking data into a pandas DataFrame using the provided data URL.")

# Step 2: Understand the variables in the data
st.header("Step 2: Understand the Variables")
st.write("We examine the variables present in the dataset to get a better understanding of the information available.")

# Step 3: Clean the data if necessary
st.header("Step 3: Clean the Data")
st.write("If there are any missing values, outliers, or inconsistencies in the data, we will perform data cleaning to ensure data quality.")

# Step 4: Analyze the data
st.header("Step 4: Analyze the Data")
st.write("We will use various descriptive statistics, visualizations, and other techniques to gain insights from the data. This may include histograms, scatter plots, and summary statistics.")
st.write("By following these steps, we can gain valuable insights into the hotel booking data and make informed decisions based on the analysis.")

# Load data from CSV
df = pd.read_csv("hotel_booking.csv")

# Display the first few rows of the DataFrame
st.write("First few rows of the dataset:")
st.dataframe(df.head())

# Filter the data for specific month(s)
selected_months = st.multiselect("Select Month(s)", options=df["arrival_date_month"].unique(), key="months_filter")

# Filter the data for specific hotel type(s)
selected_hotels = st.multiselect("Select Hotel Types", options=df["hotel"].unique(), key="hotel_types_filter")

# Filter the DataFrame based on the selected filters
filtered_df = df[
    (df["arrival_date_month"].isin(selected_months)) &
    (df["hotel"].isin(selected_hotels))
] if selected_months or selected_hotels else df

# Display the filtered data
st.write("Filtered Data:")
st.dataframe(filtered_df)

# Checkbox to toggle the display of data description
show_data_description = st.checkbox("Show Data Description")
if show_data_description:
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

st.header("Histogram of lead time to see the distribution of booking lead times")
# Create a histogram of lead time to see the distribution of booking lead times
# Checkbox to modify the lead time histogram
show_cumulative = st.checkbox("Show Cumulative Histogram")
fig1 = px.histogram(df, x="lead_time", nbins=50, title="Distribution of Booking Lead Time", cumulative=show_cumulative)
st.plotly_chart(fig1)

# Explanation for the histogram
st.write("The histogram of lead time represents the distribution of booking lead times in the dataset. It provides insights into how far in advance bookings are made before the actual arrival date.")

st.write("- The majority of bookings have a lead time ranging from around 0 to 200 days. This indicates that most customers make their bookings within this timeframe before the arrival date.")
st.write("- There is a peak in the histogram around the 0 to 50 days lead time range, suggesting a significant number of bookings are made relatively close to the arrival date.")
st.write("- As the lead time increases beyond 200 days, the frequency of bookings decreases, indicating that fewer customers make bookings well in advance.")
st.write("- The histogram shows a somewhat right-skewed distribution, with a longer tail on the right side. This indicates that there are relatively fewer bookings with very long lead times, but there are still some bookings made several hundred days in advance.")

st.header("Histogram: ADR distribution, faceted by arrival month")
# Histogram: ADR distribution, faceted by arrival month
# Add an interactive filter for arrival month
selected_months = st.multiselect("Filter by Arrival Month", options=df['arrival_date_month'].unique(), key="arrival_month_filter")

# Filter the DataFrame based on the selected arrival months
filtered_df = df[df['arrival_date_month'].isin(selected_months)] if selected_months else df

# Create a histogram of ADR distribution
fig_month = px.histogram(filtered_df, x='adr', color='arrival_date_month', nbins=50,
                   facet_col='arrival_date_month', facet_col_wrap=4,
                   title='ADR Distribution by Arrival Month', labels={'adr': 'Average Daily Rate (ADR)'})

# Display the histogram
st.plotly_chart(fig_month, use_container_width=True)

# Explanation for the histogram
st.write("The histogram represents the distribution of Average Daily Rate (ADR) values, segmented by the arrival month. It provides insights into the variation in ADR across different months.")

st.write("- After analyzing the histograms representing ADR (Average Daily Rate) for different arrival months, it becomes evident that ADR values are notably elevated during July and August, whereas they significantly decrease from November to January, revealing distinct seasonal trends.")
st.write("- This analysis indicates a surge in hotel bookings during the summer months, while the winter months experience a substantial decline in reservations.")


st.header("Histogram: Lead Time distribution, faceted by hotel type")

# Add an interactive filter for hotel type
selected_hotels = st.multiselect("Filter by Hotel Type", options=df['hotel'].unique())

# Filter the DataFrame based on the selected hotel types
filtered_df = df[df['hotel'].isin(selected_hotels)] if selected_hotels else df

# Create a histogram of lead time distribution
fig3 = px.histogram(filtered_df, x='lead_time', color='hotel', nbins=50, facet_col='hotel',
                    title='Lead Time Distribution by Hotel Type', labels={'lead_time': 'Lead Time'})

# Display the histogram
st.plotly_chart(fig3)

# Explanation for the histogram
st.write("From the histogram, we can observe the following:")
st.write("- The lead time distribution for the 'Resort Hotel' appears to be skewed towards shorter lead times, with a peak around 0-60 days. This suggests that many bookings for the resort hotel are made relatively close to the arrival date.")
st.write("- In contrast, the lead time distribution for the 'City Hotel' shows a wider spread and a higher frequency of longer lead times. This indicates that bookings for the city hotel are made well in advance, with a significant number of reservations made several months before the arrival date.")
st.write("- By comparing the two hotel types, we can see that the lead time distribution differs, reflecting the unique characteristics and booking patterns associated with each hotel.")


st.header("Scatter plot: Lead Time vs. ADR with separate colors for city hotel and resort hotel")
# Scatter plot: Lead Time vs. ADR
# Filter the data for specific month(s)
selected_months = st.multiselect("Select Month(s)", df["arrival_date_month"].unique())

# Filter the data for specific hotel type(s)
selected_hotels = st.multiselect("Select Hotel Types", df["hotel"].unique())

# Filter the DataFrame based on the selected hotel types
filtered_df = df[df['hotel'].isin(selected_hotels)] if selected_hotels else df

# Filter the DataFrame based on the selected arrival months
filtered_df = filtered_df[filtered_df['arrival_date_month'].isin(selected_months)] if selected_months else filtered_df

# Scatter plot: Lead Time vs. ADR
fig4 = px.scatter(filtered_df, x='lead_time', y='adr', color='hotel',
                  title='Lead Time vs. ADR', labels={'lead_time': 'Lead Time', 'adr': 'ADR'},
                  hover_data=['hotel'])

# Display the scatter plot
st.plotly_chart(fig4, use_container_width=True)

# Explanation for the scatter plot
st.write("The scatter plot visualizes the relationship between lead time (x-axis) and ADR (y-axis). Each point in the plot represents a booking record, with its position determined by the corresponding lead time and ADR values.")

st.write("From the scatter plot, we can observe the following:")
st.write("- There is a wide range of lead time values, ranging from 0 to around 700 days, and ADR values, ranging from around 0 to 5400.")
st.write("- There is no clear linear relationship between lead time and ADR.")

st.write("However, we can notice some clustering patterns:")
st.write("- The majority of bookings have relatively shorter lead times (below 200 days) and ADR values below 1000.")
st.write("- There are also some bookings with longer lead times (above 200 days) and higher ADR values, but these are relatively fewer in number.")


st.header("Scatter plot: Total Guests vs. Stays in Week Nights")
# Scatter plot: Total Guests vs. Stays in Week Nights
show_scatter_plot = st.checkbox("Show Scatter Plot: Total Guests vs. Stays in Week Nights")

if show_scatter_plot:
    fig5 = px.scatter(df, x='total_guests', y='stays_in_week_nights',
                      title='Total Guests vs. Stays in Week Nights',
                      labels={'total_guests': 'Total Guests', 'stays_in_week_nights': 'Stays in Week Nights'})
    st.plotly_chart(fig5)

# Explanation for the scatter plot
st.write("The scatter plot visualizes the relationship between the total number of guests (x-axis) and the number of stays in week nights (y-axis). Each point in the plot represents a booking record, with its position determined by the corresponding total guests and stays in week nights values.")

st.write("From the scatter plot, we can observe the following:")
st.write("- There is a wide range of values for both total guests and stays in week nights.")
st.write("- The majority of bookings have a total guest count of 1 to 4 and stays in week nights ranging from 0 to 10.")
st.write("- There are some bookings with a higher number of guests and longer stays, but these are relatively fewer in number.")

st.header("Conclusion")

st.write("Based on the analysis of the provided data and visualizations, we can draw the following business conclusions and make assumptions about booking behavior:")

st.subheader("Booking Behavior Assumptions:")
st.write("- Customers tend to make bookings relatively close to their planned arrival dates, as indicated by the lead time distribution histogram. This suggests that many bookings are made on short notice or within a few months of the intended stay.")
st.write("- The ADR distribution by arrival month shows some variation, implying that customers may consider factors such as seasonal demand, events, or hotel promotions when making their bookings.")
st.write("- The lead time distribution for different hotel types (Resort Hotel and City Hotel) is similar, indicating that customers follow similar booking patterns regardless of the hotel type they choose.")

st.subheader("Business Conclusions:")
st.write("- Pricing strategies: The ADR distribution by arrival month can help inform pricing strategies. Hotels can adjust their rates based on seasonal demand, higher ADR months, and lower ADR months to optimize revenue.")
st.write("- Resource allocation: Understanding the lead time distribution can assist in resource planning and allocation. Hotels can adjust staffing levels and inventory management based on anticipated booking patterns, ensuring optimal resource utilization.")
st.write("- Marketing and promotions: The analysis of booking behavior can guide marketing efforts and promotional campaigns. For example, hotels can target customers with last-minute deals or offer early bird discounts to capture bookings with shorter lead times.")
st.write("- Capacity planning: The scatter plot of total guests vs. stays in week nights provides insights into booking patterns related to guest count and duration of stays. Hotels can use this information to forecast demand, manage capacity, and plan for peak periods.")