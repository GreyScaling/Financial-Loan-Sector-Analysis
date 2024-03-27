import streamlit as st
import pandas as pd
import plotly.express as px

# Load data
df = pd.read_csv('/Users/szemin/Documents/DAC External Project/combined_sentiments.csv')

# Initialize Streamlit app
st.title("Mean Sentiment Scores by Sector")

# Create a dropdown to select sentiment model
selected_sentiment_model = st.selectbox("Select Sentiment Model",
                                        ['Financial_Sentiments', 'Finbert_Sentiments', 'Sigma_Sentiments', 
                                         'Soleimanian_Sentiments', 'Yiyangkhost_Sentiments'])

# Calculate mean sentiment scores by sector for the selected sentiment model
mean_scores = df.groupby('Sector')[selected_sentiment_model].mean().reset_index()

# Create bar chart using Plotly Express
fig = px.bar(mean_scores, x='Sector', y=selected_sentiment_model,
             labels={'Sector': 'Sector', selected_sentiment_model: 'Mean Sentiment Score'},
             title=f'Mean Sentiment Scores by Sector for {selected_sentiment_model}',
             width=800, height=500)

# Display the bar chart
st.plotly_chart(fig)
