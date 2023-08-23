import random
import time
import requests
import pandas as pd

from enum import IntEnum

class GameConstants(IntEnum):
    NUMBER_OF_PLAYERS_IN_A_GAME = 10
    NUMBER_OF_MATCHES = 5
    PLAYERS_TO_FETCH = 5000



# Assign the development key located in 'api_key.txt' to api_key
f = open('api_key.txt','r')
api_key = f.read()
f.close()

keyParams = '?api_key=' + api_key

def getSummoner(summonerName: str, field: str):
    """
    Retrieves information about a summoner based on a specific field. It is used to fetch match data for a summoner in another API call.

    Parameters:
    summonerName (str): The name of the summoner.
    field (str): The field you want to obtain. For example, the summoner's 'puuid'.
    """
    params = keyParams
    summonerNameURL = f"https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/{summonerName}" + params
    resp = requests.get(summonerNameURL)
    summonerInfo = resp.json()[field]
    return summonerInfo
    

def getRankedMatchList(summonerPuuid: str, count: int = 20):
    """
    Returns a list of sorted match IDs. It is used as input to retrieve the details of each match in another API call.

    Parameters:
    summonerPuuid (str): The summoner's PUUID.
    count (str): The number of matches to return, between '0' and '100'. Defaults to 20.

    """
    params = keyParams + f'&type=ranked&count={str(count)}'
    summonerMatchListURL = f"https://americas.api.riotgames.com/lol/match/v5/matches/by-puuid/{summonerPuuid}/ids" + params
    timeCounter = 0
    while True:
        resp = requests.get(summonerMatchListURL)
        print(resp.status_code)
        if resp.status_code == 429:
            print("Waiting 130 seconds for API rate limit..." + f"{timeCounter} seconds elapsed")
            time.sleep(10)
            timeCounter+=10
            continue
        summonerMatchList = resp.json()
        return summonerMatchList


def getMatchData(match: str):
    """
    Retrieves the data of a match.
    """
    params = keyParams
    matchDataURL = f'https://americas.api.riotgames.com/lol/match/v5/matches/{match}' + params
    timeCounter = 0
    while True:
        resp = requests.get(matchDataURL)
        print(resp.status_code)
        if resp.status_code == 429:
            print("Waiting 130 seconds for API rate limit..." + f"{timeCounter} seconds elapsed")
            time.sleep(10)
            timeCounter+=10
            continue
        matchData = resp.json()
            
        return matchData

def loadData(matchData: dict, df: pd.core.frame.DataFrame):
    """
    Loads match data (which contains data for 10 players) into the provided DataFrame, 'df'.
    """
    for participant in range(GameConstants.NUMBER_OF_PLAYERS_IN_A_GAME):
            player_data = matchData['info']['participants'][participant]

            list = [
                    player_data['puuid'],player_data['summonerId'], player_data['championId'],
                    player_data['championName'], player_data['win']
                   ]
                    
            
            df.loc[0] = list
            df.index = df.index + 1

    return None

def getChampionMastery(championId: int, summonerId: str, field: str):
    """
    Retrieves details of a summoner's mastery of a certain champion.

    Parameters:
    championId (int): The ID of the champion.
    summonerId (str): The encrypted summoner ID.
    field (str): The field you want to obtain. For example, 'championLevel'.
    """
    params = keyParams
    championMasteryURL = f'https://na1.api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-summoner/{summonerId}/by-champion/{championId}' + params
    resp = requests.get(championMasteryURL)
    masteryData = resp.json()[field]

    return masteryData

def selectRandomPlayer(puuid: list):
    """
    Sélectionne le puuid d'un invocateur au hasard dans une liste fournie de puuids d'invocateurs
    """
    return random.choice(puuid)


"""
CODE EXECUTION STARTS HERE
"""

id = 'dhAJ9HbAox7FewEaIlN28yWB8LTZbisT67wGZQ1c1Pi3r2GiU7vqvv6DDIIqrshpkP-gogZL4JhGug' 

fetched_players_count = 0

# While we haven't retrieved match data for the number of players specified by COUNT_OF_PLAYERS_TO_FETCH, continue looping.
while fetched_players_count < 5000:
    
    # Reset the contents of the dataframes to empty.
    df_matchData = pd.DataFrame(columns = ['puuid','summonerId', 'championId','championName', 'win'])

    df_fetchedPlayers = pd.DataFrame(columns = ['puuid'])
    

    # Retrieve the player's match list and fetch data for 5 matches. Note that there are 10 players in each match.
    matchlist = getRankedMatchList(id, 5)

    for match in matchlist:
        matchData = getMatchData(match)
        loadData(matchData, df_matchData)



    # Once the data for a player is retrieved, randomly select a new player from the match list of the previous player.
    id = selectRandomPlayer(df_matchData['puuid'].unique().tolist()) 
    df_matchData.to_csv('LoL_Match_Data.csv', header = False, index = False, mode = 'a')
    
    fetched_players_count += 1











