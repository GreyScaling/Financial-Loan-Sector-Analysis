import streamlit as st
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import pandas as pd

# Load data
df = pd.read_csv('/Users/szemin/Documents/DAC External Project/combined_sentiments.csv')

# Initialize Streamlit app
st.title("Site Name Word Cloud")

# Check if 'Site_Name' column exists in the DataFrame
if 'Site-Name' not in df.columns:
    st.error("Error: 'Site_Name' column not found in the dataset.")
    st.write("Available columns:", df.columns.tolist())
else:
    # Generate word cloud based on 'Site_Name' column
    wordcloud_data = df['Site-Name'].value_counts().to_dict()
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(wordcloud_data)

    # Display the word cloud using st.pyplot(fig)
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis('off')
    st.pyplot(fig)

    # Optional: Display the count of each site name
    st.write("Site Name Counts:")
    st.write(df['Site-Name'].value_counts())
