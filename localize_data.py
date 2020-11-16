import requests
import json

request_headers = {
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-US,en;q=0.9,it;q=0.8,und;q=0.7',
    'Access-Control-Request-Headers': 'x-nba-stats-origin,x-nba-stats-token',
    'Access-Control-Request-Method': 'GET',
    'Connection': 'keep-alive',
    'Host': 'stats.nba.com',
    'Origin': 'https://www.nba.com',
    'Referer': 'https://www.nba.com/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-site',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36'
}

#DATA MINING FUNCTION
def get_player_data():
    url = "https://stats.nba.com/stats/leaguegamelog?Counter=29520&DateFrom=&DateTo=&Direction=DESC&LeagueID=00&PlayerOrTeam=P&Season=2019-20&SeasonType=Regular+Season&Sorter=DATE"
    re = requests.get(url, headers=request_headers)
    print(re.status_code)
    nba_p_json = json.loads(re.text)
    return nba_p_json

def get_teams_data():
    url = "https://stats.nba.com/stats/leaguegamefinder?Conference=&DateFrom=&DateTo=&Division=&DraftNumber=&DraftRound=&DraftYear=&GB=N&LeagueID=00&Location=&Outcome=&PlayerOrTeam=T&Season=2019-20&SeasonType=&StatCategory=PTS&TeamID=&VsConference=&VsDivision=&VsTeamID="
    this_user_agent = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36"}
    re = requests.get(url, headers=request_headers)
    print(re.status_code)
    nba_t_json = json.loads(re.text)
    return nba_t_json

#DATA LOCALIZATION
def localize_data():
    nba_p_json = get_player_data()
    with open("data/nba_player_boxscores.json", "w") as file_p_out:
        json.dump(nba_p_json, file_p_out)
    nba_t_json = get_teams_data()
    with open("data/nba_team_boxscores.json", "w") as file_t_out:
        json.dump(nba_t_json, file_t_out)

localize_data()
