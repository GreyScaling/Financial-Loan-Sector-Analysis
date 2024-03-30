import streamlit as st
import pandas as pd
import streamlit.components.v1 as components
import requests
from components.SentimentAnalysis import SentimentAnalysis
from components.sentiment_components import *

st.set_page_config(
  page_title = 'Financial Loan Analysis Dashboard',
  layout = 'wide',
  initial_sidebar_state="expanded"
)

def mainpage(sentimentAnalysis, options, sector, country):
  """
  This function is responsible for displaying the main page of the dashboard based on the selected options.

  Parameters:
  - sentimentAnalysis (object): The sentiment analysis object.
  - topicModeling (object): The topic modeling object.
  - options (str): The selected option ('Sentiment Analysis' or 'Topic Modeling').
  - sector (str): The selected sector.
  - country (str): The selected country.

  Returns:
  None
  """

  if options == 'Sentiment Analysis':
    sentiment_analysis_page(sentimentAnalysis, sector, country)
      
  elif options == 'Topic Modeling':
    topic_modeling_page()
  return None

def sidebar(df : pd.DataFrame):
  """
  This function creates a sidebar for the loan analysis dashboard.
  
  Parameters:
    df (pd.DataFrame): The DataFrame containing the loan data.
  
  Returns:
    tuple: A tuple containing the selected option and sector.
  """

  location = "https://raw.githubusercontent.com/GreyScaling/UOB-Financial-Loan-Analysis/main/dashboard/assets/UOB-logo.png"

  req = requests.get(location)
  img = req.content
  st.sidebar.image(img , width=200)
 
  st.sidebar.title('Financial Loan Analysis')
  st.sidebar.header("Filter : ")
  
  options = st.sidebar.selectbox(
    'Select the option :',
    options = ['Sentiment Analysis', 'Topic Modeling']
  )
  
  if options == 'Topic Modeling':
    return options, None, None
  
  sectors = df['Sector'].unique()
  sector = st.sidebar.selectbox(
    'Select the sector :',
    options = ['All'] + list(sectors),
    key='sector',
  )
  
  countries = df['Country'].unique()
  country = st.sidebar.selectbox(
    'Select the country :',
    options = ['All'] + list(countries),
    key='country'
  )

  
  return options, sector, country

def sentiment_analysis_page(sentimentAnalysis, sector, country):
  """
  Displays the sentiment analysis page with various visualization options.

  Parameters:
  - sentimentAnalysis (object): The sentiment analysis object.
  - sector (str): The sector for which the sentiment analysis is performed.

  Returns:
  None
  """
  st.title("Sentiment Analysis")
  
  selection = ["Pie Chart", "WordCloud", "Dataframes", "Stacked Bar Chart", 'Mean Score']  
  options = st.selectbox("Visualizations : ", selection)

  if options == "Pie Chart":
    generate_pie_chart_page(sentimentAnalysis, sector, country)
  elif options == "WordCloud":
    generate_wordcloud_page(sentimentAnalysis, sector, country)                                             
  elif options == "Stacked Bar Chart":
    generate_stacked_bar_chart_page(sentimentAnalysis, country)
  elif options == "Dataframes":
    generate_dataframe_page(sentimentAnalysis, sector, country)
  elif options == 'Mean Score':
    generate_mean_score_page(sentimentAnalysis, sector, country)

  return None

def topic_modeling_page():
  """
  Renders an interactive topic modeling page based on the number of topics selected.

  Returns:
    None
  """
  options = st.selectbox("Visualizations : ", ['Interactive Topic Modeling', 'Coherence Score'])
  if options == 'Interactive Topic Modeling':
    slider = st.slider('Select the number of topics', 3, 20, 2)
    filename = f'https://raw.githubusercontent.com/GreyScaling/UOB-Financial-Loan-Analysis/main/dashboard/assets/topic_model_{slider}_topics.html'
    st.markdown(f'#### `Interactive topic Modeling based on the number of topics selected`')
    response = requests.get(filename)
    html_string = response.text
    components.html(html_string, width=4000, height=1500, scrolling=False)
  elif options == 'Coherence Score':
    filename = 'https://raw.githubusercontent.com/GreyScaling/UOB-Financial-Loan-Analysis/main/Topic Modelling/topics_coherence.png'
    
    st.markdown(f'#### `Coherence Score based on the number of topics`')
    response = requests.get(filename)
    st.image(response.content, width=800)
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

  
  options, sector, country = sidebar(sentimentAnalysis.df)
  mainpage(sentimentAnalysis, options, sector, country)
  return None

if __name__ == '__main__':
  main()
