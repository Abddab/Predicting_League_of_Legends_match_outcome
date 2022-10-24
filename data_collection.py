import json
import random
import time
import requests
import pandas as pd

from enum import IntEnum

class GameConstants(IntEnum):
    NUMBER_OF_PLAYERS_IN_A_GAME = 10



# Assign the developpement key located in 'api_key.txt' to api_key.
f = open('api_key.txt','r')
api_key = f.read()
f.close()

keyParams = '?api_key=' + api_key

def getSummoner(summonerName: str, field: str):
    """
    Retrieves the summoner's unique identifier. It is used to fetch a summoner's match data

    Parameters:
    summonerName (str): the name of the summoner
    """
    params = keyParams
    summonerNameURL = f"https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/{summonerName}" + params
    resp = requests.get(summonerNameURL)
    summonerInfo = resp.json()[field]
    return summonerInfo
    

def getMatchList(summonerPuuid: str, count: int = 20):
    """
    Returns a list of RANKED match ids. It is used to fetch each match's details

    Parameters:
    summonerPuuid (str): the summoners puuid
    count (str): the number of matches to return between '0' and '100'. Defaults to 20

    """
    params = keyParams + f'&type=ranked&count={str(count)}'
    summonerMatchListURL = f"https://americas.api.riotgames.com/lol/match/v5/matches/by-puuid/{summonerPuuid}/ids" + params
    timeCounter = 0
    while True:
        resp = requests.get(summonerMatchListURL)
        if resp.status_code == 429:
            print("Waiting 130 seconds for API rate limit..." + f"{timeCounter} seconds elapsed")
            time.sleep(10)
            timeCounter+=10
            continue
        summonerMatchList = resp.json()
        return summonerMatchList


def getMatchData(match: str):
    """
    Fetches the data of one match
    """
    params = keyParams
    matchDataURL = f'https://americas.api.riotgames.com/lol/match/v5/matches/{match}' + params
    timeCounter = 0
    while True:
        resp = requests.get(matchDataURL)
        if resp.status_code == 429:
            print("Waiting 130 seconds for API rate limit..." + f"{timeCounter} seconds elapsed")
            time.sleep(10)
            timeCounter+=10
            continue
        matchData = resp.json()
            
        return matchData

def loadData(matchData: dict, df: pd.core.frame.DataFrame):
    """
    Loads the match data (which contains 10 players) in the provided dataframe
    """
    for participant in range(GameConstants.NUMBER_OF_PLAYERS_IN_A_GAME):
            player_data = matchData['info']['participants'][participant]
            matchInfo = matchData['info']

            list = [matchData['metadata']['matchId'], matchInfo['gameDuration'], matchInfo['gameMode'],
                    player_data['summonerId'], player_data['puuid'], player_data['teamId'], player_data['championId'],
                    player_data['championName'], player_data['kills'], player_data['deaths'], 
                    player_data['assists'], player_data['wardsPlaced'], player_data['win'], player_data['teamPosition']
                   ]
                    
            #insert into the provided dataframe
            df.loc[0] = list
            df.index = df.index + 1

    return None

def getChampionMastery(championId: int, summonerId: str, field: str):
    """
    """
    params = keyParams
    championMasteryURL = f'https://na1.api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-summoner/{summonerId}/by-champion/{championId}' + params
    resp = requests.get(championMasteryURL)
    masteryData = resp.json()[field]

    return masteryData

def selectRandomPlayer(puuid: list):

    return random.choice(puuid)


"""
CODE EXECUTION BEGINS HERE
"""
#The id chosen to start the chain of random selection
id = 'SNPQFj1t1CVQtEm8SQAgXjs_xcH9KGgx5CYQ32KiY8l5YJAyf0-h9YzBs1v2T0HO3Rj5sNnNxs7PFw' 
fetched_players_count = 0

#Until we have fetched the match data for 1000 players, continue to loop
while fetched_players_count < 1500:
    
    #reset the dataframes for every player loaded
    df_matchData = pd.DataFrame(columns = ['matchId','gameDuration(s)','gameMode', 'summonerId', 'puuid', 'teamId', 'championId',
                                 'championName', 'kills', 'deaths', 'assists', 'wardsPlaced', 'win', 'teamPosition'
                                ])

    df_fetchedPlayers = pd.DataFrame(columns = ['puuid'])
    

    # For each player, gather the data of 7 matches. Note that there's 10 players in each match.
    matchlist = getMatchList(id, 5)
    for match in matchlist:
        matchData = getMatchData(match)
        loadData(matchData, df_matchData)
    
    df_fetchedPlayers.loc[0] = id
    df_fetchedPlayers.index += 1
    df_fetchedPlayers.to_csv('fetched_players_list.csv', header = False, index = False, mode = 'a')

    # Once the 7 games for a player have been fetched, select a new random player from the 7 matchs of the previous player
    id = selectRandomPlayer(df_matchData['puuid'].unique().tolist()) 
    df_matchData.to_csv('league_match_data.csv', header = False, index = False, mode = 'a')
    
    fetched_players_count += 1











