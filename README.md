# data-analysis-dashboard

https://hotel-booking-layd.onrender.com/

# Hotel Booking Analysis Application

This is a Streamlit application for analyzing hotel booking data. The application provides visualizations and insights based on the dataset.

## Installation

To run the application locally, please follow these steps:

1. Clone the repository:
   git clone https://github.com/Nitsh-sha/data-analysis-dashboard.git

2. Install the required dependencies:
   pip install -r requirements.txt

3. Run the Streamlit app:
   streamlit run app.py

This will start the application, and you can access it by opening the provided URL in your web browser.

## Usage

Once the application is running, you will see the following features:

- The first few rows of the dataset: This section displays the initial records of the dataset.

- Data description: This section provides statistical information about the dataset.

- Distribution of Booking Lead Time: This histogram shows the distribution of lead time for hotel bookings.

- ADR Distribution by Arrival Month: This histogram displays the average daily rate (ADR) distribution by arrival month.

- Lead Time Distribution by Hotel Type: This histogram shows the lead time distribution categorized by hotel type.

- Lead Time vs. ADR: This scatter plot visualizes the relationship between lead time and ADR.

- Total Guests vs. Stays in Week Nights: This scatter plot represents the relationship between the total number of guests and the number of stays in week nights.

## Data

The application uses the "hotel_booking.csv" dataset for analysis. The dataset contains information about hotel bookings, including guest details, booking dates, room types, and more.

## Dependencies

The application relies on the following libraries:

- Pandas
- Plotly Express
- Plotly Graph Objects
- Streamlit

All the necessary dependencies are listed in the `requirements.txt` file.

## Contributing

Contributions to this project are welcome! If you encounter any issues or have suggestions for improvements, please open an issue or submit a pull request.

## References
Hotel dataset from:
https://www.kaggle.com/datasets/mojtaba142/hotel-booking?select=hotel_booking.csv
