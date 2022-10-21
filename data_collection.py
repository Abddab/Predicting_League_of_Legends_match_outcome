import requests


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
    summonerMatchList = requests.get(summonerMatchListURL).json()
    return summonerMatchList


def getMatchData(matches: list):
    """
    
    """
    params = keyParams
    matchListIterator = 0
    
    for match in matches:
        matchDataURL = f'https://americas.api.riotgames.com/lol/match/v5/matches/{matches[matchListIterator]}' + params
        resp = requests.get(matchDataURL)
        matchData = resp.json()

    return matchData

print(getSummonerPuuid("PapaMochii"))
test= "hi"

