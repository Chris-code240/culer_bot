import time, schedule
from .main import COLLECTION

def refresh_barca_data(data:list):
    print("Refreshing Barça data...")

    # 1. Fetch fresh data from API
    # Example: players = client.get("teams", "get-squad", params={"teamId": 2817})

    # 2. Convert into documents
    players = [
        {"id": "messi", "name": "Lionel Messi", "matches": 778, "goals": 672},
        {"id": "pedri", "name": "Pedri", "matches": 120, "goals": 15}
    ]
    docs = [f"{p['name']} played {p['matches']} matches and scored {p['goals']} goals" for p in players]

    # 3. Upsert into Chroma
    COLLECTION.add(
        documents=docs,
        ids=[p["id"] for p in players],
        metadatas=[{"type": "player"} for _ in players]
    )

    print("✅ Barça data refreshed!")

# Run daily at midnight
schedule.every().day.at("00:00").do(refresh_barca_data)

while True:
    schedule.run_pending()
    time.sleep(60)
