import pandas as pd
from dash.dependencies import Input, Output

# app = dash.Dash(__name__)

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options
df = pd.read_csv('next_7_avgs_with_sentiment.csv')
df['date'] = pd.to_datetime(df['date'], format="%Y-%m-%d")
players = pd.read_csv('NBA-data\\data\\players.csv')
df = df.merge(players, how='left', on='player_id')

# assigning a season column 
def assign_szn(row):
    if row['date'] < pd.to_datetime('2013-05-01', format='%Y-%m-%d'):
        return 2012
    elif pd.to_datetime('2013-10-01', format='%Y-%m-%d') < row['date'] < pd.to_datetime('2014-05-01', format='%Y-%m-%d'):
        return 2013
    elif pd.to_datetime('2014-10-01', format='%Y-%m-%d') < row['date'] < pd.to_datetime('2015-05-01', format='%Y-%m-%d'):
        return 2014
    elif pd.to_datetime('2015-10-01', format='%Y-%m-%d') < row['date'] < pd.to_datetime('2016-05-01', format='%Y-%m-%d'):
        return 2015
    elif pd.to_datetime('2016-10-01', format='%Y-%m-%d') < row['date'] < pd.to_datetime('2017-05-01', format='%Y-%m-%d'):
        return 2016
    elif pd.to_datetime('2017-10-01', format='%Y-%m-%d') < row['date'] < pd.to_datetime('2018-05-01', format='%Y-%m-%d'):
        return 2017
    elif pd.to_datetime('2018-10-01', format='%Y-%m-%d') < row['date'] < pd.to_datetime('2019-05-01', format='%Y-%m-%d'):
        return 2018
    elif pd.to_datetime('2019-10-01', format='%Y-%m-%d') < row['date'] < pd.to_datetime('2020-05-01', format='%Y-%m-%d'):
        return 2019
    elif pd.to_datetime('2020-10-01', format='%Y-%m-%d') < row['date'] < pd.to_datetime('2021-05-01', format='%Y-%m-%d'):
        return 2020
    elif pd.to_datetime('2021-10-01', format='%Y-%m-%d') < row['date'] < pd.to_datetime('2022-05-01', format='%Y-%m-%d'):
        return 2021

df['season'] = df.apply(assign_szn, axis=1)
print(df.info())