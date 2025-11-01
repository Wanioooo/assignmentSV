import streamlit as st
import pandas as pd
import plotly.express as px

# Set up the Streamlit page configuration
st.set_page_config(layout="wide", page_title="Gender Distribution")

st.title("Gender Distribution of Drug Users")

## 🚀 Data Loading (Placeholder - Replace with your actual data loading)
# Assuming 'drug_users_df' is the main DataFrame from your application.
# --- Placeholder DataFrame Creation ---
data = {'Gender': ['Male', 'Female', 'Male', 'Female', 'Male', 'Other', 'Female', 'Male', 'Female', 'Male']}
drug_users_df = pd.DataFrame(data)

# You can uncomment and use the data loading logic from your previous query if applicable:
# URL = "https://raw.githubusercontent.com/Wanioooo/assignmentSV/refs/heads/main/processed_drug_data.csv"
# try:
#     drug_users_df = pd.read_csv(URL)
# except Exception as e:
#     st.error(f"Error loading data: {e}")
#     drug_users_df = pd.DataFrame() 
# ----------------------------------------


if not drug_users_df.empty:
    
    ### 🧮 Data Processing
    
    # 1. Calculate the counts of each gender
    gender_counts = drug_users_df['Gender'].value_counts().reset_index()
    gender_counts.columns = ['Gender', 'Count']
    
    st.subheader("Gender Counts Table")
    st.dataframe(gender_counts, use_container_width=True)
    
    
    ### 📈 Plotly Pie Chart Visualization
    
    st.subheader("Interactive Distribution of Drug Users by Gender")
    
    # Create the Plotly Pie Chart using the calculated counts
    fig = px.pie(
        gender_counts, 
        values='Count', 
        names='Gender', 
        title='**Distribution of Drug Users by Gender**',
        # Set text to show percentage and label inside the slices
        # 'percent' will match the autopct='%1.1f%%' from your original code
        hole=0.3, # Optional: makes it a donut chart for better central text space
    )
    
    # Optional: Customize the appearance for better readability
    fig.update_traces(
        textposition='inside', 
        textinfo='percent+label',
        marker=dict(line=dict(color='#000000', width=1))
    )
    
    fig.update_layout(
        uniformtext_minsize=12, 
        uniformtext_mode='hide',
        # Equal aspect ratio is default for Plotly pie charts but can be ensured
        autosize=True,
        margin=dict(t=50, b=0, l=0, r=0)
    )
    
    # Display the Plotly chart in Streamlit
    st.plotly_chart(fig, use_container_width=True)

else:
    st.warning("Data is empty. Please ensure the DataFrame is loaded correctly.")

st.markdown("---")
st.caption("Application powered by Streamlit and Plotly.")
