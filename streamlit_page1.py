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
