import streamlit as st
import pandas as pd

from components.SentimentAnalysis import SentimentAnalysis
from components.TopicModelling import TopicModelling

# import imgkit
# config = imgkit.config(wkhtmltoimage='../wkhtmltoimage')
# imgkit.from_file('assets/topic_model_2_topics.html', 'output.jpg', config=config)


import streamlit.components.v1 as components

# Load the HTML content

from components.sentiment_components import *

st.set_page_config(
  page_title = 'Financial Loan Analysis Dashboard',
  layout = 'wide',
  initial_sidebar_state="expanded"
)



def mainpage(sentimentAnalysis, topicModeling, options, sector):
  """
  This function is responsible for displaying the main page of the dashboard based on the selected options.

  Parameters:
  - sentimentAnalysis (object): The sentiment analysis object.
  - topicModeling (object): The topic modeling object.
  - options (str): The selected option ('Sentiment Analysis' or 'Topic Modeling').
  - sector (str): The selected sector.

  Returns:
  None
  """
  if options == 'Sentiment Analysis':
    sentiment_analysis_page(sentimentAnalysis, sector)
      
  elif options == 'Topic Modeling':
    topic_modeling_page(topicModeling, sector)
  return None

def sidebar(df : pd.DataFrame):
  """
  This function creates a sidebar for the loan analysis dashboard.
  
  Parameters:
    df (pd.DataFrame): The DataFrame containing the loan data.
  
  Returns:
    tuple: A tuple containing the selected option and sector.
  """
  st.sidebar.title('Loan Analysis')
  st.sidebar.header("Filter : ")
  
  options = st.sidebar.selectbox(
    'Select the option :',
    options = ['Sentiment Analysis', 'Topic Modeling']
  )
  
  if options == 'Topic Modeling':
    return options, None
  
  sectors = df['Sector'].unique()
  sector = st.sidebar.selectbox(
    'Select the sector :',
    options = ['All'] + list(sectors)
  )
    
  return options, sector

def sentiment_analysis_page(sentimentAnalysis, sector):
  """
  Displays the sentiment analysis page with various visualization options.

  Parameters:
  - sentimentAnalysis (object): The sentiment analysis object.
  - sector (str): The sector for which the sentiment analysis is performed.

  Returns:
  None
  """
  st.text("Sentiment Analysis")
  
  selection = ["Pie Chart", "WordCloud", "Dataframes", "Stacked Bar Chart"]  
  options = st.selectbox("Visualizations : ", selection)
  
  if options == "Pie Chart":
    generate_pie_chart_page(sentimentAnalysis, sector)
  elif options == "WordCloud":
    generate_wordcloud_page(sentimentAnalysis, sector)                                             
  elif options == "Stacked Bar Chart":
    generate_stacked_bar_chart_page(sentimentAnalysis)
  elif options == "Dataframes":
    generate_dataframe_page(sentimentAnalysis, sector)

  return None

def topic_modeling_page(topicModeling, sector):
  slider = st.select_slider('Select the number of topics', options=[i for i in range(2, 21)])
  filename = f'assets/topic_model_{slider}_topics.html'
  with open(filename, 'r') as f:
    html_string = f.read()

  components.html(html_string, width=4000, height=1500, scrolling=False)
  return None

def main():
  """
  This function is the entry point of the application.
  It initializes the SentimentAnalysis and TopicModelling objects,
  reads the data, and calls the sidebar and mainpage functions.

  Returns:
    None
  """
  sentimentAnalysis = SentimentAnalysis("Sentiment Analysis Dashboard") ; sentimentAnalysis.read_data()
  topicModeling = TopicModelling("Topic Modelling Dashboard")
  options, sector = sidebar(sentimentAnalysis.df)
  mainpage(sentimentAnalysis, topicModeling, options, sector)
  return None

if __name__ == '__main__':
  main()
