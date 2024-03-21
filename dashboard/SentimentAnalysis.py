import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from wordcloud import STOPWORDS
from utilities import horizontalStackedBar

class SentimentAnalysis:
  def __init__(self, name):
    self.name = name 

  def make_pie_charts(self, df):
    cmap = plt.cm.get_cmap('RdYlGn')
    colors = {1: cmap(0.9), 0: cmap(0.5), -1: cmap(0.1)}
    sentiment_counts = df['sentiment'].value_counts().sort_index()
    sentiment_colors = [colors[sentiment] for sentiment in sentiment_counts.index]
    fig, ax = plt.subplots()
    sentiment_counts.plot(kind='pie', colors=sentiment_colors, autopct='%1.1f%%', ax=ax)

    return fig
  
  def make_stacked_bar(self, df):
    category_names = ['Negative', 'Neutral', 'Positive']

    models_name = ['Financial_Sentiments', 'Finbert_Sentiments', 'Sigma_Sentiments', 'Soleimanian_Sentiments', 'Yiyangkhost_Sentiments']

    results = dict()

    for i in range(len(df)):
      # make it so that it will follow the order
      model_list = []
      model_dict = df[i]['sentiment'].value_counts().to_dict()
      model_list.append(model_dict[-1]); model_list.append(model_dict[0]); model_list.append(model_dict[1])
      results[models_name[i]] = model_list

    fig, ax = horizontalStackedBar(results, category_names, title="Bar chart based on Sentiment Models")

    return fig, ax 
    
    
  def read_data(self):
    # need to change the path to the absolute path
    self.df = pd.read_csv('/Users/jovan/Documents/UOB-Financial-Loan-Analysis/sentiment_analysis/combined_sentiments.csv', index_col=0)
    sigma_sentiments = pd.read_csv('/Users/jovan/Documents/UOB-Financial-Loan-Analysis/sentiment_analysis/sigma_sentiments.csv', index_col=0)
    finbert_sentiments = pd.read_csv('/Users/jovan/Documents/UOB-Financial-Loan-Analysis/sentiment_analysis/finbert_sentiments.csv', index_col=0)
    financial_sentiments = pd.read_csv('/Users/jovan/Documents/UOB-Financial-Loan-Analysis/sentiment_analysis/financial_sentiments.csv', index_col=0)
    soleimanian_sentiments = pd.read_csv('/Users/jovan/Documents/UOB-Financial-Loan-Analysis/sentiment_analysis/soleimanian_sentiments.csv', index_col=0)
    yiyangkhost_sentiments = pd.read_csv('/Users/jovan/Documents/UOB-Financial-Loan-Analysis/sentiment_analysis/yiyangkhost_sentiments.csv', index_col=0)
    self.dfs = [sigma_sentiments, finbert_sentiments, financial_sentiments, soleimanian_sentiments, yiyangkhost_sentiments]
    return self.df, self.dfs

  def make_plot(self, df):
    pass
  
  def make_wordcloud(self, df, colNames="Content"):
    wordcloud = WordCloud(width=800, height=400, max_font_size=100,
                          max_words=100, background_color="white").generate(' '.join(df[colNames]))
    return wordcloud