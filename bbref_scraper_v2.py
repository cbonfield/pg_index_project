#
# Template code for scraping data from bbref.  
#
# Author: Charlie Bonfield
# Created: March 2017

import re
import csv
import requests
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup as bs

base_url = 'http://www.basketball-reference.com/leagues/NBA_'
year = '2017'
addons = 'advanced'
#addons = ['per_game','totals','per_minute','per_poss','advanced']
#table_ids = ['all_per_game_stats',]
column_titles = ['Name', 'Pos', 'Age', 'Tm', 'G', 'MP', 'PER', 'TS%', '3PAr',
                 'FTr', 'ORB%', 'DRB%', 'TRB%', 'AST%', 'STL%', 'BLK%', 
                 'TOV%', 'USG%', 'OWS', 'DWS', 'WS', 'WS/48', 'OBPM', 'DBPM',
                 'BPM', 'VORP']

full_url = base_url + year + '_' + addons + '.html'
page = requests.get(full_url)
soup = bs(page.content, 'html.parser')

table_id = 'all_advanced_stats'
all_stats = soup.find(id=table_id)
all_rows = all_stats.find_all(class_='full_table')
all_data = pd.DataFrame(columns=column_titles)

for player_index, player in enumerate(all_rows):
    fl_name = player.find('td', {'data-stat': 'player'}).text
    first, last = fl_name.split(' ',1)
    lf_name = last + ', ' + first
    position = player.find('td', {'data-stat': 'pos'}).text 
    age = player.find('td', {'data-stat': 'age'}).text 
    team = player.find('td', {'data-stat': 'team_id'}).text 
    games = player.find('td', {'data-stat': 'g'}).text 
    minutes = player.find('td', {'data-stat': 'mp'}).text 
    per = player.find('td', {'data-stat': 'per'}).text 
    ts_pct = player.find('td', {'data-stat': 'ts_pct'}).text
    three_pa_fga = player.find('td', {'data-stat': 'fg3a_per_fg_pct'}).text
    fta_fga = player.find('td', {'data-stat': 'fta_per_fg_pct'}).text
    oreb = player.find('td', {'data-stat': 'orb_pct'}).text 
    dreb = player.find('td', {'data-stat': 'drb_pct'}).text 
    treb = player.find('td', {'data-stat': 'trb_pct'}).text 
    ast = player.find('td', {'data-stat': 'ast_pct'}).text 
    stl = player.find('td', {'data-stat': 'stl_pct'}).text 
    blk = player.find('td', {'data-stat': 'blk_pct'}).text 
    tov = player.find('td', {'data-stat': 'tov_pct'}).text
    usg = player.find('td', {'data-stat': 'usg_pct'}).text
    ows = player.find('td', {'data-stat': 'ows'}).text
    dws = player.find('td', {'data-stat': 'dws'}).text
    ws = player.find('td', {'data-stat': 'ws'}).text
    ws_per48 = player.find('td', {'data-stat': 'ws_per_48'}).text
    obpm = player.find('td', {'data-stat': 'obpm'}).text
    dbpm = player.find('td', {'data-stat': 'dbpm'}).text
    bpm = player.find('td', {'data-stat': 'bpm'}).text
    vorp = player.find('td', {'data-stat': 'vorp'}).text 
    
    new_df = pd.DataFrame([[lf_name, position, age, team, games, minutes,
                            per, ts_pct, three_pa_fga, fta_fga, oreb, dreb, treb, 
                            ast, stl, blk, tov, usg, ows, dws, ws, ws_per48, 
                            obpm, dbpm, bpm, vorp]], columns=column_titles)
    all_data = all_data.append(new_df, ignore_index=True)

all_data.to_csv('%s_%s.csv' % (year, addons))
    