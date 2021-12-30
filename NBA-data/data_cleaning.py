import pandas as pd
from nba_api.stats.static import players

# reading in the data
data = pd.read_csv('master_adv.csv', dtype={'Game_ID':str, 'SEASON_ID':str, 'Player_ID':str})

# dropping empty columns and dupliucate rows
data.dropna(axis='columns', inplace=True)
data.drop(['Unnamed: 0', 'Unnamed: 0.1'], axis='columns', inplace=True)
data.drop_duplicates(inplace=True)

# dropping unneded columns
gamelog = data.drop(['VIDEO_AVAILABLE', 'GAME_DATE', 'MATCHUP'], axis='columns')
gamelog.to_csv('gamelog.csv', index=False)

# Creating seperate table with just data on games
# will reduce repeated data in database
# for the 'games' table in database
games = data[['Game_ID', 'MATCHUP', 'GAME_DATE']]
games['GAME_DATE'] = pd.to_datetime(games['GAME_DATE'], format="%b %d, %Y", errors='coerce')
games.drop_duplicates('Game_ID', inplace=True)
print(games.info())
games.to_csv('games.csv', index=False)

# Creating table with for players
# containing player_id, name and years of experience
player_dict = players.get_players()
players = {'Davion Mitchell':1, 'Evan Mobley':1, 'LeBron James':19,
                'Kevin Durant':14, 'Tyrese Haliburton':2, 'Buddy Hield':6,
                'Joel Embiid':6,'Josh Hart':5, 'Kyle Kuzma':5, 'Stephen Curry':13, 
                'LaMelo Ball':2, 'Dejounte Murray':6, 'Shai Gilgeous-Alexander':4,
                'Nikola Jokic':7, 'Julius Randle':8, 'Scottie Barnes':1
}
player_df = pd.DataFrame(columns=['player_id', 'player_name', 'exp'])
for player, exp in players.items():
    player_obj = [x for x in player_dict if x['full_name'] == player][0]
    player_id = player_obj['id']
    player_df.loc[len(player_df.index)] = [player_id, player, exp]

player_df.to_csv('players.csv', index=False)


print(gamelog.info())
print(games.info())
print(player_df.info())