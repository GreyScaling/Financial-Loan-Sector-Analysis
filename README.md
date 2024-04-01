# Financial Loan Sector Analysis

This project performs web scraping, sentiment analysis, and topic modeling on the financial loan market based on a few sectors. It also includes an interactive dashboard to visualize the findings.

## Features

- **Web Scraping:** Uses `Selenium` to scrape data from the financial loan market for specific sectors.
- **Sentiment Analysis:** Uses models from Hugging Face's `transformers` library to analyze the sentiment of the scraped data and understand the market sentiment for each sector.
- **Topic Modeling:** This documentation provides an overview of the topic modeling pipeline implemented for analyzing a collection of documents. The pipeline includes data preprocessing, tokenization, phrase modeling, dictionary and corpus creation, topic modeling using Latent Dirichlet Allocation (LDA), and visualization of the results.
- **Interactive Dashboard:** Uses `Streamlit` to create an interactive dashboard that visualizes the results of the sentiment analysis and topic modeling.

## Installation

1. Clone this repository.
  ```bash
  git clone https://github.com/GreyScaling/Financial-Loan-Sector-Analysis/
  ```
   
2. Install the required packages:
  ```bash
  pip install -r requirements.txt
  ```

## Running the Dashboard

Follow these steps to view the interactive dashboard:

1. Open your terminal.

2. Navigate to the `dashboard` directory:

 ```bash
 cd dashboard
 ```
3. Run the streamlit app :
  ```bash
  streamlit run app.py
  ```


