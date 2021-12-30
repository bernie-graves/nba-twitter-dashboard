
def twitter_search(query, results, begin_date, end_date, file_name):
    # TODO: Function to use snscrape to scrape Twitter
    pass


def clean_json(json, new_json):
    # TODO: Function to format the JSON result from twitter_search()
    pass


def to_df(json, verified=False):
    # TODO: function to transform cleaned json to a Pandas DF
    pass


def get_player_data(player, season):
    # TODO: function to use nba_api to get player gamelogs into Pandas DF
    pass


def sentiment_analysis(tweet):
    # TODO: function to run sentiment analysis model on a single tweet
    # use TextBlob package from pretrained model
    pass


def total_sentiment(df, day):
    # TODO: function to total the sentiment for a day
    # could be total of 0 and 1's or percents for sentiment
    pass


def corr_sentiment_stat(tweets_df, stats_df, stat, begin, end):
    # TODO: function that finds correlation between sentiment and next 7 day stats
    # Needs to compare sentiment to future stats so that we can tell if the sentiment is
    # affecting performance
    # Also likely to have negative tweets after a bad performance
    # returns a list of correlations
    pass
