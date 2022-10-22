import json
import random
import time
import requests
import pandas as pd

from enum import IntEnum

class GameConstants(IntEnum):
    NUMBER_OF_PLAYERS = 10



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
    Returns a list of match ids. It is used to fetch each match's details

    Parameters:
    summonerPuuid (str): the summoners puuid
    count (str): the number of matches to return between '0' and '100'. Defaults to 20

    """
    params = keyParams + f'&count={str(count)}'
    summonerMatchListURL = f"https://americas.api.riotgames.com/lol/match/v5/matches/by-puuid/{summonerPuuid}/ids" + params
    resp = requests.get(summonerMatchListURL)
    summonerMatchList = resp.json()

    return summonerMatchList


def getMatchData(matches: list, df: pd.core.frame.DataFrame):
    """
    Iterates through the match list fetch the data for each match in the list.
    """
    params = keyParams
    
    for match in matches:
        matchDataURL = f'https://americas.api.riotgames.com/lol/match/v5/matches/{match}' + params
        resp = requests.get(matchDataURL)
        matchData = resp.json()
       
        loadData(matchData, df)
            
            

    return matchData

def loadData(matchData: dict, df: pd.core.frame.DataFrame):
    """
    """
    for participant in range(GameConstants.NUMBER_OF_PLAYERS):
            player_data = matchData['info']['participants'][participant]

            list = [matchData['metadata']['matchId'],player_data['puuid'],player_data['teamId'], player_data['championId'],
                    player_data['championName'], player_data['kills'], player_data['deaths'], 
                    player_data['assists'], player_data['wardsPlaced'],player_data['win'], player_data['teamPosition'], 
                    getChampionMastery(player_data['championId'], player_data['summonerId'],'championLevel')
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



df = pd.DataFrame(columns = ['matchId', 'puuid', 'teamId', 'championId', 'championName',
                             'kills', 'deaths', 'assists', 'wardsPlaced', 'win', 'teamPosition',
                             'championLevel',
                             
                            ])

id = getSummoner('Sleetus','puuid')
matchlist = getMatchList(id,2)
matchData = getMatchData(matchlist, df)
print(df)
print(df['teamPosition'])

id = selectRandomPlayer(df['puuid'].to_list()) # important to not choose a player we already did
matchlist = getMatchList(id,2)
getMatchData(matchlist, df)
print(df)
print(df['teamPosition'])


#test = matchData['info']['participants'][9]
#print(test['teamId'],test['role'],test['lane'],test['kills'], test['deaths'], test['assists'])

#df = pd.DataFrame.from_dict(test, orient='index')
#getMatchData(matchlist)['info']['participants'][0].keys()





