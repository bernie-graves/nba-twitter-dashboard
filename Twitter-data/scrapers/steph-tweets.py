import snscrape.modules.twitter as sntwitter
import pandas as pd
from datetime import datetime, timedelta
from nba_api.stats.static import players
player_dict = players.get_players()

# Creating list to append tweet data to
tweets_df = pd.DataFrame(columns=['Datetime', 'tweet_id', 'Text', 'Username',
                                 'Verified', 'likes', 'replies', 'player_id'])



players_nicknames = {'Stephen Curry':['Stephen Curry']}

players_exp = {'Stephen Curry':13}


# creating a dictionary with player names as keys and
# the dates during typical NBA seasons that each player 
# has been in the league
# going to search twitter on these dates
player_dates = {}
for player,e in players_exp.items():
    start_date = datetime.now() - timedelta(days=1)
    career_begin = datetime(2022-e, 10, 15)
    earliest = datetime(2012, 11, 4)
    dates = list()
    while start_date > career_begin and start_date > earliest:
        # selecting all dates Nov - Mar
        if int(start_date.strftime('%m')) in [11, 12, 1, 2, 3]:
            dates.append(start_date)
        # selecting dates in Apr before the 10th
        elif int(start_date.strftime('%m')) == 4 and int(start_date.strftime('%d')) < 10:
            dates.append(start_date)
        # Selecting dates in Oct after 15
        elif int(start_date.strftime('%m')) == 10 and int(start_date.strftime('%d')) > 15:
            dates.append(start_date)
        
        start_date -= timedelta(days=1)
    player_dates[player] = dates


for player, dates in player_dates.items():
    # getting nicknames for player - used as search item
    nicknames = players_nicknames[player]

    # getting the players id to put in final df
    player_obj = [x for x in player_dict if x['full_name'] == player][0]
    player_id = player_obj['id']

    # Iterate over player's dates
    for date in dates:
        start = date.strftime('%Y-%m-%d')
        end_dt = date + timedelta(days=1)
        end = end_dt.strftime('%Y-%m-%d')
        for nickname in nicknames:
            for tweet in sntwitter.TwitterSearchScraper('{} since:{} until:{} min_faves:300 min_replies:10 lang:en'.format(nickname, start, end)).get_items():
                tweets_df = tweets_df.append({'Datetime':tweet.date, 'tweet_id':tweet.id, 'Text':tweet.content, 
                                            'Username':tweet.user.username, 'Verified':tweet.user.verified,
                                             'likes':tweet.likeCount, 'replies':tweet.replyCount,'player_id': player_id},
                                             ignore_index=True)
                print(start + '----' + nickname)

                    
print(tweets_df.sample(10))
tweets_df.to_json('steph_tweets_en_master.json', orient='index')