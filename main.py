import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# Set up the Streamlit page configuration
st.set_page_config(layout="wide", page_title="Drug Distribution Analysis")

## 🚀 Data Loading and Preparation
# Define the URL of the CSV file
URL = "https://raw.githubusercontent.com/Wanioooo/assignmentSV/refs/heads/main/processed_drug_data.csv"

@st.cache_data
def load_data(url):
    """Loads the data from the URL and handles potential errors."""
    try:
        # Read the CSV file into a pandas DataFrame
        df = pd.read_csv(url)
        return df
    except Exception as e:
        st.error(f"An error occurred while loading the data: {e}")
        return pd.DataFrame() # Return an empty DataFrame on failure

st.title("Drug Type Distribution by Age Group")

arts_df_online = load_data(URL)

if not arts_df_online.empty:
    st.subheader("Raw Data Preview")
    st.dataframe(arts_df_online)
    
    # Use a copy of the loaded DataFrame for processing
    df = arts_df_online.copy()

    ### 🧮 Data Processing
    
    # Define age groups
    bins = [0, 18, 25, 35, 50, np.inf]
    labels = ['<18', '18-25', '26-35', '36-50', '51+']
    
    # Assuming 'Age' column exists (based on your original code)
    if 'Age' in df.columns:
        df['Age_Group'] = pd.cut(df['Age'], bins=bins, labels=labels, right=False, include_lowest=True)
        
        # Group data by age group and drug type and count occurrences
        DRUG_COLUMN = 'What is the name of the drug you used for the 1st time?'
        
        # Group data and count occurrences
        drug_age_counts = df.groupby(['Age_Group', DRUG_COLUMN], observed=True).size().reset_index(name='Count')
        
        st.subheader("Count of Drug Use by Age Group and Drug Type")
        st.dataframe(drug_age_counts.head())
        
        # Pivot the data to create a matrix for the heatmap
        heatmap_data = drug_age_counts.pivot(
            index='Age_Group', 
            columns=DRUG_COLUMN, 
            values='Count'
        ).fillna(0)
        
        st.subheader("Heatmap Data Matrix")
        st.dataframe(heatmap_data)
        
        ### 📈 Plotly Heatmap Visualization
        
        st.subheader("Interactive Drug Type Distribution Heatmap")
        
        # Use plotly.express.imshow to create the heatmap
        # We pass the pivoted DataFrame directly to px.imshow
        fig = px.imshow(
            heatmap_data, 
            x=heatmap_data.columns.tolist(), 
            y=heatmap_data.index.tolist(),
            color_continuous_scale='YlGnBu', # Matching the original Seaborn color map style
            text_auto=True, # Automatically display the count value on each cell
            aspect="auto"
        )
        
        # Update layout for better appearance and titles
        fig.update_layout(
            title_text='**Drug Type Distribution by Age Group**',
            xaxis_title=DRUG_COLUMN,
            yaxis_title='Age Group',
            xaxis={'side': 'bottom'}
        )
        
        # Display the Plotly chart in Streamlit
        st.plotly_chart(fig, use_container_width=True)

    else:
        st.error("The DataFrame must contain an 'Age' column to create age groups.")
else:
    st.warning("Could not proceed with data processing and visualization as data loading failed.")

st.markdown("---")
st.caption("Application powered by Streamlit and Plotly.")

import streamlit as st
import pandas as pd
import plotly.express as px

# Set up the Streamlit page configuration
st.set_page_config(layout="wide", page_title="Gender Distribution Pie Chart")

st.title("Distribution of Drug Users by Gender")

# --- ASSUMED DATA PREPARATION (Based on a typical scenario) ---
# NOTE: Replace this section with your actual data loading and processing
# if your gender_counts calculation is more complex.

# 1. Simulate data loading (You should replace this with your actual DataFrame 'df')
# For demonstration, I'll use a simple mock DataFrame
data = {
    'Gender': ['Male', 'Female', 'Male', 'Non-Binary', 'Female', 'Male', 'Female', 'Male', 'Male', 'Female']
}
df = pd.DataFrame(data) 
# Assuming you have loaded your main DataFrame 'df' earlier

# 2. Calculate the 'gender_counts' DataFrame
# This step replaces the matplotlib data preparation logic
gender_counts = df['Gender'].value_counts().reset_index()
gender_counts.columns = ['Gender', 'Count']

# --- PLOTLY VISUALIZATION ---

if not gender_counts.empty:
    st.subheader("Gender Count Data")
    st.dataframe(gender_counts)
    
    # Create the Plotly Pie Chart
    # Plotly Express automatically calculates proportions for pie charts
    fig = px.pie(
        gender_counts, 
        values='Count', 
        names='Gender', 
        title='**Distribution of Drug Users by Gender**',
        # Set the starting angle and colors for a more visually appealing chart
        hole=0.3, # Creates a donut chart (optional, but often preferred)
        color_discrete_sequence=px.colors.qualitative.Pastel # Use a nice color scheme
    )
    
    # Customize the figure layout
    fig.update_traces(
        textposition='inside', 
        textinfo='percent+label', 
        pull=[0.05 if label == gender_counts['Gender'].iloc[0] else 0 for label in gender_counts['Gender']], # Optional: pulls out the largest slice
        marker=dict(line=dict(color='#000000', width=1))
    )
    
    # Display the Plotly chart in Streamlit
    st.plotly_chart(fig, use_container_width=True)
    
else:
    st.warning("Gender data is not available or the DataFrame is empty.")

