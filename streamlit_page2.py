import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

st.title("EPL PREDICTOR")
st.header('', divider='rainbow')

##---CHART-----------------------------------------------------------------------------------## 

st.header('EPL : Points Prediction')


all_sim_df = pd.read_csv('./simulation_data _step6/step6_all_simulations_results.csv')
av_pts_df = pd.read_csv('./simulation_data _step6/step6_average_points.csv')
rank_pb_df = pd.read_csv('./simulation_data _step6/step6_rank_probabilities.csv')
rank_count_df = pd.read_csv('./simulation_data _step6/step6_rankings_count.csv')


## --- combine data files
average_points = av_pts_df[['Team', 'Average Points']]
rank_probabilities = rank_pb_df.set_index('Team')
rankings_count = rank_count_df.set_index('Team')

combined_data = average_points.copy()
combined_data['Expected Number of Points'] = np.nan
combined_data['Qualify for UCL'] = np.nan
combined_data['Win Premier League'] = np.nan 
combined_data['Relegate'] = np.nan

for team in combined_data['Team']:
    if team in rank_probabilities.index:
        combined_data.loc[combined_data['Team'] == team, 'Expected Number of Points'] = int(average_points.loc[average_points['Team'] == team, 'Average Points'])
        combined_data.loc[combined_data['Team'] == team, 'Qualify for UCL'] = f"{rank_probabilities.loc[team, '1'] * 100:.1f}%" if rank_probabilities.loc[team, '1'] * 100 >= 1.0 else "<1%"
        combined_data.loc[combined_data['Team'] == team, 'Win Premier League'] = f"{rank_probabilities.loc[team, '1'] * 100:.1f}%" if rank_probabilities.loc[team, '1'] * 100 >= 1.0 else "<1%"
        combined_data.loc[combined_data['Team'] == team, 'Relegate'] = f"{rank_probabilities.loc[team, '20'] * 100:.1f}%" if rank_probabilities.loc[team, '20'] * 100 >= 1.0 else "<1%"

combined_data['Expected Number of Points'] = pd.to_numeric(combined_data['Expected Number of Points'], errors='coerce').astype(int)

combined_data.drop(columns=['Average Points'], inplace=True)

combined_data.set_index('Team', inplace=True)
combined_data = combined_data.nlargest(20, 'Expected Number of Points')

# Visualization
fig, ax = plt.subplots(figsize=(14, 10))
ax.axis('off')
table_data = [combined_data.reset_index().columns.values.tolist()] + combined_data.reset_index().values.tolist()
table = ax.table(cellText=table_data, cellLoc='center', loc='center')

table.auto_set_font_size(False)
table.set_fontsize(12)
table.scale(1.5, 1.5)

header_cells = [table[(0, col)] for col in range(len(combined_data.columns) + 1)]
for cell in header_cells:
    cell.set_fontsize(14)
    cell.set_text_props(weight='bold', color='white')
    cell.set_facecolor('#40466e')

for i in range(1, len(table_data)):
    for j in range(len(table_data[0])):
        cell = table[(i, j)]
        if j == 0:
            cell.set_text_props(weight='bold')
        if table_data[i][j] == '✔':
            cell.set_facecolor('#c6efce')
            cell.set_text_props(color='#006100')
        elif table_data[i][j] == '✘':
            cell.set_facecolor('#ffc7ce')
            cell.set_text_props(color='#9c0006')
        else:
            cell_value = str(table_data[i][j])
            if '%' in cell_value:
                if cell_value == '<1%':
                    cell.set_facecolor('white')
                else:
                    value = float(cell_value.strip('%'))
                    if value >= 50.0:
                        cell.set_facecolor('#ffcccc')  # Light Red for highest possibility
                        cell.set_text_props(color='black')
                    elif value >= 10.0:
                        cell.set_facecolor('#ffd9b3')  # Light Orange for over 10%
                        cell.set_text_props(color='black')
                    elif value >= 1.0:
                        cell.set_facecolor('#ffffcc')  # Light Yellow for other values
                        cell.set_text_props(color='black')
                    else:
                        cell.set_facecolor('white')
            else:
                cell.set_facecolor('#f0f0f0')

for i, col in enumerate(table_data[0]):
    table.auto_set_column_width(i)

plt.subplots_adjust(left=0.2, right=0.8, top=0.9, bottom=0.1)

st.pyplot(plt)
