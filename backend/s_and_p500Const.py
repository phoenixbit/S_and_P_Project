# Import the required libraries
from flask import Flask,  jsonify
from flask_cors import CORS
import yfinance as yf
import pandas as pd
import threading
import time
import requests
from bs4 import BeautifulSoup

# Function to scrape the S&P 500 P/E ratio from a specific website
def get_sp500_pe_ratio():
    url = "https://www.multpl.com/s-p-500-pe-ratio/table/by-month"  # URL to scrape data from
    response = requests.get(url)  # Send GET request to the URL
    soup = BeautifulSoup(response.text, 'html.parser')  # Parse the HTML content of the page
    pe_ratio_elements = soup.find_all('td', attrs={'class': 'right'})  # Find all <td> tags with class 'right'
    # Loop through all the elements found
    for pe_ratio_element in pe_ratio_elements:
        # If the 'estimate' keyword is found in the element text
        if "estimate" in pe_ratio_element.text:
            # Get the P/E ratio (remove 'estimate' and trim leading/trailing spaces)
            pe_ratio = pe_ratio_element.text.replace('estimate', '').strip()
            return pe_ratio  # Return the P/E ratio
    return "N/A"  # Return 'N/A' if no P/E ratio found

# Initialize the Flask application
app = Flask(__name__)
CORS(app)

# Define the S&P 500 constituents
sp500_constituents = ["AAPL", "MSFT", "AMZN", "META", "GOOG", "GOOGL", "BRK-B", "JNJ", "V", "PG"]

# A class to manage the data update process
class DataUpdater:
    # Constructor takes the list of tickers to track
    def __init__(self, tickers):
        self.tickers = tickers
        self.data = []  # List to store data
        self.sp500_pe = "N/A"  # Variable to store S&P 500 P/E ratio

    # Function to update the data
    def update(self):
        while True:  # Run indefinitely
            self.data.clear()  # Clear the existing data
            # Loop through all the tickers
            for ticker in self.tickers:
                yf_ticker = yf.Ticker(ticker)  # Get the ticker data from yfinance
                info = yf_ticker.info  # Get the ticker information
                pe_ratio = info.get("trailingPE", "N/A")  # Get the P/E ratio
                self.data.append([ticker, pe_ratio])  # Add the ticker and P/E ratio to the data list
            self.sp500_pe = get_sp500_pe_ratio()  # Update the S&P 500 P/E ratio
            time.sleep(60)  # Wait for 60 seconds

# Initialize the data updater
data_updater = DataUpdater(sp500_constituents)

# Define the route for the home page
@app.route('/data')
def data():
    return jsonify({'data': data_updater.data, 'sp500_pe': data_updater.sp500_pe})
#
# Main execution
if __name__ == '__main__':
    # Start the data updater in a separate thread
    update_thread = threading.Thread(target=data_updater.update)
    update_thread.start()
    # Start the Flask application
    app.run(debug=True)
