import json
from numpy import number
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



def getSummonerPuuid(summonerName: str):
    """
    Retrieves the summoner's unique identifier. It is used to fetch a summoner's match data

    Parameters:
    summonerName (str): the name of the summoner
    """
    params = keyParams
    summonerNameURL = f"https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/{summonerName}" + params
    resp = requests.get(summonerNameURL)
    summonerPuuid = resp.json()['puuid']
    return summonerPuuid
    

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


def getMatchData(matches: list, df: pd.core.frame.DataFrame ):
    """
    Iterates through the match list fetch the data for each match in the list.
    """
    params = keyParams
    
    for match in matches:
        matchDataURL = f'https://americas.api.riotgames.com/lol/match/v5/matches/{match}' + params
        resp = requests.get(matchDataURL)
        matchData = resp.json()

        for participant in range(GameConstants.NUMBER_OF_PLAYERS):
            test = matchData['info']['participants'][participant]
            list = [matchData['metadata']['matchId'],test['puuid'],test['teamId'], test['championId'],
                    test['championName'],test['role'], test['lane'],test['kills'], test['deaths'], 
                    test['assists'], test['wardsPlaced'],test['win']]
                    
            #insert into the provided dataframe
            df.loc[0] = list
            df.index = df.index + 1
            
            

    return list

df = pd.DataFrame(columns = ['matchId', 'puuid', 'teamId', 'championId', 'championName',
                             'role', 'lane', 'kills', 'deaths', 'assists', 'wardsPlaced', 'win'
                            ])

id = getSummonerPuuid("Sleetus")
matchlist = getMatchList(id,1)
matchData = getMatchData(matchlist, df)
print(df)

print(df.loc[df['puuid'] == id])
print(id)
#test = matchData['info']['participants'][9]
#print(test['teamId'],test['role'],test['lane'],test['kills'], test['deaths'], test['assists'])

#df = pd.DataFrame.from_dict(test, orient='index')
#getMatchData(matchlist)['info']['participants'][0].keys()





