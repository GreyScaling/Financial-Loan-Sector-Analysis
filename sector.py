import streamlit as st
import pandas as pd
import plotly.express as px

# Load data
df = pd.read_csv('/Users/szemin/Documents/DAC External Project/combined_sentiments.csv')

# Initialize Streamlit app
st.title("Sentiments Count by Sector")

# Create a dropdown to select sector
selected_sector = st.selectbox("Select Sector", df['Sector'].unique())

# Filter data based on selected sector
filtered_df = df[df['Sector'] == selected_sector]

# Define sentiment columns
sentiment_columns = ['Financial_Sentiments', 'Finbert_Sentiments', 'Sigma_Sentiments', 'Soleimanian_Sentiments', 'Yiyangkhost_Sentiments']

# Prepare data for plotting
plot_data_list = []

# Count occurrences of -1, 0, and 1 across all sentiment columns
for sentiment_col in sentiment_columns:
    sentiment_counts = filtered_df[sentiment_col].value_counts()
    for sentiment_value in [-1, 0, 1]:
        count = sentiment_counts.get(sentiment_value, 0)
        plot_data_list.append({'Sentiment': sentiment_col, 'Sentiment Value': sentiment_value, 'Count': count})

# Convert list to DataFrame
plot_data = pd.DataFrame(plot_data_list)

# Create bar chart using Plotly Express
fig = px.bar(plot_data, x='Sentiment Value', y='Count', color='Sentiment', 
             labels={'Sentiment': 'Sentiment', 'Count': 'Count', 'Sentiment Value': 'Sentiment Value'},
             title=f'Sentiments Count for {selected_sector}',
             category_orders={'Sentiment': sentiment_columns, 'Sentiment Value': [-1, 0, 1]},
             width=800, height=500)

# Display the bar chart
st.plotly_chart(fig)


