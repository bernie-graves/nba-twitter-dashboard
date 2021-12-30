# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

from pandas.io.parquet import FastParquetImpl
import dash
from dash import dcc
from dash import html
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output

app = dash.Dash(__name__)

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

df_davion = df[df['player_name'] == 'Davion Mitchell']

fig = px.bar(df_davion, x="date", y="total_tweets")

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
        ], style={'width':'45%', 'display':'inline-block'}),

        html.Div([
            dcc.Dropdown(
                id='season-dropdown',
                options = [{'label': '2021-22', 'value': 2021}],
                value=[2021],
                multi=True
            )
        ], style={'width':'45%', 'float':'right', 'display':'inline-block'}),
    ]),
    dcc.Graph(
        id='total-tweets-graph',
        figure=fig
    )
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


if __name__ == '__main__':
    app.run_server(debug=True)