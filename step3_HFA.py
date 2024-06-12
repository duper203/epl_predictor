import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv("premier_league_scores_and_fixtures.csv")

## -------------------- Elo ratings dictionary by teams ------------------- ##
# Initialize Elo ratings dictionary
# by 1600 : the mid number between 200~3000
teams = df['Home'].unique().tolist()
# print(teams)
elo_ratings = {team: 1600 for team in set(teams)} 


## -------------------- function: calculate  expected score ------------------- ##

def expected_score(rating1, rating2):
    return 1 / (1 + 10**((rating2 - rating1) / 400))

## -------------------- function: update Elo ratings ------------------- ##

def update_elo_ratings(home_team, away_team, home_goals, away_goals, K, HFA):
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
K = 7.6 #from step2 py file  
HFA_values = np.arange(0, 101, 1)  # Home Field Advantage values from 0 to 100 in increments of 1
errors = []

for HFA in HFA_values:
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
    errors.append(mean_squared_error)

# Plotting the results
# plt.plot(HFA_values, errors)
# plt.xlabel('Home Field Advantage (HFA)')
# plt.ylabel('Mean Squared Error')
# plt.title('Mean Squared Error vs Home Field Advantage (HFA)')
# plt.savefig('step3_msq_&_hfa.png')
# plt.show()

# Best HFA
best_HFA = HFA_values[np.argmin(errors)]
print(f"The best Home Field Advantage (HFA) is: {best_HFA}") 
# result:  2

for index, row in df.iterrows():
    update_elo_ratings(row['Home'], row['Away'], row['Home_Score'], row['Away_Score'], K, best_HFA)

print(elo_ratings)