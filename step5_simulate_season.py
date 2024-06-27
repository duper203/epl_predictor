import numpy as np
import pandas as pd
# from step4
# K = 29.5
# HFA = 43
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

elo_model = EloModel()
simulation = Simulation(elo_model)

# read data
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
    'Luton Town': 1500,
}
# Luton Town!!!!  -> was not in the elo rate : need to check


current_n_points = {team: 0 for team in elo_ratings.keys()}


# Simulate the season
updated_points = simulation.simulated_one_possible_season(current_n_points, df_remaining_matches, elo_ratings)
sorted_updated_points = dict(sorted(updated_points.items(), key=lambda item: item[1], reverse=True))

print(sorted_updated_points)
print(elo_ratings)
