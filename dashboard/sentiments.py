import pandas as pd
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
import streamlit as st

# Load the data
df = pd.read_csv('/Users/szemin/Documents/DAC External Project/combined_sentiments.csv')

# Add your sector-specific words to the stopwords list
additional_stopwords = {'Oil', 'Gas', 'Sector', 'Market','Financials','Financial','Consumer Goods','Construction','Logistics','Industrials','Healthcare','Technology','Real Estate','Media'} # Add sector-specific words here

#streamlit interface set up
def generate_wordcloud(text, title):
    wordcloud = WordCloud(stopwords=STOPWORDS.union(additional_stopwords), background_color='white').generate(text)
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.title(title)
    plt.show()

# Streamlit interface
st.title('Sentiment Analysis Dashboard')

# Dropdown for sectors
sector = st.selectbox('Select Sector:', options=['All'] + list(df['Sector'].unique()))

# Dropdown for sentiments
sentiment = st.selectbox('Select Sentiment:', options=['All', 'Positive', 'Neutral', 'Negative'])


#generate wordcloud
# Mapping sentiments to numerical values
sentiment_values = {'Positive': 1, 'Neutral': 0, 'Negative': -1}

# Filter the data based on the selection
filtered_df = df[df['Sector'] == sector] if sector != 'All' else df
if sentiment != 'All':
    sentiment_value = sentiment_values[sentiment]
    filtered_df = filtered_df[(filtered_df['Financial_Sentiments'] == sentiment_value) |
                              (filtered_df['Finbert_Sentiments'] == sentiment_value) |
                              (filtered_df['Sigma_Sentiments'] == sentiment_value) |
                              (filtered_df['Soleimanian_Sentiments'] == sentiment_value) |
                              (filtered_df['Yiyangkhost_Sentiments'] == sentiment_value)]

# Generate wordclouds for each sentiment model
sentiment_columns = ['Financial_Sentiments', 'Finbert_Sentiments', 'Sigma_Sentiments', 'Soleimanian_Sentiments', 'Yiyangkhost_Sentiments']
for col in sentiment_columns:
    # Concatenate all texts for the current sentiment model
    text = " ".join(review for review in filtered_df['Content'].astype(str))
    st.subheader(f'{col}')
    wordcloud = WordCloud(stopwords=STOPWORDS.union(additional_stopwords), background_color='white').generate(text)
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    st.pyplot(plt)
