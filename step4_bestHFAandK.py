import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv("premier_league_scores_and_fixtures.csv")

## -------------------- Elo ratings dictionary by teams ------------------- ##
# Initialize Elo ratings dictionary
# by 1600 : the mid number between 200~3000
teams = df['Home'].unique().tolist()
# print(teams)
elo_ratings = {team: 1500 for team in set(teams)} 


## -------------------- function: calculate  expected score ------------------- ##

def expected_score(rating1, rating2):
    return 1 / (1 + 10**((rating2 - rating1) / 400))

## -------------------- function: update Elo ratings ------------------- ##

def update_elo_ratings(home_team, away_team, home_goals, away_goals, K, HFA, elo_ratings):
    home_rating = elo_ratings[home_team]+HFA
    away_rating = elo_ratings[away_team]
    
    expected_home = expected_score(home_rating, away_rating)
    expected_away = expected_score(away_rating, home_rating)
    
    if home_goals > away_goals:
        actual_home, actual_away = 1, 0
    elif home_goals < away_goals:
        actual_home, actual_away = 0, 1
    else:
        actual_home, actual_away = 0.5, 0.5
    
    # Elo system Formula
    new_home_rating = home_rating + K * (actual_home - expected_home)
    new_away_rating = away_rating + K * (actual_away - expected_away)
    
    elo_ratings[home_team] = new_home_rating
    elo_ratings[away_team] = new_away_rating

#function to encode match
def encode_result(home_score, away_score):
    if home_score > away_score:
        return 1, 0
    elif home_score < away_score:
        return 0, 1
    else:
        return 0.5, 0.5
    
#### -------------------------------------------------------------------------------------------------------------------------------------------- ####

# K_values = np.arange(7, 25.1, 0.1)
# HFA_values = np.arange(45, 101, 1)
K_values = np.arange(7, 26, 0.5)
HFA_values = np.arange(0, 101, 5)

# Initialize error matrix
error_matrix = np.zeros((len(K_values), len(HFA_values)))

# Perform grid search
for i, K in enumerate(K_values):
    for j, HFA in enumerate(HFA_values):
        elo_ratings = elo_ratings.copy()
        squared_errors = []

        for _, row in df.iterrows():
            home_team = row['Home']
            away_team = row['Away']
            home_score = row['Home_Score']
            away_score = row['Away_Score']

            home_result, away_result = encode_result(home_score, away_score)

            home_rating = elo_ratings[home_team] + HFA
            away_rating = elo_ratings[away_team]

            expected_home = expected_score(home_rating, away_rating)
            expected_away = expected_score(away_rating, home_rating)

            update_elo_ratings(home_team, away_team, home_score, away_score, K, HFA, elo_ratings)

            squared_errors.append((expected_home - home_result)**2 + (expected_away - away_result)**2)

        mean_squared_error = np.mean(squared_errors)
        error_matrix[i, j] = mean_squared_error

print("plot")
# plot
K_grid, HFA_grid = np.meshgrid(K_values, HFA_values)
plt.contourf(K_grid, HFA_grid, error_matrix.T, 20, cmap='viridis')
plt.colorbar(label='Mean Squared Error')
plt.xlabel('K-factor')
plt.ylabel('Home Field Advantage')
plt.title('Mean Squared Error vs K-factor and Home Field Advantage')
plt.savefig('step4_mse_vs_k_and_hfa.png')

plt.show()

# Find the optimal K and HFA
# optimal_indices = np.unravel_index(np.argmin(error_matrix), error_matrix.shape)
# optimal_K = K_values[optimal_indices[0]]
# optimal_HFA = HFA_values[optimal_indices[1]]
# print(f"The optimal K-factor is: {optimal_K}")
# print(f"The optimal Home Field Advantage (HFA) is: {optimal_HFA}")

# # Apply the optimal K and HFA to update the ratings
# elo_ratings = elo_ratings.copy()
# for _, row in df.iterrows():
#     update_elo_ratings(row['Home'], row['Away'], row['Home_Score'], row['Away_Score'], optimal_K, optimal_HFA, elo_ratings)

# print(elo_ratings)