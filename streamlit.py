import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

#---TITLE-----------------------------------------------------------------------------------# 
st.title("EPL PREDICTOR")
st.header('', divider='rainbow')

#---CHART-----------------------------------------------------------------------------------# 
st.header('EPL Season Simulation Probabilities')

# Load data
prob_file_path = './simulation_data _step6/step6_rank_probabilities.csv'
probabilities_df = pd.read_csv(prob_file_path)

# 'Team' == index 
probabilities_df.set_index('Team', inplace=True)
probabilities_df = probabilities_df.astype(float)
df_percentage = probabilities_df * 100

# Sort the DataFrame by the highest probability of achieving the top rank (Rank 1)
df_sorted_by_rank1 = df_percentage.sort_values(by='1', ascending=False)
df_sorted_by_rank1 = df_sorted_by_rank1.loc[:, '1':'20']

# Filter out teams with all probabilities equal to 0
df_non_zero = df_sorted_by_rank1[(df_sorted_by_rank1.T != 0).any()]

# Filter out values less than 5% and set them to NaN
df_filtered_non_zero = df_non_zero[df_non_zero >= 5].fillna(0)

def annotate_heatmap(ax, data, textcolors=["black", "white"], threshold=None, **textkw):
    """
    A function to annotate a heatmap.
    """
    from matplotlib.colors import Normalize

    if threshold is not None:
        threshold = Normalize(vmin=np.nanmin(data.values), vmax=np.nanmax(data.values))(threshold)
    else:
        threshold = Normalize(vmin=np.nanmin(data.values), vmax=np.nanmax(data.values))(data.values.max()) / 2.

    kw = dict(horizontalalignment="center",
              verticalalignment="center")
    kw.update(textkw)

    texts = []
    for i in range(data.shape[0]):
        for j in range(data.shape[1]):
            value = data.iloc[i, j]
            if value > 0:  # Skip zero values
                kw.update(color=textcolors[int(Normalize(vmin=np.nanmin(data.values), vmax=np.nanmax(data.values))(value) > threshold)])
                text = ax.text(j + 0.5, i + 0.5, f"{value:.1f}%", **kw)
                texts.append(text)

    return texts

# Create the heatmap with filtered data
plt.figure(figsize=(15, 10))
ax = sns.heatmap(df_filtered_non_zero, annot=False, fmt='.1f', cmap='Reds', cbar_kws={'label': 'Probability (%)'}, xticklabels=True, yticklabels=True)

annotate_heatmap(ax, df_filtered_non_zero)

# Set labels and title, with x label on the top
plt.xlabel('Rank Position', labelpad=10)
plt.ylabel('Team')
plt.title('Season Simulation Probabilities')
plt.xticks(rotation=90)
plt.gca().xaxis.set_label_position('top')
plt.gca().xaxis.tick_top()

# Show plot in Streamlit
st.pyplot(plt)


##---CHART-----------------------------------------------------------------------------------## 

st.header('Prediction for Points')


all_sim_df = pd.read_csv('./simulation_data _step6/step6_all_simulations_results.csv')
av_pts_df = pd.read_csv('./simulation_data _step6/step6_average_points.csv')
rank_pb_df = pd.read_csv('./simulation_data _step6/step6_rank_probabilities.csv')
rank_count_df = pd.read_csv('./simulation_data _step6/step6_rankings_count.csv')


## --- combine data files
average_points = av_pts_df[['Team', 'Average Points']]
rank_probabilities = rank_pb_df.set_index('Team')
rankings_count = rank_count_df.set_index('Team')

combined_data = average_points.copy()
combined_data['Points'] = np.nan
combined_data['Qualify for UCL'] = np.nan
combined_data['Win Premier League'] = np.nan 

for team in combined_data['Team']:
    if team in rank_probabilities.index:
        combined_data.loc[combined_data['Team'] == team, 'Points'] = int(average_points.loc[average_points['Team'] == team, 'Average Points'])
        combined_data.loc[combined_data['Team'] == team, 'Qualify for UCL'] = '✔' if rank_probabilities.loc[team, '1'] * 100 > 50 else '✘'
        combined_data.loc[combined_data['Team'] == team, 'Win Premier League'] = '✔' if rank_probabilities.loc[team, '1'] * 100 > 50 else '✘'

combined_data.set_index('Team', inplace=True)

combined_data = combined_data.nlargest(20, 'Points')



## --- combine data files

combined_data['Points'] = combined_data['Points'].apply(lambda x: int(x) if pd.notnull(x) else 0)

# UCL qualification
combined_data['Qualify for UCL'] = '✘'
combined_data.loc[combined_data.head(4).index, 'Qualify for UCL'] = '✔'

# Winner of the Premier League
combined_data['Win Premier League'] = '✘'
combined_data.loc[combined_data.head(1).index, 'Win Premier League'] = '✔'

fig, ax = plt.subplots(figsize=(14, 10))
ax.axis('off')
table_data = [combined_data.reset_index().columns.values.tolist()] + combined_data.reset_index().values.tolist()
table = ax.table(cellText=table_data, cellLoc='center', loc='center')

# table style
table.auto_set_font_size(False)
table.set_fontsize(12)
table.scale(1.5, 1.5)

# header styling
header_cells = [table[(0, col)] for col in range(len(combined_data.columns) + 1)]
for cell in header_cells:
    cell.set_fontsize(14)
    cell.set_text_props(weight='bold', color='white')
    cell.set_facecolor('#40466e')

# color
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
            cell.set_facecolor('#f0f0f0')

# adjust plt
for i, col in enumerate(table_data[0]):
    table.auto_set_column_width(i)
plt.subplots_adjust(left=0.2, right=0.8, top=0.9, bottom=0.1)
# plt.show()

st.pyplot(plt, use_container_width=True)
