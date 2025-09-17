
import os, dotenv, requests, json

dotenv.load_dotenv()

import http.client



class APIClient:
    def __init__(self, api_key:str = os.environ.get('FOOTBALL_API_KEY', None), base_url:str=os.environ.get('FOOTBALL_API_BASE_URL', None)):
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
        self.barca_id = 529
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
    def get_player_by_name(self, player_name=None):
        try:
            self.httpConnection.request("GET", f"https://{self.base_url.strip()}/players/profiles?search={player_name}".replace(' ', '%20'), headers=self.headers)
            res = self.httpConnection.getresponse()
            if res.status >= 200 and res.status < 300:
                print(res.read().decode("utf-8"))
                return { "success":True, "data":json.loads(res.read().decode("utf-8"))['response'][0]['player']}
            raise Exception(res.reason)
        except Exception as e:
            return { "success":False, "message":str(e)}
    
    def get_squad(self):
        try:
            res = requests.get(url = f"https://v3.football.api-sports.io/players/squads?team={self.barca_id}", headers=self.headers)
            if res.ok:
                return { "success":True, "data":res.json()['response'][0]['players']}
            raise Exception(res.reason)
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

print(client.get_squad())

"""
{
get: "teams"
parameters: {   name: "barcelona"}
errors: []
results: 1
paging: {

    current: 1
    total: 1

}
response: [{team: {

    id: 529
    name: "Barcelona"
    code: "BAR"
    country: "Spain"
    founded: 1899
    national: false
    logo: "https://media.api-sports.io/football/teams/529.png"

}
venue: {

                id: 19939
                name: "Estadi Olímpic Lluís Companys"
                address: "Carrer de l'Estadi"
                city: "Barcelona"
                capacity: 55926
                surface: "grass"
                image: "https://media.api-sports.io/football/venues/19939.png"
            }
        }
    ]

}
"""

