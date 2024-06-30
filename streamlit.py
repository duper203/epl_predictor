import streamlit as st
import pandas as pd

##---TITLE-----------------------------------------------------------------------------------## 
st.title("EPL PREDICTOR")
st.header('This is a header with a divider', divider='rainbow')

##---CHART-----------------------------------------------------------------------------------## 

st.header('Probabilities of Teams Achieving Each Rankings in the League')

file_path = 'rank_probabilities.csv'
probabilities_df = pd.read_csv(file_path)

# Extract team names
teams = probabilities_df.iloc[:, 0].repeat(20).values

# Unpivot the probability data
probability_values = probabilities_df.iloc[:, 1:21].values.flatten()

# Create the ranking list
ranking = list(range(1, 21)) * 28

# Create the final DataFrame
chart_data = pd.DataFrame({
    "ranking": ranking,
    "probability": probability_values,
    "teams": teams
})


st.bar_chart(chart_data, x="ranking", y="probability", color="teams")


##---CHART-----------------------------------------------------------------------------------## 

df_avg_points = pd.read_csv("step6_average_points.csv")
st.data_editor(
    df_avg_points, 
    height=1020,
    
    
)