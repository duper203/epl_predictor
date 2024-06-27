
##### RESULT ######
# The best K-factor is: 29.5
# The best Home Field Advantage (HFA) is: 43

from step4_bestHFAandK import update_elo_ratings
import pandas as pd

# Initialize
df = pd.read_csv("premier_league_scores_and_fixtures.csv")
teams = df['Home'].unique().tolist()
elo_ratings = {team: 1600 for team in set(teams)}


best_K = 29.5
best_HFA = 43

# Update elo ratings with best K and HFA
for index, row in df.iterrows():
    update_elo_ratings(row['Home'], row['Away'], row['Home_Score'], row['Away_Score'], best_K, best_HFA, elo_ratings)

print(elo_ratings) 
# RESULT
# {'Fulham': 1590.4520733001257, "Nott'ham Forest": 1577.7896459888827, 
# 'Bournemouth': 1528.8001104169223, 'Everton': 1568.1129597609636, 
# 'Leeds United': 1504.7515778679863, 'West Ham': 1588.7384037927798, 
# 'Huddersfield': 1398.5420184021978, 'Aston Villa': 1706.3432551756077, 
# 'Burnley': 1546.1968630924457, 'Sheffield Utd': 1484.2027593402315, 
# 'Cardiff City': 1501.6017089043262, 'Manchester Utd': 1760.008159682275, 
# 'Watford': 1426.9645240434695, 'Newcastle Utd': 1748.0369420328332, 
# 'Leicester City': 1552.793101627741, 'Liverpool': 1795.9256890722083, 
# 'Brentford': 1699.2979697517358, 'Southampton': 1463.8772027379066, 
# 'Wolves': 1582.5470683905176, 'Brighton': 1685.872684804144, 
# 'Tottenham': 1675.0226507994428, 'Arsenal': 1789.9947344294567, 
# 'Norwich City': 1411.811545638283, 'Crystal Palace': 1611.7268785716935, 
# 'Chelsea': 1603.9447589979388, 'West Brom': 1499.7016773393257, 'Manchester City': 1896.9430360385604}