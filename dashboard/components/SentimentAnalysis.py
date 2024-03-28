import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from wordcloud import STOPWORDS

class SentimentAnalysis:
  """
  A class for performing sentiment analysis on financial loan data.

  Attributes:
    name (str): The name of the sentiment analysis object.
    df (pandas.DataFrame): The main dataframe containing the combined sentiments.
    dfs (list): A list of dataframes containing individual sentiment analysis results.

  Methods:
    make_pie_charts(df): Generates pie charts based on sentiment counts.
    make_stacked_bar(df): Generates a stacked bar chart based on sentiment models.
    read_data(): Reads the sentiment data from CSV files.
    make_plot(df): Placeholder method for making a plot.
    make_wordcloud(df, colNames): Generates a wordcloud based on the specified column.

  """

  def __init__(self, name):
    self.name = name 

  def make_pie_charts(self, df):
    """
    Generates pie charts based on sentiment counts.

    Args:
      df (pandas.DataFrame): The dataframe containing sentiment data.

    Returns:
      matplotlib.figure.Figure: The generated figure object.

    """
    cmap = plt.cm.get_cmap('RdYlGn')
    colors = {1: cmap(0.9), 0: cmap(0.5), -1: cmap(0.1)}
    sentiment_counts = df['sentiment'].value_counts().sort_index()
    sentiment_colors = [colors[sentiment] for sentiment in sentiment_counts.index]
    fig, ax = plt.subplots()
    sentiment_counts.plot(kind='pie', colors=sentiment_colors, autopct='%1.1f%%', ax=ax, labels=['Negative', 'Neutral', 'Positive'])
    ax.set_ylabel('')

    return fig
  
  def make_stacked_bar(self, df):
    """
    Generates a stacked bar chart based on sentiment models.

    Args:
      df (pandas.DataFrame): The dataframe containing sentiment data.

    Returns:
      matplotlib.figure.Figure: The generated figure object.
      matplotlib.axes.Axes: The generated axes object.

    """
    category_names = ['Negative', 'Neutral', 'Positive']

    models_name = ['Financial_Sentiments', 'Finbert_Sentiments', 'Sigma_Sentiments', 'Soleimanian_Sentiments', 'Yiyangkhost_Sentiments']

    results = dict()

    for i in range(len(df)):
      # make it so that it will follow the order
      model_list = []
      model_dict = df[i]['sentiment'].value_counts().to_dict()
      model_list.append(model_dict[-1]); model_list.append(model_dict[0]); model_list.append(model_dict[1])
      results[models_name[i]] = model_list

    fig, ax = self.horizontalStackedBar(results, category_names, title="Bar chart based on Sentiment Models")

    return fig, ax 
    
    
  def read_data(self):
    """
    Reads the sentiment data from CSV files.

    Returns:
      pandas.DataFrame: The main dataframe containing the combined sentiments.
      list: A list of dataframes containing individual sentiment analysis results.

    """
    # need to change the path to the absolute path
    self.df = pd.read_csv('https://raw.githubusercontent.com/GreyScaling/UOB-Financial-Loan-Analysis/main/dashboard/csvs/combined_sentiments.csv', index_col=0)
    sigma_sentiments = pd.read_csv('https://raw.githubusercontent.com/GreyScaling/UOB-Financial-Loan-Analysis/main/dashboard/csvs/sigma_sentiments.csv', index_col=0)
    finbert_sentiments = pd.read_csv('https://raw.githubusercontent.com/GreyScaling/UOB-Financial-Loan-Analysis/main/dashboard/csvs/finbert_sentiments.csv', index_col=0)
    financial_sentiments = pd.read_csv('https://raw.githubusercontent.com/GreyScaling/UOB-Financial-Loan-Analysis/main/dashboard/csvs/financial_sentiments.csv', index_col=0)
    soleimanian_sentiments = pd.read_csv('https://raw.githubusercontent.com/GreyScaling/UOB-Financial-Loan-Analysis/main/dashboard/csvs/soleimanian_sentiments.csv', index_col=0)
    yiyangkhost_sentiments = pd.read_csv('https://raw.githubusercontent.com/GreyScaling/UOB-Financial-Loan-Analysis/main/dashboard/csvs/yiyangkhost_sentiments.csv', index_col=0)
    self.dfs = [sigma_sentiments, finbert_sentiments, financial_sentiments, soleimanian_sentiments, yiyangkhost_sentiments]
    return self.df, self.dfs

  def make_plot(self, df):
    """
    Placeholder method for making a plot.

    Args:
      df (pandas.DataFrame): The dataframe containing data for the plot.

    """
    pass
  
  def make_wordcloud(self, df, colNames="Content", sector=None):
    """
    Generates a wordcloud based on the specified column.

    Args:
      df (pandas.DataFrame): The dataframe containing text data.
      colNames (str): The name of the column to generate the wordcloud from. Default is "Content".

    Returns:
      wordcloud.WordCloud: The generated wordcloud object.

    """
    data = df[colNames]
    
    if sector == 'All':
      sector = df['Sector'].unique()
      remove_words = [word.split() for word in sector]
      remove_words = [item for sublist in remove_words for item in sublist]
      remove_words = remove_words + [word.lower() for word in remove_words] + [word.upper() for word in remove_words]
      remove_words += "oil gas"
      print(remove_words)
      data = data.apply(lambda x: ' '.join([word for word in x.split() if word not in sector]))
  
    else:
      print(sector + " is getting removed")
      # if sector is more than 1 word
      sector_words = sector.split()
      remove_words = sector_words + [word.lower() for word in sector_words] + [word.upper() for word in sector_words]
      print(remove_words)
      data = data.apply(lambda x: ' '.join([word for word in x.split() if word not in remove_words]))
     
    
    data = data.astype(str)
    
    wordcloud = WordCloud(width=800, height=400, max_font_size=100,
                          max_words=100, background_color="white").generate(' '.join(data))
    return wordcloud
  
    
  def sentiment_color(self, sentiment):
    """
    Returns the background color based on the sentiment value.

    Parameters:
    sentiment (int): The sentiment value (-1, 0, or 1).

    Returns:
    str: The CSS background color value.

    """
    if sentiment == -1:
      return 'background-color: red'
    elif sentiment == 0:
      return 'background-color: yellow'
    elif sentiment == 1:
      return 'background-color: green'
    
  def horizontalStackedBar(self, results, category_names, title="Sentiment Analysis Results"):
    """
    Parameters
    ----------
    results : dict
        A mapping from question labels to a list of answers per category.
        It is assumed all lists contain the same number of entries and that
        it matches the length of *category_names*.
    category_names : list of str
        The category labels.
    """

    labels = list(results.keys())
    data = np.array(list(results.values()))
    data_cum = data.cumsum(axis=1)
    category_colors = plt.colormaps['RdYlGn'](
        np.linspace(0.15, 0.85, data.shape[1]))

    fig, ax = plt.subplots(figsize=(10, 4))

    ax.invert_yaxis()
    ax.xaxis.set_visible(False)
    ax.set_xlim(0, np.sum(data, axis=1).max())

    for i, (colname, color) in enumerate(zip(category_names, category_colors)):
        widths = data[:, i]
        starts = data_cum[:, i] - widths
        rects = ax.barh(labels, widths, left=starts, height=0.5,
                        label=colname, color=color)

        r, g, b, _ = color
        text_color = 'white' if r * g * b < 0.5 else 'darkgrey'
        ax.bar_label(rects, label_type='center', color=text_color)
    ax.legend(ncols=len(category_names), bbox_to_anchor=(0, 1),
                loc='lower left', fontsize='small')

    ax.set_title(title, loc = 'right')
    return fig, ax

  def get_results_for_model(self, model, column_name="Sector", country="All"):
    """
    Calculates the sentiment analysis results for each unique value in the specified column of the given model.

    Parameters:
      model (pandas.DataFrame): The dataframe containing the data for sentiment analysis.
      column_name (str, optional): The name of the column to group the results by. Defaults to "Sector".

    Returns:
      dict: A dictionary where the keys are the unique values in the specified column and the values are lists
          containing the counts of negative, neutral, and positive sentiments for each unique value.
    """
    result = dict()
    sectors = model[column_name].unique()

    for s in sectors:
      subset = model.query("Sector == @s")
      if country != "All":
        subset = subset[subset['Country'] == country]
        
      positive = subset[subset['sentiment'] == 1]
      negative = subset[subset['sentiment'] == -1]
      neutral = subset[subset['sentiment'] == 0]
      result[s] = [len(negative), len(neutral), len(positive)]
    return result
