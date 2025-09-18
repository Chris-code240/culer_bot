
import os, dotenv, requests, json

dotenv.load_dotenv()

import http.client


MATCHES_ENPOINTS_WITH_PARAMS = {
    "detail":"matchtId",
    "get-lineups":"matchtId",
    "get-comments":"matchtId",
    "get-incidents":"matchtId",
    "get-managers":"matchtId",
    "get-graph":"matchtId",
    "get-statistics":"matchtId",
    "get-team-streaks":"matchtId",
    "get-best-players":"matchtId",
    "get-player-statistics":["matchtId","playerId"],
    "get-player-heatmap":["matchtId","playerId"],
    "get-h2h":"matchtId"
}
PLAYERS_ENDPOINTS_WITH_PARAMS = {
    "detail":"playerId",
    "get-characteristics":"playerId",
    "get-ratings":"playerId",
    "get-transfer-history":"playerId",
    "get-statistics":"playerId",
    "get-national-team-statistics":"playerId",
    "get-statistics-season":"playerId",
    "get-all-statistics":"playerId",
    "get-next-matches":"playerId",
    "get-last-matches":"playerId",
    "get-last-year-summary":"playerId"
}

class APIClient:
    def __init__(self, api_key:str = os.environ.get('x-rapidapi-key', None), base_url:str=os.environ.get('x-rapidapi-host', None)):
        if not api_key:
            raise ValueError("API_KEY cannot be None")
        if not base_url:
            raise ValueError("BASE_URL cannot be None")
        self.api_key = api_key
        self.base_url = base_url
        self.headers = {
                'x-rapidapi-host': self.base_url,
                'x-rapidapi-key': self.api_key
        }
        self.httpConnection = http.client.HTTPConnection(self.base_url)
        # self.barca_id = 529
        self.barca_id = 2817
        self.barca_code = "BAR"


    def get_team(self, team_code:str = None, team_id:int = None):
        try:
            self.httpConnection.request("GET", f"{ self.base_url }/teams?code={team_code}", headers=self.headers)
            res = self.httpConnection.getresponse()
            if res.status >= 200 and res.status < 300:
                print(res.read().decode("utf-8"))
                return { "success":True, "data":json.loads(res.read().decode("utf-8"))['response'][0]['team']}
            raise Exception(res.reason)
        except Exception as e:
            return {"success":False, "message":str(e)}
    def get_player_details(self, playerID:int):
        try:
            url = f"http://{self.base_url}/players/detail"
            response = requests.get(url=url, headers=self.headers, params={"playerId":str(playerID)})
            if response.ok:
                return response.json()
            raise Exception(response.reason)
        except Exception as e:
            return  { "success":False, "message":str(e)}
    def get_player_statistics(self, playerID:int):
        try:
            url = f"https://{self.base_url}/players/get-all-statistics"
            params = {"playerId":str(playerID)}
            response = requests.get(url=url, headers=self.headers, params=params)
            if response.ok:
                return response.json()
            raise Exception(response.reason)
        except Exception as e:
            return { "success":False, "message":str(e)}
    def get_player_by_name(self, player_name:str):
        try:
            response = requests.get(url = "https://"+self.base_url + "/search?", headers=self.headers, params={"q":player_name,"type":"all","page":0})
            if response.ok:
                return response.json()
            raise Exception(response.reason)
        except Exception as e:
            return { "success":False, "message":str(e)}
    
    def get_squad(self):
        try:
            response = requests.get(url = "https://"+self.base_url + "/teams/squad", headers=self.headers, params={"teamId":str(self.barca_id)})
            if response.ok:
                return response.json()
            raise Exception(response.reason)
        except Exception as e:
            return { "success":False, "message":str(e)}
    def get_player_characteristics(self, playerID:int):
        try:
            response = requests.get(url = "https://"+self.base_url + "/players/get-characteristics", headers=self.headers, params={"playerId":str(playerID)})
            if response.ok:
                return response.json()
            raise Exception(response.reason)
        except Exception as e:
            return { "success":False, "message":str(e)}
    def get_transfer_history(self, playerID:int):
        try:
            response = requests.get(url = "https://"+self.base_url + "/players/get-transfer-history", headers=self.headers, params={"playerId":str(playerID)})
            if response.ok:
                return response.json()
            raise Exception(response.reason)
        except Exception as e:
            return { "success":False, "message":str(e)}
    def get_player_characteristics(self, playerID:int):
        try:
            response = requests.get(url = "https://"+self.base_url + "/players/get-national-team-statistics", headers=self.headers, params={"playerId":str(playerID)})
            if response.ok:
                return response.json()
            raise Exception(response.reason)
        except Exception as e:
            return { "success":False, "message":str(e)}
    def get_all_players(self):
        pass
    def get_players_in_a_season(self, season:str = "2024/25"):
        pass

    def get_team_statitics(self):
        pass

    def get_player_statitics(self, player_id:int):
        pass


client = APIClient()

print(client.get_player_by_name("lionel messi"))

"""
 {'results': [{'entity': {'id': 12994, 'name': 'Lionel Messi', 'slug': 'lionel-messi', 'retired': False, 'userCount': 1559095, 'team': {'id': 337602, 'name': 'Inter Miami CF', 'nameCode': 'IMC', 'slug': 'inter-miami-cf', 'national': False, 'sport': {'id': 1, 'slug': 'football', 'name': 'Football'}, 'userCount': 1510605, 'teamColors': {'primary': '#212322', 'secondary': '#f6b5cc', 'text': '#f6b5cc'}, 'gender': 'M', 'fieldTranslations': {'nameTranslation': {'ar': 'إنتر ميامي', 'ru': 'Интер Майами', 'hi': 'इंटर मिआमि सीऍफ़'}, 'shortNameTranslation': {}}}, 'deceased': False, 'country': {'alpha2': 'AR', 'name': 'Argentina', 'slug': 'argentina'}, 'shortName': 'L. Messi', 'position': 'F', 'jerseyNumber': '10', 'sofascoreId': 'LM10', 'fieldTranslations': {'nameTranslation': {'ar': 'ل. ميسي', 'hi': 'एल. मेसी', 'bn': 'এল. মেসি'}, 'shortNameTranslation': {}}}, 'score': 1127260.6, 'type': 'player'}
"""