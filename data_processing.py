import pandas as pd

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

# function to get a players sentiment counts for a given date
def get_daily_sent(player, date):
    player_tweets = all_tweets[all_tweets['player_name'] == player]
    days_tweets = player_tweets[player_tweets['Datetime'].apply(get_date) == date.date()]
    days_sent = pd.DataFrame(columns=['sentiment', 'tot'])
    days_sent = days_sent.append({'sentiment':'Positive', 'tot': sum(days_tweets['sentiment'] == 'POSITIVE')}, ignore_index=True)
    days_sent = days_sent.append({'sentiment':'Negative', 'tot': sum(days_tweets['sentiment'] == 'NEGATIVE')}, ignore_index=True)
    days_sent = days_sent.append({'sentiment':'Neutral', 'tot': sum(days_tweets['sentiment'] == 'NEUTRAL')}, ignore_index=True)
    days_sent = days_sent.append({'sentiment':'Mixed', 'tot': sum(days_tweets['sentiment'] == 'MIXED')}, ignore_index=True)
    return days_sent

def get_date(date_obj):
    return date_obj.date()

if __name__ == '__main__':
    # Making a df with each players season averages
    gamelogs = pd.read_csv('NBA-data\\data\\gamelog.csv')
    players = pd.read_csv('NBA-data\\data\\players.csv')
    games = pd.read_csv('NBA-data\\data\\games.csv')

    gamelogs = gamelogs.merge(players, how='left', left_on='Player_ID', right_on='player_id')
    gamelogs = gamelogs.drop(['Player_ID'], axis=1)

    gamelogs = gamelogs.merge(games, how='left', on='Game_ID')
    gamelogs['date'] = pd.to_datetime(gamelogs['GAME_DATE'], infer_datetime_format=True)
    gamelogs = gamelogs.drop('GAME_DATE', axis=1)

    gamelogs['season'] = gamelogs.apply(assign_szn, axis=1)

    season_averages = gamelogs.groupby(['player_id', 'season']).mean().round(2)
    season_averages = season_averages.drop(['Game_ID', 'exp'], axis=1)
    season_averages = season_averages.merge(players, how='left', on='player_id')
    season_averages['season'] = season_averages['SEASON_ID'].astype(int).astype(str).str[1:]

    season_averages.to_csv('NBA-data\\data\\season_averages.csv')


    # assigning season to each day
    df = pd.read_csv('next_7_avgs_with_sentiment.csv')
    df['season'] = df['SEASON_ID'].astype(int).astype(str).str[1:]
    df['date'] = pd.to_datetime(df['date'], format="%Y-%m-%d")
    players = pd.read_csv('NBA-data\\data\\players.csv')
    df = df.merge(players, how='left', on='player_id')
    # df['season'] = df.apply(assign_szn, axis=1)
    df.to_csv('next_7_avgs_with_sentiment.csv')


