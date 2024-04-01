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

A live demo can be found at: https://financial-loan-sector-analysis.streamlit.app/


## Documentation

1. Web Scraping
- Process:
Scrapers located in the scrapers folder are used to collect data.
Each scraper generates a CSV file within its respective folder.
- Manual Intervention:
The generated CSVs are manually copied and pasted into the csvs folder.
- Justification:
This manual step prevents accidental overwriting of working data in case of scraping errors that might create empty CSVs.

2. Sentiment Analysis
- Process: <br>
The sentiment analysis script reads all CSV files within the csvs folder.It performs sentiment analysis on the concatinated data using various models.Outputs are generated for each model and saved within the sentiment_analysis folder. 
    - Outputs are:
        - combined_sentiments.csv
        - financial_sentiments.csv
        - finbert_sentiments.csv
        - sigma_sentiments.csv
        - soleimanian_sentiments.csv
        - yiyanghost_sentiments.csv
- Manual Intervention:
The generated CSVs are manually copied and pasted into the dashboard/csvs folder.
- Justification:
This manual step prevents accidental overwriting of working data in case of  errors that might create empty CSVs.

3. Topic Modeling
Process:
The topic modeling script reads all CSV files within the csvs folder.
It performs topic modeling on each file, creating 19 models with varying numbers of topics (2 to 20).
Each model generates an HTML dashboard file showcasing the identified topics.
Additionally, the script calculates coherence scores for each model and creates a plot visualization.
All outputs (HTML dashboards, coherence score plots) are saved within the topic_modeling folder.
- Manual Intervention:
The generated CSVs are manually copied and pasted into the dashboard/assets folder.
- Justification:
This manual step allows the user to try different pre-processing steps/changes in the algorithm that would affect the topics without affecting the files meant for the dashboard

4. Data Visualization Dashboard
Process:
The dashboard script reads the data files from the dashboard folder, specifically:
CSV files located in the csvs subfolder (presumably containing sentiment analysis results).
HTML file located in the assets subfolder (likely the topic modeling dashboard).
Coherence score plot also located in the assets subfolder.
Based on the read data, the script generates visualizations for the dashboard.
