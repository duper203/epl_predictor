import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load data
df = pd.read_csv("premier_league_scores_and_fixtures.csv")

# Initialize Elo ratings
teams = df['Home'].unique().tolist()
elo_ratings = {team: 1600 for team in set(teams)}

# Functions
def expected_score(rating1, rating2):
    return 1 / (1 + 10**((rating2 - rating1) / 400))

def update_elo_ratings(home_team, away_team, home_goals, away_goals, K, HFA):
    home_rating = elo_ratings[home_team] + HFA
    away_rating = elo_ratings[away_team]
    
    expected_home = expected_score(home_rating, away_rating)
    expected_away = expected_score(away_rating, home_rating)
    
    if home_goals > away_goals:
        actual_home, actual_away = 1, 0
    elif home_goals < away_goals:
        actual_home, actual_away = 0, 1
    else:
        actual_home, actual_away = 0.5, 0.5
    
    new_home_rating = elo_ratings[home_team] + K * (actual_home - expected_home)
    new_away_rating = elo_ratings[away_team] + K * (actual_away - expected_away)
    
    elo_ratings[home_team] = new_home_rating
    elo_ratings[away_team] = new_away_rating

def encode_result(home_score, away_score):
    if home_score > away_score:
        return 1, 0
    elif home_score < away_score:
        return 0, 1
    else:
        return 0.5, 0.5

# Grid search for K and HFA
K_values = np.arange(15, 35.5, 0.5)
HFA_values = np.arange(0, 101, 1)
errors = np.zeros((len(K_values), len(HFA_values)))

for i, K in enumerate(K_values):
    for j, HFA in enumerate(HFA_values):
        ratings = elo_ratings.copy()
        squared_errors = []

        for _, row in df.iterrows():
            home_team = row['Home']
            away_team = row['Away']
            home_score = row['Home_Score']
            away_score = row['Away_Score']

            home_result, away_result = encode_result(home_score, away_score)

            home_rating = ratings[home_team] + HFA
            away_rating = ratings[away_team]

            expected_home = expected_score(home_rating, away_rating)
            expected_away = expected_score(away_rating, home_rating)

            update_elo_ratings(home_team, away_team, home_score, away_score, K, HFA)

            squared_errors.append((expected_home - home_result)**2 + (expected_away - away_result)**2)

        mean_squared_error = np.mean(squared_errors)
        errors[i, j] = mean_squared_error

# Plotting the results
K_values_grid, HFA_values_grid = np.meshgrid(K_values, HFA_values)
plt.contourf(K_values_grid, HFA_values_grid, errors.T, levels=50, cmap='viridis')
plt.colorbar(label='Mean Squared Error')
plt.xlabel('K-factor')
plt.ylabel('Home Field Advantage (HFA)')
plt.title('Mean Squared Error vs K-factor and Home Field Advantage (HFA)')
plt.savefig('step4_msq_&_contour.png')
plt.show()

# Best K and HFA
best_index = np.unravel_index(np.argmin(errors), errors.shape)
best_K = K_values[best_index[0]]
best_HFA = HFA_values[best_index[1]]
print(f"The best K-factor is: {best_K}")
print(f"The best Home Field Advantage (HFA) is: {best_HFA}")

##### RESULT ######
# The best K-factor is: 15.0
# The best Home Field Advantage (HFA) is: 47



# # Update elo ratings with best K and HFA
# elo_ratings = {team: 1600 for team in set(teams)}
# for index, row in df.iterrows():
#     update_elo_ratings(row['Home'], row['Away'], row['Home_Score'], row['Away_Score'], best_K, best_HFA)

# print(elo_ratings)