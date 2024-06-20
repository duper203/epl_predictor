import pandas as pd

df = pd.read_csv("EPL_23_24season.csv")
teams = df['Home'].unique().tolist()
elo_ratings = {team: 1600 for team in set(teams)} 

# Elo rating parameters
# K = 15
# HFA = 47

# K = 1
# HFA = 64

# K = 5.5
# HFA = 45

K = 7.6
HFA = 45

def update_elo(home_team, away_team, home_goals, away_goals, elo_ratings, K, HFA):
    home_elo = elo_ratings[home_team] + HFA
    away_elo = elo_ratings[away_team]
    
    expected_home = 1 / (1 + 10 ** ((away_elo - home_elo) / 400))
    expected_away = 1 - expected_home
    
    if home_goals > away_goals:
        actual_home = 1
        actual_away = 0
    elif home_goals < home_goals:
        actual_home = 0
        actual_away = 1
    else:
        actual_home = 0.5
        actual_away = 0.5
    
    elo_ratings[home_team] += K * (actual_home - expected_home)
    elo_ratings[away_team] += K * (actual_away - expected_away)
    
    return elo_ratings


def simulate_season(df, initial_elo, K, HFA, num_simulations=10000):
    teams = list(initial_elo.keys())
    results = {team: [] for team in teams}
    
    for _ in range(num_simulations):
        elo_ratings = initial_elo.copy()
        for _, row in df.iterrows():
            home_team = row['Home']
            away_team = row['Away']
            home_goals = row['Home_Score']
            away_goals = row['Away_Score']
            
            elo_ratings = update_elo(home_team, away_team, home_goals, away_goals, elo_ratings, K, HFA)
        
        for team in teams:
            results[team].append(elo_ratings[team])
    
    return results






simulation_results = simulate_season(df, elo_ratings, K, HFA, num_simulations=10000)



df_simulation_results = pd.DataFrame(simulation_results)
# simulation_results_csv_path = 'simulation_results.csv'
# df_simulation_results.to_csv(simulation_results_csv_path, index=False)
# the average Elo rating for each team
average_elo_ratings = df_simulation_results.mean().sort_values(ascending=False)

# descending order
for team, rating in average_elo_ratings.items():
    print(f"{team}: {rating:.2f}")