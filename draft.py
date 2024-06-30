import pandas as pd

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


chart_data.to_csv('step7_chart_data.csv')

##--------------------------------------------------------------------------------------## 


