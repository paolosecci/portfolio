import requests
import json

#DATA MINING FUNCTION
def get_player_data():
    url = "https://stats.nba.com/stats/leaguegamelog?Counter=1000&DateFrom=&DateTo=&Direction=DESC&LeagueID=00&PlayerOrTeam=P&Season=2018-19&SeasonType=Regular+Season&Sorter=DATE"
    this_user_agent = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36"}
    re = requests.get(url, headers=this_user_agent)
    print(re.status_code)
    nba_p_json = json.loads(re.text)
    return nba_p_json

def get_teams_data():
    url = "https://stats.nba.com/stats/leaguegamelog?Counter=1000&DateFrom=&DateTo=&Direction=DESC&LeagueID=00&PlayerOrTeam=T&Season=2018-19&SeasonType=Regular+Season&Sorter=DATE"
    this_user_agent = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36"}
    re = requests.get(url, headers=this_user_agent)
    print(re.status_code)
    nba_t_json = json.loads(re.text)
    return nba_t_json
    
#DATA LOCALIZATION
def localize_data():
    nba_p_json = get_player_data()
    nba_t_json = get_teams_data()
    with open("data/nba_player_boxscores.json", "w") as file_p_out:
        json.dump(nba_p_json, file_p_out)
    with open("data/nba_team_boxscores.json", "w") as file_t_out:
        json.dump(nba_t_json, file_t_out)
        
localize_data();