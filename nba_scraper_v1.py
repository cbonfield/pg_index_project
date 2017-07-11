#
# Scraper to pull data from nba.com/stats that may be useful for PG index
# project.
#
# Author: Charlie Bonfield
# Date Created: April 2017
# Last Modified: May 2017

#import re
import csv
import json
import requests
import numpy as np
import pandas as pd
#import sys, os, pickle
#import urllib.request
#from urllib.parse import quote
#from bs4 import BeautifulSoup as bs

### Example URL to JSON feed:
# http://stats.nba.com/stats/leaguedashplayerstats?College=&Conference=&
# Country=&DateFrom=&DateTo=&Division=&DraftPick=&DraftYear=&GameScope=&
# GameSegment=&Height=&LastNGames=0&LeagueID=00&Location=&MeasureType=Usage&
# Month=0&OpponentTeamID=0&Outcome=&PORound=0&PaceAdjust=N&PerMode=PerGame&
# Period=0&PlayerExperience=&PlayerPosition=&PlusMinus=N&Rank=N&Season=2016-17
# &SeasonSegment=&SeasonType=Regular+Season&ShotClockRange=&StarterBench=&
# TeamID=0&VsConference=&VsDivision=&Weight=
###

# option=1 for general, clutch, tracking
# option=2 for playtype
# option=3 for shooting, opponent shooting
def find_stats(address, option):
    response = requests.get(address, headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'})
    response.raise_for_status()         # Raise exception if invalid response. 
    data = response.json()              # JSON decoding. 
    
    if option == 1:
        result_sets = data['resultSets']
        headers = result_sets[0]['headers']
        row_sets = result_sets[0]['rowSet']
    
        all_player_data = pd.DataFrame(columns=headers)
    
        for player in row_sets:
            player_df = pd.DataFrame([player], columns=headers)
            all_player_data = all_player_data.append(player_df, ignore_index=True)
    
    elif option == 2:
        result_sets = data['results']
        
        headers = list(result_sets[0].keys())
        
        all_player_data = pd.DataFrame(columns=headers)
        
        for player in result_sets:
            player_info = list(player.values())
            player_df = pd.DataFrame([player_info], columns=headers)
            all_player_data = all_player_data.append(player_df, ignore_index=True)
            
    elif option == 3:
        result_sets = data['resultSets']
        headers = result_sets['headers'][1]['columnNames']
        row_sets = result_sets['rowSet']
    
        all_player_data = pd.DataFrame(columns=headers)
    
        for player in row_sets:
            player_df = pd.DataFrame([player], columns=headers)
            all_player_data = all_player_data.append(player_df, ignore_index=True)
    
    return all_player_data

### GENERAL TAB
### General: Traditional (Only guards)
# http://stats.nba.com/stats/leaguedashplayerstats?College=&Conference=&
# Country=&DateFrom=&DateTo=&Division=&DraftPick=&DraftYear=&GameScope=&
# GameSegment=&Height=&LastNGames=0&LeagueID=00&Location=&MeasureType=Base&
# Month=0&OpponentTeamID=0&Outcome=&PORound=0&PaceAdjust=N&PerMode=Totals&
# Period=0&PlayerExperience=&PlayerPosition=G&PlusMinus=N&Rank=N&Season=2016-17&
# SeasonSegment=&SeasonType=Regular+Season&ShotClockRange=&StarterBench=&
# TeamID=0&VsConference=&VsDivision=&Weight=
###
### Places to modify:
# MeasureType = ['Base','Advanced','Misc','Scoring','Opponent','Usage','Defense']
# Season = (specify desired ranges)
###
"""
general_url_front = 'http://stats.nba.com/stats/leaguedashplayerstats?College=&' + \
                    'Conference=&Country=&DateFrom=&DateTo=&Division=&DraftPick=&' + \
                    'DraftYear=&GameScope=&GameSegment=&Height=&LastNGames=0&LeagueID=00&' + \
                    'Location=&MeasureType='
general_url_back = '&Month=0&OpponentTeamID=0&Outcome=&PORound=0&PaceAdjust=N&' + \
                   'PerMode=Totals&Period=0&PlayerExperience=&PlayerPosition=G&' + \
                   'PlusMinus=N&Rank=N&Season=2016-17&SeasonSegment=&' + \
                   'SeasonType=Regular+Season&ShotClockRange=&StarterBench=&TeamID=0&' + \
                    'VsConference=&VsDivision=&Weight='
measure_type = ['Base','Advanced','Misc','Scoring','Opponent','Usage','Defense']
#measure_type = ['Base']
#address = url_front + 'Base' + url_back
   
for mt in measure_type:
    if mt == 'Opponent':
        address = 'http://stats.nba.com/stats/leagueplayerondetails?College=&' + \
                  'Conference=&Country=&DateFrom=&DateTo=&Division=&DraftPick=&' + \
                  'DraftYear=&GameScope=&GameSegment=&Height=&LastNGames=0&' + \
                  'LeagueID=00&Location=&MeasureType=Opponent&Month=0&OpponentTeamID=0&' + \
                  '&Outcome=&PORound=0&PaceAdjust=N&PerMode=Totals&Period=0&' + \
                  'PlayerExperience=&PlayerPosition=G&PlusMinus=N&Rank=N&Season=2016-17&' + \
                  'SeasonSegment=&SeasonType=Regular+Season&ShotClockRange=&StarterBench=&' + \
                  'TeamID=0&VsConference=&VsDivision=&Weight='
    else:
        address = general_url_front + mt + general_url_back
    data = find_stats(address,1)
    data.to_csv('%s.csv' % mt)    
"""
### CLUTCH TAB
### Clutch: Traditional (only guards)
# http://stats.nba.com/stats/leaguedashplayerclutch?AheadBehind=Ahead+or+Behind&
# ClutchTime=Last+5+Minutes&College=&Conference=&Country=&DateFrom=&DateTo=&
# Division=&DraftPick=&DraftYear=&GameScope=&GameSegment=&Height=&LastNGames=0&
# LeagueID=00&Location=&MeasureType=Base&Month=0&OpponentTeamID=0&Outcome=&
# PORound=0&PaceAdjust=N&PerMode=Totals&Period=0&PlayerExperience=&PlayerPosition=G&
# PlusMinus=N&PointDiff=5&Rank=N&Season=2016-17&SeasonSegment=&SeasonType=Regular+Season&
# ShotClockRange=&StarterBench=&TeamID=0&VsConference=&VsDivision=&Weight=
###
"""
clutch_url_front = 'http://stats.nba.com/stats/leaguedashplayerclutch?' + \
                    'AheadBehind=Ahead+or+Behind&ClutchTime=Last+5+Minutes&College=&' + \
                    'Conference=&Country=&DateFrom=&DateTo=&Division=&DraftPick=&' + \
                    'DraftYear=&GameScope=&GameSegment=&Height=&LastNGames=0&' + \
                    'LeagueID=00&Location=&MeasureType='
clutch_url_back = '&Month=0&OpponentTeamID=0&Outcome=&PORound=0&PaceAdjust=N&' + \
                  'PerMode=Totals&Period=0&PlayerExperience=&PlayerPosition=G&' + \
                  'PlusMinus=N&PointDiff=5&Rank=N&Season=2016-17&SeasonSegment=&' + \
                  'SeasonType=Regular+Season&ShotClockRange=&StarterBench=&' + \
                  'TeamID=0&VsConference=&VsDivision=&Weight='
measure_type = ['Base','Advanced','Misc','Scoring','Usage']

for mt in measure_type: 
    address = clutch_url_front + mt + clutch_url_back
    data = find_stats(address,1)
    data.to_csv('%s.csv' % mt) 
"""
### PLAYTYPE TAB
### Playtype (Offensive, Transition)
# http://stats-prod.nba.com/wp-json/statscms/v1/synergy/player/?
# category=Transition&limit=500&names=offensive&q=2492172&season=2016&seasonType=Reg
# 
# http://stats-prod.nba.com/wp-json/statscms/v1/synergy/player/?
# category=Isolation&limit=500&names=offensive&q=2492172&season=2016&seasonType=Reg
#
# http://stats-prod.nba.com/wp-json/statscms/v1/synergy/player/?
# category=PRBallHandler&limit=500&names=offensive&q=2492172&season=2016&seasonType=Reg
#
# http://stats-prod.nba.com/wp-json/statscms/v1/synergy/player/?
# category=PRRollman&limit=500&names=offensive&q=2492172&season=2016&seasonType=Reg
#
# http://stats-prod.nba.com/wp-json/statscms/v1/synergy/player/?
# category=Postup&limit=500&names=offensive&q=2492172&season=2016&seasonType=Reg
#
# Note: Format differs from other tabs - could be worth revisiting. 
#
###

category_type = ['Transition', 'Isolation', 'PRBallHandler', 'PRRollman', 
                 'Postup', 'Spotup', 'Handoff', 'Cut', 'OffScreen', 
                 'OffRebound', 'Misc']

playtype_url_front = 'http://stats-prod.nba.com/wp-json/statscms/v1/synergy/player/?category='
playtype_url_back = '&limit=500&names=offensive&q=2492172&season=2016&seasonType=Reg'

for ct in category_type: 
    address = playtype_url_front + ct + playtype_url_back
    data = find_stats(address,2)
    data.to_csv('%s.csv' % ct)

### TRACKING TAB
###
# http://stats.nba.com/stats/leaguedashptstats?College=&Conference=&Country=&
# DateFrom=&DateTo=&Division=&DraftPick=&DraftYear=&GameScope=&Height=&
# LastNGames=0&LeagueID=00&Location=&Month=0&OpponentTeamID=0&Outcome=&PORound=0&
# PerMode=Totals&PlayerExperience=&PlayerOrTeam=Player&PlayerPosition=G&
# PtMeasureType=Drives&Season=2016-17&SeasonSegment=&SeasonType=Regular+Season&
# StarterBench=&TeamID=0&VsConference=&VsDivision=&Weight=
###                
"""
tracking_url_front = 'http://stats.nba.com/stats/leaguedashptstats?College=&Conference=&Country=&DateFrom=&DateTo=&Division=&DraftPick=&DraftYear=&GameScope=&Height=&LastNGames=0&LeagueID=00&Location=&Month=0&OpponentTeamID=0&Outcome=&PORound=0&PerMode=Totals&PlayerExperience=&PlayerOrTeam=Player&PlayerPosition=G&PtMeasureType='
tracking_url_back = '&Season=2016-17&SeasonSegment=&SeasonType=Regular+Season&StarterBench=&TeamID=0&VsConference=&VsDivision=&Weight='                                

pt_measure_type = ['Drives', 'Defense', 'CatchShoot', 'Passing', 'Possessions',
                   'PullUpShot', 'Rebounding', 'Efficiency', 'SpeedDistance',
                   'ElbowTouch', 'PostTouch', 'PaintTouch'] 

for ptm in pt_measure_type: 
    address = tracking_url_front + ptm + tracking_url_back
    data = find_stats(address,1)
    data.to_csv('%s.csv' % ptm)
"""
### DEFENSE DASHBOARD TAB
###
# http://stats.nba.com/stats/leaguedashptdefend?College=&Conference=&Country=&DateFrom=&DateTo=&DefenseCategory=Overall&Division=&DraftPick=&DraftYear=&GameSegment=&Height=&LastNGames=0&LeagueID=00&Location=&Month=0&OpponentTeamID=0&Outcome=&PORound=0&PerMode=Totals&Period=0&PlayerExperience=&PlayerPosition=G&Season=2016-17&SeasonSegment=&SeasonType=Regular+Season&StarterBench=&TeamID=0&VsConference=&VsDivision=&Weight=
###
"""
defense_categories = ['Overall', '3+Pointers', '2+Pointers', 'Less+Than+6Ft', 
                      'Less+Than+10Ft', 'Greater+Than+15Ft']

defense_url_front = 'http://stats.nba.com/stats/leaguedashptdefend?College=&Conference=&Country=&DateFrom=&DateTo=&DefenseCategory=' 
defense_url_back = '&Division=&DraftPick=&DraftYear=&GameSegment=&Height=&LastNGames=0&LeagueID=00&Location=&Month=0&OpponentTeamID=0&Outcome=&PORound=0&PerMode=Totals&Period=0&PlayerExperience=&PlayerPosition=G&Season=2016-17&SeasonSegment=&SeasonType=Regular+Season&StarterBench=&TeamID=0&VsConference=&VsDivision=&Weight='

for dc in defense_categories:
    address = defense_url_front + dc + defense_url_back
    data = find_stats(address,1)
    data.to_csv('%s.csv' % dc)
"""
### SHOT DASHBOARD TAB
###
# http://stats.nba.com/stats/leaguedashplayerptshot?CloseDefDistRange=&College=&Conference=&Country=&DateFrom=&DateTo=&Division=&DraftPick=&DraftYear=&DribbleRange=&GameScope=&GameSegment=&GeneralRange=Overall&Height=&LastNGames=0&LeagueID=00&Location=&Month=0&OpponentTeamID=0&Outcome=&PORound=0&PaceAdjust=N&PerMode=Totals&Period=0&PlayerExperience=&PlayerPosition=G&PlusMinus=N&Rank=N&Season=2016-17&SeasonSegment=&SeasonType=Regular+Season&ShotClockRange=&ShotDistRange=&StarterBench=&TeamID=0&TouchTimeRange=&VsConference=&VsDivision=&Weight=
###
"""
general_ranges = ['Overall', 'Catch+and+Shoot', 'Pullups', 'Less+Than+10+ft']
url_front = 'http://stats.nba.com/stats/leaguedashplayerptshot?CloseDefDistRange=&College=&Conference=&Country=&DateFrom=&DateTo=&Division=&DraftPick=&DraftYear=&DribbleRange=&GameScope=&GameSegment=&GeneralRange=' 
url_back = '&Height=&LastNGames=0&LeagueID=00&Location=&Month=0&OpponentTeamID=0&Outcome=&PORound=0&PaceAdjust=N&PerMode=Totals&Period=0&PlayerExperience=&PlayerPosition=G&PlusMinus=N&Rank=N&Season=2016-17&SeasonSegment=&SeasonType=Regular+Season&ShotClockRange=&ShotDistRange=&StarterBench=&TeamID=0&TouchTimeRange=&VsConference=&VsDivision=&Weight='

for gr in general_ranges:
    address = url_front + gr + url_back
    data = find_stats(address,1)
    data.to_csv('%s.csv' % gr)


shot_clock_ranges = ['24-22', '22-18+Very+Early', '18-15+Early', '15-7+Average', 
                     '7-4+Late', '4-0+Very+Late', 'ShotClock+Off']

url_front = 'http://stats.nba.com/stats/leaguedashplayerptshot?CloseDefDistRange=&College=&Conference=&Country=&DateFrom=&DateTo=&Division=&DraftPick=&DraftYear=&DribbleRange=&GameScope=&GameSegment=&GeneralRange=&Height=&LastNGames=0&LeagueID=00&Location=&Month=0&OpponentTeamID=0&Outcome=&PORound=0&PaceAdjust=N&PerMode=Totals&Period=0&PlayerExperience=&PlayerPosition=G&PlusMinus=N&Rank=N&Season=2016-17&SeasonSegment=&SeasonType=Regular+Season&ShotClockRange='
url_back = '&ShotDistRange=&StarterBench=&TeamID=0&TouchTimeRange=&VsConference=&VsDivision=&Weight='

for sc in shot_clock_ranges:
    address = url_front + sc + url_back
    data = find_stats(address,1)
    data.to_csv('%s.csv' % sc)

dribble_ranges = ['0+Dribbles', '1+Dribble', '2+Dribbles', '3-6+Dribbles', 
                  '7%2B+Dribbles']

url_front = 'http://stats.nba.com/stats/leaguedashplayerptshot?CloseDefDistRange=&College=&Conference=&Country=&DateFrom=&DateTo=&Division=&DraftPick=&DraftYear=&DribbleRange='
url_back = '&GameScope=&GameSegment=&GeneralRange=&Height=&LastNGames=0&LeagueID=00&Location=&Month=0&OpponentTeamID=0&Outcome=&PORound=0&PaceAdjust=N&PerMode=Totals&Period=0&PlayerExperience=&PlayerPosition=G&PlusMinus=N&Rank=N&Season=2016-17&SeasonSegment=&SeasonType=Regular+Season&ShotClockRange=&ShotDistRange=&StarterBench=&TeamID=0&TouchTimeRange=&VsConference=&VsDivision=&Weight='

for dr in dribble_ranges:
    address = url_front + dr + url_back
    data = find_stats(address,1)
    data.to_csv('%s.csv' % dr)


tt_ranges = ['Touch+<+2+Seconds', 'Touch+2-6+Seconds', 'Touch+6%2B+Seconds']
url_front = 'http://stats.nba.com/stats/leaguedashplayerptshot?CloseDefDistRange=&College=&Conference=&Country=&DateFrom=&DateTo=&Division=&DraftPick=&DraftYear=&DribbleRange=&GameScope=&GameSegment=&GeneralRange=&Height=&LastNGames=0&LeagueID=00&Location=&Month=0&OpponentTeamID=0&Outcome=&PORound=0&PaceAdjust=N&PerMode=Totals&Period=0&PlayerExperience=&PlayerPosition=G&PlusMinus=N&Rank=N&Season=2016-17&SeasonSegment=&SeasonType=Regular+Season&ShotClockRange=&ShotDistRange=&StarterBench=&TeamID=0&TouchTimeRange='
url_back = '&VsConference=&VsDivision=&Weight='

for tt in tt_ranges:
    address = url_front + tt + url_back
    data = find_stats(address,1)
    data.to_csv('%s.csv' % tt)

"""
"""
clos_def_ranges = ['0-2+Feet+-+Very+Tight', '2-4+Feet+-+Tight', '4-6+Feet+-+Open', 
                   '6%2B+Feet+-+Wide+Open']
url_front = 'http://stats.nba.com/stats/leaguedashplayerptshot?CloseDefDistRange=' 
url_back = '&College=&Conference=&Country=&DateFrom=&DateTo=&Division=&DraftPick=&DraftYear=&DribbleRange=&GameScope=&GameSegment=&GeneralRange=&Height=&LastNGames=0&LeagueID=00&Location=&Month=0&OpponentTeamID=0&Outcome=&PORound=0&PaceAdjust=N&PerMode=Totals&Period=0&PlayerExperience=&PlayerPosition=G&PlusMinus=N&Rank=N&Season=2016-17&SeasonSegment=&SeasonType=Regular+Season&ShotClockRange=&ShotDistRange=&StarterBench=&TeamID=0&TouchTimeRange=&VsConference=&VsDivision=&Weight='
"""
"""
for cd in clos_def_ranges:
    address = url_front + cd + url_back
    data = find_stats(address,1)
    data.to_csv('%s.csv' % cd)
"""
"""
url_front = 'http://stats.nba.com/stats/leaguedashplayerptshot?CloseDefDistRange='
url_back = '&College=&Conference=&Country=&DateFrom=&DateTo=&Division=&DraftPick=&DraftYear=&DribbleRange=&GameScope=&GameSegment=&GeneralRange=&Height=&LastNGames=0&LeagueID=00&Location=&Month=0&OpponentTeamID=0&Outcome=&PORound=0&PaceAdjust=N&PerMode=Totals&Period=0&PlayerExperience=&PlayerPosition=G&PlusMinus=N&Rank=N&Season=2016-17&SeasonSegment=&SeasonType=Regular+Season&ShotClockRange=&ShotDistRange=%3E%3D10.0&StarterBench=&TeamID=0&TouchTimeRange=&VsConference=&VsDivision=&Weight='

for cd in clos_def_ranges:
    address = url_front + cd + url_back
    data = find_stats(address,1)
    data.to_csv('%s.csv' % cd)
"""
### SHOOTING TAB
###
# http://stats.nba.com/stats/leaguedashplayershotlocations?College=&Conference=&Country=&DateFrom=&DateTo=&DistanceRange=5ft+Range&Division=&DraftPick=&DraftYear=&GameScope=&GameSegment=&Height=&LastNGames=0&LeagueID=00&Location=&MeasureType=Base&Month=0&OpponentTeamID=0&Outcome=&PORound=0&PaceAdjust=N&PerMode=Totals&Period=0&PlayerExperience=&PlayerPosition=&PlusMinus=N&Rank=N&Season=2016-17&SeasonSegment=&SeasonType=Regular+Season&ShotClockRange=&StarterBench=&TeamID=0&VsConference=&VsDivision=&Weight=
###
"""
distance_ranges = ['5ft+Range', '8ft+Range', 'By+Zone']
shooting_url_front = 'http://stats.nba.com/stats/leaguedashplayershotlocations?College=&Conference=&Country=&DateFrom=&DateTo=&DistanceRange='
shooting_url_back = '&Division=&DraftPick=&DraftYear=&GameScope=&GameSegment=&Height=&LastNGames=0&LeagueID=00&Location=&MeasureType=Base&Month=0&OpponentTeamID=0&Outcome=&PORound=0&PaceAdjust=N&PerMode=Totals&Period=0&PlayerExperience=&PlayerPosition=G&PlusMinus=N&Rank=N&Season=2016-17&SeasonSegment=&SeasonType=Regular+Season&ShotClockRange=&StarterBench=&TeamID=0&VsConference=&VsDivision=&Weight='

for dr in distance_ranges:
    address = shooting_url_front + dr + shooting_url_back
    data = find_stats(address,3)
    data.to_csv('%s.csv' % dr)
"""
### OPPONENT SHOOTING TAB
###
# (same as above, with MeasureType=Opponent)
###
"""
shooting_url_back = '&Division=&DraftPick=&DraftYear=&GameScope=&GameSegment=&Height=&LastNGames=0&LeagueID=00&Location=&MeasureType=Opponent&Month=0&OpponentTeamID=0&Outcome=&PORound=0&PaceAdjust=N&PerMode=Totals&Period=0&PlayerExperience=&PlayerPosition=G&PlusMinus=N&Rank=N&Season=2016-17&SeasonSegment=&SeasonType=Regular+Season&ShotClockRange=&StarterBench=&TeamID=0&VsConference=&VsDivision=&Weight='

for dr in distance_ranges:
    address = shooting_url_front + dr + shooting_url_back
    data = find_stats(address,3)
    data.to_csv('%s.csv' % dr)
"""
### HUSTLE TAB
###
# http://stats.nba.com/stats/leaguehustlestatsplayer?College=&Conference=&
# Country=&DateFrom=&DateTo=&Division=&DraftPick=&DraftYear=&GameScope=&Height=&
# LastNGames=0&LeagueID=00&Location=&Month=0&OpponentTeamID=0&Outcome=&PORound=0&
# PaceAdjust=N&PerMode=Totals&PlayerExperience=&PlayerPosition=G&PlusMinus=N&
# Rank=N&Season=2016-17&SeasonSegment=&SeasonType=Regular+Season&TeamID=0&
# VsConference=&VsDivision=&Weight=
###
"""
hustle_url = 'http://stats.nba.com/stats/leaguehustlestatsplayer?College=&Conference=&Country=&DateFrom=&DateTo=&Division=&DraftPick=&DraftYear=&GameScope=&Height=&LastNGames=0&LeagueID=00&Location=&Month=0&OpponentTeamID=0&Outcome=&PORound=0&PaceAdjust=N&PerMode=Totals&PlayerExperience=&PlayerPosition=G&PlusMinus=N&Rank=N&Season=2016-17&SeasonSegment=&SeasonType=Regular+Season&TeamID=0&VsConference=&VsDivision=&Weight='
data = find_stats(hustle_url, 1)
data.to_csv('Hustle.csv')
"""