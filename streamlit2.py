import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
prob_file_path = './simulation_data _step6/step6_rank_probabilities.csv'
probabilities_df = pd.read_csv(prob_file_path)


# Ensure the 'Team' column is set as the index and convert to float for heatmap
probabilities_df.set_index('Team', inplace=True)
dprobabilities_dff = probabilities_df.astype(float)

# Convert probabilities to percentages for better visualization
df_percentage = probabilities_df * 100

# Sort the teams by the highest probability for the first rank (column '1')
df_sorted = df_percentage.sort_values(by='1', ascending=False)

# Select only up to rank 20
df_sorted = df_sorted.loc[:, '1':'20']

# Define a function to format the annotations
def annotate_heatmap(ax, data, textcolors=["black", "white"], threshold=None, **textkw):
    """
    A function to annotate a heatmap.
    """
    from matplotlib.colors import Normalize

    if threshold is not None:
        threshold = Normalize(vmin=np.min(data.values), vmax=np.max(data.values))(threshold)
    else:
        threshold = Normalize(vmin=np.min(data.values), vmax=np.max(data.values))(data.values.max()) / 2.

    # Set default alignment to center
    kw = dict(horizontalalignment="center",
              verticalalignment="center")
    kw.update(textkw)

    # Loop over the data and create a `Text` for each "pixel".
    # Change the text's color depending on the data.
    texts = []
    for i in range(data.shape[0]):
        for j in range(data.shape[1]):
            value = data.iloc[i, j]
            kw.update(color=textcolors[int(Normalize(vmin=np.min(data.values), vmax=np.max(data.values))(value) > threshold)])
            text = ax.text(j + 0.5, i + 0.5, f"{value:.1f}%", **kw)
            texts.append(text)

    return texts

# Plot the heatmap with the desired adjustments
plt.figure(figsize=(15, 10))
ax = sns.heatmap(df_sorted, annot=False, fmt='.1f', cmap='coolwarm', cbar_kws={'label': 'Probability (%)'}, xticklabels=True)

# Add annotations manually
annotate_heatmap(ax, df_sorted)

# Set labels and title, with x label on the top
plt.xlabel('Rank Position', labelpad=10)
plt.ylabel('Team')
plt.title('Season Simulation Probabilities')
plt.xticks(rotation=90)
plt.gca().xaxis.set_label_position('top')
plt.gca().xaxis.tick_top()

# Show plot
# plt.show()

st.pyplot(plt, use_container_width=True)




