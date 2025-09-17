import requests
import json
import csv
import dotenv
import os
dotenv.load_dotenv()


API_KEY = os.getenv("FOOTBALL_API_TOKEN")   # replace with your football-data.org API key

BASE_URL = "https://api.football-data.org/v4"
headers = {"X-Auth-Token": API_KEY}

# Team ID for FC Barcelona = 81
TEAM_ID = 81

# Get team info (players, coach, etc.)
def fetch_team_info():
    url = f"{BASE_URL}/teams/{TEAM_ID}"
    response = requests.get(url, headers=headers)
    return response.json() if response.status_code == 200 else None

# Get recent matches
def fetch_matches(limit=20):
    url = f"{BASE_URL}/teams/{TEAM_ID}/matches?limit={limit}"
    response = requests.get(url, headers=headers)
    return response.json() if response.status_code == 200 else None

# Save data to JSON and CSV
def save_data():
    team_data = fetch_team_info()
    match_data = fetch_matches()

    if team_data:
        # Save team info JSON
        with open("barca_team.json", "w", encoding="utf-8") as f:
            json.dump(team_data, f, indent=4, ensure_ascii=False)

        # Save players to CSV
        with open("barca_players.csv", "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Name", "Position", "Nationality", "Shirt Number"])
            for player in team_data.get("squad", []):
                writer.writerow([
                    player.get("name"),
                    player.get("position"),
                    player.get("nationality"),
                    player.get("shirtNumber")
                ])

    if match_data:
        # Save matches JSON
        with open("barca_matches.json", "w", encoding="utf-8") as f:
            json.dump(match_data, f, indent=4, ensure_ascii=False)

        # Save matches to CSV
        with open("barca_matches.csv", "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Home Team", "Away Team", "Date", "Score Home", "Score Away"])
            for match in match_data.get("matches", []):
                writer.writerow([
                    match["homeTeam"]["name"],
                    match["awayTeam"]["name"],
                    match["utcDate"],
                    match["score"]["fullTime"]["home"],
                    match["score"]["fullTime"]["away"]
                ])

    print("✅ Data saved: barca_team.json, barca_players.csv, barca_matches.json, barca_matches.csv")

save_data()

