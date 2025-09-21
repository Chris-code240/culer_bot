import os, dotenv, requests, json
from urllib.parse import urljoin

dotenv.load_dotenv()

MATCHES_ENDPOINTS_WITH_PARAMS: dict[str, list[str] | str] = {
    "detail": "matchId",
    "get-lineups": "matchId",
    "get-comments": "matchId",
    "get-incidents": "matchId",
    "get-managers": "matchId",
    "get-graph": "matchId",
    "get-statistics": "matchId",
    "get-team-streaks": "matchId",
    "get-best-players": "matchId",
    "get-player-statistics": ["matchId", "playerId"],
    "get-player-heatmap": ["matchId", "playerId"],
    "get-h2h": "matchId"
}

PLAYERS_ENDPOINTS_WITH_PARAMS: dict[str, list[str] | str] = {
    "detail": "playerId",
    "get-characteristics": "playerId",
    "get-ratings": "playerId",
    "get-transfer-history": "playerId",
    "get-statistics": "playerId",
    "get-national-team-statistics": "playerId",
    "get-statistics-season": "playerId",
    "get-all-statistics": "playerId",
    "get-next-matches": "playerId",
    "get-last-matches": "playerId",
    "get-last-year-summary": "playerId"
}

TEAMS_ENDPOINTS_WITH_PARAMS: dict[str, list[str] | str] = {
    "detail": "teamId",
    "get-squad": "teamId",
    "get-transfers": "teamId",
    "get-performance": "teamId",
    "get-rankings": "teamId",
    "get-tournaments": "teamId",
    "get-near-events": "teamId",
    "get-ranks": "teamId",
    "get-statistics": "teamId",
    "get-statistics-seasons": "teamId",
    "get-last-matches": "teamId",
    "get-next-matches": "teamId",
    "get-player-statistics": ["teamId", "seasonId"],
}


class APIClient:
    def __init__(
        self,
        api_key: str | None = os.environ.get("x-rapidapi-key"),
        base_url: str | None = os.environ.get("x-rapidapi-host"),
    ):
        if not api_key:
            raise ValueError("API_KEY cannot be None")
        if not base_url:
            raise ValueError("BASE_URL cannot be None")

        self.api_key = api_key
        self.base_url = base_url
        self.headers = {
            "x-rapidapi-host": self.base_url,
            "x-rapidapi-key": self.api_key,
        }
    
        # Example defaults
        self.barca_id = 2817
        self.barca_code = "BAR"
        self.la_liga_id = 8
        self.champions_league_id = 7
        self.copa_del_rey = 329
        self.supa_copa_de_espana = 213
        self.eufa_eroupa_league = 679
        self.eufa_europa_conference_league = 17015
        self.eufa_super_cup = 465

        self.tournaments_with_ids = {
            "laliga":self.la_liga_id, 
            "champions_league":self.champions_league_id,
            "copa-del-rey":self.copa_del_rey,
            "supa-copa-de-espana":self.supa_copa_de_espana,
            "uefa-europa-league": self.eufa_eroupa_league,
            "eufa-europa-conference-league":self.eufa_europa_conference_league,
            "eufa-super-cup":self.eufa_super_cup
            }

    def get(self, endpoint_base: str, endpoint_end: str = "", params: dict | None = None):
        params = params or {}
        try:
            url = f"https://{self.base_url}/{endpoint_base.lower().strip('/')}/{endpoint_end.strip('/')}"
            response = requests.get(url=url, headers=self.headers, params=params)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {"success": False, "message": str(e)}
    
    def get_seasons(self):
        return None
