import streamlit as st
import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt
import os

from SentimentAnalysis import SentimentAnalysis
from TopicModelling import TopicModelling

from utilities import horizontalStackedBar, get_results_for_model

# emojis: https://www.webfx.com/tools/emoji-cheat-sheet/
st.set_page_config(
  page_title = 'Financial Loan Analysis Dashboard',
  layout = 'wide',
  initial_sidebar_state="expanded"
)


def main():
  sentimentAnalysis = SentimentAnalysis("Sentiment Analysis Dashboard")
  sentimentAnalysis.read_data()
  topicModeling = TopicModelling("Topic Modelling Dashboard")
  options, sector = sidebar(sentimentAnalysis.df)
  mainpage(sentimentAnalysis, topicModeling, options, sector)
  return None

def mainpage(sentimentAnalysis, topicModeling,  options, sector): # just pass the object instead of the df
  if options == 'Sentiment Analysis':
    sentiment_analysis_page(sentimentAnalysis, sector)
          
  elif options == 'Topic Modeling':
    topic_modeling_page(topicModeling, sector)
    pass
      
  return None

def sentiment_analysis_page(sentimentAnalysis, sector):
  
  st.text("Sentiment Analysis")
  all, negative, neutral, positive = sentiment_header()
  
  if sector == 'All': # sector
    with all: # 'tab all'
      options = st.selectbox("Select the option", ["Pie Chart", "WordCloud", "Stacked Bar Chart"])
      if options == "Pie Chart":
        generate_pie_chart_page(sentimentAnalysis)
      elif options == "WordCloud":
        generate_wordcloud_page(sentimentAnalysis, sector)  
      elif options == "Stacked Bar Chart":
        generate_stacked_bar_chart_page(sentimentAnalysis)
    with positive:
      pass
    with negative:
      pass
    with neutral:
      pass
    
  else:
    options = st.selectbox("Select the option", ["Pie Chart", "WordCloud"])
    if options == "Pie Chart":
      generate_pie_chart_page(sentimentAnalysis, sector)
    elif options == "WordCloud":
      generate_wordcloud_page(sentimentAnalysis, sector)
    pass
  
  return None


def generate_pie_chart_page(sentimentAnalysis, sector="All"):
  if sector == "All":
    left_column, right_column = st.columns(2)
    model_names = ['Financial_Sentiments', 'Finbert_Sentiments', 'Sigma_Sentiments', 'Soleimanian_Sentiments', 'Yiyangkhost_Sentiments']
    for i , df in enumerate(sentimentAnalysis.dfs):
      if i % 2 == 0:
        with left_column:
          st.text(model_names[i])
          fig = sentimentAnalysis.make_pie_charts(df)
          st.pyplot(fig)
      else:
        with right_column:
          st.text(model_names[i])
          fig = sentimentAnalysis.make_pie_charts(df)
          st.pyplot(fig)
  else:
    left_column, right_column = st.columns(2)
    model_names = ['Financial_Sentiments', 'Finbert_Sentiments', 'Sigma_Sentiments', 'Soleimanian_Sentiments', 'Yiyangkhost_Sentiments']
    for i , df in enumerate(sentimentAnalysis.dfs):
      subset = df[df['Sector'] == sector]
      if i % 2 == 0:
        with left_column:
          st.text(model_names[i])
          fig = sentimentAnalysis.make_pie_charts(subset)
          st.pyplot(fig)
      else:
        with right_column:
          st.text(model_names[i])
          fig = sentimentAnalysis.make_pie_charts(subset)
          st.pyplot(fig)
  return None

def generate_wordcloud_page(sentimentAnalysis, sector):
  options = st.radio("Select the option", ["All", "Negative", "Neutral", "Positive"])
  if sector == "All": # need to apply 
    st.text("WordCloud for " + sector)
    wordcloud = sentimentAnalysis.make_wordcloud(sentimentAnalysis.df)
    st.image(wordcloud.to_image())
  else:
    st.text("WordCloud for " + sector)
    subset = sentimentAnalysis.df[sentimentAnalysis.df['Sector'] == sector]
    wordcloud = sentimentAnalysis.make_wordcloud(subset)
    st.image(wordcloud.to_image())
  return None

def generate_stacked_bar_chart_page(sentimentAnalysis):
  model_names = ['Financial_Sentiments', 'Finbert_Sentiments', 'Sigma_Sentiments', 'Soleimanian_Sentiments', 'Yiyangkhost_Sentiments']
  category_names = ['Negative', 'Neutral', 'Positive']
  results = dict()
  for i in range(len(sentimentAnalysis.dfs)):
    model_list = []
    model_dict = sentimentAnalysis.dfs[i]['sentiment'].value_counts().to_dict()
    model_list.append(model_dict[-1]); model_list.append(model_dict[0]); model_list.append(model_dict[1])
    results[model_names[i]] = model_list
    
  st.text("Bar chart based on Sentiment Models")
  fig, ax = horizontalStackedBar(results, category_names, title="Bar chart based on Sentiment Models")
  st.pyplot(fig)
  
  for i , df in enumerate(sentimentAnalysis.dfs):
    st.text(model_names[i])
    df = get_results_for_model(df, 'Sector')
    fig, ax = horizontalStackedBar(df, category_names, title=model_names[i] + " Sentiment Analysis")
    st.pyplot(fig)
  return None

def topic_modeling_page(topicModeling, sector):
  st.text("Topic Modeling")
  return None

def sentiment_header():
  tab1, tab2, tab3, tab4 = st.tabs(["All", "Negative ☹️", "Neutral", "Positive 😊"])
  
  return tab1, tab2, tab3, tab4

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
