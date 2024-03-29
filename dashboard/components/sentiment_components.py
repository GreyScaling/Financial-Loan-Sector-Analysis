import streamlit as st
import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt

def generate_pie_chart_page(sentimentAnalysis, sector="All", country="All"):
  """
  Generates a pie chart page for sentiment analysis.

  Parameters:
    - sentimentAnalysis: An instance of the SentimentAnalysis class.
    - sector (optional): The sector to filter the data by. Default is "All".
    - country (optional): The country to filter the data by. Default is "All".

  Returns:
    None
  """
  model_names = ['Financial_Sentiments', 'Finbert_Sentiments', 'Sigma_Sentiments', 'Soleimanian_Sentiments', 'Yiyangkhost_Sentiments']

  
  for i in range(len(sentimentAnalysis.dfs)):
    if sector != 'All':
      sentimentAnalysis.dfs[i] = sentimentAnalysis.dfs[i][sentimentAnalysis.dfs[i]['Sector'] == sector]
    if country != 'All':
      sentimentAnalysis.dfs[i] = sentimentAnalysis.dfs[i][sentimentAnalysis.dfs[i]['Country'] == country]
  
  st.markdown(f"#### Total value : {len(sentimentAnalysis.dfs[0])}")
  st.markdown("#### `Pie chart based on the different sentiments results for all models `" , unsafe_allow_html=True)
  left_column, right_column = st.columns(2)
  for i in range(len(sentimentAnalysis.dfs)):
    if i % 2 == 0:
      with left_column:
        st.subheader(model_names[i])
        fig = sentimentAnalysis.make_pie_charts(sentimentAnalysis.dfs[i])
        st.pyplot(fig)
    else:
      with right_column:
        st.subheader(model_names[i])
        fig = sentimentAnalysis.make_pie_charts(sentimentAnalysis.dfs[i])
        st.pyplot(fig)
  
  return None

def generate_wordcloud_page(sentimentAnalysis, sector, country="All"):
  """
  Generates and displays wordclouds based on sentiment analysis data.

  Parameters:
  - sentimentAnalysis: An instance of the SentimentAnalysis class.
  - sector: A string representing the sector to filter the data by.
  - country: A string representing the country to filter the data by.

  Returns:
  None
  """
  columns = ['Financial', 'Finbert', 'Sigma', 'Soleimanian', 'Yiyangkhost']
  if sector == "All":
    wordcloud_df = sentimentAnalysis.df
  else:
    wordcloud_df = sentimentAnalysis.df[sentimentAnalysis.df['Sector'] == sector]
    
  if country == "All":
    wordcloud_df = wordcloud_df
  else:
    wordcloud_df = wordcloud_df[wordcloud_df['Country'] == country]
    
  options = st.radio("Select the option", ["All", "Negative", "Neutral", "Positive"])

  sentimentsDict = {
    "Negative" : -1,
    "Neutral" : 0,
    "Positive" : 1
  }

  if options == "All":
    wordcloud = sentimentAnalysis.make_wordcloud(wordcloud_df, sector=sector)
    st.markdown(f'#### `Wordcloud for {sector.lower()} sector based on the country {country.lower()}` ')
    st.image(wordcloud.to_image())
  else:
    st.markdown(f'#### `Wordcloud for {options.lower()} sentiments in {sector.lower()} sector based on different models` ')
    left, right = st.columns(2)
    for i in range(len(columns)):
      if i % 2 == 0:
        with left:
          try:
            column = columns[i] + "_Sentiments"
            subset = wordcloud_df[wordcloud_df[column] == sentimentsDict[options]]
            wordcloud = sentimentAnalysis.make_wordcloud(subset, sector=sector)
            st.markdown(f'#### {columns[i]}  Model')
            st.image(wordcloud.to_image())
          except ValueError:
            st.text("No data available")
      else:
        with right:
          try:
            column = columns[i] + "_Sentiments"
            subset = wordcloud_df[wordcloud_df[column] == sentimentsDict[options]]
            wordcloud = sentimentAnalysis.make_wordcloud(subset, sector=sector)
            st.markdown(f'#### {columns[i]}  Model')
            st.image(wordcloud.to_image())
          except ValueError:
            st.text("No data available")
  return None

def generate_stacked_bar_chart_page(sentimentAnalysis, country="All"):
  """
  Generates a stacked bar chart page based on sentiment analysis.

  Parameters:
  - sentimentAnalysis: An object of the SentimentAnalysis class.
  - country: A string representing the country to filter the data by.
  Returns:
  - None
  """
  model_names = ['Financial_Sentiments', 'Finbert_Sentiments', 'Sigma_Sentiments', 'Soleimanian_Sentiments', 'Yiyangkhost_Sentiments']
  category_names = ['Negative', 'Neutral', 'Positive']
  results = dict()
  
  for i in range(len(sentimentAnalysis.dfs)):
    if country == "All":
      data = sentimentAnalysis.dfs[i]
    else:
      data = sentimentAnalysis.dfs[i][sentimentAnalysis.dfs[i]['Country'] == country]
    model_list = []
    model_dict = data['sentiment'].value_counts().to_dict()
    print(model_dict)
    
    if len(model_dict) < 3:
      for j in range(-1, 2):
        if j not in model_dict.keys():
          model_dict[j] = 0
    
    model_list.append(model_dict[-1]); model_list.append(model_dict[0]); model_list.append(model_dict[1])

    results[model_names[i]] = model_list
  st.markdown("##### Total value : " + str(len(data)))
  st.markdown("#### `Bar chart based on Sentiment Models` ")
  fig, ax = sentimentAnalysis.horizontalStackedBar(results, category_names, title="")
  st.pyplot(fig)
  st.markdown("#### `Bar chart based on every sectors for all models` ")
  for i , df in enumerate(sentimentAnalysis.dfs):
    if country != "All":
      df = df[df['Country'] == country]
    df = sentimentAnalysis.get_results_for_model(df, 'Sector')
    fig, ax = sentimentAnalysis.horizontalStackedBar(df, category_names, title=model_names[i] + " model")
    st.pyplot(fig)
  return None

def generate_dataframe_page(sentimentAnalysis, sector="All", country="All"):
  """
  Generates a dataframe page with sentiment analysis results.

  Args:
    sentimentAnalysis (SentimentAnalysis): An instance of the SentimentAnalysis class.
    sector (str): The sector to filter the dataframe by. If "All", no filtering is applied.
    country (str): The country to filter the dataframe by. If "All", no filtering is applied.

  Returns:
    None
  """
  df = sentimentAnalysis.df.reset_index()

  if sector == "All":
    pass
  else:
    df = df[df['Sector'] == sector]

  if country == "All":
    pass
  else:
    df = df[df['Country'] == country]

  columns = ['Financial', 'Finbert', 'Sigma', 'Soleimanian', 'Yiyangkhost']
  selected_columns = ['Title', 'Sector', 'Country'] + [f'{column}_Sentiments' for column in columns]
  st.markdown("##### Total value : " + str(len(df)))
  st.markdown(f"### `Dataframes based on the different sentiments results for all models `" , unsafe_allow_html=True)
  st.dataframe(
    df[selected_columns].reset_index(drop=True).style.applymap(
      sentimentAnalysis.sentiment_color, subset=[f'{column}_Sentiments' for column in columns]
    ),
    height=750
  )