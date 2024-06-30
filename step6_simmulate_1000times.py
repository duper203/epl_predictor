import numpy as np
import pandas as pd

# Elo Model and Simulation Classes
class EloModel:
    def __init__(self, k=29.5, hfa=43):
        self.k = k
        self.hfa = hfa

    def expected_score(self, rating_a, rating_b):
        return 1 / (1 + 10 ** ((rating_b - rating_a) / 400))

    def probability(self, home_rating, away_rating):
        adjusted_home_rating = home_rating + self.hfa
        return self.expected_score(adjusted_home_rating, away_rating)

    def update_elo(self, home_rating, away_rating, result):
        adjusted_home_rating = home_rating + self.hfa
        home_expected = self.expected_score(adjusted_home_rating, away_rating)
        away_expected = self.expected_score(away_rating, adjusted_home_rating)

        home_actual = result[0]
        away_actual = result[1]

        new_home_rating = home_rating + self.k * (home_actual - home_expected)
        new_away_rating = away_rating + self.k * (away_actual - away_expected)

        return new_home_rating, new_away_rating

class Simulation:
    def __init__(self, elo_model):
        self.elo_model = elo_model

    def simulated_one_possible_season(self, current_n_points, df_remaining_matches, elo_ratings):
        for _, match in df_remaining_matches.iterrows():
            home_team_id = match["Home"]
            away_team_id = match["Away"]

            p_home = self.elo_model.probability(
                elo_ratings[home_team_id], elo_ratings[away_team_id]
            )

            result = np.random.choice([1, 0], p=[p_home, 1 - p_home])

            if result == 1:
                current_n_points[home_team_id] += 3
                home_team_elo, away_team_elo = self.elo_model.update_elo(
                    elo_ratings[home_team_id], elo_ratings[away_team_id], [1, 0]
                )
            else:
                current_n_points[away_team_id] += 3
                home_team_elo, away_team_elo = self.elo_model.update_elo(
                    elo_ratings[home_team_id], elo_ratings[away_team_id], [0, 1]
                )

            elo_ratings[home_team_id] = home_team_elo
            elo_ratings[away_team_id] = away_team_elo

        return current_n_points

# Initialize model and simulation
elo_model = EloModel()
simulation = Simulation(elo_model)

# Load data and initialize ratings
df_season2324 = pd.read_csv("EPL_23_24season.csv")
df_remaining_matches = df_season2324
elo_ratings = {
    'Fulham': 1590.4520733001257, "Nott'ham Forest": 1577.7896459888827, 
    'Bournemouth': 1528.8001104169223, 'Everton': 1568.1129597609636, 
    'Leeds United': 1504.7515778679863, 'West Ham': 1588.7384037927798, 
    'Huddersfield': 1398.5420184021978, 'Aston Villa': 1706.3432551756077, 
    'Burnley': 1546.1968630924457, 'Sheffield Utd': 1484.2027593402315, 
    'Cardiff City': 1501.6017089043262, 'Manchester Utd': 1760.008159682275, 
    'Watford': 1426.9645240434695, 'Newcastle Utd': 1748.0369420328332, 
    'Leicester City': 1552.793101627741, 'Liverpool': 1795.9256890722083, 
    'Brentford': 1699.2979697517358, 'Southampton': 1463.8772027379066, 
    'Wolves': 1582.5470683905176, 'Brighton': 1685.872684804144, 
    'Tottenham': 1675.0226507994428, 'Arsenal': 1789.9947344294567, 
    'Norwich City': 1411.811545638283, 'Crystal Palace': 1611.7268785716935, 
    'Chelsea': 1603.9447589979388, 'West Brom': 1499.7016773393257, 
    'Manchester City': 1896.9430360385604,
    'Luton Town': 1412.439,
}

# Set up the simulation to run 1000 times
n_simulations = 1000

# Initialize dictionaries to accumulate results
accumulated_points = {team: 0 for team in elo_ratings.keys()}
rankings_count = {team: {i: 0 for i in range(1, len(elo_ratings) + 1)} for team in elo_ratings.keys()}

# Initialize a DataFrame to store all simulation results
all_simulations_results = pd.DataFrame()

# Run the simulation 1000 times
for i in range(n_simulations):
    current_n_points = {team: 0 for team in elo_ratings.keys()}
    elo_ratings_init = elo_ratings.copy()
    
    # Simulate one season
    updated_points = simulation.simulated_one_possible_season(current_n_points, df_remaining_matches, elo_ratings_init)
    
    # Accumulate points
    for team, points in updated_points.items():
        accumulated_points[team] += points
    
    # Determine rankings
    sorted_teams = sorted(updated_points.items(), key=lambda item: item[1], reverse=True)
    for rank, (team, points) in enumerate(sorted_teams, start=1):
        rankings_count[team][rank] += 1
    
    # Add results of this simulation to the DataFrame
    simulation_results = pd.DataFrame(updated_points, index=[i])
    all_simulations_results = pd.concat([all_simulations_results, simulation_results])

# Calculate average points
average_points = {team: points / n_simulations for team, points in accumulated_points.items()}

# Convert rankings_count to DataFrame for easier analysis
rankings_df = pd.DataFrame(rankings_count).T
rankings_df.index.name = 'Team'


# Calculate the probability of each rank for each team
rank_probabilities = rankings_df.apply(lambda x: x / n_simulations)
rank_probabilities.index.name = 'Team'


rankings_df.to_csv('step6_rankings_count.csv')
all_simulations_results.to_csv('step6_all_simulations_results.csv')
rank_probabilities.to_csv('rank_probabilities.csv')


average_points_df = pd.DataFrame.from_dict(average_points, orient='index',columns=['Average Points'])
average_points_df.index.name = 'Team'
average_points_df_sorted = average_points_df.sort_values(by='Average Points', ascending=False)
average_points_df_sorted['Rank'] = range(1, len(average_points_df_sorted) + 1)

average_points_df_sorted.to_csv('step6_average_points.csv')





