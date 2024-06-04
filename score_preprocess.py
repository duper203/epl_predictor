import requests
from bs4 import BeautifulSoup
import pandas as pd

# get the score table
standings_url = "https://fbref.com/en/comps/9/schedule/Premier-League-Scores-and-Fixtures"
data = requests.get(standings_url)
shooting = pd.read_html(data.text)[0]


## ----- preprocessing ----- ##
# Wk : float -> int
shooting['Wk'] = shooting['Score'].astype(int)
shooting[['Home_Goals', 'Away_Goals']] = shooting['Score'].str.split('-')

shooting['Home_Goals'] = shooting['Home_Goals'].astype(int)
shooting['Away_Goals'] = shooting['Away_Goals'].astype(int)

