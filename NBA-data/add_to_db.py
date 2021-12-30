import mysql.connector
import pandas as pd

connection = mysql.connector.connect(user='admin', password='Bo&Chuck15', 
                                    host='nba-twitter-db.cawrdqygknxl.us-east-2.rds.amazonaws.com',
                                    database='nba_twitter_db')

cursor = connection.cursor()

# cursor.execute("""CREATE TABLE gamelogs(
# SEASON_ID integer,
# Player_ID integer,
# Game_ID SERIAL PRIMARY KEY,
# GAME_DATE text,
# MATCHUP text,
# WL text,
# MIN integer,
# FGM integer,
# FGA integer,
# FG_PCT float,
# FG3M integer,
# FG3A integer,
# FG3_PCT float,
# FTM integer,
# FTA integer,
# FT_PCT float,
# OREB integer,
# DREB integer,
# REB integer,
# AST integer,
# STL integer,
# BLK integer,
# TOV integer,
# PF integer,
# PTS integer,
# PLUS_MINUS integer,
# VIDEO_AVAILABLE integer)""")

sql = """
SELECT * FROM  gamelogs
"""
print(pd.read_sql(sql, con=connection))
# connection.commit()