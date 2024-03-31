import streamlit as st
import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt
import plotly.express as px

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
  
  # used for labeling the pie chart
  model_names = ['Financial Sentiments', 'Finbert Sentiments', 'Sigma Sentiments', 'Soleimanian Sentiments', 'Yiyangkhost Sentiments']

  for i in range(len(sentimentAnalysis.dfs)):
    if sector != 'All':
      sentimentAnalysis.dfs[i] = sentimentAnalysis.dfs[i][sentimentAnalysis.dfs[i]['Sector'] == sector]
    if country != 'All':
      sentimentAnalysis.dfs[i] = sentimentAnalysis.dfs[i][sentimentAnalysis.dfs[i]['Country'] == country]
  
  st.markdown(f"###### Total value : {len(sentimentAnalysis.dfs[0])}")
  st.markdown("#### Breakdown of the different sentiments based on the models for:" )
  st.markdown(f"###### Sector: {sector} \n ###### Country: {country} " )

  left_column, right_column = st.columns(2)
  try:
    for i in range(len(sentimentAnalysis.dfs)):
      # if the index is even, display the pie chart in the left column
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
  except ValueError:
    st.text("No data available")
    
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
  
  wordcloud_df = sentimentAnalysis.df
  if sector != "All":
    wordcloud_df = sentimentAnalysis.df[sentimentAnalysis.df['Sector'] == sector]

  if country != "All":
    wordcloud_df = wordcloud_df[wordcloud_df['Country'] == country]
        
  options = st.radio("Select the option", ["All", "Negative", "Neutral", "Positive"])

  # dictionary to convert sentiment to numerical values
  sentimentsDict = {
    "Negative" : -1,
    "Neutral" : 0,
    "Positive" : 1
  }

  # generate wordcloud for all sentiments
  if options == "All":
    try:
      wordcloud = sentimentAnalysis.make_wordcloud(wordcloud_df, sector=sector)
      #st.markdown(f'#### `Wordcloud for {sector.lower()} sector based on the country {country.lower()}` ')
      st.markdown(f'#### Wordcloud of the words used for:  ')
      st.markdown(f'###### Sector: {sector}  \n ###### Country: {country}  ')
      st.image(wordcloud.to_image())
    except ValueError:
      st.text("No data available")
  else:
    st.markdown(f'#### Wordcloud of the words used in {options.lower()} sentiments based on the different models for :  ')
    st.markdown(f'###### Sector: {sector}  \n ###### Country: {country}  ') 
    try:  
      left, right = st.columns(2)
      for i in range(len(columns)):
        # if the index is even, display the wordcloud in the left column
        if i % 2 == 0:
          with left:
    
              # making wordcloud for the selected sentiment
            column = columns[i] + "_Sentiments"
            subset = wordcloud_df[wordcloud_df[column] == sentimentsDict[options]]
            wordcloud = sentimentAnalysis.make_wordcloud(subset, sector=sector)
            st.markdown(f'#### {columns[i]}  Model')
            st.image(wordcloud.to_image())
        else:
          # if the index is odd, display the wordcloud in the right column
          with right:
              # making wordcloud for the selected sentiment
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
  model_names = ['Financial Sentiments', 'Finbert Sentiments', 'Sigma Sentiments', 'Soleimanian Sentiments', 'Yiyangkhost Sentiments']
  category_names = ['Negative', 'Neutral', 'Positive']
  results = dict()
  # iterate through the models
  for i in range(len(sentimentAnalysis.dfs)):
    data = sentimentAnalysis.dfs[i]
    if country != "All":
      data = data[data['Country'] == country]
    
    model_list = []
    model_dict = data['sentiment'].value_counts().to_dict()
    print(model_dict)
    
    # if the model does not have all the sentiments, add the missing sentiments
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
  # iterate through the models
  for i , df in enumerate(sentimentAnalysis.dfs):
    # generating the plot
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

  if sector != "All":
    df = df[df['Sector'] == sector]
    
  if country != "All":
    df = df[df['Country'] == country]

  columns = ['Financial', 'Finbert', 'Sigma', 'Soleimanian', 'Yiyangkhost']
  selected_columns = ['Title', 'Sector', 'Country'] + [f'{column}_Sentiments' for column in columns]
  st.markdown("##### Total value : " + str(len(df)))
  st.markdown(f"### `Dataframes based on the different sentiments results for all models `" , unsafe_allow_html=True)
  # display the dataframe
  st.dataframe(
    df[selected_columns].reset_index(drop=True).style.map(
      sentimentAnalysis.sentiment_color, subset=[f'{column}_Sentiments' for column in columns]
    ),
    height=750
  )
  
def generate_mean_score_page(sentimentAnalysis, sector="All", country="All"):
  
  sentiment_model = st.selectbox("Select Sentiment Model", ['Financial Sentiments', 'Finbert Sentiments', 'Sigma Sentiments', 'Soleimanian Sentiments', 'Yiyangkhost Sentiments'])

  data = sentimentAnalysis.df
  
  if country != "All":
    data = data[data['Country'] == country]
  
  mean_scores = data.groupby('Sector')[sentiment_model].mean().reset_index()
  
  fig = px.bar(mean_scores, x='Sector', y=sentiment_model,
               text = sentiment_model,text_auto='.2f',
                labels={'Sector': 'Sector', sentiment_model: 'Mean Sentiment Score'},
                title=f'Mean Sentiment Scores by Sector for {sentiment_model}',
                width=800, height=500)

  st.plotly_chart(fig)

