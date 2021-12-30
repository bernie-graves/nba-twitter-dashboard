import pandas as pd
from nba_api.stats.static import players
from nba_api.stats.endpoints import playergamelog, boxscoreadvancedv2
import time
player_dict = players.get_players()

def mine_adv_stat(game_id, player_id):
    # game_id is a string
    # player_id is integer
    master_df = pd.DataFrame(columns=['GAME_ID', 'PLAYER_ID', 'PIE'])
    for id in game_id:
        adv_gamelog =boxscoreadvancedv2.BoxScoreAdvancedV2( game_id=id)
        time.sleep(1)
        df_adv_gamelog = adv_gamelog.get_data_frames()[0]
        df_adv_player = df_adv_gamelog[df_adv_gamelog['PLAYER_ID'].isin(player_id)]
        df_adv_player = df_adv_player[['GAME_ID', 'PLAYER_ID', 'PIE']]
        master_df = master_df.append(df_adv_player)
    return master_df

if __name__ == '__main__':
    # df = mine_adv_stat('0022100386', 203507)
    # print(df)
    gamelogs = pd.read_csv('master.csv', dtype={'Game_ID':str})
    gamelogs['Player_ID'].astype('object')
    adv_df = mine_adv_stat(gamelogs['Game_ID'], gamelogs['Player_ID'])
    adv_df = adv_df.rename({'GAME_ID': 'Game_ID', 'PLAYER_ID': 'Player_ID'}, axis=1)
    print(adv_df.head())
    test_adv_final = pd.merge(gamelogs, adv_df, on=['Player_ID', 'Game_ID'])
    print(test_adv_final.head())
    test_adv_final.to_csv('master_adv.csv')