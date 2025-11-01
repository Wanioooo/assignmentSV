import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

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

## 🚀 Data Loading
# Define the URL of the CSV file (Assuming the same URL from the previous request)
URL = "https://raw.githubusercontent.com/Wanioooo/assignmentSV/refs/heads/main/processed_drug_data.csv"

@st.cache_data
def load_data(url):
    """Loads the data from the URL."""
    try:
        df = pd.read_csv(url)
        return df
    except Exception as e:
        st.error(f"An error occurred while loading the data: {e}")
        return pd.DataFrame()

st.title("Gender Distribution Among Drug Users")

df = load_data(URL)

if not df.empty:
    
    ### 🧮 Data Processing
    
    # 1. Filter for users who have taken drugs
    # Assuming 'Have you ever taken drug?' is the correct column name for filtering
    DRUG_TAKEN_COLUMN = 'Have you ever taken drug?'
    GENDER_COLUMN = 'Gender'
    
    if DRUG_TAKEN_COLUMN in df.columns and GENDER_COLUMN in df.columns:
        drug_users_df = df[df[DRUG_TAKEN_COLUMN].str.lower() == 'yes'].copy()
        
        st.subheader(f"Total Drug Users: {len(drug_users_df)}")
        
        if len(drug_users_df) > 0:
            # 2. Count the occurrences of each gender
            gender_counts = drug_users_df[GENDER_COLUMN].value_counts().reset_index()
            gender_counts.columns = [GENDER_COLUMN, 'Count']
            
            st.subheader("Gender Counts Data")
            st.dataframe(gender_counts)

            # 3. Create the Plotly Pie Chart
            fig = px.pie(
                gender_counts, 
                values='Count', 
                names=GENDER_COLUMN, 
                title='**Distribution of Drug Users by Gender**',
                # Custom colors for distinction
                color=GENDER_COLUMN,
                color_discrete_map={
                    'Female':'#ff6692',  # Pink
                    'Male':'#636efa',    # Blue
                    'Other':'#ef553b'    # Red/Orange
                },
                # Display percentage and value in the hover text
                hover_data=['Count'],
                # Define text info for labels
                hole=0.3 # Creates a donut chart
            )
            
            # Update trace for percentage display on the chart
            fig.update_traces(textposition='inside', textinfo='percent+label')
            
            # Display the Plotly chart in Streamlit
            st.subheader("Interactive Pie Chart")
            st.plotly_chart(fig, use_container_width=True)
            
        else:
            st.warning("No users found who reported taking drugs ('yes'). Check the data source.")
            
    else:
        st.error(f"Required columns ('{DRUG_TAKEN_COLUMN}' and '{GENDER_COLUMN}') not found in the data.")
        
else:
    st.warning("Could not proceed with visualization as data loading failed.")

st.markdown("---")
st.caption("Application powered by Streamlit and Plotly.")
