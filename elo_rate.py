import pandas as pd

df = pd.read_csv("premier_league_scores_and_fixtures.csv")

## -------------------- Elo ratings dictionary by teams ------------------- ##
## 1 Initialize Elo ratings dictionary
# 1600 : the mid number between 200~3000
teams = df['Home'].unique().tolist()
# print(teams)
elo_ratings = {team: 1600 for team in set(teams)} 

# adjustinng K
K = 30  # adjustinng K

## -------------------- function: calculate  expected score ------------------- ##

def expected_score(rating1, rating2):
    return 1 / (1 + 10**((rating2 - rating1) / 400))

## -------------------- function: update Elo ratings ------------------- ##

def update_elo_ratings(home_team, away_team, home_goals, away_goals):
    home_rating = elo_ratings[home_team]
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


## -------------------- main ------------------- ##

for index, row in df.iterrows():
    update_elo_ratings(row['Home'], row['Away'], row['Home_Score'], row['Away_Score'])


print(elo_ratings)