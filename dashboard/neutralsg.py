import streamlit as st
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import pandas as pd

# Load data
df = pd.read_csv('/Users/szemin/Documents/DAC External Project/combined_sentiments.csv')

# Define the sentiment columns
sentiment_columns = ['Financial_Sentiments', 'Finbert_Sentiments', 'Sigma_Sentiments', 
                     'Soleimanian_Sentiments', 'Yiyangkhost_Sentiments']

# Initialize Streamlit app
st.title("Word Cloud for Content in Singapore with Neutral Sentiment")

# Initialize an empty text variable to concatenate content
text_neutral = ''

# Filter data for Singapore and neutral sentiment in each sentiment column
for col in sentiment_columns:
    df_sg_neutral = df[(df['Country'] == 'Singapore') & (df[col] == 0)]
    if 'Content' in df_sg_neutral.columns:
        text_neutral += ' '.join(df_sg_neutral['Content'].dropna()) + ' '

# Check if any data is available
if len(text_neutral) == 0:
    st.error("Error: No data found for Singapore with neutral sentiment.")
else:
    # Generate word cloud based on concatenated text
    wordcloud_neutral = WordCloud(width=800, height=400, background_color='white').generate(text_neutral)

    # Display the word cloud using st.image
    st.image(wordcloud_neutral.to_array(), caption='Word Cloud for Content in Singapore with Neutral Sentiment')

    # Optional: Display the count of words
    words_count_neutral = len(text_neutral.split())
    st.write(f"Total words in Content for Singapore with Neutral Sentiment: {words_count_neutral}")
