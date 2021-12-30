import pandas as pd
from nba_api.stats.static import players
from nba_api.stats.endpoints import playergamelog, boxscoreadvancedv2
player_dict = players.get_players()
import time

# df_adv_games_2021 = adv_gamelog_giannis.get_data_frames()[0]
# df_adv_games_2021.to_csv('adv_giannis_2021.csv')

def mine_gamelogs(player_name, season):
    player_obj = [x for x in player_dict if x['full_name'] == player_name][0]
    player_id = player_obj['id']
    gamelog = playergamelog.PlayerGameLog(
                player_id=player_id,
                season = season
    )
    gamelog_df = gamelog.get_data_frames()[0]
    return gamelog_df
if __name__ == '__main__':
    player_list = [ 'Davion Mitchell', 'Evan Mobley',
                    'LeBron James', 'Kevin Durant',
                    'Tyrese Haliburton', 'Buddy Hield', 'Joel Embiid',
                    'Josh Hart', 'Kyle Kuzma', 'Stephen Curry', 
                    'LaMelo Ball', 'Dejounte Murray', 
                    'Shai Gilgeous-Alexander', 'Nikola Jokic',
                    'Julius Randle', 'Scottie Barnes'
                    ]
    seasons = ['2012', '2013', '2014', '2015', '2016',
                '2017', '2018', '2019', '2020', '2021']

    master_df = pd.DataFrame(columns=['SEASON_ID','Player_ID', 'Game_ID',
                                ' GAME_DATE', 'MATCHUP','WL','MIN','FGM',
                                'FGA','FG_PCT'',FG3M','FG3A','FG3_PCT'',FTM',
                                'FTA','FT_PCT','OREB','DREB','REB','AST',
                                'STL','BLK','TOV','PF','PTS','PLUS_MINUS',
                                'VIDEO_AVAILABLE'])
    for player in player_list:
        for season in seasons:
            print(player + ' ' + season)
            df = mine_gamelogs(player, season)
            master_df = master_df.append(df)
            time.sleep(10)
    
    master_df.to_csv('master.csv')

    # for player in player_list:
    #     player_obj = [x for x in player_dict if x['full_name']
    #                     == player][0]
    #     player_id = player_obj['id']
    #     for season in seasons:
    #         gamelog = playergamelog.PlayerGameLog(
    #             player_id=player_id, season=season
    #         )

    #         gamelog_df = gamelog.get_data_frames()[0]
    #         master_df = master_df.append(gamelog_df)


    