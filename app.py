# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

from ast import In
from datetime import date
from turtle import width
from pandas.io.formats import style
from pandas.io.parquet import FastParquetImpl
import dash
from dash import dcc, dash_table
from dash import html
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template

dbc_css = ("https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates@V1.0.2/dbc.min.css")
load_figure_template('minty')
app = dash.Dash(__name__,
            external_stylesheets=[dbc.themes.BOOTSTRAP])

# reading in the next 7 day averages and the sentiment for each day
df = pd.read_csv('next_7_avgs_with_sentiment.csv')
df['date'] = pd.to_datetime(df['date'], format="%Y-%m-%d")
players = pd.read_csv('NBA-data\\data\\players.csv')

# importing all tweets
all_tweets = pd.read_json('Twitter-data\\data\\all_tweets.json', orient='records')
all_tweets = all_tweets.merge(players, how='left', on='player_id')
all_tweets_tbl = all_tweets.loc[:, ['player_name', 'Text', 'Username', 'Verified', 'likes', 'replies', 'sentiment']]
all_tweets_tbl['Date'] = all_tweets.loc[:, 'Datetime'].dt.date


# importing each players seasona averages to comapare to next 7 day averages
season_averages = pd.read_csv('NBA-data\\data\\season_averages.csv')

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

# function to get the NBA season associated with each date
def get_szn(date):
    if date < pd.to_datetime('2013-05-01', format='%Y-%m-%d'):
        return 2012
    elif pd.to_datetime('2013-10-01', format='%Y-%m-%d') < date < pd.to_datetime('2014-05-01', format='%Y-%m-%d'):
        return 2013
    elif pd.to_datetime('2014-10-01', format='%Y-%m-%d') < date < pd.to_datetime('2015-05-01', format='%Y-%m-%d'):
        return 2014
    elif pd.to_datetime('2015-10-01', format='%Y-%m-%d') < date < pd.to_datetime('2016-05-01', format='%Y-%m-%d'):
        return 2015
    elif pd.to_datetime('2016-10-01', format='%Y-%m-%d') < date < pd.to_datetime('2017-05-01', format='%Y-%m-%d'):
        return 2016
    elif pd.to_datetime('2017-10-01', format='%Y-%m-%d') < date < pd.to_datetime('2018-05-01', format='%Y-%m-%d'):
        return 2017
    elif pd.to_datetime('2018-10-01', format='%Y-%m-%d') < date < pd.to_datetime('2019-05-01', format='%Y-%m-%d'):
        return 2018
    elif pd.to_datetime('2019-10-01', format='%Y-%m-%d') < date < pd.to_datetime('2020-05-01', format='%Y-%m-%d'):
        return 2019
    elif pd.to_datetime('2020-10-01', format='%Y-%m-%d') < date < pd.to_datetime('2021-05-01', format='%Y-%m-%d'):
        return 2020
    elif pd.to_datetime('2021-10-01', format='%Y-%m-%d') < date < pd.to_datetime('2022-05-01', format='%Y-%m-%d'):
        return 2021

# function that generates bar grpah comparing next 7 day averages with season averages
def daily_vs_szn_graph(player, date, szn, stats):
    selected_stats = stats
    next_7 = df[(df['player_name'] == player) & (df['date'] == date)]
    next_7 = next_7[selected_stats]
    next_7['cat'] = 'next7'
    szn_avg = season_averages[(season_averages['player_name'] == player) & (season_averages['season'] == szn)]
    szn_avg = szn_avg[selected_stats]
    szn_avg['cat'] = 'season'
    szn_vs_day = szn_avg.append(next_7)
    szn_vs_day.set_index('cat', inplace=True)
    szn_vs_day = szn_vs_day.transpose().reset_index()
    szn_vs_day_graph = px.bar(szn_vs_day, x='index', y=['season', 'next7'], barmode='group',
                                        labels={'index': 'Statistics', 'value':'Per Game'},
                                        title='Season Averages vs Next 7 day averages from {}'.format(
                                            date.strftime('%b %d, %Y')
                                        ))
    return szn_vs_day_graph
    
# making Davion Mitchell the default graph
df_davion = df[df['player_name'] == 'Davion Mitchell']
fig = px.bar(df_davion, x="date", y="total_tweets")

# making a graph with sentiment on Davion Mitchell for most recent date
recent_date = df_davion['date'].max()
daily_davion_sent = get_daily_sent('Davion Mitchell', recent_date)
daily_sent_graph = px.bar(daily_davion_sent, x='sentiment', y='tot',
                            title='Sentiment Surronding Davion Mitchell on {}'.format(recent_date.strftime("%b %d, %Y")))


app.layout = html.Div(children=[
    html.H1(children='NBA Player Twitter Sentiment', style={'textAlign':'center'}),

    html.Div(children='''
        This is a dashboard that can be used to examine the sentiment in the online community surronding certain NBA players
    ''', style={'textAlign': 'center'}),

    html.Div([ 

        html.Div([
            dcc.Dropdown(
                id='name-dropdown',
                options=[{'label': i, 'value': i} for i in df['player_name'].unique()],
                value='Davion Mitchell'
            )
        ], style={'width':'48%', 'display':'inline-block'}),

        html.Div([
            dcc.Dropdown(
                id='season-dropdown',
                options = [{'label': '2021-22', 'value': 2021}],
                value=[2021],
                multi=True
            )
        ], style={'width':'48%', 'float':'right', 'display':'inline-block'}),
    ]),
    dcc.Graph(
        id='total-tweets-graph',
        figure=fig
    ),
    html.Div([
        dcc.Graph(
            id='daily-sentiment-graph',
            clickData={'points': [{'x': recent_date}]}
        )
    ], style={'width':'50%', 'float': 'left', 'display':'inline-block', "padding":20}),
    html.Div([
        dcc.Dropdown(
                id='stats-dropdown',
                options = [{'label': 'PTS', 'value': 'PTS'},
                            {'label': 'REB', 'value': 'REB'},
                            {'label': 'AST', 'value': 'AST'},
                            {'label': 'STL', 'value': 'STL'},
                            {'label': 'BLK', 'value': 'BLK'},
                            {'label': 'FG PCT', 'value': 'FG_PCT'},
                            {'label': 'FG3_PCT', 'value': 'FG3_PCT'},
                            {'label': 'TO', 'value': 'TOV'},
                            {'label': '+/-', 'value': 'PLUS_MINUS'},
                            {'label': 'OREB', 'value': 'OREB'},
                            {'label': 'DREB', 'value': 'DREB'},
                            {'label': 'PIE', 'value': 'PIE'},],
                value=['PTS', 'REB', 'AST'],
                multi=True
            ),
        dcc.Graph(
            id='daily-vs-season-graph',
            clickData={'points': [{'x': recent_date}]}
        )
    ], style={'width':'50%', 'float': 'right', 'padding':10}),
    html.Div(id='tweets_title'),
    html.Div(id='tweets_tbl', style={'margin-left':'1%', 'margin-right':'1%', "paddingBottom":'5%'}),

])

@app.callback(
    Output('total-tweets-graph', 'figure'),
    Input('name-dropdown', 'value'),
    Input('season-dropdown', 'value'))
def update_graph(name, seasons):
    df_player = df[df['player_name'] == name]
    df_player = df_player[df_player['season'].isin(seasons)]
    fig = px.bar(df_player, x="date", y="total_tweets")
    if name in ['LeBron James', 'Kevin Durant', 'Stephen Curry']:
        y_title = '# of Tweets w/ more than 300 likes'
    else:
        y_title = '# of Tweets w/ more than 100 likes'
    fig.update_yaxes(title=y_title)
    return fig

@app.callback(
    Output('season-dropdown', 'options'),
    Input('name-dropdown', 'value'))
def set_szn_options(selected_name):
    df_player = df[df['player_name'] == selected_name]
    return [{'label':"{}-{}".format(i, int(str(i)[-2:])+1), 'value':i} for i in df_player['season'].unique()]


@app.callback(
    Output('daily-sentiment-graph', 'figure'),
    Input('total-tweets-graph', 'clickData'),
    Input('name-dropdown', 'value'))
def update_daily_sentiment(clickData, player):
    if clickData:
        date = pd.to_datetime(clickData['points'][0]['x'], infer_datetime_format=True)
        daily_sent_df = get_daily_sent(player, date)
        fig = px.bar(daily_sent_df, x='sentiment', y='tot',
                    title='Sentiment Surronding {} on {}'.format(player, date.strftime("%b %d, %Y")))
        return fig
    else:
        return daily_sent_graph

@app.callback(
    Output('daily-vs-season-graph', "figure"),
    Input('total-tweets-graph', 'clickData'),
    Input('name-dropdown', 'value'),
    Input('stats-dropdown', 'value'))
def update_daily_vs_season(clickData, player, stats):
    selected_stats = stats
    if clickData:
        date = pd.to_datetime(clickData['points'][0]['x'], infer_datetime_format=True)
        szn = get_szn(date)
        return daily_vs_szn_graph(player, date, szn, selected_stats)
    else:
        date = recent_date
        szn = get_szn(date)
        return daily_vs_szn_graph(player, date, szn, selected_stats)

@app.callback(
    Output('tweets_tbl', 'children'),
    Input('total-tweets-graph', 'clickData'),
    Input('name-dropdown', 'value'))
def update_tweets(clickData, player):
    if clickData:
        date = pd.to_datetime(clickData['points'][0]['x'], infer_datetime_format=True)
    else:
        date = recent_date

    players_tweets = all_tweets_tbl[(all_tweets_tbl['player_name'] == player) &
         (all_tweets_tbl['Date'] == date.date())]
    return dash_table.DataTable(data = players_tweets.to_dict('records'),
                    columns = [{'name': i, 'id': i} for i in players_tweets.columns],
                    sort_action='native',
                    fixed_rows={'headers': True},
                    style_table={
                        'height': 600
                        },
                    style_data={
                        'whiteSpace': 'normal'
                    },
                    style_cell_conditional=[
                        {'if': {'column_id': 'player_name'},
                        'width': '150px'},
                        {'if': {'column_id': 'Text'},
                        'width': '1000px'},
                        {'if': {'column_id': 'Username'},
                        'width': '200px'},
                        {'if': {'column_id': 'replies'},
                        'width': '90px'}
                    ],
                    style_cell={
                        'font-family':'sans-serif',
                        'paddingLeft':'10px',
                        'paddingRight':'10px',
                        'paddingTop':'15px',
                        'paddingBottom':'15px'
                    },
                    style_data_conditional = [
                        {
                            'if': {
                                    'filter_query': '{Verified} contains "true"',
                                'column_id': 'Verified'
                                },
                            'backgroundColor': '#1DA1F2',
                            'color': 'black',
                            'fontWeight':'bold'
                        },
                        {
                            'if':{
                                'filter_query': '{sentiment} contains "NEUTRAL"',
                                'column_id': 'sentiment'
                            },
                            'backgroundColor':'#D4D4D4'
                        },
                        {
                            'if':{
                                'filter_query': '{sentiment} contains "POSITIVE"',
                                'column_id': 'sentiment'
                            },
                            'backgroundColor':'green'
                        },
                        {
                            'if':{
                                'filter_query': '{sentiment} contains "NEGATIVE"',
                                'column_id': 'sentiment'
                            },
                            'backgroundColor':'red'
                        },
                        {
                            'if':{
                                'filter_query': '{sentiment} contains "MIXED"',
                                'column_id': 'sentiment'
                            },
                            'backgroundColor':'purple'
                        },
                    ]
                    )
@app.callback(
    Output('tweets_title', 'children'),
    Input('total-tweets-graph', 'clickData'),
    Input('name-dropdown', 'value'))
def update_tweets_title(clickData, player):
    if clickData:
        date = pd.to_datetime(clickData['points'][0]['x'], infer_datetime_format=True)
    else:
        date = recent_date

    tit = "Tweets regarding {} on {}".format(player, date.date())
    return html.H4(tit, style={'margin-left': '3%', 'padding':20})




if __name__ == '__main__':
    app.run_server(debug=True)