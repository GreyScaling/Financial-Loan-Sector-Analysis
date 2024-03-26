import streamlit as st
import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt

def generate_pie_chart_page(sentimentAnalysis, sector="All"):
  """
  Generates a pie chart page for sentiment analysis.

  Parameters:
    - sentimentAnalysis: An instance of the SentimentAnalysis class.
    - sector (optional): The sector to filter the data by. Default is "All".

  Returns:
    None
  """
  model_names = ['Financial_Sentiments', 'Finbert_Sentiments', 'Sigma_Sentiments', 'Soleimanian_Sentiments', 'Yiyangkhost_Sentiments']
  
  left_column, right_column = st.columns(2)
  for i , df in enumerate(sentimentAnalysis.dfs):
    if sector == "All":
      pass
    else:
      df = df[df["Sector"] == sector]
      
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
  
  return None

def generate_wordcloud_page(sentimentAnalysis, sector):
  """
  Generates and displays wordclouds based on sentiment analysis data.

  Parameters:
  - sentimentAnalysis: An instance of the SentimentAnalysis class.
  - sector: A string representing the sector to filter the data by.

  Returns:
  None
  """
  columns = ['Financial', 'Finbert', 'Sigma', 'Soleimanian', 'Yiyangkhost']
  if sector == "All":
    wordcloud_df = sentimentAnalysis.df
  else:
    wordcloud_df = sentimentAnalysis.df[sentimentAnalysis.df['Sector'] == sector]
    
  options = st.radio("Select the option", ["All", "Negative", "Neutral", "Positive"])

  sentimentsDict = {
    "Negative" : -1,
    "Neutral" : 0,
    "Positive" : 1
  }

  if options == "All":
    st.text("Wordcloud for " + sector)
    wordcloud = sentimentAnalysis.make_wordcloud(wordcloud_df, sector=sector)
    st.image(wordcloud.to_image())
  else:
    for column in columns:
      try:
        st.text(column)
        column += "_Sentiments"
        subset = wordcloud_df[wordcloud_df[column] == sentimentsDict[options]]
        wordcloud = sentimentAnalysis.make_wordcloud(subset, sector=sector)
        st.image(wordcloud.to_image())
      except ValueError:
        st.text("No data available")
  return None

def generate_stacked_bar_chart_page(sentimentAnalysis):
  """
  Generates a stacked bar chart page based on sentiment analysis.

  Parameters:
  - sentimentAnalysis: An object of the SentimentAnalysis class.

  Returns:
  - None
  """
  model_names = ['Financial_Sentiments', 'Finbert_Sentiments', 'Sigma_Sentiments', 'Soleimanian_Sentiments', 'Yiyangkhost_Sentiments']
  category_names = ['Negative', 'Neutral', 'Positive']
  results = dict()
  for i in range(len(sentimentAnalysis.dfs)):
    model_list = []
    model_dict = sentimentAnalysis.dfs[i]['sentiment'].value_counts().to_dict()
    model_list.append(model_dict[-1]); model_list.append(model_dict[0]); model_list.append(model_dict[1])
    results[model_names[i]] = model_list
    
  st.text("Bar chart based on Sentiment Models")
  fig, ax = sentimentAnalysis.horizontalStackedBar(results, category_names, title="Bar chart based on Sentiment Models")
  st.pyplot(fig)
  
  for i , df in enumerate(sentimentAnalysis.dfs):
    st.text(model_names[i])
    df = sentimentAnalysis.get_results_for_model(df, 'Sector')
    fig, ax = sentimentAnalysis.horizontalStackedBar(df, category_names, title=model_names[i] + " Sentiment Analysis")
    st.pyplot(fig)
  return None

def generate_dataframe_page(sentimentAnalysis, sector):
  """
  Generates a dataframe page with sentiment analysis results.

  Args:
    sentimentAnalysis (SentimentAnalysis): An instance of the SentimentAnalysis class.
    sector (str): The sector to filter the dataframe by. If "All", no filtering is applied.

  Returns:
    None
  """
  df = sentimentAnalysis.df.reset_index()

  if sector == "All":
    pass
  else:
    df = df[df['Sector'] == sector]

  columns = ['Financial', 'Finbert', 'Sigma', 'Soleimanian', 'Yiyangkhost']
  selected_columns = ['Title', 'Sector'] + [f'{column}_Sentiments' for column in columns]

  st.dataframe(
    df[selected_columns].reset_index(drop=True).style.applymap(
      sentimentAnalysis.sentiment_color, subset=[f'{column}_Sentiments' for column in columns]
    ),
    height=750
  )