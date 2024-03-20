import streamlit as st
import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt
import os

from SentimentAnalysis import SentimentAnalysis


# emojis: https://www.webfx.com/tools/emoji-cheat-sheet/
st.set_page_config(
  page_title = 'Financial Loan Analysis Dashboard',
  layout = 'wide',
  initial_sidebar_state="expanded"
)


def main():
  sentimentAnalysis = SentimentAnalysis("Sentiment Analysis Dashboard")
  df, dfs = sentimentAnalysis.read_data()
  options, sector = sidebar(df)
  mainpage(sentimentAnalysis, options, sector, df, dfs)
  return None

def mainpage(sentimentAnalysis, options, sector, df, dfs):
  
  df_sector = df.query(
    "Sector == @sector"
  )
  
  st.title('Financial Loan Analysis Dashboard')
  st.write('This is the main page of the dashboard')
  
  st.text(df_sector)
  st.text(sector)
  
  if df_sector.empty:
    st.write('No data available for the selected sector')
  else:
    st.write(df_sector)
    st.write(type(df_sector))
    
  left_column, right_column = st.columns(2)
  if sector == 'All':
    with left_column:
      fig, ax = sentimentAnalysis.make_stacked_bar() # need to make it bigger 
      st.pyplot(fig)
    with right_column:
      pass
      
  return None

def sidebar(df : pd.DataFrame):
  st.sidebar.title('Loan Analysis')
  st.sidebar.header("Filter : ")
  
  options = st.sidebar.selectbox(
    'Select the option :',
    options = ['Sentiment Analysis', 'Topic Modeling']
  )
  
  sectors = df['Sector'].unique()
  sector = st.sidebar.selectbox(
    'Select the sector :',
    options = ['All'] + list(sectors)
  )
    
  return options, sector

def get_data():
  script_dir = os.path.dirname(__file__)
  rel_path = '/sentiment_analysis/combined_sentiments.csv'
  abs_file_path = os.path.join(script_dir, rel_path)
  df = pd.read_csv(abs_file_path, index_col=0)
  return df 

if __name__ == '__main__':
  main()


  
  
  
