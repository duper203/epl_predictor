import requests
import pandas as pd

## -------------------- get the score table ------------------- ##


## 3) 2023-2024
standings_url = "https://fbref.com/en/comps/9/schedule/Premier-League-Scores-and-Fixtures"
data = requests.get(standings_url)
shooting_2023_2024 = pd.read_html(data.text)[0]
shooting_2023_2024['Season'] = 2324

shooting = shooting_2023_2024


## merge all seasons
# shooting = pd.concat([shooting_2023_2024, shooting_2022_2023, shooting_2021_2022, shooting_2020_2021,shooting_2019_2020])
# shooting = pd.concat([shooting_2022_2023, shooting_2021_2022, shooting_2020_2021,shooting_2019_2020, shooting_2018_2019])



## -------------------- preprocessing ------------------- ##
## 1 - Wk : float -> int
# Replace non-finite values (NA or inf) with a default value, such as 0
shooting['Wk'].fillna(0, inplace=True)
shooting['Wk'] = shooting['Wk'].astype(int)




## 2 - Score : 3-1 -> 3 & 1 in different column

# split by '-'
shooting['Score'].str.split('–')
shooting['Home_Score'] = shooting['Score'].str[0]
shooting['Away_Score'] = shooting['Score'].str[2]

# Replace NaN values in the 'Home_Score' column with -1
shooting['Home_Score'].fillna(-1, inplace=True)
shooting['Away_Score'].fillna(-1, inplace=True)

# str -> int
shooting['Home_Score'] = shooting['Home_Score'].astype(int)
shooting['Away_Score'] = shooting['Away_Score'].astype(int)



## 3 - Delete "Match Report" column
shooting.drop(columns=['Match Report'], inplace=True)
shooting.drop(columns=['Notes'], inplace=True)

##4 - Delete Rows that are blank == no matches
shooting = shooting[shooting['Wk'] != 0]

##5 - Sorted by 'Wk' of matches (for example: one of the week 2 matches was on 2023-10-03)
shooting.sort_values(by=['Date', 'Wk'], inplace=True)


## ---------- download to csv ---------- ##
shooting.to_csv("EPL_23_24season.csv")