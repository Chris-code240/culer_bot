
from datetime import datetime
from typing import Any, Dict, List

def parse_team_matches(api_response: dict) -> list[dict]:
    """
    Parse matches from the /team/get-last-matches API response.

    Args:
        api_response (dict): JSON from the API.

    Returns:
        list[dict]: List of simplified matches.
    """
    events = api_response.get("events", [])
    parsed = []

    for ev in events:
        match = {
            "match_id": ev.get("id"),
            "tournament": ev.get("tournament", {}).get("name"),
            "season": ev.get("season", {}).get("name"),
            "round": ev.get("roundInfo", {}).get("round"),
            "status": ev.get("status", {}).get("description"),
            "winner_code": ev.get("winnerCode"),
            "home_team": ev.get("homeTeam", {}).get("name"),
            "away_team": ev.get("awayTeam", {}).get("name"),
            "home_score": ev.get("homeScore", {}).get("display"),
            "away_score": ev.get("awayScore", {}).get("display"),
            "start_time": datetime.fromtimestamp(ev.get("startTimestamp")).isoformat()
                if ev.get("startTimestamp") else None,
            "slug": ev.get("slug"),
        }
        parsed.append(match)

    return parsed

def parse_team_performance(api_response: dict) -> list[dict]:
    """
    Parse performance events from the /teams/get-performance API response.

    Args:
        api_response (dict): JSON from the API.

    Returns:
        list[dict]: List of simplified performance events.
    """
    events = api_response.get("events", [])
    parsed = []

    for ev in events:
        match = {
            "match_id": ev.get("id"),
            "tournament": ev.get("tournament", {}).get("name"),
            "season": ev.get("season", {}).get("name"),
            "round": ev.get("roundInfo", {}).get("round"),
            "status": ev.get("status", {}).get("description"),
            "winner_code": ev.get("winnerCode"),
            "home_team": ev.get("homeTeam", {}).get("name"),
            "away_team": ev.get("awayTeam", {}).get("name"),
            "home_score": ev.get("homeScore", {}).get("display"),
            "away_score": ev.get("awayScore", {}).get("display"),
            "start_time": datetime.fromtimestamp(ev.get("startTimestamp")).isoformat()
                if ev.get("startTimestamp") else None,
            "slug": ev.get("slug"),

            # Performance-specific extras
            "injury_time_1": ev.get("time", {}).get("injuryTime1"),
            "injury_time_2": ev.get("time", {}).get("injuryTime2"),
            "has_highlights": ev.get("hasGlobalHighlights"),
            "has_xg": ev.get("hasXg"),
            "has_player_stats": ev.get("hasEventPlayerStatistics"),
        }
        parsed.append(match)

    return parsed

def parse_team_transfers(api_response: dict) -> dict[str, list[dict]]:
    """
    Parse transfers from the /teams/get-transfers API response.

    Args:
        api_response (dict): JSON from the API.

    Returns:
        dict: { "in": [...], "out": [...] } with simplified transfer info.
    """
    def simplify_transfer(transfer: dict) -> dict:
        return {
            "transfer_id": transfer.get("id"),
            "player_id": transfer.get("player", {}).get("id"),
            "player_name": transfer.get("player", {}).get("name"),
            "player_short": transfer.get("player", {}).get("shortName"),
            "position": transfer.get("player", {}).get("position"),
            "jersey_number": transfer.get("player", {}).get("jerseyNumber"),

            "from_team": transfer.get("transferFrom", {}).get("name"),
            "to_team": transfer.get("transferTo", {}).get("name"),

            "transfer_fee": transfer.get("transferFee"),
            "transfer_fee_desc": transfer.get("transferFeeDescription"),
            "transfer_currency": transfer.get("transferFeeRaw", {}).get("currency"),
            "transfer_date": datetime.fromtimestamp(
                transfer.get("transferDateTimestamp")
            ).isoformat() if transfer.get("transferDateTimestamp") else None,
        }

    return {
        "in": [simplify_transfer(t) for t in api_response.get("transfersIn", [])],
        "out": [simplify_transfer(t) for t in api_response.get("transfersOut", [])],
    }

def parse_squad_response(data: Dict[str, Any]) -> Dict[str, List[Dict[str, Any]]]:
    def extract_player(p: Dict[str, Any]) -> Dict[str, Any]:
        player = p.get("player", {})
        team = player.get("team", {})
        return {
            "id": player.get("id"),
            "name": player.get("name"),
            "shortName": player.get("shortName"),
            "slug": player.get("slug"),
            "position": player.get("position"),
            "positionsDetailed": player.get("positionsDetailed", []),
            "jerseyNumber": player.get("jerseyNumber"),
            "shirtNumber": player.get("shirtNumber"),
            "height": player.get("height"),
            "dateOfBirth": player.get("dateOfBirth"),
            "preferredFoot": player.get("preferredFoot"),
            "marketValue": player.get("proposedMarketValue"),
            "country": player.get("country", {}).get("name"),
            "team": team.get("name"),
            "teamSlug": team.get("slug"),
            "tournament": team.get("tournament", {}).get("name"),
        }

    parsed = {}
    for key in ["players", "foreignPlayers", "nationalPlayers", "playerPreviousTeam"]:
        items = data.get(key, [])
        players_list = []
        for item in items:
            player_info = extract_player(item)
            if key == "playerPreviousTeam":
                prev = item.get("previousTeam", {})
                player_info["previousTeam"] = prev.get("name")
                player_info["previousTeamId"] = prev.get("id")
            players_list.append(player_info)
        parsed[key] = players_list

    return parsed

def parse_tournaments_list(data: Dict[str, Any]) -> List[Dict[str, Any]]:
    tournaments = []

    for group in data.get("groups", []):
        for t in group.get("uniqueTournaments", []):
            category = t.get("category", {})
            sport = category.get("sport", {})
            tournaments.append({
                "id": t.get("id"),
                "name": t.get("name"),
                "slug": t.get("slug"),
                "primaryColor": t.get("primaryColorHex"),
                "secondaryColor": t.get("secondaryColorHex"),
                "userCount": t.get("userCount"),
                "country": category.get("name"),
                "countrySlug": category.get("slug"),
                "countryCode": category.get("alpha2"),
                "flag": category.get("flag"),
                "sport": sport.get("name"),
                "sportId": sport.get("id"),
                "translations": {
                    "tournamentNames": t.get("fieldTranslations", {}).get("nameTranslation", {}),
                    "countryNames": category.get("fieldTranslations", {}).get("nameTranslation", {})
                }
            })

    return tournaments
